# Testing Anti-Patterns: Traps, Tells & Remediation

Purpose: Identify and eliminate common testing anti-patterns that create brittle test suites, false confidence, or implementation coupling.

---

## The Three Iron Laws of Test Integrity

```
1. NEVER test mock behavior instead of real behavior.
2. NEVER add test-only methods to production classes.
3. NEVER mock without understanding the full dependency chain.
```

---

## Anti-Pattern 1: Testing Mock Behavior

### The Violation
Asserting on the existence, state, or invocation of mock objects rather than observable system behavior.

```typescript
// ❌ BAD: Verifying that the mock UI component was rendered
test('renders navigation sidebar', () => {
  render(<DashboardPage />);
  expect(screen.getByTestId('sidebar-mock')).toBeInTheDocument();
});
```

### Why It Harms the Suite
- You verify only that your test mock was wired up, not that the actual component works.
- The test passes even if the real component throws runtime errors or renders broken markup.
- Refactoring the internal component breaks the test even when user experience is unchanged.

### Remediation
Test through the real component, or assert on user-observable roles/text:
```typescript
// ✅ GOOD: Test real component through accessible role
test('renders navigation sidebar', () => {
  render(<DashboardPage />);
  expect(screen.getByRole('navigation', { name: /main navigation/i })).toBeInTheDocument();
});
```

### Gate Function
> **BEFORE asserting on any mock object or spy:**
> Ask: *"Am I verifying observable system outcome, or merely asserting that a test double exists?"*
> If asserting on test double mechanics, delete the assertion and test real behavior.

---

## Anti-Pattern 2: Test-Only Methods in Production Classes

### The Violation
Adding methods, flags, or hooks to production domain classes purely to satisfy test harness teardown or inspection.

```typescript
// ❌ BAD: Production class polluted with test-only teardown
class SessionManager {
  // Only called by test afterEach hooks!
  async destroyForTesting() {
    await this.storageEngine.dropAllTables();
  }
}
```

### Why It Harms the Suite
- Pollutes public API surface area with dangerous capabilities that could accidentally execute in production.
- Blurs lifecycle boundaries and violates Single Responsibility and YAGNI principles.

### Remediation
Move test setup, teardown, and lifecycle management into isolated test helper utilities:
```typescript
// ✅ GOOD: Production class remains lean; test helper handles environment reset
// In tests/helpers/session-test-utils.ts:
export async function cleanupTestSession(manager: SessionManager, storage: StorageEngine) {
  await storage.resetTestDatabase();
}
```

### Gate Function
> **BEFORE adding a method to a production class:**
> Ask: *"Will this method ever be called by real production use cases?"*
> If no, move it immediately to test helpers.

---

## Anti-Pattern 3: Mocking Without Understanding Dependencies

### The Violation
Mocking a high-level service or class to bypass slow operations, inadvertently suppressing essential side effects that downstream code requires.

```typescript
// ❌ BAD: Mocking the whole catalog suppresses configuration writes
test('rejects duplicate server registration', async () => {
  vi.mock('ServerCatalog', () => ({
    registerServer: vi.fn().mockResolvedValue(undefined) // Suppressed state mutation!
  }));

  await register('server-1');
  await register('server-1'); // Should throw DuplicateServerError, but won't!
});
```

### Why It Harms the Suite
- Tests pass for the wrong reasons or fail mysteriously because implicit state transitions were stubbed away.
- High-level mocks disguise architectural coupling.

### Remediation
Mock only at the lowest possible external I/O seam (e.g. network transport, database connection) while preserving business logic execution:
```typescript
// ✅ GOOD: Mock only the network ping; preserve registration logic
test('rejects duplicate server registration', async () => {
  vi.mock('NetworkProbe', () => ({ ping: vi.fn().mockResolvedValue(true) }));

  await register('server-1');
  await expect(register('server-1')).rejects.toThrow(DuplicateServerError);
});
```

---

## Anti-Pattern 4: Incomplete / Partial Mocks

### The Violation
Stubbing API or database responses with only the minimal subset of fields the immediate line of code accesses, omitting standard fields.

```typescript
// ❌ BAD: Incomplete payload missing standard metadata
const mockUserResponse = {
  id: 'usr_123',
  name: 'Alex'
  // Missing: tenantId, permissions, createdAt, updatedAt
};
```

### Why It Harms the Suite
- Downstream helpers, middleware, or logging functions fail silently or throw unexpected `TypeError: Cannot read properties of undefined`.
- Gives false confidence that changes are compatible with real upstream schemas.

### Remediation
Ensure test doubles conform to the full, canonical schema using typed factory functions with spread defaults:
```typescript
// Define factory with complete canonical defaults and typed Partial overrides
interface User {
  id: string;
  name: string;
  tenantId: string;
  permissions: string[];
  createdAt: string;
  updatedAt: string;
}

const defaultUser: User = {
  id: 'usr_default',
  name: 'Default User',
  tenantId: 'ten_default',
  permissions: ['read'],
  createdAt: '2026-01-01T00:00:00Z',
  updatedAt: '2026-01-01T00:00:00Z',
};

export function buildUserFixture(overrides: Partial<User> = {}): User {
  return { ...defaultUser, ...overrides };
}

// ✅ GOOD: Test specifies only assertion-relevant fields while guaranteeing 100% schema completeness
const mockAdmin = buildUserFixture({
  id: 'usr_123',
  permissions: ['read', 'write', 'admin'],
});
```

---

## Anti-Pattern 5: Implementation-Coupled & Whitebox Testing

### The Violation
Testing private methods directly, asserting on internal collaborator call order, or bypassing public interfaces to query internal database tables.

```typescript
// ❌ BAD: Asserts on private collaborator mechanics
test('checkout charges payment service', async () => {
  const spy = vi.spyOn(orderService, '_calculateTaxInternal');
  await checkout(cart);
  expect(spy).toHaveBeenCalledWith(cart.items, 'US_CA');
});
```

### Why It Harms the Suite
- Tests freeze internal implementation details, preventing refactoring.
- Tests break when internal code structure changes, even if public behavior remains 100% correct.

### Remediation
Test through the public contract and verify observable results:
```typescript
// ✅ GOOD: Tests observable business outcome through public interface
test('checkout calculates total inclusive of regional sales tax', async () => {
  const receipt = await checkout(cart, { region: 'US_CA' });
  expect(receipt.total).toBe(108.25);
});
```

### Critical Nuance: When Private Logic Demands Testing ("Listen to the Test")
**Do NOT use "don't test internals" as an excuse to leave complex logic untested.** If a private helper has intricate business rules or calculations that are difficult to reach from the top-level interface:
- **In Greenfield / New Code**: Extract the trapped abstraction into its own cohesive module (e.g. `TaxCalculationEngine`, `TieredDiscountPolicy`) with a dedicated public seam, test it test-first, and inject it as a collaborator.
- **In Existing / Legacy Code**: Use Seam Engineering (`Sprout Class`, `Sprout Method`, package-private/`internal` visibility, or `Subclass and Override`) to create a safe testing boundary.

### Gate Function
> **BEFORE testing a private method or bypassing a public interface:**
> Ask: *"Is this logic complex enough to require dedicated tests?"*
> - If **NO**: Test it through the existing public interface.
> - If **YES (New Code)**: Stop and extract the logic into its own class/module with a clean public seam.
> - If **YES (Legacy Code)**: Use a Sprout Class or widen visibility to package-private/internal.

---

## Anti-Pattern 6: Tautological Tests

### The Violation
Asserting an outcome by recomputing the expected value with the exact same formula or algorithm used in production code.

```typescript
// ❌ BAD: Tautological calculation (passes by construction)
test('calculates cart total with discount', () => {
  const items = [{ price: 20 }, { price: 30 }];
  const discountRate = 0.1;
  const expected = items.reduce((sum, i) => sum + i.price, 0) * (1 - discountRate);
  expect(calculateTotal(items, discountRate)).toBe(expected);
});
```

### Why It Harms the Suite
- If the calculation algorithm has a logical flaw, the test copies the exact same flaw and passes.

### Remediation
Use independent, precomputed literals or verified test vectors:
```typescript
// ✅ GOOD: Independent literal verified by domain spec
test('calculates cart total with discount', () => {
  const items = [{ price: 20 }, { price: 30 }];
  expect(calculateTotal(items, 0.1)).toBe(45.00);
});
```

---

## Anti-Pattern 7: Horizontal Slicing (Bulk Test-Writing)

### The Violation
Writing 20 failing tests upfront for an entire system before writing any implementation code.

### Why It Harms the Suite
- Tests written in bulk reflect *imagined* architecture before concrete feedback from the implementation is gathered.
- Leads to mass test churn when early architectural assumptions prove invalid.

### Remediation
Work in **Vertical Slices** (tracer bullets):
1. Write **one** test for the next smallest behavioral increment.
2. Watch it fail (Verify Red).
3. Write minimal code to pass (Verify Green).
4. Refactor and repeat.
