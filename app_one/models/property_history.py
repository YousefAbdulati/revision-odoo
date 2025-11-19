from odoo import models , fields

class PropertyHistory(models.Model):
    _name="property.history"
    _description="Property History"
    _rec_name="property_id"


    user_id=fields.Many2one("res.users")
    property_id=fields.Many2one("property")
    old_state=fields.Char()
    new_state=fields.Char()
    reason=fields.Char()

    property_history_line_ids = fields.One2many("property.history.line" , "property_history_id")


class PropertyHistoryLine(models.Model):
    _name="property.history.line"
    _description="Property History Line"



    description=fields.Char()
    area=fields.Char()

    property_history_id=fields.Many2one("property.history")