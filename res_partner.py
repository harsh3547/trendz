from openerp.osv import fields, osv

class res_company(osv.osv):
    _inherit = "res.company"
    _description = "Adding Fields"
    _columns = {
                'mobile':fields.char('Mobile'),
                'tin':fields.char('TIN',size=15),
                'gstin':fields.char("GSTIN",size=16)
                }



class res_partner(osv.osv):
    _inherit = "res.partner"
    _description = "Adding Fields"
    _columns = {
                'street': fields.char('Street',size=60),
                'street2': fields.char('Street2',size=60),
                'tin':fields.char('TIN',size=14),
                'cst':fields.char('CST',size=14),
                'gstin':fields.char("GSTIN",size=16)
                }
