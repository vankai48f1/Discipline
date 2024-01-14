from odoo import models, fields, api, _


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    company_id = fields.Many2one(
        'res.company',
    )
    email = fields.Char(
        string="Email Văn Lang",
        related="company_id.email",
        readonly=False,
    )
