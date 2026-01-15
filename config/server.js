module.exports = ({ env }) => {
  const isProduction = env('NODE_ENV') === 'production';

  // Development fallback keys (never used in production)
  const devKeys = ['dev-key-1-change-in-production', 'dev-key-2-change-in-production'];

  const appKeys = env.array('APP_KEYS');

  // In production, require APP_KEYS to be properly configured
  if (isProduction) {
    if (!appKeys || appKeys.length === 0) {
      throw new Error('APP_KEYS environment variable is required in production');
    }
  }

  return {
    host: env('HOST', '0.0.0.0'),
    port: env.int('PORT', 1337),
    app: {
      keys: appKeys || devKeys,
    },
    logger: {
      level: isProduction ? 'error' : 'debug',
    },
    webhooks: {
      populateRelations: env.bool('WEBHOOKS_POPULATE_RELATIONS', false),
    },
    transfer: {
      remote: {
        enabled: true,
      },
    },
  };
};