module.exports = ({ env }) => {
  const isProduction = env('NODE_ENV') === 'production';

  // In production, require all secrets to be set
  if (isProduction) {
    const required = ['ADMIN_JWT_SECRET', 'API_TOKEN_SALT', 'TRANSFER_TOKEN_SALT'];
    const missing = required.filter((key) => !env(key));
    if (missing.length > 0) {
      throw new Error(`Missing required environment variables: ${missing.join(', ')}`);
    }
  }

  return {
    auth: {
      secret: env('ADMIN_JWT_SECRET', 'dev-secret-change-in-production'),
    },
    apiToken: {
      salt: env('API_TOKEN_SALT', 'dev-salt-change-in-production'),
    },
    transfer: {
      token: {
        salt: env('TRANSFER_TOKEN_SALT', 'dev-transfer-salt-change-in-production'),
      },
    },
    flags: {
      nps: env.bool('FLAG_NPS', true),
      promoteEE: env.bool('FLAG_PROMOTE_EE', true),
    },
  };
};