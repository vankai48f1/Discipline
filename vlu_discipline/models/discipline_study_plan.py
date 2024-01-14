from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.tools.translate import _


class DisciplineStudyPlan(models.Model):
    _name = 'discipline.study.plan'
    _description = 'Discipline Study Plan'

    discipline_line_id = fields.Many2one(
        comodel_name='discipline.line',
        ondelete='cascade',
        string='Discipline Lines',
        require=True,
        readonly=True,
    )
    module = fields.Char(
        string='Module',
        require=True,
    )
    number_of_credit = fields.Integer(
        string='Number of Credits',
        default=1,
    )
    semester = fields.Many2one(
        related='discipline_line_id.semester_id',
        string="Semester",
    )

    @api.constrains('number_of_credit')
    def _check_values(self):
        if self.number_of_credit <= 0:
            raise ValidationError(_("Values should not be zero."))
