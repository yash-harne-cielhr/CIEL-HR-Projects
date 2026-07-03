/* eslint-disable no-console */
type Level = 'INFO' | 'WARN' | 'ERROR' | 'DEBUG';

export class Logger {
  private static write(level: Level, scope: string, message: string, meta?: unknown) {
    const line = `[${new Date().toISOString()}] [${level}] [${scope}] ${message}`;
    if (meta !== undefined) console.log(line, meta);
    else console.log(line);
  }

  static info(scope: string, message: string, meta?: unknown) {
    this.write('INFO', scope, message, meta);
  }

  static warn(scope: string, message: string, meta?: unknown) {
    this.write('WARN', scope, message, meta);
  }

  static error(scope: string, message: string, meta?: unknown) {
    this.write('ERROR', scope, message, meta);
  }

  static debug(scope: string, message: string, meta?: unknown) {
    if (process.env.DEBUG) this.write('DEBUG', scope, message, meta);
  }
}
