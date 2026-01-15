module.exports = ({ env }) => {
  const isProduction = env('NODE_ENV') === 'production';

  // Check if DATABASE_URL exists (Railway provides this)
  const databaseUrl = env('DATABASE_URL');

  if (databaseUrl) {
    // Parse DATABASE_URL for PostgreSQL
    try {
      const url = new URL(databaseUrl);
      return {
        connection: {
          client: 'postgres',
          connection: {
            host: url.hostname,
            port: parseInt(url.port, 10) || 5432,
            database: url.pathname.slice(1),
            user: url.username,
            password: url.password,
            ssl: {
              rejectUnauthorized: false,
            },
          },
          debug: false,
        },
      };
    } catch (error) {
      // In production, fail fast if DATABASE_URL is invalid
      if (isProduction) {
        throw new Error(`Invalid DATABASE_URL format: ${error.message}`);
      }
      // In development, log warning and fall back to individual env vars
      console.warn(`Warning: Could not parse DATABASE_URL (${error.message}), using individual env vars`);
    }
  }

  // Require DATABASE_URL in production
  if (isProduction && !databaseUrl) {
    throw new Error('DATABASE_URL is required in production');
  }

  // PostgreSQL configuration using individual env vars (development fallback)
  return {
    connection: {
      client: 'postgres',
      connection: {
        host: env('DATABASE_HOST', 'localhost'),
        port: env.int('DATABASE_PORT', 5432),
        database: env('DATABASE_NAME', 'mintdeals_db'),
        user: env('DATABASE_USERNAME', 'postgres'),
        password: env('DATABASE_PASSWORD', ''),
        ssl: env.bool('DATABASE_SSL', false) ? { rejectUnauthorized: false } : false,
      },
      debug: false,
    },
  };
};