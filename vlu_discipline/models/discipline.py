import base64
import io
import json
from datetime import datetime, date
import xlrd, xlwt
import xlsxwriter
from pathlib import Path
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from odoo.tools import date_utils


class Discipline(models.Model):
    _name = 'discipline'
    _description = 'Discipline'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(
        string="Name",
        readonly=True,
        default=_('New')
    )
    description = fields.Text(
        string="Description",
    )
    state = fields.Selection(
        [
            ('draft', 'DRAFT'),
            ('processing', 'PROCESSING'),
            ('done', 'DONE'),
            ('cancel', 'CANCEL')
        ],
        string="State",
        default='draft',
        tracking=1,
        store=True,
        compute="_compute_state",
    )
    semester_id = fields.Many2one(
        comodel_name='semester',
        string="Semester",
    )
    year = fields.Char(
        related='semester_id.year',
        store=True,
    )
    line_ids = fields.One2many(
        comodel_name='discipline.line',
        inverse_name='discipline_id',
        string="Discipline Lines",
    )

    tags_ids = fields.Many2many(
        comodel_name='tags',
        relation='discipline_tags_types',
        column1='discipline_ids',
        column2='tags_ids',
        groups="base.group_system"
    )

    reports = fields.Binary(
        compute='_compute_reports',
    )

    file_import = fields.Binary(
        string="File Import Lines",
    )
    file_import_name = fields.Char()  # Customise File Import Name

    is_exist_line = fields.Boolean(
        compute="_compute_is_exist_line"
    )

    @api.depends('line_ids')
    def _compute_is_exist_line(self):
        for record in self:
            if record.line_ids:
                record.is_exist_line = True
            else:
                record.is_exist_line = False

    # Prepare all data before create multi line
    def prepare_import_data(self):
        self.ensure_one()
        data = base64.decodebytes(self.file_import)
        book = xlrd.open_workbook(file_contents=data)
        sheet = book.sheet_by_index(0)
        vals = {}
        for row in range(1, sheet.nrows):
            if not sheet.cell(row, 0).value:
                raise ValidationError(
                    _("Dòng %s cột %s hiện tại không có giá trị" % (row, "A")))
            if not sheet.cell(row, 1).value:
                raise ValidationError(
                    _("Dòng %s cột %s hiện tại không có giá trị" % (row, "B")))
            id = int(sheet.cell(row, 0).value)
            partner = self.env['res.partner'].search([('vlu_code', '=', id)])[0]
            if sheet.cell(row, 1).value == 'a':
                o_type = self.env['discipline.type'].search(
                    [('code', '=', 'CM')])
            if sheet.cell(row, 1).value == 'b':
                o_type = self.env['discipline.type'].search(
                    [('code', '=', 'QS')])[0]
            if not o_type:
                raise ValidationError(
                    _("Hình thức kỷ luật chưa được cấu hình vui lòng kiểm tra lại dữ liệu"))
            if not partner:
                raise ValidationError(
                    _("Học sinh chưa được cấu hình vui lòng kiểm tra lại dữ "
                      "liệu"))
            else:
                if str(id) in vals:
                    raise ValidationError(
                        _("Mỗi sinh viên trong danh sách phải là duy nhất"))
                else:
                    vals[str(id)] = o_type.code
        return vals

    def act_create_lines(self):
        self.ensure_one()
        if not self.file_import:
            raise ValidationError(
                _("Bạn chưa tải tệp dữ liệu, vui lòng kiểm tra lại."))
        else:
            vals = self.prepare_import_data()
            print(vals)
            for key in vals:
                student = self.env['res.users'].search([('partner_id.vlu_code',
                                                         '=',
                                                         key)])[0]
                d_type = self.env['discipline.type'].search([('code', '=',
                                                              vals[key])])[0]
                if student and d_type:
                    line = self.env['discipline.line'].create({
                        'student_id': student.id,
                        'discipline_type_id': d_type.id,
                    })
                    line.write({
                        'discipline_id': self.id
                    })

    def act_download(self):
        self.ensure_one()
        name = "Sheet"
        if self.semester_id:
            name = self.semester_id.name + self.semester_id.year
        path = str(Path.home() / "Downloads/template.xlsx")
        book = xlsxwriter.Workbook(path)
        sheet = book.add_worksheet(name=name)
        sheet.write("A1", "Students Code")
        sheet.write("B1", "Discipline Types")
        book.close()

    @api.depends('line_ids.state')
    def _compute_state(self):
        self.ensure_one()
        if self.line_ids:
            for line in self.line_ids:
                if line.state != 'done':
                    return
            else:
                self.send_mail_done()
                self.state = 'done'

    def _async_lines_state(self, _state=None, _state_line=None):
        """
        >> async state of lines follow state of list.
        >> :param : current list state.
        >> :param: state line async follow state of list.
        >> :return lines updated state
        """
        self.ensure_one()
        if self.state == _state:
            for line in self.line_ids:
                line.state = _state_line

    def act_cancel(self):
        vals = {'state': 'cancel'}
        o = self._write(vals)
        self._async_lines_state(_state='cancel', _state_line='cancel')
        return o

    def act_draft(self):
        self.ensure_one()
        vals = {'state': 'draft'}
        o = self._write(vals)
        self._async_lines_state(_state='draft', _state_line='draft')
        return o

    def act_lock(self):
        self.ensure_one()
        o = self.write({'state': 'done'})
        self._async_lines_state(_state='done', _state_line='done')
        return o

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'discipline') or _('New')
        return super(Discipline, self).create(vals)

    """
    * Permisson: Staff.
    * Purpose: switch state from 'draft' to 'processing' and send mail to 
            partner related.
    * Ensure some rules: 
        1. Record must be exist.
        2. The lines not empty.
    * :return object updated.
    """

    def act_confirm(self):
        """
        Check lines belong to list.
        :return: Raising exception
        """

        def _is_empty_lines():
            if not self.line_ids:
                raise ValidationError(
                    _("The current processing list is empty, must contain at least one line."))

        self.ensure_one()
        _is_empty_lines()
        self.send_mail_confirm()
        for line in self.line_ids:
            if line.state != 'done':
                o = self.write({'state': 'processing'})
                return o
        else:
            o = self.write({'state': 'done'})
        return o

    def prepare_vals_email_state_new(self):
        menu_id = self.env.ref(
            'vlu_discipline.vlu_discipline_discipline_menu')
        line_menu_id = self.env.ref(
            'vlu_discipline.vlu_discipline_discipline_line_menu_student')
        menu_action_id = self.env.ref(
            'vlu_discipline.vlu_discipline_discipline_action')
        line_menu_action_id = self.env.ref(
            'vlu_discipline.vlu_discipline_discipline_line_action_student')
        student_template_new = self.env.ref(
            'vlu_discipline.mail_template_student_new')
        teacher_template_new = self.env.ref(
            'vlu_discipline.mail_template_teacher_new')
        kwargs = {
            'student_template': student_template_new,
            'teacher_template': teacher_template_new,
            'menu_id': menu_id,
            'line_menu_id': line_menu_id,
            'menu_action_id': menu_action_id,
            'line_menu_action_id': line_menu_action_id,
        }
        return kwargs

    def prepare_vals_email_state_done(self):
        menu_id = self.env.ref(
            'vlu_discipline.vlu_discipline_discipline_menu')
        menu_action_id = self.env.ref(
            'vlu_discipline.vlu_discipline_discipline_action')
        template = self.env.ref('vlu_discipline.mail_template_done')
        vals = {
            'menu_id': menu_id,
            'menu_action_id': menu_action_id,
            'template': template
        }
        return vals

    def send_mail_done(self):
        email_vals = self.prepare_vals_email_state_done()
        self.create_uid.send_mail(res_id=self.id,
                                  type_view='form',
                                  res_model=self._name,
                                  template=email_vals['template'],
                                  menu=email_vals['menu_id'],
                                  action=email_vals['menu_action_id'],
                                  sender=self.env.user.company_id)

    def send_mail_confirm(self):
        email_vals = self.prepare_vals_email_state_new()
        teachers = []
        for line in self.line_ids:
            line.student_id.send_mail(res_id=line.id,
                                      type_view='form',
                                      res_model=line._name,
                                      template=email_vals['student_template'],
                                      menu=email_vals['line_menu_id'],
                                      action=email_vals[
                                          'line_menu_action_id'],
                                      sender=self.env.user)
            if line.teacher_id not in teachers:
                teachers.append(line.teacher_id)
                line.teacher_id.send_mail(res_id=self.id,
                                          type_view='form',
                                          res_model=self._name,
                                          template=email_vals[
                                              'teacher_template'],
                                          menu=email_vals['menu_id'],
                                          action=email_vals[
                                              'menu_action_id'],
                                          sender=self.env.user)
    @api.depends(
        'line_ids.report_file'
    )
    def _compute_reports(self):
        self.ensure_one()
        for line in self.line_ids:
            if line.report_file:
                self.reports = line.report_file