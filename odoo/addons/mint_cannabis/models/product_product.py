# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProductProduct(models.Model):
    """
    Extended product.product for cannabis product variants.

    Maps to Dutchie inventory-level data (specific SKU/variant with potency, pricing).
    Each variant represents a specific size/potency combination at a location.
    """
    _inherit = 'product.product'

    # ===========================================
    # Dutchie Sync Fields
    # ===========================================
    x_dutchie_inventory_id = fields.Char(
        string='Dutchie Inventory ID',
        index=True,
        copy=False,
        help='Unique inventory item ID from Dutchie POS'
    )
    x_dutchie_sku = fields.Char(
        string='Dutchie SKU',
        index=True,
        help='SKU from Dutchie POS system'
    )
    x_dutchie_location_id = fields.Char(
        string='Dutchie Location ID',
        index=True,
        help='Dispensary location ID from Dutchie'
    )
    x_dutchie_pos_inventory_id = fields.Char(
        string='Dutchie POS Inventory ID',
        help='POS-specific inventory ID'
    )
    x_warehouse_id = fields.Many2one(
        'stock.warehouse',
        string='Store/Warehouse',
        index=True,
        help='Warehouse/store this variant is located at'
    )
    x_store_name = fields.Char(
        string='Store Name',
        compute='_compute_store_name',
        store=True,
        help='Name of the store for display'
    )

    @api.depends('x_warehouse_id', 'x_warehouse_id.name')
    def _compute_store_name(self):
        for product in self:
            product.x_store_name = product.x_warehouse_id.name if product.x_warehouse_id else ''

    # ===========================================
    # Potency Fields
    # ===========================================
    x_thc_percentage = fields.Float(
        string='THC %',
        digits=(5, 2),
        help='THC percentage (0-100)'
    )
    x_thc_percentage_min = fields.Float(
        string='THC % Min',
        digits=(5, 2),
        help='Minimum THC percentage for range'
    )
    x_thc_percentage_max = fields.Float(
        string='THC % Max',
        digits=(5, 2),
        help='Maximum THC percentage for range'
    )
    x_cbd_percentage = fields.Float(
        string='CBD %',
        digits=(5, 2),
        help='CBD percentage (0-100)'
    )
    x_cbd_percentage_min = fields.Float(
        string='CBD % Min',
        digits=(5, 2),
        help='Minimum CBD percentage for range'
    )
    x_cbd_percentage_max = fields.Float(
        string='CBD % Max',
        digits=(5, 2),
        help='Maximum CBD percentage for range'
    )
    x_thc_mg = fields.Float(
        string='THC (mg)',
        digits=(10, 2),
        help='Total THC in milligrams'
    )
    x_cbd_mg = fields.Float(
        string='CBD (mg)',
        digits=(10, 2),
        help='Total CBD in milligrams'
    )
    x_thc_mg_per_serving = fields.Float(
        string='THC mg/serving',
        digits=(10, 2),
        help='THC milligrams per serving'
    )
    x_cbd_mg_per_serving = fields.Float(
        string='CBD mg/serving',
        digits=(10, 2),
        help='CBD milligrams per serving'
    )
    x_potency_thc_formatted = fields.Char(
        string='THC Formatted',
        help='Formatted THC potency string (e.g., "25.5%", "10mg")'
    )
    x_potency_cbd_formatted = fields.Char(
        string='CBD Formatted',
        help='Formatted CBD potency string'
    )

    # ===========================================
    # Terpenes (individual fields for top terpenes)
    # ===========================================
    x_terpene_myrcene = fields.Float(string='Myrcene %', digits=(5, 3))
    x_terpene_limonene = fields.Float(string='Limonene %', digits=(5, 3))
    x_terpene_caryophyllene = fields.Float(string='Caryophyllene %', digits=(5, 3))
    x_terpene_pinene = fields.Float(string='Pinene %', digits=(5, 3))
    x_terpene_linalool = fields.Float(string='Linalool %', digits=(5, 3))
    x_terpene_humulene = fields.Float(string='Humulene %', digits=(5, 3))
    x_total_terpenes = fields.Float(string='Total Terpenes %', digits=(5, 2))

    # ===========================================
    # Batch/Lot Tracking
    # ===========================================
    x_batch_id = fields.Char(
        string='Batch ID',
        help='Manufacturing batch identifier'
    )
    x_package_id = fields.Char(
        string='Package ID',
        help='METRC/tracking package ID'
    )
    x_lab_test_status = fields.Selection([
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('passed', 'Passed'),
        ('failed', 'Failed'),
        ('expired', 'Expired'),
    ], string='Lab Test Status',
       default='pending',
       help='Current lab testing status'
    )
    x_tested_date = fields.Date(
        string='Tested Date',
        help='Date lab testing was completed'
    )
    x_harvest_date = fields.Date(
        string='Harvest Date',
        help='Date product was harvested (for flower)'
    )
    x_package_date = fields.Date(
        string='Package Date',
        help='Date product was packaged'
    )
    x_expiration_date = fields.Date(
        string='Expiration Date',
        help='Product expiration date'
    )

    # ===========================================
    # Pricing Fields
    # ===========================================
    x_unit_cost = fields.Float(
        string='Unit Cost',
        digits=(10, 2),
        help='Cost per unit from Dutchie'
    )
    x_special_price = fields.Float(
        string='Special Price',
        digits=(10, 2),
        help='Discounted/sale price'
    )
    x_special_price_rec = fields.Float(
        string='Recreational Special Price',
        digits=(10, 2),
        help='Special price for recreational customers'
    )
    x_special_price_med = fields.Float(
        string='Medical Special Price',
        digits=(10, 2),
        help='Special price for medical patients'
    )
    x_price_rec = fields.Float(
        string='Recreational Price',
        digits=(10, 2),
        help='Regular recreational price'
    )
    x_price_med = fields.Float(
        string='Medical Price',
        digits=(10, 2),
        help='Regular medical patient price'
    )

    # ===========================================
    # Product Size/Weight
    # ===========================================
    x_net_weight = fields.Float(
        string='Net Weight',
        digits=(10, 3),
        help='Product net weight'
    )
    x_net_weight_grams = fields.Float(
        string='Net Weight (g)',
        digits=(10, 3),
        help='Net weight in grams'
    )
    x_weight_unit = fields.Char(
        string='Weight Unit',
        help='Unit of measurement (g, oz, mg, etc.)'
    )
    x_size = fields.Char(
        string='Size',
        help='Product size descriptor'
    )
    x_servings = fields.Integer(
        string='Servings',
        help='Number of servings per package'
    )

    # ===========================================
    # Inventory Fields
    # ===========================================
    x_quantity_available = fields.Float(
        string='Quantity Available',
        digits=(10, 2),
        help='Available quantity from Dutchie (synced)'
    )
    x_quantity_reserved = fields.Float(
        string='Quantity Reserved',
        digits=(10, 2),
        help='Reserved/held quantity'
    )
    x_quantity_on_floor = fields.Float(
        string='Quantity on Floor',
        digits=(10, 2),
        help='Quantity on dispensary floor'
    )
    x_quantity_in_back = fields.Float(
        string='Quantity in Back',
        digits=(10, 2),
        help='Quantity in back stock'
    )
    x_low_stock_threshold = fields.Integer(
        string='Low Stock Threshold',
        default=10,
        help='Alert when quantity falls below this'
    )
    x_reorder_point = fields.Integer(
        string='Reorder Point',
        default=5,
        help='Quantity at which to reorder'
    )

    # ===========================================
    # Media
    # ===========================================
    x_image_url = fields.Char(
        string='Image URL',
        help='Product image URL from Dutchie'
    )
    x_images = fields.Text(
        string='Images (JSON)',
        help='JSON array of all product images'
    )

    # ===========================================
    # Sync Metadata
    # ===========================================
    x_synced_at = fields.Datetime(
        string='Last Synced',
        readonly=True,
        help='Timestamp of last sync from Dutchie'
    )

    @api.model
    def find_or_create_by_sku_location(self, sku, location_id, vals):
        """
        Find existing variant by SKU and location, or create new one.
        Used by sync service to upsert inventory items.
        """
        existing = self.search([
            ('x_dutchie_sku', '=', sku),
            ('x_dutchie_location_id', '=', location_id)
        ], limit=1)

        if existing:
            existing.write(vals)
            return existing
        else:
            vals['x_dutchie_sku'] = sku
            vals['x_dutchie_location_id'] = location_id
            return self.create(vals)

    def action_mark_low_stock(self):
        """Mark products as low stock based on threshold."""
        for product in self:
            if product.x_quantity_available <= product.x_low_stock_threshold:
                # Could trigger notification or workflow here
                pass
