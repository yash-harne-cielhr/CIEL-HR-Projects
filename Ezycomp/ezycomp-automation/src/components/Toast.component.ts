import { Page } from '@playwright/test';
import { BaseComponent } from '../core/base/BaseComponent';

export class Toast extends BaseComponent {
  constructor(page: Page) {
    super(page, '[data-testid="app-toast"]');
  }

  get message() {
    return this.root;
  }

  async waitForDismiss(): Promise<void> {
    await this.root.waitFor({ state: 'hidden', timeout: 10_000 });
  }
}
