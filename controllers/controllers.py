# -*- coding: utf-8 -*-
from odoo import http

# class OdooTravelEpenses(http.Controller):
#     @http.route('/odoo_travel_epenses/odoo_travel_epenses/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/odoo_travel_epenses/odoo_travel_epenses/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('odoo_travel_epenses.listing', {
#             'root': '/odoo_travel_epenses/odoo_travel_epenses',
#             'objects': http.request.env['odoo_travel_epenses.odoo_travel_epenses'].search([]),
#         })

#     @http.route('/odoo_travel_epenses/odoo_travel_epenses/objects/<model("odoo_travel_epenses.odoo_travel_epenses"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('odoo_travel_epenses.object', {
#             'object': obj
#         })