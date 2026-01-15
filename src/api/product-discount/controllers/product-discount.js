'use strict';

/**
 * product-discount controller
 */

const { createCoreController } = require('@strapi/strapi').factories;

// Validation constants
const MAX_PAGE_SIZE = 100;
const DEFAULT_PAGE_SIZE = 25;
const STORE_ID_PATTERN = /^[a-zA-Z0-9_-]+$/;

module.exports = createCoreController('api::product-discount.product-discount', ({ strapi }) => ({
  async getProductDiscounts(ctx) {
    try {
      const { dutchie_store_id, page = 1, pageSize = DEFAULT_PAGE_SIZE } = ctx.query;

      // Validate dutchie_store_id if provided
      if (dutchie_store_id && !STORE_ID_PATTERN.test(dutchie_store_id)) {
        return ctx.badRequest('Invalid dutchie_store_id format');
      }

      // Validate and sanitize pagination params
      const pageNum = Math.max(1, parseInt(page, 10) || 1);
      const limit = Math.min(MAX_PAGE_SIZE, Math.max(1, parseInt(pageSize, 10) || DEFAULT_PAGE_SIZE));
      const offset = (pageNum - 1) * limit;

      // Build filters
      const filters = {};
      if (dutchie_store_id) {
        filters.dutchie_store_id = dutchie_store_id;
      }

      // Get total count for pagination meta
      const total = await strapi.entityService.count(
        'api::product-discount.product-discount',
        { filters }
      );

      // Fetch paginated results
      const results = await strapi.entityService.findMany(
        'api::product-discount.product-discount',
        {
          filters,
          limit,
          offset,
        }
      );

      strapi.log.debug(`Product discounts: found ${results.length} of ${total} total`);

      return {
        data: results,
        meta: {
          pagination: {
            page: pageNum,
            pageSize: limit,
            pageCount: Math.ceil(total / limit),
            total,
          },
        },
      };
    } catch (error) {
      strapi.log.error(`Product discount fetch error: ${error.message}`, {
        dutchie_store_id: ctx.query.dutchie_store_id,
        page: ctx.query.page,
        pageSize: ctx.query.pageSize,
      });
      strapi.log.error(error.stack);
      ctx.throw(500, 'Failed to fetch product discounts');
    }
  },
}));
