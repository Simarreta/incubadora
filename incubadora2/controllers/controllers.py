# -*- coding: utf-8 -*-
# from odoo import http


# class Incubadora(http.Controller):
#     @http.route('/incubadora/incubadora/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/incubadora/incubadora/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('incubadora.listing', {
#             'root': '/incubadora/incubadora',
#             'objects': http.request.env['incubadora.incubadora'].search([]),
#         })

#     @http.route('/incubadora/incubadora/objects/<model("incubadora.incubadora"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('incubadora.object', {
#             'object': obj
#         })
