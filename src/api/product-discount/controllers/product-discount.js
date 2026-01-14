'use strict';

/**
 * product-discount controller
 */

const { createCoreController } = require('@strapi/strapi').factories;

module.exports = createCoreController('api::product-discount.product-discount', ({ strapi }) => ({
  async getProductDiscounts(ctx) {
    try {
      const { dutchie_store_id } = ctx.query;

      const knex = strapi.db.connection;

      let query = 'SELECT * FROM public.product_discounts';
      const bindings = [];

      if (dutchie_store_id) {
        query += ' WHERE dutchie_store_id = $1';
        bindings.push(dutchie_store_id);
      }

      query += ' LIMIT 1000';

      const result = await knex.raw(query, bindings);
      const rows = result.rows || [];

      console.log(`Found ${rows.length} product discounts`);

      return {
        data: rows,
        meta: { total: rows.length }
      };

    } catch (error) {
      console.error('Product Discount Error:', error.message);

      return ctx.badRequest('Failed to fetch product discounts', {
        message: error.message,
        details: error.toString()
      });
    }
  },
}));
