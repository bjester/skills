# Learning Equality Sync, Multi-DB & Legacy Runtime Reference

Purpose: Capture cross-repository sync, SQLite/PostgreSQL engine, multi-database routing, and legacy runtime invariants across `morango`, `kolibri`, `studio`, `kolibri-data-portal`, `le-utils`, and `ricecooker`.

---

## 1. Minimum Runtime & SQLite Bound-Parameter Floor

- **Check Minimum Supported Runtime & Framework Floors**: Inspect `pyproject.toml`, `setup.cfg`, `tox.ini`, and `.github/workflows/` for legacy compatibility floors (`python>=3.6`, `django>=3,<4`) across `morango`, `kolibri` runtime vendoring, and standalone workspace packages (such as `django-vectors`). Do not assume Django 3.2+ APIs (for example, `ConnectionProxy(connections, alias)`) when `django>=3` is supported.
- **SQLite 999 Bound-Variable Ceiling**: Legacy Python CI containers (for example, Debian Buster) ship SQLite < 3.32 with a hard **999 bound-SQL-variable ceiling** (`calculate_max_sqlite_variables()`). Never pass unbounded ID lists into `filter(id__in=...)`, `exclude(id__in=...)`, or `bulk_create(...)`. Chunk bulk queries and writes explicitly (typically `<= 500` rows per batch).

---

## 2. Dual SQLite & PostgreSQL Engine Semantics

- **Deferred Foreign Keys Require `TransactionTestCase`**: Morango and Kolibri sync schemas rely on `DEFERRABLE INITIALLY DEFERRED` foreign keys. Standard Django `TestCase` wraps each test in a transaction that rolls back without committing, so deferred foreign-key violations never fire in `TestCase`. Use `TransactionTestCase` whenever testing FK ordering, cascades, or streaming deserialization commits.
- **Transaction SQL Visibility (`execute_wrapper` vs. `in_atomic_block`)**: Entering a top-level `transaction.atomic()` emits `BEGIN` through `connection.execute_wrapper` on SQLite, whereas PostgreSQL (`psycopg2`) toggles connection `autocommit = False` on the driver with zero SQL statements sent through `execute_wrapper`. Assert `connection.in_atomic_block` directly when testing transaction state across both backends.
- **Single-Table Expression Index Rule**: On both PostgreSQL and SQLite, expression indexes (`CREATE INDEX ... ON table ((expr))`) can reference columns of a single table only. Never propose or write an expression index over a `COALESCE` or `CASE` expression spanning joined tables.

---

## 3. Django Multi-Database Handles, Thread-Locality & Test Routers

- **Thread-Local `django.db.connections[alias]`**: Django's `connections[alias]` mapping is thread-local (`asgiref.local.Local` / `threading.local()`). Never cache `connections[alias]` or a wrapper around it inside `@cached_property` or an instance attribute shared across worker threads. Resolve `connections[alias]` per operation or store per-thread handles on `threading.local()`.
- **Catch-All Test Routers Mask Unpinned Queries**: Test routers such as Morango's `TestingRouter` silently route unpinned `.save()`, `.delete()`, and lazy FK lookups to `"default"`, allowing bugs in multi-database pinning to pass tests unnoticed. Apply `@override_settings(DATABASE_ROUTERS=[])` (or route target models to a distinct non-default database alias) in pinned-database tests so unpinned ORM operations fail loud.

---

## 4. Cross-Partition Sync Ordering & Sibling-Repo Library Contracts

- **Preserve Intentional `Scope` Partition Ordering**: Morango `Scope` filters order partitions intentionally (`shared` -> `read-only` -> `user read-write`) so parent records arrive before dependent user records. Streaming pipelines iterating outer-by-partition (`for partition -> for model_in_fk_order`) must preserve the filter partition sequence rather than sorting partition prefixes alphabetically, or cross-partition foreign keys fail at commit time.
- **Sibling-Repo Python Library Contracts (`CHANGELOG.md`)**: Downstream Learning Equality apps (`kolibri`, `studio`, `kolibri-data-portal`) directly import entry points, keyword arguments, logger names, and semi-private `_`-prefixed helpers from `morango` (for example, `_deserialize_from_store`), `le-utils`, and `ricecooker`. Whenever changing or removing any public or semi-private library interface, document the exact parameter and call-site migration mapping in `CHANGELOG.md` and check sibling-repo callers.
