from odoo import models


class ReportDocumentQRcodeAblepack(models.AbstractModel):
    _name = "report.abp_report.report_document_qrcode_abp"
    _description = "Ablepack Report Document QR Code"
    
    def _get_report_values(self, docids, data):
        model = self.env.context.get('active_model')
        docs = self.env[str(model)].browse(docids)
        
        # If printed not using button and don't have data passed
        if not data.get('values'):
            data['values'] = self.env[str(model)]._prepare_report_values(docs)
            
        return {
            'doc_ids' : docids,
            'data' : data.get('values'),
            'docs' : docs,
        }