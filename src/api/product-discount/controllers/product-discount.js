'use strict';

/**
 * product-discount controller
 */

const { createCoreController } = require('@strapi/strapi').factories;

module.exports = createCoreController('api::product-discount.product-discount', ({ strapi }) => ({
  async getProductDiscounts(ctx) {
    try {
      const { dutchie_store_id } = ctx.query;

      // Build filters based on query params
      const filters = {};
      if (dutchie_store_id) {
        filters.dutchie_store_id = dutchie_store_id;
      }

      // Use Strapi's entity service for reliable querying
      const results = await strapi.entityService.findMany(
        'api::product-discount.product-discount',
        {
          filters,
          limit: 1000,
        }
      );

      console.log(`Found ${results.length} product discounts`);

      return {
        data: results,
        meta: { total: results.length }
      };

    } catch (error) {
      console.error('Product Discount Error:', error.message);
      ctx.throw(500, 'Failed to fetch product discounts');
    }
  },
}));
