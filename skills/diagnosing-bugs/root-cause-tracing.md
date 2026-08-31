# Root Cause Tracing: Backward Call Chain Analysis

Purpose: Trace defects and corrupt state backwards from deep execution failure points to their root trigger before attempting fixes.

---

## Core Principle

Bugs often manifest deep in the call stack (e.g. database opened with invalid path, subshell executed in wrong directory, unexpected `undefined`/`null` exception). 

**The Instinctive Mistake**: Fixing or patching where the error surfaces (symptom masking).
**The Discipline**: Trace backward through the call chain until you pinpoint the original trigger, and fix at the true source.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                          BACKWARD TRACING FLOW                          │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │
         ┌───────────────────────────┴───────────────────────────┐
         ▼                                                       ▼
   [Symptom Point]                                        [Call Chain]
   Error thrown deep in system logic.                      Inspect stack / callers one by one.
         │                                                       │
         └───────────────────────────┬───────────────────────────┘
                                     ▼
                        [Identify Root Trigger]
                        Where was invalid value created or passed?
                                     │
                                     ▼
                        [Fix at Source + Defend]
                        Fix root origin; add multi-layer validation.
```

---

## When to Use

- An error occurs deep in execution (not directly at the entry API boundary).
- Stack trace shows a deep call chain across multiple modules or services.
- Data arrives corrupted, empty, or invalid, but origin is unobvious.
- You need to determine which test or caller causes shared state pollution.

---

## The 5-Step Tracing Technique

### Step 1: Observe the Exact Symptom
Capture the literal exception, error code, and immediate failure context:
```text
Error: git init failed in ~/project/packages/core
```

### Step 2: Identify the Immediate Cause
Examine the exact routine that failed:
```typescript
await execFileAsync('git', ['init'], { cwd: targetDir });
```
Ask: *Why did this fail here?* (e.g. `targetDir` was `""`, which resolved to `process.cwd()`).

### Step 3: Inspect the Immediate Caller
Examine what invoked the immediate cause:
```typescript
WorktreeManager.createSessionWorktree(projectDir, sessionId)
  → called by Session.initializeWorkspace()
  → called by Session.create()
  → called by test suite at Project.create()
```
Ask: *What exact arguments were passed down each frame?*

### Step 4: Step Backwards Frame by Frame
Trace the parameter value up each calling layer:
- `projectDir = ""` (empty string)
- Where was `projectDir` constructed or returned?
- `const context = setupCoreTest();` returns `{ tempDir: "" }` before `beforeEach` runs.

### Step 5: Pinpoint the Root Trigger
- Root cause: Top-level variable initialization accessed `context.tempDir` before the test runner's setup hook assigned a real temporary directory.
- **Fix at Source**: Make `tempDir` a property/getter that throws an explicit descriptive error if accessed before setup initialization.
- **Add Defense in Depth**: Add validation at each intermediate layer (`Project.create`, `WorkspaceManager`, and environment guards).

---

## Diagnostic Instrumentation & Stack Captures

When static code analysis cannot trace an issue (e.g. async event loops, dynamic callbacks, dependency injection):

### 1. In-Flight Stack Tracing
Log full stack traces *before* the dangerous operation executes:

```typescript
// Insert before suspected operation
async function executeOperation(directory: string) {
  const stack = new Error().stack;
  console.error('[DEBUG-TRACE] executeOperation invoked with:', {
    directory,
    cwd: process.cwd(),
    stack,
  });

  return await runUnderlying(directory);
}
```

> **Important**:
> - Use standard error (`console.error` / `stderr`) or unbuffered output during tests to prevent logger suppression.
> - Capture context variables: current working directory, environment flags, timestamp, caller identifiers.
> - Tag logs with a unique searchable prefix (`[DEBUG-TRACE]` or `[DEBUG-<id>]`) for easy cleanup.

---

## Locating Test Suite Pollution

When a test pollutes shared state (e.g. creates unexpected files, mutates global singletons, leaks database records) causing downstream tests to fail unpredictably:

1. Use the bisection script `scripts/find-polluter.sh`:
   ```bash
   ./scripts/find-polluter.sh '<polluted_file_or_artifact>' '<test_glob_pattern>'
   ```
2. The script runs test files sequentially, verifying state before and after each test, and halts immediately on the first test that produces the pollution.
3. Once isolated, inspect that specific test's setup/teardown hooks and isolation boundaries.
