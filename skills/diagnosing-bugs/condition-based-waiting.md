# Condition-Based Waiting for Flaky Tests & Async Logic

Purpose: Eliminate race conditions and test flakiness caused by arbitrary timeouts (`sleep`, `setTimeout`) by polling for deterministic conditions.

---

## Core Principle

**The Antipattern**: Guessing at timing using fixed delays (`await sleep(50ms)` or `time.sleep(1)`).
- On fast developer machines, the test passes.
- Under CI load or in parallel execution, 50ms expires before the asynchronous operation completes, resulting in flaky failures.
- Alternatively, generous timeouts (e.g. 5000ms per step) bloat test suite runtime unnecessarily.

**The Rule**: **Wait for the actual state or condition you care about, bounded by a reasonable safety timeout.**

```
┌──────────────────────────────────────────────────────────────────────────┐
│                         ARBITRARY SLEEP vs POLLING                       │
└──────────────────────────────────────────────────────────────────────────┘

  ❌ ARBITRARY SLEEP:
  Action ──► sleep(100ms) ──► Assert State
             [Race condition if system is loaded; wasted time if fast]

  ✅ CONDITION POLLING:
  Action ──► Poll predicate every 10ms until true (or timeout) ──► Assert State
             [Fastest possible completion; immune to CPU load variance]
```

---

## Pattern Comparison

### ❌ Fragile: Guessing at Timings
```typescript
// Fragile: Assumes background worker completes within 100ms
triggerBackgroundProcessing();
await new Promise(resolve => setTimeout(resolve, 100));
const status = getJobStatus();
expect(status).toBe('COMPLETED');
```

### ✅ Robust: Polling the Condition
```typescript
triggerBackgroundProcessing();
await waitFor(() => getJobStatus() === 'COMPLETED', 'Job status to reach COMPLETED');
const status = getJobStatus();
expect(status).toBe('COMPLETED');
```

---

## Generic Condition Waiting Helper

```typescript
/**
 * Polls a synchronous or asynchronous condition function until it returns a truthy value or times out.
 */
export async function waitFor<T>(
  condition: () => T | Promise<T> | null | undefined | false,
  description: string,
  timeoutMs = 5000,
  intervalMs = 10
): Promise<T> {
  const startTime = Date.now();

  while (true) {
    const result = await condition();
    if (result) {
      return result;
    }

    if (Date.now() - startTime > timeoutMs) {
      throw new Error(`Timeout waiting for [${description}] after ${timeoutMs}ms`);
    }

    await new Promise((resolve) => setTimeout(resolve, intervalMs));
  }
}
```

---

## Common Event & State Patterns

| Scenario | Condition Pattern |
| :--- | :--- |
| **Wait for Event** | `await waitFor(() => events.find(e => e.type === 'JOB_DONE'), 'JOB_DONE event');` |
| **Wait for Count** | `await waitFor(() => queue.processedCount >= 5, '5 items processed');` |
| **Wait for File System** | `await waitFor(() => fs.existsSync(targetFilePath), 'File creation on disk');` |
| **Wait for DB Row** | `await waitFor(async () => (await db.users.find(id))?.active, 'User active flag');` |
| **Wait for HTTP 200** | `await waitFor(async () => (await fetch(url)).ok, 'Health check OK');` |

---

## When Arbitrary Delays ARE Justified

Arbitrary sleep is justified **ONLY** when testing intentional timing behavior itself (e.g. rate limiter tokens, debounce thresholds, or exponential backoff intervals).

When used:
1. First wait for the triggering event or state via condition-based waiting.
2. Sleep for the explicit duration being tested.
3. Include a comment documenting the exact mathematical justification (e.g. `// Debounce is 200ms; wait 250ms to ensure trailing execution fires`).
