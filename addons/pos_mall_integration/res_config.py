# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Business Applications
#    Copyright (C) 2004-2012 OpenERP S.A. (<http://openerp.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import logging

from openerp.osv import fields, osv
from openerp.tools.translate import _

_logger = logging.getLogger(__name__)


class mall_integration_configuration(osv.TransientModel):
    _inherit = 'sale.config.settings'

    _columns = {
        'mall_tenant_id': fields.char('Mall tenant id',
            implied_group='sale.group_invoice_so_lines',
            help="ID given by Mall Management for integration"),
        'ftp_address': fields.char('FTP Address',
            help='IP Address for FTP location'),
        'ftp_user_id': fields.char('FTP User Id',
            help='User id for FTP file transfer'),
        'ftp_password': fields.char('FTP password', help='Passworf for FTP file transfer'),
        'temporary_folder': fields.char('Temporary Folder', help='Temporary folder to create files to store')
    }

    def get_default_mall_tenant_id(self, cr, uid, ids, context=None):
        mall_tenant_id = self.pool.get("ir.config_parameter").get_param(cr, uid, "mall.asiamall.mall_tenant_id", default=None, context=context)
        if mall_tenant_id is None:
            mall_tenant_id = "tenantid.1234"

        return {'mall_tenant_id': mall_tenant_id or False}

    def set_alias_mall_tenant_id(self, cr, uid, ids, context=None):
        config_parameters = self.pool.get("ir.config_parameter")
        for record in self.browse(cr, uid, ids, context=context):
            config_parameters.set_param(cr, uid, "mall.asiamall.mall_tenant_id", record.mall_tenant_id or '', context=context)

    def get_default_ftp_address(self, cr, uid, ids, context=None):
        ftp_address = self.pool.get("ir.config_parameter").get_param(cr, uid, "mall.asiamall.ftp_address", default=None, context=context)
        if ftp_address is None:
            ftp_address = "ftp.add.1234"

        return {'ftp_address': ftp_address or False}

    def set_alias_ftp_address(self, cr, uid, ids, context=None):
        config_parameters = self.pool.get("ir.config_parameter")
        for record in self.browse(cr, uid, ids, context=context):
            config_parameters.set_param(cr, uid, "mall.asiamall.ftp_address", record.ftp_address or '', context=context)

    def get_default_ftp_password(self, cr, uid, ids, context=None):
        ftp_password = self.pool.get("ir.config_parameter").get_param(cr, uid, "mall.asiamall.ftp_password", default=None, context=context)
        if ftp_password is None:
            ftp_password = "ftp.password.1234"

        return {'ftp_password': ftp_password or False}

    def set_alias_ftp_password(self, cr, uid, ids, context=None):
        config_parameters = self.pool.get("ir.config_parameter")
        for record in self.browse(cr, uid, ids, context=context):
            config_parameters.set_param(cr, uid, "mall.asiamall.ftp_password", record.ftp_password or '', context=context)

    def get_default_ftp_user_id(self, cr, uid, ids, context=None):
        ftp_user_id = self.pool.get("ir.config_parameter").get_param(cr, uid, "mall.asiamall.ftp_user_id", default=None, context=context)
        if ftp_user_id is None:
            ftp_user_id = "ftp.userid.1234"

        return {'ftp_user_id': ftp_user_id or False}

    def set_alias_ftp_user_id(self, cr, uid, ids, context=None):
        config_parameters = self.pool.get("ir.config_parameter")
        for record in self.browse(cr, uid, ids, context=context):
            config_parameters.set_param(cr, uid, "mall.asiamall.ftp_user_id", record.ftp_user_id or '', context=context)

    def get_default_temporary_folder(self, cr, uid, ids, context=None):
        temporary_folder = self.pool.get("ir.config_parameter").get_param(cr, uid, "mall.asiamall.temporary_folder", default=None, context=context)
        if temporary_folder is None:
            temporary_folder = "ftp.userid.1234"

        return {'temporary_folder': temporary_folder or False}

    def set_alias_temporary_folder(self, cr, uid, ids, context=None):
        config_parameters = self.pool.get("ir.config_parameter")
        for record in self.browse(cr, uid, ids, context=context):
            config_parameters.set_param(cr, uid, "mall.asiamall.temporary_folder", record.temporary_folder or '', context=context)
