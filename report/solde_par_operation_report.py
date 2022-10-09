# -*- coding: utf-8 -*-

from odoo import tools
from odoo import models,fields,api
from odoo.tools.translate import _


class SoldeParOperationReport(models.Model):
    _name = "kmn.solde.par.operation.report"
    _description = "Solde par opération et par compte"
    _auto = False
    _order = "post_date desc, id desc"


    post_date = fields.Date('Date')
    payee_id   = fields.Many2one('res.partner', 'Tiers')
    account_id = fields.Many2one('kmn.accounts', 'Compte')
    solde      = fields.Float("Solde" )




    def init(self):
        cr,uid,context,su = self.env.args
        tools.drop_view_if_exists(cr, 'kmn_solde_par_operation_report')
        cr.execute("""CREATE or REPLACE VIEW kmn_solde_par_operation_report as (
            select 
                row_number() over(order by am.id )  as id,
                am.post_date,
                am.payee_id,
                am.account_id,
                am.value as solde
             from (
                

                select 
                    am.id,
                    am.post_date,
                    am.payee_id,
                    am.account1_id as account_id, 
                    am.value
                from kmn_account_move am

                union

                select 
                    am.id,
                    am.post_date,
                    am.payee_id,
                    am.account2_id as account_id, 
                    -am.value
                from kmn_account_move am
            ) am
        )""")



            # select 
            #     am.id,
            #     am.post_date,
            #     am.payee_id,
            #     am.account1_id as account_id, 
            #     am.value as solde
            #  from kmn_account_move am


            #    (coalesce((select sum(value) from kmn_account_move where account2_id=a.id and post_date<=m.mois),0)-
            #      coalesce((select sum(value) from kmn_account_move where account1_id=a.id and post_date<=m.mois),0)) as solde



# _SELECT_STOCK_MOVE="""
#     select 
#             sm.id                               as move_id,
#             sm2.date                            as date,
#             sm2.product_id                      as product_id, 
#             ic.name                             as category,
#             COALESCE(im.name,id.name)           as mold,
#             COALESCE(spt.name,sm.src)           as type_mv,
#             COALESCE(spt.name,sp.name,sm2.name) as name,
#             sm2.picking_id                      as picking_id,
#             sm2.purchase_line_id,
#             sm2.raw_material_production_id,
#             sm2.production_id,
#             sm2.is_sale_line_id,
#             sm.lot_id                          as lot_id,
#             spl.is_lot_fournisseur             as lot_fournisseur,
#             sm.qty                             as qty,
#             pt.uom_id                          as product_uom,
#             sm.dest                            as location_dest,
#             sm2.is_employee_theia_id	   as is_employee_theia_id,
#             rp.name                            as login
#     from (

#         select 
#             sm.id,
#             sq.lot_id           as lot_id,
#             sum(sq.qty)         as qty,
#             sl1.name            as src,
#             sl2.name            as dest
#         from stock_move sm inner join stock_location        sl1 on sm.location_id=sl1.id
#                             inner join stock_location        sl2 on sm.location_dest_id=sl2.id
#                             left outer join stock_quant_move_rel sqmr on sm.id=sqmr.move_id
#                             left outer join stock_quant            sq on sqmr.quant_id=sq.id
#         where sm.state='done' and sl2.usage='internal' 
#         group by 
#             sm.id,
#             sq.lot_id,
#             sl1.name,
#             sl2.name

#         union

#         select 
#             sm.id,
#             sq.lot_id           as lot_id,
#             -sum(sq.qty)        as qty,
#             sl1.name            as dest,
#             sl2.name            as src
#         from stock_move sm inner join stock_location        sl1 on sm.location_dest_id=sl1.id
#                             inner join stock_location        sl2 on sm.location_id=sl2.id
#                             left outer join stock_quant_move_rel sqmr on sm.id=sqmr.move_id
#                             left outer join stock_quant            sq on sqmr.quant_id=sq.id
#         where sm.state='done' and sl2.usage='internal' 
#         group by 
#             sm.id,
#             sq.lot_id,
#             sl1.name,
#             sl2.name

#     ) sm    inner join stock_move                sm2 on sm.id=sm2.id           
#             inner join product_product            pp on sm2.product_id=pp.id
#             inner join product_template           pt on pp.product_tmpl_id=pt.id
#             inner join res_users                  ru on sm2.write_uid=ru.id
#             inner join res_partner                rp on ru.partner_id=rp.id
#             left outer join stock_picking_type   spt on sm2.picking_type_id=spt.id
#             left outer join stock_picking         sp on sm2.picking_id=sp.id
#             left outer join is_category           ic on pt.is_category_id=ic.id
#             left outer join is_mold               im on pt.is_mold_id=im.id
#             left outer join is_dossierf           id on pt.is_dossierf_id=id.id
#             left outer join stock_production_lot spl on sm.lot_id=spl.id
# """
# #    order by sm2.date desc, sm2.id


