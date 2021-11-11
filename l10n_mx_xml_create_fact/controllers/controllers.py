# -*- coding: utf-8 -*-
# from odoo import http


# class L10nMxXmlCreateFact(http.Controller):
#     @http.route('/l10n_mx_xml_create_fact/l10n_mx_xml_create_fact/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/l10n_mx_xml_create_fact/l10n_mx_xml_create_fact/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('l10n_mx_xml_create_fact.listing', {
#             'root': '/l10n_mx_xml_create_fact/l10n_mx_xml_create_fact',
#             'objects': http.request.env['l10n_mx_xml_create_fact.l10n_mx_xml_create_fact'].search([]),
#         })

#     @http.route('/l10n_mx_xml_create_fact/l10n_mx_xml_create_fact/objects/<model("l10n_mx_xml_create_fact.l10n_mx_xml_create_fact"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('l10n_mx_xml_create_fact.object', {
#             'object': obj
#         })
