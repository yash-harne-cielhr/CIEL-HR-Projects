import { Role } from '../../constants/roles';
import { Environment } from '../../constants/environment';
import { ConfigManager } from './ConfigManager';
import { stagingUsers, Credentials } from '../../../config/users/staging.users';
import { internalUsers } from '../../../config/users/internal.users';
import { productionUsers } from '../../../config/users/production.users';

const USER_MAP: Record<Environment, Record<Role, Credentials>> = {
  [Environment.STAGING]: stagingUsers,
  [Environment.INTERNAL]: internalUsers,
  [Environment.PRODUCTION]: productionUsers,
};

/**
 * Single place tests go to for "give me a user with this role" — scoped
 * automatically to whichever environment ConfigManager resolved (staging
 * by default).
 */
export class UserManager {
  static getCredentials(role: Role, overrides?: Partial<Credentials>): Credentials {
    const env = ConfigManager.getInstance().environment;
    const base = USER_MAP[env][role];

    if (!base.username || !base.password) {
      throw new Error(
        `Missing credentials for role "${role}" in environment "${env}". ` +
          `Check .env.${env} is filled in for that role.`
      );
    }

    return { ...base, ...overrides };
  }
}
