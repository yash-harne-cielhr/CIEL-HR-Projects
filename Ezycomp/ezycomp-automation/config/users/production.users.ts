import * as dotenv from 'dotenv';
import * as path from 'path';
import { Role } from '../../src/constants/roles';

dotenv.config({ path: path.resolve(__dirname, '..', '..', '.env.production') });

export interface Credentials {
  username: string;
  password: string;
}

/**
 * Maps each Location Audit role to its login credentials for PRODUCTION.
 * Values come from .env.production — nothing sensitive lives in this file.
 * Tests never import this directly; they go through UserManager.
 */
export const productionUsers: Record<Role, Credentials> = {
  [Role.VENDOR_USER]: {
    username: process.env.VENDOR_USER_USERNAME ?? '',
    password: process.env.VENDOR_USER_PASSWORD ?? '',
  },
  [Role.VENDOR_ADMIN]: {
    username: process.env.VENDOR_ADMIN_USERNAME ?? '',
    password: process.env.VENDOR_ADMIN_PASSWORD ?? '',
  },
  [Role.AUDITOR_USER]: {
    username: process.env.AUDITOR_USER_USERNAME ?? '',
    password: process.env.AUDITOR_USER_PASSWORD ?? '',
  },
  [Role.AUDITOR_ADMIN]: {
    username: process.env.AUDITOR_ADMIN_USERNAME ?? '',
    password: process.env.AUDITOR_ADMIN_PASSWORD ?? '',
  },
  [Role.CLIENT_ADMIN]: {
    username: process.env.CLIENT_ADMIN_USERNAME ?? '',
    password: process.env.CLIENT_ADMIN_PASSWORD ?? '',
  },
};
