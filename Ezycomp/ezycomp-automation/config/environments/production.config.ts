import * as dotenv from 'dotenv';
import * as path from 'path';

// path.resolve() builds an OS-correct absolute path (works on Windows, Mac, Linux)
dotenv.config({ path: path.resolve(__dirname, '..', '..', '.env.production') });

export const productionConfig = {
  name: 'production',
  reactAppUrl: process.env.REACT_APP_URL ?? '',
  testUser: {
    username: process.env.TEST_USER_USERNAME ?? '',
    password: process.env.TEST_USER_PASSWORD ?? '',
  },
};

export type EnvConfig = typeof productionConfig;
