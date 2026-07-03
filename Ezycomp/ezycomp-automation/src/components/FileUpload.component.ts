import { Page } from '@playwright/test';
import { BaseComponent } from '../core/base/BaseComponent';

export class FileUpload extends BaseComponent {
  constructor(page: Page, rootSelector = '[data-testid="file-upload"]') {
    super(page, rootSelector);
  }

  async upload(filePath: string | string[]): Promise<void> {
    await this.root.locator('input[type="file"]').setInputFiles(filePath);
  }

  async submit(): Promise<void> {
    await this.root.locator('[data-testid="upload-submit"]').click();
  }
}
