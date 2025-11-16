from odoo import models , fields

class TodoTask(models.Model):
    _name="todo.task"
    _inherit=["mail.thread","mail.activity.mixin"]


    name=fields.Char(required=True ,size=6)
    _sql_constraints=[('unique_name','unique("name")','This Name Already Exist!'),]


    assign_to=fields.Many2one("res.partner")

    description=fields.Char()
    due_date=fields.Datetime()
    state=fields.Selection([
        ("new","New"),
        ("in_progress","In Progress"),
        ("completed","Completed")
    ],default="new",tracking=True)


    def to_progress(self):
        for rec in self:
            rec.state="in_progress"
            
    def to_completed(self):
        for rec in self:
            rec.state="completed"




    