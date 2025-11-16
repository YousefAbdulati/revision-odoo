from odoo import models , fields


class Building(models.Model):
    _name="building"
    _rec_name="name"


    name=fields.Integer()
    no=fields.Integer()
    code=fields.Char()
    active=fields.Boolean(default=True)