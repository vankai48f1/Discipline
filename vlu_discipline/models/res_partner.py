from odoo import models, fields, api, _


class ResPartner(models.Model):
    _inherit = "res.partner"

    vlu_code = fields.Char(
        string="Code",
    )
    majors_id = fields.Many2one(
        comodel_name='majors',
        string="Majors",
        compute="_compute_majors_id",
        readonly=True,
        store=True,
    )
    classes_id = fields.Many2one(
        comodel_name='classes',
        string="Classes",
    )

    _sql_constraints = [
        ('res_partner_unique_code', 'unique(code)',
         'The partner code must be unique.')
    ]

    @api.depends(
        'classes_id'
    )
    def _compute_majors_id(self):
        for rec in self:
            rec.majors_id = rec.classes_id.majors_id

    @api.model
    def _notification(self, message=None, url=None):
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'message': message,
                'type': 'warning',
                'links': {
                    'label': "Ref:",
                    'url': url
                }
            },
            'sticky': False,
        }
