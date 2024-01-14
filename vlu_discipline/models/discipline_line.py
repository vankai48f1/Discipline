import json
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import base64


class DisciplineLine(models.Model):
    _name = 'discipline.line'
    _rec_name = 'student_id'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    state = fields.Selection(
        [
            ('draft', 'NEW'),
            ('to_commit', 'TO COMMIT'),
            ('to_validate', 'TO VALIDATE'),
            ('done', 'DONE'),
            ('cancel', 'CANCEL')
        ],
        string="Status",
        readonly=True,
        default='draft',
        tracking=1,
        store=True,
        compute="_compute_state",
    )
    parent_state = fields.Selection(
        related='discipline_id.state'
    )

    student_id = fields.Many2one(
        comodel_name='res.users',
        string="Student",
        required=True,
        domain=lambda self: [('groups_id', '=', self.env.ref(
            'vlu_discipline.group_vlu_student').id)],
    )
    student_code = fields.Char(
        string="Student Code",
        related="student_id.partner_id.vlu_code",
    )
    classes_id = fields.Many2one(
        'classes',
        string="Classes",
        related='student_id.partner_id.classes_id',
    )
    majors_id = fields.Many2one(
        'majors',
        string="Majors",
        related='student_id.partner_id.majors_id',
    )
    teacher_id = fields.Many2one(
        'res.users',
        string="Teacher",
        compute='_compute_teacher_id',
        store=True,
    )
    discipline_type_id = fields.Many2one(
        comodel_name='discipline.type',
        ondelete='restrict',
        string="Discipline Types",
    )
    discipline_id = fields.Many2one(
        comodel_name='discipline',
        string="Discipline",
        ondelete='cascade',
    )

    semester_id = fields.Many2one(
        comodel_name='semester',
        ondelete='restrict',
        string="Semester",
        related='discipline_id.semester_id',
        store=True
    )
    study_plan_ids = fields.One2many(
        comodel_name='discipline.study.plan',
        inverse_name='discipline_line_id',
        string="Discipline Lines",
    )
    excuse = fields.Text(
        string="Your Excuse",
    )
    is_read_excuse = fields.Boolean(
        compute="_is_read_excuse",
    )
    is_excuse = fields.Boolean(
        string="Excuse",
        compute="_compute_is_excuse"
    )

    report_file = fields.Binary(
        string="Report File(PDF)",
        tracking=2,
    )
    file_name = fields.Char(
        compute="_compute_file_name",
    )
    comment = fields.Text(
        string="Comment",
    )
    is_read_comment = fields.Boolean(
        compute="_is_read_comment",
    )

    """
    --------------------------------------------------------------------------------
    """

    def _is_read_excuse(self):
        self.ensure_one()
        if self.env.user.has_group(
                'vlu_discipline.group_vlu_student') \
                or self.env.user.has_group('base.group_system'):
            self.is_read_excuse = False
        else:
            self.is_read_excuse = True

    """
    --------------------------------------------------------------------------------
    """

    def _is_read_comment(self):
        self.ensure_one()
        if self.env.user.has_group(
                'vlu_discipline.group_vlu_teacher') \
                or self.env.user.has_group('base.group_system'):
            self.is_read_comment = False
        else:
            self.is_read_comment = True

    """
    --------------------------------------------------------------------------------
    """

    @api.depends(
        'discipline_type_id.need_commitment'
    )
    def _compute_is_excuse(self):
        for line in self:
            if line.discipline_type_id.need_commitment:
                line.is_excuse = True
            else:
                line.is_excuse = False

    """
    --------------------------------------------------------------------------------
    """

    @api.depends(
        'discipline_id.state',
        'discipline_type_id.need_commitment'
    )
    def _compute_state(self):
        if self.discipline_id.state in ['processing', 'done']:
            for line in self:
                line.ensure_one()
                if line.discipline_type_id.need_commitment and line.state != 'done':
                    line.state = 'to_commit'
                else:
                    line.state = 'done'

    @api.depends(
        'student_id.partner_id.name',
        'student_code',
    )
    def _compute_file_name(self):
        for r in self:
            f_name = 'report_student'
            if r.student_id.partner_id.name and r.student_code:
                f_name = '%s_%s' % (
                    r.student_code, r.student_id.partner_id.name)
            r.file_name = f_name.lower().replace(" ", "_")

    @api.depends(
        'classes_id',
    )
    def _compute_teacher_id(self):
        for line in self:
            line.teacher_id = line.classes_id.teacher_id

    def act_confirm(self):
        for line in self:
            if not line.study_plan_ids or not line.excuse:
                raise ValidationError(
                    _("Please, input your plans study or raise "
                      "some reasons!"))
            line.send_mail_confirm()
            print("click")
            line._write({'state': 'to_validate'})

    def act_validate(self):
        for line in self:
            if not self.comment:
                raise ValidationError(_("Please give some comments about this "
                                        "student."))
            line.send_mail_validate()
            line.state = 'done'
            line._write({'state': 'done'})

    def act_print_report(self):
        self.report_file = base64.b64encode(self.env.ref(
            'vlu_discipline.vlu_discipline_student_report_action'
            '')._render_qweb_pdf(
            self.id)[0])
        return self.env.ref(
            'vlu_discipline.vlu_discipline_student_report_action'
            '').report_action(self)

    def act_approve(self):
        vals = {
            'state': 'to_commit',
            'is_excuse': True,
            "discipline_type_id": self.env['discipline.type'].search([(
                'code', '=', 'CM')]).id,
        }
        return self.write(vals)

    def act_disapprove(self):
        vals = {
            'state': 'done',
            'is_excuse': False,
            "discipline_type_id": self.env['discipline.type'].search([(
                'code', '=', 'QS')]).id,
        }
        return self.write(vals)

    def prepare_vals_email_state_validate(self):
        line_menu_id = self.env.ref(
            'vlu_discipline.vlu_discipline_discipline_line_menu_student')
        line_menu_action_id = self.env.ref(
            'vlu_discipline.vlu_discipline_discipline_line_action_student')
        template_validate = self.env.ref(
            'vlu_discipline.mail_template_validate')
        vals = {
            'template_validate': template_validate,
            'line_menu_id': line_menu_id,
            'line_menu_action_id': line_menu_action_id,
        }
        return vals

    def prepare_vals_email_state_process(self):
        line_menu_id = self.env.ref(
            'vlu_discipline.vlu_discipline_discipline_line_menu_student')
        line_menu_action_id = self.env.ref(
            'vlu_discipline.vlu_discipline_discipline_line_action_student')
        template_process = self.env.ref(
            'vlu_discipline.mail_template_process')
        vals = {
            'template_process': template_process,
            'line_menu_id': line_menu_id,
            'line_menu_action_id': line_menu_action_id,
        }
        return vals

    def send_mail_confirm(self):
        self.ensure_one()
        email_vals = self.prepare_vals_email_state_process()
        self.teacher_id.send_mail(res_id=self.id,
                                  type_view='form',
                                  res_model=self._name,
                                  template=email_vals[
                                      'template_process'],
                                  menu=email_vals['line_menu_id'],
                                  action=email_vals[
                                      'line_menu_action_id'],
                                  sender=self.env.user)

    def send_mail_validate(self):
        self.ensure_one()
        email_vals = self.prepare_vals_email_state_validate()
        self.student_id.send_mail(res_id=self.id,
                                  type_view='form',
                                  res_model=self._name,
                                  template=email_vals[
                                      'template_validate'],
                                  menu=email_vals['line_menu_id'],
                                  action=email_vals[
                                      'line_menu_action_id'],
                                  sender=self.env.user)
