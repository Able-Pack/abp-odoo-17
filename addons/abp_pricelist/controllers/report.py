# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo.addons.web.controllers.report import ReportController

import json
import logging

import werkzeug.exceptions
from werkzeug.urls import url_parse

from odoo import http
from odoo.http import content_disposition, request
from odoo.tools.misc import html_escape
from odoo.tools.safe_eval import safe_eval, time


_logger = logging.getLogger(__name__)


class CustomReportController(ReportController):
    # OVERWRITE
    @http.route(['/report/download'], type='http', auth="user")
    def report_download(self, data, context=None, token=None):  # pylint: disable=unused-argument
        """This function is used by 'action_manager_report.js' in order to trigger the download of
        a pdf/controller report.
        
        :param data: a javascript array JSON.stringified containg report internal url ([0]) and
        type [1]
        :returns: Response with an attachment header
        
        """
        requestcontent = json.loads(data)
        url, type_ = requestcontent[0], requestcontent[1]
        reportname = '???'
        try:
            if type_ in ['qweb-pdf', 'qweb-text']:
                converter = 'pdf' if type_ == 'qweb-pdf' else 'text'
                extension = 'pdf' if type_ == 'qweb-pdf' else 'txt'
                
                pattern = '/report/pdf/' if type_ == 'qweb-pdf' else '/report/text/'
                reportname = url.split(pattern)[1].split('?')[0]
                
                docids = None
                if '/' in reportname:
                    reportname, docids = reportname.split('/')
                    
                if docids:
                    # Generic report:
                    response = self.report_routes(reportname, docids=docids, converter=converter, context=context)
                else:
                    # Particular report:
                    data = url_parse(url).decode_query(cls=dict)  # decoding the args represented in JSON
                    if 'context' in data:
                        context, data_context = json.loads(context or '{}'), json.loads(data.pop('context'))
                        context = json.dumps({**context, **data_context})
                    response = self.report_routes(reportname, converter=converter, context=context, **data)
                    
                report = request.env['ir.actions.report']._get_report_from_name(reportname)
                filename = "%s.%s" % (report.name, extension)
                
                if docids:
                    ids = [int(x) for x in docids.split(",") if x.isdigit()]
                    obj = request.env[report.model].browse(ids)
                    if report.print_report_name and not len(obj) > 1:
                        report_name = safe_eval(report.print_report_name, {'object': obj, 'time': time})
                        filename = "%s.%s" % (report_name, extension)
                        
                ### MODIFICATION START
                if 'options' in data:
                    data_options = data.get('options')
                    # Replace 'false' with 'null' to make it a valid JSON string
                    data_options = data_options.replace("false", "null")
                    # Convert the string to a Python dictionary
                    options_dict = json.loads(data_options)
                    custom_filename = options_dict.get('filename')
                    if custom_filename:
                        filename = "%s.%s" % (custom_filename, extension)
                ### MODIFICATION END
                
                response.headers.add('Content-Disposition', content_disposition(filename))
                return response
            else:
                return
        except Exception as e:
            _logger.warning("Error while generating report %s", reportname, exc_info=True)
            se = http.serialize_exception(e)
            error = {
                'code': 200,
                'message': "Odoo Server Error",
                'data': se
            }
            res = request.make_response(html_escape(json.dumps(error)))
            raise werkzeug.exceptions.InternalServerError(response=res) from e