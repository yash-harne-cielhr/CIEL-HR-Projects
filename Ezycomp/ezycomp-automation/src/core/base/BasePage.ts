import { Page, Locator, expect } from '@playwright/test';
import { ConfigManager } from '../managers/ConfigManager';
import { Logger } from '../managers/Logger';
import { buildUrl } from '../../constants/url.util';
import { Toast } from '../../components/Toast.component';

/**
 * Root of the page-object inheritance chain. Every concrete page extends
 * this to get goto()/waitForPageLoad()/assertToastMessage() for free, and
 * to guarantee URLs are built consistently.
 */
export abstract class BasePage {
  protected readonly page: Page;
  protected readonly config: ConfigManager;
  readonly toast: Toast;

  constructor(page: Page) {
    this.page = page;
    this.config = ConfigManager.getInstance();
    this.toast = new Toast(page);
  }

  /** Subclasses declare the relative route they represent (see routes.ts). */
  abstract readonly path: string;

  async goto(): Promise<void> {
    const url = buildUrl(this.config.reactAppUrl, this.path);
    Logger.info(this.constructor.name, `Navigating to ${url}`);
    await this.page.goto(url, { waitUntil: 'domcontentloaded' });
    Logger.info(this.constructor.name, `Landed on ${this.page.url()}`);
  }

  async waitForPageLoad(): Promise<void> {
    await this.page.waitForLoadState('load');
  }

  async assertToastMessage(expected: string): Promise<void> {
    await expect(this.toast.message).toContainText(expected);
  }

  protected locator(selector: string): Locator {
    return this.page.locator(selector);
  }

  /**
   * Waits until the browser actually finishes redirecting to this page's
   * path — needed after actions (like login) that trigger a client-side
   * redirect that can land after the "load" event fires. Reused by any
   * page in any module that needs a post-action redirect check.
   */
  async waitForRedirect(timeoutMs = 30_000): Promise<void> {
    Logger.info(this.constructor.name, `Waiting for redirect to ${this.path}`);
    await this.page.waitForURL((url) => url.pathname.endsWith(this.path), { timeout: timeoutMs });
    Logger.info(this.constructor.name, `Redirected to ${this.page.url()}`);
  }
  
}


