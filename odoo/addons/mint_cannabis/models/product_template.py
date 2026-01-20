# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProductTemplate(models.Model):
    """
    Extended product.template for cannabis products.

    Maps to Dutchie product-level data (shared across variants/inventory items).
    """
    _inherit = 'product.template'

    # ===========================================
    # Dutchie Sync Fields
    # ===========================================
    x_dutchie_product_id = fields.Char(
        string='Dutchie Product ID',
        index=True,
        copy=False,
        help='Unique product identifier from Dutchie POS'
    )
    x_dutchie_pos_id = fields.Char(
        string='Dutchie POS ID',
        index=True,
        copy=False,
        help='POS-specific product ID from Dutchie'
    )

    # ===========================================
    # Cannabis Classification
    # ===========================================
    x_is_cannabis = fields.Boolean(
        string='Is Cannabis Product',
        default=True,
        help='Indicates this is a regulated cannabis product'
    )
    x_strain_id = fields.Many2one(
        'cannabis.strain',
        string='Strain',
        help='Cannabis strain associated with this product'
    )
    x_strain_type = fields.Selection([
        ('indica', 'Indica'),
        ('sativa', 'Sativa'),
        ('hybrid', 'Hybrid'),
        ('cbd', 'CBD'),
        ('high_cbd', 'High CBD'),
    ], string='Strain Type',
       help='Primary strain classification'
    )
    x_brand_id = fields.Many2one(
        'cannabis.brand',
        string='Cannabis Brand',
        help='Brand/manufacturer of this cannabis product'
    )

    # ===========================================
    # Product Attributes from Dutchie
    # ===========================================
    x_product_category = fields.Char(
        string='Dutchie Category',
        help='Product category from Dutchie (e.g., Flower, Edibles, Concentrates)'
    )
    x_product_subcategory = fields.Char(
        string='Dutchie Subcategory',
        help='Product subcategory from Dutchie'
    )
    x_dosage_form = fields.Char(
        string='Dosage Form',
        help='Form of the product (e.g., Flower, Gummy, Vape Cart)'
    )

    # ===========================================
    # Effects & Medical Info
    # ===========================================
    x_effects = fields.Text(
        string='Effects (JSON)',
        help='JSON array of effects from Dutchie Plus API'
    )
    x_terpenes = fields.Text(
        string='Terpenes (JSON)',
        help='JSON object of terpene profiles'
    )
    x_medical_only = fields.Boolean(
        string='Medical Only',
        default=False,
        help='Product is only available to medical patients'
    )
    x_special_sale = fields.Boolean(
        string='Special Sale',
        default=False,
        help='Product is marked for special sale'
    )

    # ===========================================
    # Compliance Fields
    # ===========================================
    x_regulatory_category = fields.Char(
        string='Regulatory Category',
        help='Regulatory classification for compliance'
    )
    x_flower_equivalent = fields.Float(
        string='Flower Equivalent (g)',
        digits=(10, 2),
        help='Flower equivalent in grams for compliance tracking'
    )
    x_product_type = fields.Char(
        string='Product Type',
        help='Regulatory product type classification'
    )

    # ===========================================
    # Descriptions
    # ===========================================
    x_description_html = fields.Html(
        string='Description (HTML)',
        help='HTML formatted product description from Dutchie'
    )
    x_slug = fields.Char(
        string='URL Slug',
        help='URL-friendly product identifier from Dutchie Plus'
    )

    # ===========================================
    # Additional Metadata
    # ===========================================
    x_tags = fields.Text(
        string='Tags (JSON)',
        help='JSON array of product tags from Dutchie Plus'
    )
    x_staff_pick = fields.Boolean(
        string='Staff Pick',
        default=False,
        help='Marked as staff pick in Dutchie Plus'
    )
    x_featured = fields.Boolean(
        string='Featured',
        default=False,
        help='Featured product flag'
    )

    # ===========================================
    # Sync Metadata
    # ===========================================
    x_synced_at = fields.Datetime(
        string='Last Synced',
        readonly=True,
        help='Timestamp of last sync from Dutchie'
    )
    x_sync_source = fields.Selection([
        ('dutchie_pos', 'Dutchie POS API'),
        ('dutchie_plus', 'Dutchie Plus API'),
        ('manual', 'Manual Entry'),
    ], string='Sync Source',
       default='dutchie_pos',
       help='Source of the product data'
    )

    @api.model
    def find_or_create_by_dutchie_id(self, dutchie_product_id, vals):
        """
        Find existing product by Dutchie ID or create new one.
        Used by sync service to upsert products.
        """
        existing = self.search([
            ('x_dutchie_product_id', '=', dutchie_product_id)
        ], limit=1)

        if existing:
            existing.write(vals)
            return existing
        else:
            vals['x_dutchie_product_id'] = dutchie_product_id
            return self.create(vals)
