from odoo import models , fields , api
from odoo.exceptions import ValidationError 

class TodoTask(models.Model):
    _name="todo.task"
    _description = "To-Do Task"
    _inherit=["mail.thread","mail.activity.mixin"]


    active=fields.Boolean(default=True)

    ref=fields.Char(readonly=True)



    name=fields.Char(required=True ,size=6)


    assign_to=fields.Many2one("res.partner")


    description=fields.Char()
    due_date=fields.Datetime()
    state=fields.Selection([
        ("new","New"),
        ("in_progress","In Progress"),
        ("completed","Completed"),
        ("closed","Closed"),
    ],default="new",tracking=True)


    estimated_time=fields.Float()

    time_line_ids=fields.One2many("todo.task.line","todo_task_id")

    is_late=fields.Boolean()


    _sql_constraints=[('unique_name','unique("name")','This Name Already Exist!'),]


    def to_progress(self):
        for rec in self:
            rec.state="in_progress"
            
    def to_completed(self):
        for rec in self:
            rec.state="completed"

    def to_closed(self):
        for rec in self:
            rec.state="closed"


    @api.constrains("estimated_time","time_line_ids")
    def _check_total_time(self):
        for rec in self:
            total = sum(line.time for line in rec.time_line_ids)
            if rec.estimated_time and rec.estimated_time < total:
                raise ValidationError("Total Time is Larger than Estimated Time!!")
            


    def check_due_date(self):
        todo_task_ids = self.search([])

        for rec in todo_task_ids:
            if rec.due_date and rec.due_date < fields.Datetime.now():
                rec.is_late=True



    @api.model
    def create(self, vals):
        res = super().create(vals)
        if res.ref in ("" ,  False , None ) :
            res.ref = self.env["ir.sequence"].next_by_code("task_sequence")
        return res
    
    

    # def write(self, vals):
    #     res = super().write(vals)
    #     for rec in self:
    #         if not rec.ref:
    #             rec.ref = self.env["ir.sequence"].next_by_code("task_sequence")
    #     return res


class TodoTaskLine(models.Model):
    _name="todo.task.line"

    description=fields.Char()
    time=fields.Float()
    date=fields.Date()

    todo_task_id = fields.Many2one("todo.task")


