/**
 * Roles involved in the Location Audit workflow. One person can genuinely
 * hold more than one of these in real life - but for now (per current
 * scope) each role maps to its own dedicated test account.
 */
export enum Role {
  SUPERADMIN = 'SUPERADMIN',     // can do everything, including user management
  VENDOR_USER = 'VENDOR_USER',       // uploads evidence
  VENDOR_ADMIN = 'VENDOR_ADMIN',     // reviews evidence, submits to auditor
  AUDITOR_USER = 'AUDITOR_USER',     // reviews, marks Compliant/Not Compliant
  AUDITOR_ADMIN = 'AUDITOR_ADMIN',   // same as Auditor User + publishes reports
  CLIENT_ADMIN = 'CLIENT_ADMIN',     // view-only, downloads exports/reports
}
