import json
from odoo import http
from odoo.http import content_disposition, request
from odoo.addons.web.controllers.main import _serialize_exception
from odoo.tools import html_escape


class Main(http.Controller):
    @http.route('/xlsx_reports', type='http', auth='public', methods=['POST'],
                csrf=False)
    def get_xlsx(self, model, options, output_format, report_name):
        uid = request.session.uid
        report = request.env[model].with_user(uid)
        options = json.loads(options)
        token = 'dummy-because-api-expects-one'
        try:
            if output_format == 'xlsx':
                response = request.make_response(None,
                                                 headers=[
                                                     ('Content-Type',
                                                      'application/vnd.ms-excel'),
                                                     ('Content-Disposition',
                                                      content_disposition(
                                                          report_name + '.xlsx'))
                                                 ])
                report.get_report_xlsx(options, response)
                response.set_cookie('token', token)
            return response
        except Exception as e:
            se = _serialize_exception(e)
            error = {
                'code': 200,
                'message': 'Odoo Server Error',
                'data': se
            }
            return error
