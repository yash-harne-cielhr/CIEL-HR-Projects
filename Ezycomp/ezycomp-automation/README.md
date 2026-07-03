# EzyComp UI Automation — Login only (fresh minimal setup)

Playwright + TypeScript, OOP-based, default Playwright HTML report.
**Default environment is STAGING** — fill in `.env.staging` and you're
running against staging with no extra flags.

## 1. Install everything

```bash
npm install
npx playwright install
```

`npm install` pulls every dependency listed in `package.json` into
`node_modules`. `npx playwright install` downloads the Chromium browser
binary Playwright drives. Both commands are identical on Windows/Mac/Linux.
Check `node -v` first — if that errors, install Node.js LTS from
https://nodejs.org.

## 2. Configure staging (the default)

Copy `.env.staging.example` → `.env.staging` and fill in:

```
REACT_APP_URL=https://your-staging-url-here      # NO trailing slash
TEST_USER_USERNAME=someone@ezycomp-test.com
TEST_USER_PASSWORD=********
```

That's the only file with real values in it. `.env.internal.example` and
`.env.production.example` are there for later — leave them alone for now.

## 3. Run the login test

```bash
npx playwright test tests/common/login.spec.ts --headed --debug
```

`--headed` shows the real browser; `--debug` pauses on every step. Once it
passes, drop the flags and just run `npm run test:staging`.

## The redirect bug from before — what was wrong and what changed

`BasePage.goto()` used to do `${reactAppUrl}${path}` directly. If
`REACT_APP_URL` had a trailing slash (`.../ur-nl.com/`) and `path` started
with `/` (`/login`), that produced `.../ur-nl.com//login` — a **double
slash**, which routers/servers can treat as an entirely different (and
usually broken) path, so nothing redirected correctly.

Fixed by:
- `src/constants/url.util.ts` → `buildUrl(base, path)` strips any trailing
  slash off `base` and guarantees exactly one `/` between the two pieces,
  no matter how you write the URL in `.env.staging`.
- `ConfigManager.reactAppUrl` also strips a trailing slash as a second
  safety net.
- `BasePage.goto()` now logs both the URL it's navigating to and the URL
  it actually lands on (`page.url()`), so a mismatch is visible immediately
  in the console instead of failing silently.

---

## File-by-file guide

| File | What it does |
|---|---|
| `package.json` | Dependencies + npm scripts. `npm install` reads this. |
| `tsconfig.json` | TypeScript compiler settings — no need to touch it. |
| `playwright.config.ts` | Test folder, browser, retries, and the HTML report output folder (`reports/html-report`). |
| `.gitignore` | Keeps real `.env.*` files and generated folders out of version control. |
| `.env.staging.example` | Template for the **default** environment — copy to `.env.staging` and fill in. |
| `.env.internal.example` / `.env.production.example` | Same idea, for later — not required to run anything today. |
| `config/env.ts` | Reads the `ENV` variable and resolves which environment config to use. Defaults to `staging` if `ENV` isn't set. This is the only file that reads `process.env.ENV` directly. |
| `config/environments/staging.config.ts` | Loads `.env.staging`, exposes `reactAppUrl` and `testUser` (username/password). |
| `config/environments/internal.config.ts` / `production.config.ts` | Same shape, for those environments, once you need them. |
| `src/constants/environment.ts` | The `Environment` enum (`internal`/`staging`/`production`). No `Role` enum yet — that gets added once we build a module with multiple roles. |
| `src/constants/routes.ts` | Relative paths for pages we automate. Currently just `login`. Confirm it matches the real app's address bar. |
| `src/constants/url.util.ts` | `buildUrl()` — the fix for the double-slash bug described above. |
| `src/core/managers/ConfigManager.ts` | Singleton exposing the resolved environment's `reactAppUrl` and `testUser`. Throws a clear error early if `REACT_APP_URL` is blank, instead of failing confusingly later. |
| `src/core/managers/Logger.ts` | Timestamped console logging, used by `BasePage.goto()` to show exactly what URL was requested vs. landed on. |
| `src/core/base/BaseComponent.ts` | Parent class for future reusable UI widgets (nav bar, tables...). Unused today — Login doesn't need any — but ready for the next page we build. |
| `src/core/base/BasePage.ts` | Parent class for every page object. Provides `goto()` (uses `buildUrl`) and `waitForPageLoad()`. |
| `src/pages/common/LoginPage.ts` | The only page object in this build. Selectors are placeholders (`data-testid`) — replace with real ones from your app (see below). |
| `tests/common/login.spec.ts` | Two tests: (1) navigating actually lands on the login URL, (2) valid credentials redirect away from `/login`. |

## Finding the real login selectors

The three locators in `LoginPage.ts` (`usernameInput`, `passwordInput`,
`submitButton`) are guesses. Find the real ones with:

```bash
npx playwright codegen https://your-staging-url-here
```

Type the username/password and click Login in the browser that opens — the
Inspector window shows the exact selector Playwright would use for each
field, live. Copy those into `LoginPage.ts`.

## Next step

Once `login.spec.ts` passes reliably, tell me which page/module to
automate next and I'll add it following the same pattern: route → page
object → spec — reusing `BasePage`/`ConfigManager` as-is.
