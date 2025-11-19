from datetime import timedelta
from odoo import models , fields ,api


class Owner(models.Model):
    _name="owner"

    name=fields.Char(required=True)
    phone=fields.Char()
    address=fields.Char()

    create_time = fields.Datetime(default=fields.Datetime.now)
    plus_time = fields.Datetime(compute="_compute_plus_time")

    property_ids=fields.One2many("property" ,"owner_id" )




    @api.depends("create_time")
    def _compute_plus_time(self):
        for rec in self:
            rec.plus_time = rec.create_time + timedelta(hours=1)
