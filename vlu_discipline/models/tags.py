from odoo import models, fields, api


class Tags(models.Model):
    _name = 'tags'
    _rec_name = 'types'
    _order = 'id'
    types = fields.Char(
        string="Types"
    )
    color = fields.Integer(
        string="Color",
    )
    active = fields.Boolean(
        string='Activate',
        default=True,
    )
