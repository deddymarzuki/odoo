# -*- coding: utf-8 -*-
from openerp import http

# class PosMallIntegration(http.Controller):
#     @http.route('/pos_mall_integration/pos_mall_integration/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/pos_mall_integration/pos_mall_integration/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('pos_mall_integration.listing', {
#             'root': '/pos_mall_integration/pos_mall_integration',
#             'objects': http.request.env['pos_mall_integration.pos_mall_integration'].search([]),
#         })

#     @http.route('/pos_mall_integration/pos_mall_integration/objects/<model("pos_mall_integration.pos_mall_integration"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('pos_mall_integration.object', {
#             'object': obj
#         })