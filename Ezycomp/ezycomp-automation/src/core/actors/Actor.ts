import { Browser, Page } from '@playwright/test';
import { Role } from '../../constants/roles';
import { UserManager } from '../managers/UserManager';
import { LoginPage } from '../../pages/common/LoginPage';
import { LocationAuditListingPage } from '../../pages/checker/LocationAuditListingPage';

/**
 * An Actor represents one real user in a multi-role workflow test: their
 * role, their own isolated `page` (from a dedicated browser context), and
 * lazy getters for whichever page objects that role needs to drive.
 *
 * Using an Actor instead of a raw `page` keeps workflow tests readable:
 *   vendorUser.locationAuditListing.uploadEvidence(...)
 * reads like the business step it represents, and hides which page class
 * is behind it.
 *
 * As we add more pages (Vendor Audit, Dashboards, etc.), add more lazy
 * getters here rather than constructing page objects inline in tests.
 */
export class Actor {
  constructor(readonly role: Role, readonly page: Page) {}

  /**
   * Opens a fresh, isolated browser context for this role, logs in, and
   * returns a ready-to-use Actor. Each Actor gets its own context, so 5
   * Actors = 5 independent login sessions, all alive at once - no
   * logging in/out between workflow steps.
   */
  static async login(browser: Browser, role: Role): Promise<Actor> {
    const context = await browser.newContext();
    const page = await context.newPage();

    const loginPage = new LoginPage(page);
    await loginPage.goto();
    await loginPage.login(UserManager.getCredentials(role));

    return new Actor(role, page);
  }

  async close(): Promise<void> {
    await this.page.context().close();
  }

  get locationAuditListing(): LocationAuditListingPage {
    return new LocationAuditListingPage(this.page);
  }
}
