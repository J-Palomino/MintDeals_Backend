# -*- coding: utf-8 -*-

from odoo import models, fields, api


class CannabisBrand(models.Model):
    """
    Cannabis brand/manufacturer master data.

    Tracks brand information for cannabis product manufacturers.
    """
    _name = 'cannabis.brand'
    _description = 'Cannabis Brand'
    _order = 'name'

    name = fields.Char(
        string='Brand Name',
        required=True,
        index=True,
        help='Brand/manufacturer name'
    )
    active = fields.Boolean(
        string='Active',
        default=True
    )

    # ===========================================
    # Dutchie Sync
    # ===========================================
    x_dutchie_brand_id = fields.Char(
        string='Dutchie Brand ID',
        index=True,
        copy=False,
        help='Brand identifier from Dutchie'
    )

    # ===========================================
    # Brand Information
    # ===========================================
    display_name = fields.Char(
        string='Display Name',
        help='Public-facing brand name if different from internal name'
    )
    code = fields.Char(
        string='Brand Code',
        help='Internal brand code/abbreviation'
    )
    brand_type = fields.Selection([
        ('cultivator', 'Cultivator'),
        ('processor', 'Processor'),
        ('dispensary', 'Dispensary Brand'),
        ('manufacturer', 'Manufacturer'),
        ('distributor', 'Distributor'),
    ], string='Brand Type',
       default='manufacturer',
       help='Type of brand/business'
    )

    # ===========================================
    # Contact Information
    # ===========================================
    website = fields.Char(string='Website')
    email = fields.Char(string='Email')
    phone = fields.Char(string='Phone')
    street = fields.Char(string='Street')
    street2 = fields.Char(string='Street 2')
    city = fields.Char(string='City')
    state_id = fields.Many2one(
        'res.country.state',
        string='State'
    )
    zip = fields.Char(string='ZIP')
    country_id = fields.Many2one(
        'res.country',
        string='Country'
    )

    # ===========================================
    # Licensing
    # ===========================================
    license_number = fields.Char(
        string='License Number',
        help='State cannabis license number'
    )
    license_type = fields.Selection([
        ('cultivation', 'Cultivation'),
        ('processing', 'Processing'),
        ('manufacturing', 'Manufacturing'),
        ('distribution', 'Distribution'),
        ('retail', 'Retail'),
    ], string='License Type'
    )
    license_expiry = fields.Date(
        string='License Expiry',
        help='Date license expires'
    )

    # ===========================================
    # Media & Marketing
    # ===========================================
    logo = fields.Binary(
        string='Logo',
        attachment=True
    )
    description = fields.Text(
        string='Description',
        help='Brand description for display'
    )
    featured = fields.Boolean(
        string='Featured Brand',
        default=False,
        help='Show as featured brand'
    )

    # ===========================================
    # Product Categories
    # ===========================================
    specialty = fields.Selection([
        ('flower', 'Flower'),
        ('concentrates', 'Concentrates'),
        ('edibles', 'Edibles'),
        ('vapes', 'Vapes'),
        ('topicals', 'Topicals'),
        ('tinctures', 'Tinctures'),
        ('accessories', 'Accessories'),
        ('multiple', 'Multiple Categories'),
    ], string='Primary Specialty',
       help='Main product category for this brand'
    )
    category_ids = fields.Many2many(
        'product.category',
        string='Product Categories',
        help='Product categories this brand produces'
    )

    # ===========================================
    # Relations
    # ===========================================
    product_ids = fields.One2many(
        'product.template',
        'x_brand_id',
        string='Products',
        help='Products from this brand'
    )
    product_count = fields.Integer(
        string='Product Count',
        compute='_compute_product_count',
        store=True
    )
    partner_id = fields.Many2one(
        'res.partner',
        string='Related Partner',
        help='Linked vendor/partner record'
    )

    # ===========================================
    # Metadata
    # ===========================================
    notes = fields.Text(
        string='Internal Notes'
    )

    @api.depends('product_ids')
    def _compute_product_count(self):
        for brand in self:
            brand.product_count = len(brand.product_ids)

    def action_view_products(self):
        """Open products associated with this brand."""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': f'Products - {self.name}',
            'res_model': 'product.template',
            'view_mode': 'list,form',
            'domain': [('x_brand_id', '=', self.id)],
            'context': {'default_x_brand_id': self.id},
        }

    @api.model
    def find_or_create_by_name(self, name, vals=None):
        """
        Find existing brand by name or create new one.
        Used by sync service to upsert brands.
        """
        if not name:
            return False

        existing = self.search([('name', '=ilike', name)], limit=1)
        if existing:
            if vals:
                existing.write(vals)
            return existing
        else:
            create_vals = {'name': name}
            if vals:
                create_vals.update(vals)
            return self.create(create_vals)

    _sql_constraints = [
        ('name_uniq', 'unique(name)', 'Brand name must be unique!'),
    ]
