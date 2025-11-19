from odoo import  models , fields


class ChangeState(models.TransientModel):
    _name="change.state"

    property_id=fields.Many2one("property")

    state=fields.Selection([
        ('draft','Draft'),
        ('pending','Pending'),
    ])
    reason=fields.Char()


    def confirm_action(self):
        if self.property_id.state == "closed" :
            self.property_id.state = self.state
            self.property_id.create_property_history('closed',self.state ,self.reason)




