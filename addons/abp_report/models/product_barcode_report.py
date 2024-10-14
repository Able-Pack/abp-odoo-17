from odoo import models


class ReportProductBarcodeAblepack(models.AbstractModel):
    _name = 'report.abp_report.report_product_barcode_abp'
    
    def _get_report_values(self, docids, data):
        model = self.env.context.get('active_model')
        docs = self.env[str(model)].browse(docids)
        
        # If printed not using button and don't have data passed
        if not data.get('data'):
            data['data'] = self.env[str(model)]._prepare_product_label_data(docs)
            
        return {
            'doc_ids' : docids,
            'data' : data.get('data'),
            'docs' : docs,
        }
        