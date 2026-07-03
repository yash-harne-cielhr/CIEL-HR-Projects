/**
 * Route paths, relative to REACT_APP_URL. Page objects build the full URL
 * via ConfigManager + these paths - never hardcode a URL in a page object.
 *
 * Confirm this against the real app before running tests: open the login
 * screen in a browser and check the address bar.
 */
export const ReactAppRoutes = {
  login: '/login',
  locationAuditListing: '/location-audits',
} as const;
