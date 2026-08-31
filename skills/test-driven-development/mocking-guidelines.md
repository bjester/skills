# Mocking Guidelines: Boundary Isolation & Mockability Design

Purpose: Establish strict standards for when, where, and how to use test doubles without causing test-induced architectural damage.

---

## When to Mock vs. When to Use Real Implementations

```
┌──────────────────────────────────────────────────────────────────────────┐
│                         WHERE TEST DOUBLES BELONG                        │
└──────────────────────────────────────────────────────────────────────────┘

  ✅ MOCK AT EXTERNAL BOUNDARIES ONLY:
  • Third-party HTTP/REST/gRPC APIs (Payment gateways, Email services, SMS)
  • Non-deterministic system inputs (System clock, UUID generators, Randomness)
  • Hardware & Operating System interactions (Process execution, raw sockets)
  • External message brokers / Kafka / SQS (when testing domain components)

  ❌ NEVER MOCK:
  • Your own domain entities, value objects, and business services
  • Internal collaborators within the same bounded context
  • Pure functions, utility routines, or mathematical logic
  • Relational database operations (prefer fast in-memory DB or disposable test containers)
```

---

## Designing for Mockability

Code that is difficult to test or mock indicates architectural coupling. Design interfaces that cleanly isolate external volatility:

### 1. Dependency Injection (Constructor / Parameter Passing)

Pass external dependencies into services rather than instantiating them internally:

```typescript
// ❌ HARD TO TEST: Hardcoded instantiation of external client
class BillingService {
  async chargeUser(userId: string, amount: number) {
    const client = new StripeClient(process.env.STRIPE_SECRET_KEY);
    return await client.charges.create({ customer: userId, amount });
  }
}

// ✅ EASY TO TEST: Injected interface
class BillingService {
  constructor(private readonly paymentGateway: PaymentGatewayClient) {}

  async chargeUser(userId: string, amount: number) {
    return await this.paymentGateway.createCharge({ customer: userId, amount });
  }
}
```

### 2. Specific SDK Interfaces Over Generic Transport Fetchers

Create typed, operation-specific methods rather than passing raw URLs to generic HTTP fetchers:

```typescript
// ❌ HARD TO MOCK: Generic fetcher requires complex conditional stubbing in tests
interface HttpClient {
  request(url: string, options: RequestOptions): Promise<unknown>;
}

// ✅ EASY TO MOCK: Operation-specific interface with explicit contract
interface NotificationClient {
  sendEmail(recipient: string, templateId: string, context: Record<string, unknown>): Promise<DeliveryReceipt>;
  sendSms(phoneNumber: string, message: string): Promise<DeliveryReceipt>;
}
```

**Benefits of Operation-Specific Interfaces:**
- Test setup stubs a single clear method rather than branching on regex URLs.
- Type safety enforces complete payload matching.
- Downstream refactorings of endpoints do not break domain tests.

---

## Test Double Taxonomy

Choose the simplest test double that satisfies the isolation requirement:

| Type | Definition | Best Use Case |
| :--- | :--- | :--- |
| **Dummy** | Objects passed around but never actually used (e.g. required filler parameters). | Filling unused constructor arguments. |
| **Stub** | Provides canned answers to calls made during the test. | Simulating external service responses (e.g. returning HTTP 200 JSON). |
| **Spy** | Records information about how it was called (arguments, call counts). | Verifying that an external notification or metric was emitted. |
| **Mock** | Pre-programmed with expectations about calls it should receive. | Strict boundary protocol verification (use sparingly). |
| **Fake** | Working implementation with shortcuts (e.g. in-memory database or repository). | High-speed integration testing of data repositories. |

---

## The Rule of Behavioral Verification

**Verify state and public outcomes whenever possible; verify interaction (spies/mocks) only when state verification is impossible.**

- Preferred: Call a method on the public interface and assert on the returned value or changed aggregate state.
- Secondary: Assert that a boundary port received an outbound message (e.g. email was queued to an external gateway).
