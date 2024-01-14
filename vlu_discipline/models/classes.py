from odoo import models, fields, api, _


class Classes(models.Model):
    _name = 'classes'

    code = fields.Char(
        string="Code",
        required=True,
    )
    name = fields.Char(
        string="Name",
        required=True,
    )
    majors_id = fields.Many2one(
        comodel_name='majors',
        string="Majors",
        ondelete="restrict",
        required=True,
    )
    teacher_id = fields.Many2one(
        comodel_name='res.users',
        string="Teacher",
        ondelete='restrict',
        required=True,
        domain=lambda self: [('groups_id', '=', self.env.ref(
            'vlu_discipline.group_vlu_teacher').id)]
    )

    _sql_constraints = [
        ('classes_unique_code', 'unique(code)',
         'The classes code must be unique.')
    ]
