from odoo import models, fields, api, _


class Majors(models.Model):
    _name = 'majors'

    code = fields.Char(
        string="Code",
        required=True,
    )
    name = fields.Char(
        string="Name",
        required=True,
    )
    classes_ids = fields.One2many(
        comodel_name='classes',
        inverse_name='majors_id',
        string='Classes',
    )

    _sql_constraints = [
        ('majors_unique_code', 'unique(code)',
         'The majors code must be unique.')
    ]

