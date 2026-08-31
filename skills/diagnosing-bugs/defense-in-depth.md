# Defense-in-Depth Validation

Purpose: Ensure bugs and invalid states are made structurally impossible by erecting validation barricades at every architectural layer.

---

## Core Principle

When a bug caused by invalid data or broken state is fixed at a single location, that single check remains vulnerable to future bypasses (e.g. alternative code paths, subsequent refactoring, mocks in unit tests, or direct submodule imports).

- **Single Check**: "We patched the bug."
- **Defense in Depth**: "We made the defect structurally impossible."

```
┌──────────────────────────────────────────────────────────────────────────┐
│                   THE 4-LAYER DEFENSE IN DEPTH MODEL                     │
└──────────────────────────────────────────────────────────────────────────┘

  [LAYER 1: Entry Point Barricade]
  • Validate at public API / CLI boundaries.
  • Reject malformed shapes, empty strings, missing IDs immediately.
          │
          ▼
  [LAYER 2: Domain & Business Invariant Guards]
  • Enforce domain logic rules inside entities, services, and use cases.
  • Assert state validity, non-empty preconditions, valid transitions.
          │
          ▼
  [LAYER 3: Environment & Context Safety Guards]
  • Safeguard against context-specific dangers (e.g. test vs prod).
  • Enforce sandbox boundaries (e.g. refuse filesystem mutation outside tmp in tests).
          │
          ▼
  [LAYER 4: Telemetry & Diagnostic Instrumentation]
  • Log structured forensic metadata before sensitive operations.
  • Surface stack traces and context when fallbacks or edge cases hit.
```

---

## The 4 Validation Layers

### Layer 1: Entry Point Barricades
**Purpose**: Reject invalid input at the public boundary before any subsystem processing begins.

```typescript
function createProject(name: string, workingDirectory: string) {
  if (!workingDirectory || workingDirectory.trim() === '') {
    throw new InvalidArgumentError('workingDirectory cannot be empty');
  }
  if (!existsSync(workingDirectory)) {
    throw new NotFoundError(`workingDirectory does not exist: ${workingDirectory}`);
  }
  if (!statSync(workingDirectory).isDirectory()) {
    throw new InvalidArgumentError(`workingDirectory must be a directory: ${workingDirectory}`);
  }
  // Proceed to core logic
}
```

### Layer 2: Business Logic & Invariant Validation
**Purpose**: Verify domain preconditions and data consistency within services/entities.

```typescript
function initializeWorkspace(projectDir: string, sessionId: string) {
  if (!projectDir || typeof projectDir !== 'string') {
    throw new InvariantViolationError('Valid projectDir is required for workspace initialization');
  }
  if (!sessionId) {
    throw new InvariantViolationError('Active sessionId required');
  }
  // Execute domain operations
}
```

### Layer 3: Environment & Sandbox Guards
**Purpose**: Prevent dangerous actions in specific runtimes or testing environments.

```typescript
async function runGitOperation(directory: string) {
  // During tests, strictly prevent mutations outside designated temp directories
  if (process.env.NODE_ENV === 'test') {
    const normalized = normalize(resolve(directory));
    const tmpBase = normalize(resolve(tmpdir()));

    if (!normalized.startsWith(tmpBase)) {
      throw new SecurityGuardError(
        `Refusing git mutation outside test temp directory: ${directory}`
      );
    }
  }
  // Execute git operation
}
```

### Layer 4: Forensic Telemetry & Debug Instrumentation
**Purpose**: Capture structured context for immediate diagnosis if downstream failures occur.

```typescript
async function runGitOperation(directory: string) {
  const stack = new Error().stack;
  logger.debug('Executing git operation', {
    directory,
    cwd: process.cwd(),
    nodeEnv: process.env.NODE_ENV,
    stack,
  });
  // Execute operation
}
```

---

## Systematic Application Checklist

When resolving any defect:
1. **Trace Data Flow**: Identify every checkpoint the bad or corrupt value traversed.
2. **Map Boundaries**: Identify the entry point, domain logic, environment constraints, and execution points.
3. **Implement All 4 Layers**: Add validations across every traversed layer.
4. **Test Each Boundary**: Verify that bypassing Layer 1 still triggers a hard rejection at Layer 2 or Layer 3.
