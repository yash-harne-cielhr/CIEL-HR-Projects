import { test, expect } from '@playwright/test';
import { ConfigManager } from '../../src/core/managers/ConfigManager';
import { UserManager } from '../../src/core/managers/UserManager';
import { Role } from '../../src/constants/roles';
import { LoginPage } from '../../src/pages/common/LoginPage';

test.describe('Login', () => {
  test('TC-LOGIN-001: Verify that user is successfully logged in with valid credentials', { tag: ['@smoke'] }, async ({ page }) => {
    const config = ConfigManager.getInstance();
    const loginPage = new LoginPage(page);

    await test.step('STEP-1: Verify that user is on the login page', async () => {
      await loginPage.goto();
      await expect(page).toHaveURL(`${config.reactAppUrl}${loginPage.path}`);
    });

    await test.step('STEP-2: Verify that user is successfully logged in and landed on Home page', async () => {
      await loginPage.login(UserManager.getCredentials(Role.SUPERADMIN));
      await expect(page).toHaveURL(`${ConfigManager.getInstance().reactAppUrl}`);
      await expect(page.locator('div.pageHeading h4')).toHaveText('Home');
    });
  });
});

