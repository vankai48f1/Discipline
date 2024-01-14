from odoo import models, fields, api, _


class DisciplineType(models.Model):
    _name = 'discipline.type'
    _description = 'Discipline Type'

    code = fields.Char(
        string="Code",
        required=True,
    )
    name = fields.Char(
        string="Name",
        required=True,
    )
    need_commitment = fields.Boolean(
        string="Need Commitment?"
    )
    active = fields.Boolean(
        string="Activate",
        default=True,
    )

    _sql_constraints = [
        ('discipline_type_unique_code', 'unique(code)',
         'The code discipline type must be unique.')
    ]
