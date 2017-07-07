from openerp.osv import fields, osv

class account_invoice(osv.osv):
    _inherit = "account.invoice"
    _description = "Customizations for Trendz"
    
    
    def invoice_print(self, cr, uid, ids, context=None):
        '''
        This function prints the invoice and mark it as sent, so that we can see more easily the next step of the workflow
        '''
        assert len(ids) == 1, 'This option should only be used for a single id at a time.'
        self.write(cr, uid, ids, {'sent': True}, context=context)
        datas = {
             'ids': ids,
             'model': 'account.invoice',
             'form': self.read(cr, uid, ids[0], context=context)
        }
        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'trendz_account_invoice_report',
            'datas': datas,
            'nodestroy' : True
        }
    
        
            
    
    _columns = {
                'transport':fields.many2one('transport.transport',string='Goods Sent Through'),
                'gp_no':fields.char('GR/RR No.',size=13),
                'dated':fields.date('Dated',help = "GR/RR No. Dated"),
                'packages':fields.char("No. of Packages",size=8),
                'billing_type':fields.selection([
                                         ('tax_invoice','Tax Invoice'),
                                         ('retail_invoice','Retail Invoice'),
                                         ('cash_memo','Cash Memo'),
                                         ('bill','Bill')
                                         ],"Billing Type",required = True),
                'hsn_sac':fields.char("HSN/SAC",size=10),
                'vehicle_no':fields.char("Vehicle No",size=20),
                }
    
    
    _defaults = {'billing_type':'bill',
                 }

class transport_transport(osv.osv):
    _name='transport.transport'
    _columns={'name':fields.char('Transport Name')}
    