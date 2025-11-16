from odoo import models , fields , api
from odoo.exceptions import ValidationError


class TestA(models.Model):
    _name='test.a'

    name=fields.Char(required=True ,default='stu_' ,size=5)
    code=fields.Integer()
    subjects=fields.Selection([
        ("math","Math"),
        ("arabic","Arabic"),
        ("english","English"),
    ])

    state=fields.Selection([
        ("draft","Draft"),
        ("pending","Pending"),
        ("sold","Sold"),
        ("plus","Plus"),
    ],default="draft")

    old_price=fields.Float()
    discount=fields.Float()

    new_price=fields.Float(compute="_compute_new_price",store=True)


    _sql_constraints=[('unique_code','unique("code")','This Code Already Exists!')]

            
    @api.constrains("code")
    def _code_larger_than_0(self):
        for record in self:
            if record.code < 1 :
                raise ValidationError ("Code Sould be Higher Than 0 !")


    @api.depends("old_price","discount")
    def _compute_new_price(self):
        for rec in self:
            rec.new_price= rec.old_price-rec.discount


    @api.onchange("discount")
    def _cheack_if_big(self):
        for rec in self:
            if rec.discount >= 50:
                return{
                    "warning":{"title":"warning" , "message":"Discount is Larger than 50 !" , "type":"notification" }
                }


    def change_state_to_draft(self):
        for rec in self:
            rec.state="draft"
    def change_state_to_pending(self):
        for rec in self:
            rec.state="pending"
    def change_state_to_sold(self):
        for rec in self:
            rec.state="sold"
