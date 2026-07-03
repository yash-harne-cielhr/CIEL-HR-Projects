/**
 * Joins a base URL and a relative path without producing a double slash
 * (e.g. "https://app.com/" + "/login" used to become "https://app.com//login",
 * which some servers/routers treat as a different, broken path).
 *
 * buildUrl('https://app.com/', '/login')  -> 'https://app.com/login'
 * buildUrl('https://app.com', '/login')   -> 'https://app.com/login'
 * buildUrl('https://app.com', 'login')    -> 'https://app.com/login'
 */
export function buildUrl(baseUrl: string, path: string): string {
  const trimmedBase = baseUrl.replace(/\/+$/, '');
  const normalizedPath = path.startsWith('/') ? path : `/${path}`;
  return `${trimmedBase}${normalizedPath}`;
}
