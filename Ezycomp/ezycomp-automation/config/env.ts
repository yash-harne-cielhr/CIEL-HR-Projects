import { Environment } from '../src/constants/environment';
import { internalConfig, EnvConfig } from './environments/internal.config';
import { stagingConfig } from './environments/staging.config';
import { productionConfig } from './environments/production.config';

const CONFIG_MAP: Record<Environment, EnvConfig> = {
  [Environment.INTERNAL]: internalConfig,
  [Environment.STAGING]: stagingConfig,
  [Environment.PRODUCTION]: productionConfig,
};

/**
 * Resolves the active environment from the ENV variable.
 * Defaults to STAGING (per current setup) if ENV isn't set at all.
 *
 * Override for a single run:
 *   cross-env ENV=internal playwright test   (or: npm run test:internal)
 */
export function resolveActiveEnvironment(): Environment {
  const raw = (process.env.ENV ?? Environment.STAGING).toLowerCase();
  if (!Object.values(Environment).includes(raw as Environment)) {
    throw new Error(
      `Unknown ENV "${raw}". Expected one of: ${Object.values(Environment).join(', ')}`
    );
  }
  return raw as Environment;
}

export function getEnvConfig(env: Environment = resolveActiveEnvironment()): EnvConfig {
  return CONFIG_MAP[env];
}
