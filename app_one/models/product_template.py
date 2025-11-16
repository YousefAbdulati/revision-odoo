from odoo import models,fields


class ProductTemplate(models.Model):
    _inherit="product.template"



    property_id=fields.Many2one("property")


    def action_open_label_layout(self):
        res=super().action_open_label_layout()
        print("gggggggggggggggggggggg")
        return res
    

