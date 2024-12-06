from odoo import models
from odoo.addons.abp_utils import views as utils

# TODO: Dynamically or apply to all models
# List of models to apply the logic
target_models = [
    'res.partner',
    'sale.order',
    'stock.picking',
    'account.move',
    'product.template',
    'product.product',
    'product.pricelist',
    'account.journal',
    'mrp.production',
    'mrp.unbuild',
    'stock.scrap',
    'mrp.bom',
    'crm.team',
]

# Define a function to apply field options
def apply_field_options(res):
    """Custom logic to apply field options to views."""
    utils._apply_field_options(
        res,
        ["//*[self::field]"],
        no_create=True,
        no_create_edit=True,
        no_quick_create=True
    )

# Function to dynamically override `get_view` safely
def inject_get_view():
    def _get_view(self, view_id=None, view_type="form", **options):
        # Directly call the parent class' `get_view` method to avoid recursion
        parent = super(models.Model, self)
        res = parent.get_view(view_id, view_type, **options)
        # Modify the result for 'tree' or 'form' views
        if view_type in ("tree", "form"):
            apply_field_options(res)
        return res
    return _get_view

# Dynamically create classes and inject behavior
for model_name in target_models:
    class_name = model_name.replace('.', '_').capitalize()
    globals()[class_name] = type(
        class_name,  # Class name
        (models.Model,),  # Base class
        {
            '_inherit': model_name,
            '__module__': __name__,
            'get_view': inject_get_view(),  # Dynamically inject the `get_view` override
        }
    )