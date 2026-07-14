import { Page, Locator, expect } from '@playwright/test';
import { BasePage } from '../../core/base/BasePage';
import { ReactAppRoutes } from '../../constants/routes';

export class LocationAuditListingPage extends BasePage {
  readonly path = ReactAppRoutes.locationAuditListing;

  constructor(page: Page) {
    super(page);
  }

  // Role label shown after login. TODO: confirm this selector is unique
  // once more surrounding HTML is available.
  private roleButton(expectedRole: string): Locator {
  return this.page.getByRole('button', { name: new RegExp(`${expectedRole}$`) });
  }


  async assertRoleLabel(expectedRole: string): Promise<void> {
  await expect(this.roleButton(expectedRole)).toBeVisible();
  }
}