# -*- coding: utf-8 -*-
{
    'name': 'Mint Cannabis Inventory',
    'version': '18.0.1.0.0',
    'category': 'Inventory/Inventory',
    'summary': 'Cannabis inventory management with Dutchie integration',
    'description': """
Mint Cannabis Inventory Management
==================================

This module extends Odoo's inventory management with cannabis-specific features:

* Cannabis product categorization (Flower, Edibles, Concentrates, etc.)
* Strain management (Indica, Sativa, Hybrid)
* Brand management
* Potency tracking (THC/CBD percentages and mg)
* Batch/Lot tracking with lab test results
* Dutchie POS integration fields
* Multi-location dispensary warehouse management
* Compliance fields (medical only, regulatory category, flower equivalent)

Key Features:
- Sync products from Dutchie POS API
- Track inventory across 32+ dispensary locations
- Manage cannabis-specific product attributes
- Lab test result tracking
- Expiration date management
    """,
    'author': 'Mint Deals',
    'website': 'https://mintdeals.com',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'product',
        'stock',
        'sale',
        'purchase',
        'point_of_sale',
        'stock_account',
        'website',
        'website_sale',
        'mrp',
    ],
    'data': [
        # Security
        'security/ir.model.access.csv',
        # Data
        'data/product_categories.xml',
        'data/product_attributes.xml',
        # Views
        'views/cannabis_strain_views.xml',
        'views/cannabis_brand_views.xml',
        'views/product_views.xml',
        'views/menu_views.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    # 'images': ['static/description/icon.png'],  # Add custom icon later
}
