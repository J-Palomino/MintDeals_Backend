# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is FLMintDeals Backend - a Strapi 5 CMS for a Florida cannabis deals platform. It uses PostgreSQL and Cloudinary for media storage.

## Development Commands

```bash
npm install          # Install dependencies
npm run develop      # Start dev server with hot reload (or: npm run dev)
npm run build        # Build admin panel for production
npm run start        # Start production server
npm run start:prod   # Production startup with env validation
```

**Access Points (Development):**
- Admin Panel: http://localhost:1337/admin
- REST API: http://localhost:1337/api/*
- GraphQL: http://localhost:1337/graphql
- API Documentation: http://localhost:1337/documentation

## Database Setup

PostgreSQL is required. For local development with Docker:
```bash
docker-compose up -d postgres   # Start PostgreSQL container
```

Local database credentials:
- Database: `flmintdeal_dev`
- User/Password: `postgres/postgres`
- Port: `5432`

In production (Railway), the `DATABASE_URL` environment variable is automatically provided and parsed by `config/database.js`.

## Architecture

### Content Types (`src/api/`)

**Collection types** (multiple entries):
- **store** - Dispensary locations with addresses, hours, geo coordinates, Dutchie integration
- **region** - Geographic regions containing stores (related to stores via `inversedBy`)
- **brand** - Cannabis brand information
- **discount/product-discount** - Deal and promotion data
- **inventory** - Store product inventory
- **dosage-form, dosage-ingredint, dosing-brand, dosing-product** - Dosing guide content
- **blog** - Blog posts

**Single types** (one entry, CMS-managed pages):
- **home-page** - Homepage content
- **global-about-us-page, global-contact-us-page**, etc. - Static page content

Most content types have i18n localization enabled.

### Custom Endpoints

The `product-discount` API has a custom route (`routes/custom-routes.js`) with a raw SQL query endpoint:
- `GET /api/product-discounts?dutchie_store_id=<id>` - Returns product discounts, optionally filtered by store

### Components (`src/components/`)

Reusable schema components organized by domain:
- `common/` - Address, hours, hours-exception
- `store/` - Service tags, amenity tags, offers
- `seo/` - Meta tags for SEO
- `ui/` - CTA blocks and other UI elements

### Plugins

Configured in `config/plugins.js`:
- **GraphQL** - `/graphql` with playground enabled, depth limit 7, amount limit 100
- **Documentation** - OpenAPI 3.0 docs at `/documentation`
- **Cloudinary Upload** - Media stored in Cloudinary `mintdeals` folder

### Bootstrap Permissions

`src/index.js` automatically grants public read permissions (`find`, `findOne`) for `inventory`, `discount`, and `product-discount` APIs on startup.

## Environment Variables

Required variables (see `.env.example`):
- `APP_KEYS`, `API_TOKEN_SALT`, `ADMIN_JWT_SECRET`, `JWT_SECRET`, `TRANSFER_TOKEN_SALT` - Security keys
- `DATABASE_URL` or individual `DATABASE_*` vars - PostgreSQL connection
- `CLOUDINARY_NAME`, `CLOUDINARY_KEY`, `CLOUDINARY_SECRET` - Media storage

Environment validation runs on startup via `config/env-check.js`.

## Production Deployment

Deployed on Railway. See `RAILWAY_SETUP.md` for environment variable configuration.

```bash
node scripts/verify-cloudinary.js   # Test Cloudinary credentials
node scripts/check-env.js           # Check environment variables
```

## Utility Scripts (`scripts/`)

- `start-production.js` - Production startup with env validation
- `verify-cloudinary.js` - Test Cloudinary credentials
- `add-seo-metadata.js`, `add-region-seo-metadata.js` - Bulk SEO updates
- `geocode-addresses.js`, `update-store-geo.js` - Store geolocation utilities

## Creating New Content Types

Use the Strapi CLI to generate new APIs:
```bash
npm run strapi generate
```

Standard Strapi 5 structure: each API in `src/api/<name>/` has:
- `content-types/<name>/schema.json` - Schema definition
- `controllers/<name>.js` - Controller (use `createCoreController`)
- `services/<name>.js` - Service (use `createCoreService`)
- `routes/<name>.js` - Routes (use `createCoreRouter`)

For custom routes, add a separate file like `routes/custom-routes.js` and export a `routes` array.
