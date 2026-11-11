# Learning Equality Frontend Lifecycles, Telemetry & Packaging Reference

Purpose: Capture cross-repository multi-bundle Vue lifecycle ordering, constant and telemetry conventions, defensive browser SDK boundaries, and workspace/packaging rules across `kolibri`, `kolibri-data-portal`, `studio`, and `kolibri-design-system`.

---

## 1. Multi-Bundle Apps & `RootVue` Auth/Router Lifecycle

- **Role-Split Frontend Bundles**: Kolibri plugins and portals (`kolibri`, `kolibri-data-portal`, `studio`) split frontend bundles by authentication role (for example, `src_home` for authenticated views vs. `src_user` for unauthenticated sign-in and sign-up flows).
- **`RootVue` Session Redirects vs. `router.afterEach`**: Authenticated bundles frequently enforce login inside the mounted root component (`RootVue` / `PortalIndex.vue`, redirecting in `created()` when `!session.user_id` and gating `<router-view v-if="session.user_id" />`) rather than inside a Vue Router `beforeEach` guard.
- **Prevent Phantom Side Effects on Signed-Out Deep Links**: Because `router.afterEach` runs *before* `RootVue.created()` executes the redirect, unguarded `router.afterEach` listeners fire phantom pageviews or side effects on signed-out deep links even though `<router-view>` never renders. Always inspect the mounted root component when registering router hooks and gate callbacks on `session.user_id` where appropriate.

---

## 2. Frontend Constants, Telemetry Contracts & Global SDK Boundaries

- **Plain-Object Constant Maps vs. Mutating SDK Options**: Standard constant maps across Learning Equality frontends (`PageNames`, `Modals`, `Roles`, `PageCategories`, `AnalyticsApps`) are plain exported JS objects by convention; do not wrap routine constant maps in `Object.freeze`. Reserve `Object.freeze` strictly for configuration objects passed to third-party SDKs that mutate options in place (such as `posthog.init`).
- **Immutable Analytics & Telemetry Schemas**: Shipped analytics event names and property values are historical data contracts. Assert them in unit tests against hardcoded string literal tables rather than importing the enum under test as expected values, and settle route/query-parameter event semantics before shipping.
- **Defensive Browser & SDK Boundary Guards**: Browser hooks handling external inputs (`before_send` event redactors, global `window` callbacks like `CookiebotOnConsentReady`) must guard against both `null` and `undefined` (`if (!event)`) and check global SDK presence (`if (!window.Cookiebot)`) before reading nested properties. Verify fallback behavior against issue acceptance criteria (for example, reporting nothing when an external consent script is absent rather than reporting `'denied'`).

---

## 3. Workspace Supply-Chain & Packaging Rules (`kolibri` + `kolibri-*` & Python Wheels)

- **Pair Bare `"kolibri"` with `"kolibri-*"` Globs**: Learning Equality frontend repositories depend on both the bare `"kolibri"` npm package (`"kolibri": "^0.x.y"`) **and** `"kolibri-*"` packages (direct and transitive, including `kolibri-design-system`, `kolibri-tools`, `kolibri-constants`, and `kolibri-glob`). Whenever configuring `minimumReleaseAgeExclude` in `pnpm-workspace.yaml`, `.github/dependabot.yml` cooldown/ignore rules, or bundler externals/transpile allowlists, include **both** `"kolibri"` and `"kolibri-*"` (`"kolibri-*"` alone misses bare `"kolibri"` and breaks coordinated same-day releases).
- **Verify Built Python Wheel Metadata**: When packaging standalone or workspace Python distributions inside Learning Equality repositories, build the `.whl` and `sdist` locally and inspect `dist-info/METADATA` and `dist-info/licenses/`: confirm `LICENSE` is bundled, verify runtime-only `Requires-Dist` compatibility (including `--python-version 3.6` vendoring where applicable), and avoid combining deprecated `License ::` classifiers with PEP 621 `license = "..."` strings per PEP 639.
