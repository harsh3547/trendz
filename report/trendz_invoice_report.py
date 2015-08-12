import time , math
from openerp.report import report_sxw
from openerp.osv import osv
from openerp.tools.translate import _
from openerp.tools.amount_to_text_en import amount_to_text 
from datetime import datetime, timedelta

class trendz_invoice_report(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        #print '********************************* report called sd5'
        #print cr,uid,name,context
        self.context=context
        super(trendz_invoice_report, self).__init__(cr, uid, name, context=context)
        
        self.localcontext.update({
                                  'today':time.strftime("%Y%m%d"),
                                  'len':self._len,
                                  'cr':cr,
                                  'uid': uid,
                                  'amount_to_text_report':self._amount_to_text_report,
                                  'split_money':self._split_money,
                                  'get_city_state_zip':self._get_city_state_zip,
                                  'get_pages':self._get_pages,
                                  'fit_number':self._fit_number,
                                  'get_invoice_line_data':self._get_invoice_line_data,
                                  'date_change':self._date_change,
                                  })
    def _date_change(self,date=False):
        print date,type(date)
        if date:
            date1=datetime.strptime(date,"%Y-%m-%d")
            date=date1.strftime("%d-%m-%Y")
            return date
        return ''


    def _get_pages(self):
        cr=self.cr
        uid=self.uid
        effective_line=0
        if self.context.get('active_id',False):
            for obj in self.pool.get('account.invoice').browse(cr,uid,self.context.get('active_id',False),context=None).invoice_line:
                effective_line = effective_line + int(math.ceil(len(obj.name)/41.0))
        #print "no of pages ",int(math.ceil(float(effective_line)/self._fit_number()))
        return int(math.ceil(float(effective_line)/self._fit_number()))
            
    def _get_invoice_line_data(self,page_no):
        cr=self.cr
        uid=self.uid
        lines=[]
        i=0
        fit_number=self._fit_number()
        effective_line=0
        effective_line_printed=0
        if self.context.get('active_id',False):
            for obj in self.pool.get('account.invoice').browse(cr,uid,self.context.get('active_id',False),context=None).invoice_line:
                money_rs_p=self._split_money(obj.price_subtotal)
                abc1=len(obj.name)
                abc2=len(obj.name)/41.0
                abc3=math.ceil(len(obj.name)/41.0)
                abc4=int(math.ceil(len(obj.name)/41.0))
                
                #print "-=-=-=-=-=-=,abc's-=-=",abc1,abc2,abc3,abc4
                effective_line = effective_line + abc4
                #print "----effective_line",effective_line
                i+=1
                if effective_line > page_no*fit_number and effective_line <= (page_no+1)*fit_number:
                    lines.append({'no':str(i),'name':str(obj.name),'qty':str(obj.quantity),'rate':str(obj.price_unit), 'discount':str(obj.discount) or '', 'rupee':str(money_rs_p[0]),'paisa':str(money_rs_p[1]),'effective_line_no':effective_line})
                    effective_line_printed = effective_line
                    print "----effective_line",effective_line , abc1,abc2,abc3,abc4
            print "----------lines , effective_lines",i,effective_line,lines,effective_line_printed    

            for i in range(fit_number*(page_no+1)-effective_line_printed):
                lines.append({'no':False,'name':False,'qty':False,'rate':False, 'discount':False, 'rupee':False,'paisa':False,'effective_line_no':effective_line})
            # to leave space for tax free goods
            for i in range(2):
                lines.append({'no':False,'name':False,'qty':False,'rate':False, 'discount':False, 'rupee':False,'paisa':False,'effective_line_no':effective_line})


        
        no_of_invoice_lines=len(lines)
        return [no_of_invoice_lines,lines]
    
    def _fit_number(self):
        return 27
        
    def _get_city_state_zip(self,partner_obj):
        address = (partner_obj.city if partner_obj.city else '') + (' - '+partner_obj.zip if partner_obj.zip else '') + (', '+partner_obj.state_id.name if partner_obj.state_id else '')
        return address
        
    def _split_money(self,num):
        #print num
        num=str("%.2f"%num)
        #print num
        a=num.split('.')
        #print a
        return a
    
     
    def _amount_to_text_report(self,num):
        ans=amount_to_text(num)
        #print ans
        ans = ans.replace('euro','rupees')
        ans = ans.replace('Cents','paisa')
        ans = ans.replace('Cent','paisa')
        
        #print ans
        return ans  
    
    def _len(self,string):
        return len(string)
        

        
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
