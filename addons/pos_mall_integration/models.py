# -*- coding: utf-8 -*-

from openerp import models, fields, api
import time
import logging
import os

_logger = logging.getLogger(__name__)

class MallIntegrationFile(models.Model):

    _name = 'mall.mall_integration.dailyfile'

    file_name = fields.Text(string='File Name', help="File name")
    uploaded_date = fields.Date(string='Uploaded Date', help="Uploaded Date")

    def generate_integration_file(self, cr, uid, context=None):

        _logger.debug('Generate Integration File')

        today = time.strftime("%Y%m%d")
        temp_today = time.strftime("%d-%m-%Y")

        pos_pool=self.pool.get('pos.order')
        config_pool=self.pool.get('ir.config_parameter')

        tenant_id = config_pool.get_param(cr, uid, "mall.asiamall.mall_tenant_id", default=None, context=context)
        local_directory = config_pool.get_param(cr, uid, "mall.asiamall.temporary_folder", default=None, context=context)

        _logger.debug("Tenant ID: %s", tenant_id)
        _logger.debug('Date: ' + today)
        _logger.debug("cr: %s, uid: %s", cr, uid)

        #search by order date, and pos etc
        ids = pos_pool.search(cr, uid, [], context=context)

        noOfRecord = 0
        totalSales = 0.0
        totalSalesTax = 0.0

        for record in pos_pool.browse(cr, uid, ids, context=context):
            _logger.debug("pos orders: %s", record)
            noOfRecord += 1
            totalSales += record.amount_total
            totalSalesTax += record.amount_tax

        _logger.debug("total sales: %s", totalSales)
        #self.create({'file_name': today})
        #two jobs => 1 create file, one more to transfer file

        #create file
        temp_file_name = tenant_id + today + ".txt"
        temp = os.path.join(local_directory, temp_file_name)
        temp_output = "{0}|{1}|{2}|{3}|{4}".format(totalSales, totalSalesTax, totalSalesTax - totalSales, noOfRecord, temp_today)

        _logger.debug("temp output: %s", temp_output)
        _logger.debug("temp file name: %s", temp_file_name)
        _logger.debug("temp directory: %s", local_directory)

        _logger.debug("writing")
        with open(temp, mode="w") as f:
            f.write(temp_output)

        _logger.debug("completed")
        return True

    def ftp_upload_file(self, cr, uid):
        _logger.debug('FTP Upload File')


    # => need POS id, then generate files
    # => get tenant id from files
    #mall_tenant_id = self.pool.get("ir.config_parameter").get_param(cr, uid, "mall.asiamall.mall_tenant_id", default=None, context=context)