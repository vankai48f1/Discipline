from odoo import models, fields, api, _


class Semester(models.Model):
    _name = 'semester'

    name = fields.Char(
        string="Name",
        required=True,
    )
    year = fields.Char(
        string="School Year",
        required=True,
    )

    def name_get(self):
        result = []
        for rec in self:
            result.append((rec.id, '%s %s' % (rec.name, rec.year)))
        return result
