/**
 * Concrete condition-based waiting utilities for asynchronous tests.
 * Use to replace flaky arbitrary timeouts with deterministic polling.
 */

export interface EventRecord {
  type: string;
  data?: Record<string, unknown>;
  timestamp: number;
}

export interface EventEmitterLike {
  getEvents(channelId: string): EventRecord[];
}

/**
 * Wait for a specific event type to appear on an event channel.
 */
export function waitForEvent(
  emitter: EventEmitterLike,
  channelId: string,
  eventType: string,
  timeoutMs = 5000,
  intervalMs = 10
): Promise<EventRecord> {
  return new Promise((resolve, reject) => {
    const startTime = Date.now();

    const check = () => {
      const events = emitter.getEvents(channelId);
      const match = events.find((e) => e.type === eventType);

      if (match) {
        resolve(match);
      } else if (Date.now() - startTime > timeoutMs) {
        reject(new Error(`Timeout waiting for event [${eventType}] on channel [${channelId}] after ${timeoutMs}ms`));
      } else {
        setTimeout(check, intervalMs);
      }
    };

    check();
  });
}

/**
 * Wait for a specific count of events matching an event type.
 */
export function waitForEventCount(
  emitter: EventEmitterLike,
  channelId: string,
  eventType: string,
  expectedCount: number,
  timeoutMs = 5000,
  intervalMs = 10
): Promise<EventRecord[]> {
  return new Promise((resolve, reject) => {
    const startTime = Date.now();

    const check = () => {
      const events = emitter.getEvents(channelId);
      const matching = events.filter((e) => e.type === eventType);

      if (matching.length >= expectedCount) {
        resolve(matching);
      } else if (Date.now() - startTime > timeoutMs) {
        reject(
          new Error(
            `Timeout waiting for ${expectedCount} [${eventType}] events on channel [${channelId}] after ${timeoutMs}ms (found ${matching.length})`
          )
        );
      } else {
        setTimeout(check, intervalMs);
      }
    };

    check();
  });
}

/**
 * Wait for an event matching a custom predicate.
 */
export function waitForEventMatch(
  emitter: EventEmitterLike,
  channelId: string,
  predicate: (event: EventRecord) => boolean,
  description: string,
  timeoutMs = 5000,
  intervalMs = 10
): Promise<EventRecord> {
  return new Promise((resolve, reject) => {
    const startTime = Date.now();

    const check = () => {
      const events = emitter.getEvents(channelId);
      const match = events.find(predicate);

      if (match) {
        resolve(match);
      } else if (Date.now() - startTime > timeoutMs) {
        reject(new Error(`Timeout waiting for [${description}] on channel [${channelId}] after ${timeoutMs}ms`));
      } else {
        setTimeout(check, intervalMs);
      }
    };

    check();
  });
}
