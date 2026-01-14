# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is FLMintDeals Backend - a Strapi 5 CMS for a Florida cannabis deals platform. It uses PostgreSQL and Cloudinary for media storage.

## Development Commands

```bash
# Install dependencies
npm install

# Start development server (with hot reload)
npm run develop   # or npm run dev

# Build admin panel for production
npm run build

# Start production server
npm run start
npm run start:prod  # Uses scripts/start-production.js
```

**Access Points (Development):**
- Admin Panel: http://localhost:1337/admin
- REST API: http://localhost:1337/api/*
- GraphQL: http://localhost:1337/graphql
- API Documentation: http://localhost:1337/documentation

## Database Setup

PostgreSQL is required. For local development:
```bash
# Database: flmintdeal_dev
# User: postgres / Password: postgres
# Port: 5432
```

In production (Railway), the `DATABASE_URL` environment variable is automatically provided and parsed by `config/database.js`.

## Architecture

### Content Types (`src/api/`)

Key domain entities:
- **store** - Dispensary locations with addresses, hours, geo coordinates, Dutchie integration
- **region** - Geographic regions containing stores
- **brand** - Cannabis brand information
- **discount/product-discount** - Deal and promotion data
- **inventory** - Store product inventory
- **dosage-form, dosage-ingredint, dosing-brand, dosing-product** - Dosing guide content
- **blog** - Blog posts
- **home-page, global-*-page** - CMS-managed page content

### Components (`src/components/`)

Reusable schema components organized by domain:
- `common/` - Address, hours, hours-exception
- `store/` - Service tags, amenity tags, offers
- `seo/` - Meta tags for SEO
- `ui/` - CTA blocks and other UI elements
- `discount/`, `inventory/`, `dosing/` - Domain-specific components

### Plugins

Configured in `config/plugins.js`:
- **GraphQL** - Available at `/graphql` with playground enabled
- **Documentation** - OpenAPI 3.0 docs at `/documentation`
- **Cloudinary Upload** - Media stored in Cloudinary `mintdeals` folder

### Bootstrap Permissions

`src/index.js` automatically sets public read permissions for `inventory` and `discount` APIs on startup.

## Environment Variables

Required variables (see `.env.example`):
- `APP_KEYS`, `API_TOKEN_SALT`, `ADMIN_JWT_SECRET`, `JWT_SECRET`, `TRANSFER_TOKEN_SALT` - Security keys
- `DATABASE_URL` or individual `DATABASE_*` vars - PostgreSQL connection
- `CLOUDINARY_NAME`, `CLOUDINARY_KEY`, `CLOUDINARY_SECRET` - Media storage

## Production Deployment

Deployed on Railway. See `RAILWAY_SETUP.md` for environment variable configuration.

```bash
# Verify Cloudinary config
node scripts/verify-cloudinary.js

# Check environment
node scripts/check-env.js
```

## Utility Scripts (`scripts/`)

- `start-production.js` - Production startup with env validation
- `verify-cloudinary.js` - Test Cloudinary credentials
- `add-seo-metadata.js`, `add-region-seo-metadata.js` - Bulk SEO updates
- `geocode-addresses.js`, `update-store-geo.js` - Store geolocation utilities
