import * as dotenv from 'dotenv';
import * as path from 'path';

// path.resolve() builds an OS-correct absolute path (works on Windows, Mac, Linux)
dotenv.config({ path: path.resolve(__dirname, '..', '..', '.env.staging') });

export const stagingConfig = {
  name: 'staging',
  reactAppUrl: process.env.REACT_APP_URL ?? '',
  testUser: {
    username: process.env.TEST_USER_USERNAME ?? '',
    password: process.env.TEST_USER_PASSWORD ?? '',
  },
};

export type EnvConfig = typeof stagingConfig;
