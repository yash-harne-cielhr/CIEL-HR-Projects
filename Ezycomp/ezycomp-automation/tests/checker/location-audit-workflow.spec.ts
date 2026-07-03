import { test, expect } from '@playwright/test';
import { Role } from '../../src/constants/roles';
import { Actor } from '../../src/core/actors/Actor';
import { Logger } from '../../src/core/managers/Logger';

// UI label shown per role after login - update here if the wording changes.
const ROLE_LABEL: Record<Role, string> = {
  [Role.VENDOR_USER]: 'Vendor User',
  [Role.VENDOR_ADMIN]: 'Vendor Admin',
  [Role.AUDITOR_USER]: 'Auditor User',
  [Role.AUDITOR_ADMIN]: 'Auditor Admin',
  [Role.CLIENT_ADMIN]: 'Client Admin',
};

test.describe.serial('Checker - Location Audit Workflow', () => {
  const ROLES = Object.values(Role);
  const actors: Partial<Record<Role, Actor>> = {};

  const LOGIN_TIMEOUT_MS = 90_000;

  test.beforeAll(async ({ browser }, testInfo) => {
    testInfo.setTimeout(LOGIN_TIMEOUT_MS);

    for (const role of ROLES) {
      const start = Date.now();
      actors[role] = await Actor.login(browser, role);
      Logger.info('beforeAll', `${role} ready in ${Date.now() - start}ms`);
    }
  });

  test.afterAll(async () => {
    for (const actor of Object.values(actors)) {
      await actor?.close();
    }
  });

  test('TC-LOCATION-001: redirects to Location Audit listing after login', async () => {
      for (const role of ROLES) {
        const actor = actors[role]!;
        const listing = actor.locationAuditListing;

        await test.step(`${role}: navigate to ${listing.path}`, async () => {
          Logger.info('TC-LOCATION-001', `Navigating ${role} to ${listing.path}`);
          await listing.goto();
        });

        await test.step(`${role}: verify URL`, async () => {
          Logger.info('TC-LOCATION-001', `Checking URL for ${role}`);
          await expect(actor.page).toHaveURL(new RegExp(`${listing.path}$`));
          Logger.info('TC-LOCATION-001', `${role} confirmed on ${actor.page.url()}`);
        });
      }
    });

  test('TC-LOCATION-002: role label matches the logged-in role', async () => {
    for (const role of ROLES) {
      const actor = actors[role]!;
      await test.step(`${role}: verify role label`, async () => {
        Logger.info('TC-LOCATION-002', `Checking role label for ${role}`);
        await actor.locationAuditListing.assertRoleLabel(ROLE_LABEL[role]);
        Logger.info('TC-LOCATION-002', `${role} role label confirmed`);
      });
    }
  });
});