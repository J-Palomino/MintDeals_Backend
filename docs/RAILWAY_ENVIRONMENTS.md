# Railway Environments

The MintDeals Backend is deployed on Railway with three separate environments for development, staging, and production.

## Environment Overview

| Environment | Branch | URL | Purpose |
|-------------|--------|-----|---------|
| **dev** | `dev` | https://mintdealsbackend-dev.up.railway.app | Development and testing |
| **staging** | `staging` | https://mintdealsbackend-staging.up.railway.app | Pre-production testing |
| **production** | `main` | https://mintdealsbackend-production.up.railway.app | Live production |

## Services Per Environment

Each environment has its own isolated set of services:

| Service | Description |
|---------|-------------|
| **MintDeals_Backend** | Strapi 5 CMS application |
| **Postgres** | Primary PostgreSQL database |
| **Redis** | Redis cache |
| **mintinvsvc-dev** | Inventory service |

## Deployment Workflow

Deployments are automatic via GitHub integration:

```
dev branch    →  dev environment
staging branch →  staging environment
main branch   →  production environment
```

### Promoting Changes

```bash
# Develop on dev branch
git checkout dev
# ... make changes ...
git push origin dev  # Auto-deploys to dev

# Promote to staging
git checkout staging
git merge dev
git push origin staging  # Auto-deploys to staging

# Promote to production
git checkout main
git merge staging
git push origin main  # Auto-deploys to production
```

## Service Connections

### MintDeals_Backend

The backend service has the following service connections configured:

| Variable | Source | Description |
|----------|--------|-------------|
| `DATABASE_URL` | `${{Postgres.DATABASE_URL}}` | PostgreSQL connection string |
| `REDIS_URL` | `${{Redis.REDIS_URL}}` | Redis connection string |
| `CLOUDINARY_NAME` | Manual | Cloudinary cloud name |
| `CLOUDINARY_KEY` | Manual | Cloudinary API key |
| `CLOUDINARY_SECRET` | Manual | Cloudinary API secret |

## Access Points

### Dev Environment
- **Admin Panel**: https://mintdealsbackend-dev.up.railway.app/admin
- **REST API**: https://mintdealsbackend-dev.up.railway.app/api/*
- **GraphQL**: https://mintdealsbackend-dev.up.railway.app/graphql
- **API Docs**: https://mintdealsbackend-dev.up.railway.app/documentation

### Staging Environment
- **Admin Panel**: https://mintdealsbackend-staging.up.railway.app/admin
- **REST API**: https://mintdealsbackend-staging.up.railway.app/api/*
- **GraphQL**: https://mintdealsbackend-staging.up.railway.app/graphql
- **API Docs**: https://mintdealsbackend-staging.up.railway.app/documentation

### Production Environment
- **Admin Panel**: https://mintdealsbackend-production.up.railway.app/admin
- **REST API**: https://mintdealsbackend-production.up.railway.app/api/*
- **GraphQL**: https://mintdealsbackend-production.up.railway.app/graphql
- **API Docs**: https://mintdealsbackend-production.up.railway.app/documentation

## Railway CLI Commands

### Switch Environment
```bash
railway environment dev       # Switch to dev
railway environment staging   # Switch to staging
railway environment production # Switch to production
```

### Check Status
```bash
railway status  # View current environment status
```

### View Variables
```bash
railway variables -s MintDeals_Backend  # View service variables
```

### Deploy Manually
```bash
railway up -e dev      # Deploy to dev
railway up -e staging  # Deploy to staging
```

### View Logs
```bash
railway logs -s MintDeals_Backend  # View service logs
```

## Environment Variables

Required environment variables for the backend:

| Variable | Required | Description |
|----------|----------|-------------|
| `DATABASE_URL` | Yes | PostgreSQL connection URL |
| `REDIS_URL` | No | Redis connection URL (optional caching) |
| `CLOUDINARY_NAME` | Yes | Cloudinary cloud name |
| `CLOUDINARY_KEY` | Yes | Cloudinary API key |
| `CLOUDINARY_SECRET` | Yes | Cloudinary API secret |
| `NODE_ENV` | No | Set automatically by Railway |
| `PORT` | No | Set automatically by Railway |

## Notes

- Each environment has completely isolated databases - data does not sync between environments
- The Cloudinary credentials are shared across all environments (same media storage)
- Security keys (APP_KEYS, JWT secrets) use fallback defaults for dev/staging
- Production should have unique security keys configured
