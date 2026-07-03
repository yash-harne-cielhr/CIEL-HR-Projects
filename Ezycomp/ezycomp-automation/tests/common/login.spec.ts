import { test, expect } from '@playwright/test';
import { ConfigManager } from '../../src/core/managers/ConfigManager';
import { LoginPage } from '../../src/pages/common/LoginPage';

/**
 * TC-LOGIN-001
 * Run just this file:
 *   npx playwright test tests/common/login.spec.ts --headed --debug
 */
test.describe('Login', () => {
  test('TC-LOGIN-001: navigating goes to the login page', async ({ page }) => {
    const config = ConfigManager.getInstance();
    const loginPage = new LoginPage(page);

    await loginPage.goto();

    // If this fails, the URL being built is wrong - check REACT_APP_URL in
    // your .env file has no trailing slash, and that routes.ts's `login`
    // path matches what you see in the browser's address bar.
    await expect(page).toHaveURL(`${config.reactAppUrl}${loginPage.path}`);
  });

  test('TC-LOGIN-002: valid credentials log in and redirect away from /login', async ({ page }) => {
    const loginPage = new LoginPage(page);

    await loginPage.goto();
    await loginPage.login(); // uses TEST_USER_USERNAME / TEST_USER_PASSWORD from .env

    // TODO once you know a real post-login element/URL, assert on that
    // instead - e.g. expect(page).toHaveURL(/dashboard/)
    await expect(page).not.toHaveURL(/\/login$/);
  });
});
