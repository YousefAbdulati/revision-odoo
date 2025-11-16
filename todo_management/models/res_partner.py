from odoo import models , fields

class ResPartner(models.Model):
    _inherit="res.partner"

    todo_task_ids=fields.One2many("todo.task","assign_to")