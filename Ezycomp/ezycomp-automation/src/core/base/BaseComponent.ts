import { Page, Locator } from '@playwright/test';

/**
 * Root class for reusable UI widgets (nav bar, tables, filters, etc.).
 * Not used yet - Login has no shared widgets. Keep this here so the next
 * page we automate can start reusing components immediately instead of
 * re-establishing the pattern.
 */
export abstract class BaseComponent {
  protected readonly page: Page;
  protected readonly root: Locator;

  constructor(page: Page, rootSelector: string) {
    this.page = page;
    this.root = page.locator(rootSelector);
  }

  async isVisible(): Promise<boolean> {
    return this.root.isVisible();
  }
}
