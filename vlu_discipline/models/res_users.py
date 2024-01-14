from odoo import models, fields, api, _
from odoo.osv import expression
import ast


class ResUsers(models.Model):
    _inherit = 'res.users'

    sign_initials = fields.Binary(
        string="Digitial Initials",
        groups="base.group_system,vlu_discipline.group_vlu_staff,"
               "vlu_discipline.group_vlu_teacher, "
               "vlu_discipline.group_vlu_student")

    @api.model
    def _name_search(
            self, name, args=None,
            operator='ilike',
            limit=100, name_get_uid=None):
        args = args or []
        user_ids = []
        if operator not in expression.NEGATIVE_TERM_OPERATORS:
            if operator == 'ilike' and not (name or '').strip():
                domain = []
            else:
                domain = [('login', '=', name)]
            user_ids = self._search(expression.AND(
                [domain, args]), limit=limit, access_rights_uid=name_get_uid)
        if not user_ids:
            user_ids = \
                self._search(expression.AND([['|', ('name', operator, name),
                                              ('partner_id.vlu_code', operator,
                                               name)], args]),
                             limit=limit, access_rights_uid=name_get_uid)
        return user_ids

    """
    :parameter
    :res_id: cursor id model,
    :res_model: model name,
    :type_view: can be form or tree view.
    :template: template mapping user.
    :action: action direct to type view.
    :menu: menu direct to type view.
    :return None
    """

    @api.model
    def send_mail(self, res_id=None, type_view=None, res_model=None,
                  template=None, menu=None, action=None, sender= None):
        self.ensure_one()
        url = "%s/web#id=%s&menu_id=%s&cids=1&action=%s&model" \
              "=%s&view_type=%s" \
              % (
                  self.env['ir.config_parameter'].sudo().get_param(
                      'web.base.url'),
                  res_id,
                  menu.id,
                  action.id,
                  res_model,
                  type_view,
              )
        vals = {
            'message_type': 'user_notification',
            'model': self._name,
            'email_from': self.company_id.email,
            'author_id': self.env.user.partner_id and \
                         self.env.user.partner_id.id,
            'notification_ids': [
                (0, 0,
                 {
                     'res_partner_id': self.partner_id.id,
                     'notification_type': 'inbox',
                 }),
            ],
            'res_id': sender.id,
        }
        template_ctx = {
            'url': url,
        }
        user_received = []
        if self.id not in user_received:
            template.with_context(template_ctx).send_mail(email_values=vals,
                                                          force_send=False,
                                                          res_id=self.id)
