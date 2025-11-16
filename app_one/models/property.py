from odoo import models ,fields , api
from odoo.exceptions import ValidationError

class Property(models.Model):
    _name="property"
    _description="Property -__-"
    _inherit=['mail.thread','mail.activity.mixin']


    name=fields.Char(required=True)
    discription=fields.Text()
    postcode=fields.Char(required=True,size=5,tracking=1)

    date_availability=fields.Date()
    expected_price=fields.Float(digits=(0,3))
    selling_price=fields.Float()
    bedrooms=fields.Integer(tracking=True)
    living_area=fields.Integer()

    facades=fields.Integer()
    garage=fields.Boolean()
    garden=fields.Boolean()
    garden_area=fields.Integer()
    garden_orientation=fields.Selection([("north","North"),
                                        ("south","South"),
                                        ("east","East"),
                                        ("west","West")],default="north")
    

    expected_selling_date=fields.Date()
    is_late=fields.Boolean()
    

    owner_id=fields.Many2one("owner")
    phone=fields.Char(related='owner_id.phone')
    address=fields.Char(related='owner_id.address')



    tag_ids=fields.Many2many("tag")

    property_line_ids=fields.One2many("property.line","property_id")

    state=fields.Selection([
        ("draft","Draft"),
        ("pending","Pending"),
        ("sold","Sold"),
        ("closed","Closed"),
    ],default="draft")

    diff=fields.Float(compute="_compute_diff",store=True)


    seq=fields.Char(default="New", readonly=True)


    _sql_constraints=[
        ('unique_name','unique("name")','This name already exist!')
        ]
    
    @api.constrains('bedrooms')
    def _cheak_bedrooms_greater_than_zero(self):
        for rec in self:
            if rec.bedrooms <= 0 :
                raise ValidationError("Enter a valid number for bedrooms")
            

    @api.depends("expected_price","selling_price")       
    def _compute_diff(self):
        for rec in self:
            rec.diff = rec.expected_price - rec.selling_price


    @api.onchange("expected_price" ,"selling_price")       
    def _change_garden_area(self):
        for rec in self:
            if self._origin.id: 
                rec.garden_area = rec.garden_area + 10
                return{
                    "warning":{"title":"warning","message":"garden area changed","type":"notification"}
                }


    def set_draft(self):
        for rec in self:
            rec.state = "draft"

    def set_pending(self):
        for rec in self:
            rec.state = "pending"

    def set_sold(self):
        for rec in self:
            rec.state = "sold"

    def set_closed(self):
        for rec in self:
            rec.state = "closed"


    def check_expected_selling_date(self):
        property_ids=self.search([])
        for rec in property_ids:
            if rec.expected_selling_date and rec.expected_selling_date < fields.date.today():
                rec.is_late = True



    # #create
    # @api.model_create_multi
    # def create(self,vals):
    #     res=super().create(vals)
    #     print("created")
    #     return res
    
    # #read
    # @api.model
    # def _search(self, domain, offset=0, limit=None, order=None, access_rights_uid=None):
    #     res=super()._search(domain, offset, limit, order, access_rights_uid)
    #     print("read")
    #     return res
    # #update
    # def write(self, vals):
    #     res=super().write(vals)
    #     print("updated")
    #     return res
    
    # #delete
    # def unlink(self):
    #     res=super().unlink()
    #     print("deleted")
    #     return res


    @api.model
    def create(self,vals):
        res=super().create(vals)
        if res.seq == 'New':
            res.seq = self.env["ir.sequence"].next_by_code("property_seq")

        return res
    
    # def write(self, vals):
    #     res = super().write(vals)
    #     for rec in self:
    #         if rec.seq in (False, '', 'New'):
    #             rec.seq = self.env["ir.sequence"].next_by_code("property_seq") or 'New'
    #     return res





class PropertyLine(models.Model):
    _name="property.line"


    description=fields.Char()
    area=fields.Char()


    property_id=fields.Many2one("property")




