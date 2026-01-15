/**
 * Environment variable validation
 * @param {Object} logger - Optional logger (strapi.log) for structured logging
 * @returns {boolean} - true if all required env vars are set
 */
module.exports = (logger) => {
  // Use provided logger or fallback to console for standalone script usage
  const log = {
    info: logger?.info || console.log,
    warn: logger?.warn || console.warn,
    error: logger?.error || console.error,
    debug: logger?.debug || console.log,
  };

  const required = {
    // Cloudinary
    CLOUDINARY_NAME: process.env.CLOUDINARY_NAME,
    CLOUDINARY_KEY: process.env.CLOUDINARY_KEY,
    CLOUDINARY_SECRET: process.env.CLOUDINARY_SECRET,
    // Strapi Keys
    APP_KEYS: process.env.APP_KEYS,
    API_TOKEN_SALT: process.env.API_TOKEN_SALT,
    ADMIN_JWT_SECRET: process.env.ADMIN_JWT_SECRET,
    JWT_SECRET: process.env.JWT_SECRET,
  };

  // In production, DATABASE_URL is required
  if (process.env.NODE_ENV !== 'development') {
    required.DATABASE_URL = process.env.DATABASE_URL;
  }

  const missing = [];
  for (const [key, value] of Object.entries(required)) {
    if (!value) {
      missing.push(key);
    }
  }

  // Only log details in development or if there are missing vars
  if (process.env.NODE_ENV === 'development') {
    log.debug('=== Environment Variables Check ===');
    for (const [key, value] of Object.entries(required)) {
      log.debug(`${value ? '✅' : '❌'} ${key}: ${value ? 'Set' : 'MISSING'}`);
    }
    if (missing.length === 0) {
      log.debug('All required environment variables are set');
    } else {
      log.warn(`Missing environment variables: ${missing.join(', ')}`);
    }
  } else if (missing.length > 0) {
    log.error(`Missing required environment variables: ${missing.join(', ')}`);
  }

  return missing.length === 0;
};