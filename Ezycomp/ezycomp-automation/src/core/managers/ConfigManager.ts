import { getEnvConfig, resolveActiveEnvironment } from '../../../config/env';
import { Environment } from '../../constants/environment';
import type { EnvConfig } from '../../../config/environments/internal.config';

/**
 * Singleton — resolves the active environment ONCE per test run.
 * Usage:
 *   const cfg = ConfigManager.getInstance();
 *   cfg.reactAppUrl   // e.g. "https://ezycomp.ur-nl.com" (no trailing slash)
 *   cfg.testUser       // { username, password }
 */
export class ConfigManager {
  private static instance: ConfigManager;
  private readonly env: Environment;
  private readonly config: EnvConfig;

  private constructor() {
    this.env = resolveActiveEnvironment();
    this.config = getEnvConfig(this.env);

    if (!this.config.reactAppUrl) {
      throw new Error(
        `REACT_APP_URL is empty for environment "${this.env}". ` +
          `Fill it in .env.${this.env} (copy .env.${this.env}.example first).`
      );
    }
  }

  static getInstance(): ConfigManager {
    if (!ConfigManager.instance) {
      ConfigManager.instance = new ConfigManager();
    }
    return ConfigManager.instance;
  }

  get environment(): Environment {
    return this.env;
  }

  /** Base URL with any trailing slash stripped, so path-joining is always safe. */
  get reactAppUrl(): string {
    return this.config.reactAppUrl.replace(/\/+$/, '');
  }
}
