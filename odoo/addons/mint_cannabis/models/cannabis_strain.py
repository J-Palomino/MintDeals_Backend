# -*- coding: utf-8 -*-

from odoo import models, fields, api


class CannabisStrain(models.Model):
    """
    Cannabis strain master data.

    Tracks strain information including genetics, effects, and terpene profiles.
    """
    _name = 'cannabis.strain'
    _description = 'Cannabis Strain'
    _order = 'name'

    name = fields.Char(
        string='Strain Name',
        required=True,
        index=True,
        help='Common name of the cannabis strain'
    )
    active = fields.Boolean(
        string='Active',
        default=True
    )

    # ===========================================
    # Classification
    # ===========================================
    strain_type = fields.Selection([
        ('indica', 'Indica'),
        ('sativa', 'Sativa'),
        ('hybrid', 'Hybrid'),
        ('hybrid_indica', 'Hybrid (Indica Dominant)'),
        ('hybrid_sativa', 'Hybrid (Sativa Dominant)'),
        ('cbd', 'CBD'),
        ('high_cbd', 'High CBD'),
    ], string='Strain Type',
       required=True,
       default='hybrid',
       help='Primary classification of the strain'
    )

    # ===========================================
    # Genetics
    # ===========================================
    parent_strain_1_id = fields.Many2one(
        'cannabis.strain',
        string='Parent Strain 1',
        help='First parent strain (genetics)'
    )
    parent_strain_2_id = fields.Many2one(
        'cannabis.strain',
        string='Parent Strain 2',
        help='Second parent strain (genetics)'
    )
    genetics = fields.Char(
        string='Genetics',
        help='Genetic lineage description'
    )
    breeder = fields.Char(
        string='Breeder',
        help='Original breeder/creator of the strain'
    )

    # ===========================================
    # Effects & Medical
    # ===========================================
    effects = fields.Text(
        string='Effects',
        help='Comma-separated list of common effects'
    )
    medical_uses = fields.Text(
        string='Medical Uses',
        help='Common medical applications'
    )
    flavors = fields.Text(
        string='Flavors',
        help='Flavor profile descriptions'
    )
    aromas = fields.Text(
        string='Aromas',
        help='Aroma/smell descriptions'
    )

    # ===========================================
    # Typical Potency Ranges
    # ===========================================
    typical_thc_min = fields.Float(
        string='Typical THC Min %',
        digits=(5, 2),
        help='Typical minimum THC percentage'
    )
    typical_thc_max = fields.Float(
        string='Typical THC Max %',
        digits=(5, 2),
        help='Typical maximum THC percentage'
    )
    typical_cbd_min = fields.Float(
        string='Typical CBD Min %',
        digits=(5, 2),
        help='Typical minimum CBD percentage'
    )
    typical_cbd_max = fields.Float(
        string='Typical CBD Max %',
        digits=(5, 2),
        help='Typical maximum CBD percentage'
    )

    # ===========================================
    # Terpene Profile
    # ===========================================
    dominant_terpene = fields.Selection([
        ('myrcene', 'Myrcene'),
        ('limonene', 'Limonene'),
        ('caryophyllene', 'Caryophyllene'),
        ('pinene', 'Pinene'),
        ('linalool', 'Linalool'),
        ('humulene', 'Humulene'),
        ('terpinolene', 'Terpinolene'),
        ('ocimene', 'Ocimene'),
    ], string='Dominant Terpene',
       help='Primary terpene in this strain'
    )
    terpene_profile = fields.Text(
        string='Terpene Profile (JSON)',
        help='JSON object with terpene percentages'
    )

    # ===========================================
    # Metadata
    # ===========================================
    description = fields.Text(
        string='Description',
        help='Detailed strain description'
    )
    image = fields.Binary(
        string='Image',
        attachment=True
    )
    notes = fields.Text(
        string='Internal Notes'
    )

    # ===========================================
    # Relations
    # ===========================================
    product_ids = fields.One2many(
        'product.template',
        'x_strain_id',
        string='Products',
        help='Products using this strain'
    )
    product_count = fields.Integer(
        string='Product Count',
        compute='_compute_product_count',
        store=True
    )

    @api.depends('product_ids')
    def _compute_product_count(self):
        for strain in self:
            strain.product_count = len(strain.product_ids)

    def action_view_products(self):
        """Open products associated with this strain."""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': f'Products - {self.name}',
            'res_model': 'product.template',
            'view_mode': 'list,form',
            'domain': [('x_strain_id', '=', self.id)],
            'context': {'default_x_strain_id': self.id},
        }

    _sql_constraints = [
        ('name_uniq', 'unique(name)', 'Strain name must be unique!'),
    ]
