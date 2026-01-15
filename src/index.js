'use strict';

module.exports = {
  register({ strapi }) {
    // Check environment variables on startup
    strapi.log.debug('Strapi register phase started');
    const envCheck = require('../config/env-check');
    const isValid = envCheck(strapi.log);

    if (!isValid && process.env.NODE_ENV === 'production') {
      strapi.log.warn('Missing required environment variables in production!');
    }
    strapi.log.debug('Strapi register phase completed');
  },

  async bootstrap({ strapi }) {
    try {
      // Log successful Cloudinary configuration
      const uploadConfig = strapi.config.get('plugin.upload');

      if (uploadConfig?.provider === 'cloudinary') {
        strapi.log.info('Cloudinary provider configured');
        strapi.log.info(`Cloud name: ${uploadConfig.providerOptions?.cloud_name || 'NOT SET'}`);
      } else {
        strapi.log.warn(`Upload provider: ${uploadConfig?.provider || 'NOT SET'}`);
      }

      // Set up public permissions for API endpoints
      await setPublicPermissions(strapi);
    } catch (error) {
      strapi.log.error(`Bootstrap failed: ${error.message}`);
      strapi.log.error(error.stack);
    }
  },
};

/**
 * Set public permissions for specified content types
 */
async function setPublicPermissions(strapi) {
  // Define which actions to enable for public role
  const publicPermissions = [
    // Inventory API
    { api: 'inventory', actions: ['find', 'findOne'] },
    // Discount API
    { api: 'discount', actions: ['find', 'findOne'] },
    // Product Discount API
    { api: 'product-discount', actions: ['find', 'findOne', 'getProductDiscounts'] },
  ];

  try {
    // Get the public role
    const publicRole = await strapi
      .query('plugin::users-permissions.role')
      .findOne({ where: { type: 'public' } });

    if (!publicRole) {
      strapi.log.warn('Public role not found, skipping permissions setup');
      return;
    }

    for (const { api, actions } of publicPermissions) {
      for (const action of actions) {
        const permissionAction = `api::${api}.${api}.${action}`;

        try {
          // Check if permission already exists
          const existingPermission = await strapi
            .query('plugin::users-permissions.permission')
            .findOne({
              where: {
                action: permissionAction,
                role: publicRole.id,
              },
            });

          if (!existingPermission) {
            // Create the permission
            await strapi.query('plugin::users-permissions.permission').create({
              data: {
                action: permissionAction,
                role: publicRole.id,
              },
            });
            strapi.log.info(`Created public permission: ${permissionAction}`);
          }
        } catch (permError) {
          strapi.log.error(`Failed to set permission ${permissionAction}: ${permError.message}`);
          strapi.log.error(permError.stack);
        }
      }
    }
  } catch (error) {
    strapi.log.error(`Failed to set public permissions: ${error.message}`);
    strapi.log.error(error.stack);
  }
}