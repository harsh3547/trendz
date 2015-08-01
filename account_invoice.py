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
    
    def _compute_vat_cst(self,cr,uid,ids,field_name,arg,context=None):
        res={}
        print "==============in _compute_vat_cst"
        '''for obj in self.browse(cr,uid,ids,context):
            vat=0.0
            cst=0.0
            vat_id=map(int,obj.vat_inv or [])[0] if map(int,obj.vat_inv or []) else False
            cst_id=map(int,obj.cst_inv or [])[0] if map(int,obj.cst_inv or []) else False
            for line in obj.invoice_line:
                #print "=======",line.invoice_line_tax_id,obj.vat_inv,obj.cst_inv
                tax_ids=map(int,line.invoice_line_tax_id or [])
                #print tax_ids,vat_id,cst_id
                if vat_id and vat_id in tax_ids:
                    #print "1111"
                    vat = vat + line.price_subtotal*obj.vat_inv.amount
                if cst_id and cst_id in tax_ids:
                    #print "2222"
                    cst = cst + line.price_subtotal*obj.cst_inv.amount
            res[obj.id]={'vat_inv_val':vat,
                         'cst_inv_val':cst,}
        print res
        return res'''
        ### if the above method causes problems
        ### before implementing above make account base code and account tax code in tax else it won't
        ### appear in tax_line 
        ################################################
        for obj in self.browse(cr,uid,ids,context):
            vat=0.0
            cst=0.0
            for tax_line in obj.tax_line:
                if tax_line.name==obj.vat_inv.name:
                    vat=vat+tax_line.amount
                if tax_line.name==obj.cst_inv.name:
                    cst=cst+tax_line.amount
            res[obj.id]={'vat_inv_val':vat,
                         'cst_inv_val':cst,}
            
        print res
        return res
        
            
    
    _columns = {
                'transport':fields.char('Goods Sent Through',size=48),
                'gp_no':fields.char('GR/RR No.',size=13),
                'dated':fields.date('Dated',help = "GR/RR No. Dated"),
                'packages':fields.char("No. of Packages",size=8),
                'vat_inv':fields.many2one('account.tax',string="VAT"),
                'vat_inv_val':fields.function(_compute_vat_cst,string=" ",type="float",multi="tax_sums"),
                'cst_inv':fields.many2one('account.tax',string="CST"),
                'cst_inv_val':fields.function(_compute_vat_cst,string=" ",type="float",multi="tax_sums"),
                'billing_type':fields.selection([
                                         ('tax_invoice','Tax Invoice'),
                                         ('retail_invoice','Retail Invoice'),
                                         ('cash_memo','Cash Memo'),
                                         ('bill','Bill')
                                         ],"Billing Type",required = True),
                }
    
    def _get_vat_val(self,cr,uid,context=None):
        view_ref = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'trendz', 'tax_vat_data')
        view_id = view_ref and view_ref[1] or False
        return view_id
        
    def _get_cst_val(self,cr,uid,context=None):
        view_ref = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'trendz', 'tax_cst_data')
        view_id = view_ref and view_ref[1] or False
        return view_id
    
    _defaults = {'billing_type':'bill',
                 'vat_inv':_get_vat_val,
                 'cst_inv':_get_cst_val,
                 }