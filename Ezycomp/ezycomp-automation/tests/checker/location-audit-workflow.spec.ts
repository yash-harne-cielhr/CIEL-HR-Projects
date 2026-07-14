import { test, expect } from '@playwright/test';
import { Role } from '../../src/constants/roles';
import { Actor } from '../../src/core/actors/Actor';
import { Logger } from '../../src/core/managers/Logger';

// UI label shown per role after login - update here if the wording changes.
type LocationAuditRole = Role.VENDOR_USER | Role.VENDOR_ADMIN | Role.AUDITOR_USER | Role.AUDITOR_ADMIN | Role.CLIENT_ADMIN;

const ROLE_LABEL: Record<LocationAuditRole, string> = {
  [Role.VENDOR_USER]: 'Vendor User',
  [Role.VENDOR_ADMIN]: 'Vendor Admin',
  [Role.AUDITOR_USER]: 'Auditor User',
  [Role.AUDITOR_ADMIN]: 'Auditor Admin',
  [Role.CLIENT_ADMIN]: 'Client Admin',
};

test.describe.serial('Checker - Location Audit Workflow', () => {
  const ROLES: LocationAuditRole[] = [
  Role.VENDOR_USER,
  Role.VENDOR_ADMIN,
  Role.AUDITOR_USER,
  Role.AUDITOR_ADMIN,
  Role.CLIENT_ADMIN,
];
  const actors: Record<LocationAuditRole, Actor> = {} as Record<LocationAuditRole, Actor>;

  const LOGIN_TIMEOUT_MS = 90_000;

  test.beforeAll(async ({ browser }, testInfo) => {
    testInfo.setTimeout(LOGIN_TIMEOUT_MS);

    const results = await Promise.all(
      ROLES.map(async (role) => {
        const start = Date.now();
        const actor = await Actor.login(browser, role);
        Logger.info('beforeAll', `${role} ready in ${Date.now() - start}ms`);
        return actor;
      })
    );

    ROLES.forEach((role, i) => {
      actors[role] = results[i];
    });
  });

  test.afterAll(async () => {
    for (const actor of Object.values(actors)) {
      await actor?.close();
    }
  });

  test('TC-LOCATION-001: redirects to Location Audit listing after login', { tag: ['@smoke'] },async () => {
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

  test('TC-LOCATION-002: role label matches the logged-in role', { tag: ['@smoke'] },async () => {
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