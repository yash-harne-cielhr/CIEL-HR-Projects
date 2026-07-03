import { Page } from '@playwright/test';
import { BasePage } from '../../core/base/BasePage';
import { ReactAppRoutes } from '../../constants/routes';

export interface Credentials {
  username: string;
  password: string;
}

export class LoginPage extends BasePage {
  readonly path = ReactAppRoutes.login;

  constructor(page: Page) {
    super(page);
  }

  private get usernameInput() {
    return this.locator('input[name="username"]');
  }

  private get passwordInput() {
    return this.locator('input[name="password"]');
  }

  private get submitButton() {
    return this.page.getByRole('button', { name: 'Login', exact: true });
  }

  /** Defaults to the single test user configured in .env.<environment> if no credentials are passed. */
  async login(credentials: Credentials = this.config.testUser): Promise<void> {
    await this.usernameInput.fill(credentials.username);
    await this.passwordInput.fill(credentials.password);
    await this.submitButton.click();
    await this.waitForPageLoad();
  }
}
