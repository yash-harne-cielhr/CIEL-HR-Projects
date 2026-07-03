import { Page } from '@playwright/test';
import { BaseComponent } from '../core/base/BaseComponent';

/**
 * Generic listing table. Row lookups use a visible cell's text, not row
 * index, so tests don't break when row order/sorting changes.
 */
export class DataTable extends BaseComponent {
  constructor(page: Page, rootSelector = '[data-testid="data-table"]') {
    super(page, rootSelector);
  }

  private rowByText(text: string) {
    return this.root.locator('tbody tr', { hasText: text });
  }

  async rowCount(): Promise<number> {
    return this.root.locator('tbody tr').count();
  }

  async openRowActions(rowText: string): Promise<void> {
    await this.rowByText(rowText).locator('[data-testid="row-actions"]').click();
  }

  async clickRowAction(rowText: string, actionLabel: string): Promise<void> {
    await this.openRowActions(rowText);
    await this.page.getByRole('menuitem', { name: actionLabel }).click();
  }

  async cellText(rowText: string, columnTestId: string): Promise<string | null> {
    return this.rowByText(rowText).locator(`[data-col="${columnTestId}"]`).textContent();
  }
}
