from odoo import models

class AccountMove(models.Model):
    _inherit="account.move"






    def do_action_print(self):
        print("Iam Here Now")