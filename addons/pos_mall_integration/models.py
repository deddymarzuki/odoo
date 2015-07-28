# -*- coding: utf-8 -*-

from openerp import models, fields, api
#import time
import logging
import os
import csv
import base64
from datetime import date, timedelta, datetime
import ftplib
import sys

_logger = logging.getLogger(__name__)

class MallIntegrationFile(models.Model):

    _name = 'mall.mall_integration.dailyfile'

    file_name = fields.Text(string='File Name', help="File name")
    uploaded_date = fields.Date(string='Uploaded Date', help="Uploaded Date")
    value_date = fields.Date(string='Value Date', help="Value date of this file")
    status = fields.Text(string='Upload Status', help="Upload Status")

    def test_import_brand_data(self, cr, uid, context=None):

        _logger.debug("start 5")
        encoded = None
        #with open(image, 'rb') as f:
        #    encoded = base64.b64encode(f.read())

        product_brand_pool=self.pool.get('product.brand')
        pos_category_pool=self.pool.get('pos.category')

        filename = "E:\\Temporary\\brand.csv"

        with open(filename, 'rb') as csvfile:
            spamreader = csv.DictReader(csvfile, delimiter=',')
            for row in spamreader:
                #print ', '.join(row)
                text = row['Brand']
                _logger.debug(text)
                if row:
                    _logger.debug('add row')
                    logo_filename = row['Picture']

                    if logo_filename:
                        image_dir = "E:\\Temporary\\brand_images\\" + logo_filename.strip()
                        _logger.debug('test image_dir: %s', image_dir)

                        with open(image_dir, 'rb') as imagefile:
                            encoded = base64.b64encode(imagefile.read())

                        product_brand_pool.create(cr, uid, {'name': text, 'logo': encoded}, context=context)
                        pos_category_pool.create(cr, uid, {'name': text, 'sequence': 3, 'image': encoded}, context=context)
                    else:
                        product_brand_pool.create(cr, uid, {'name': text}, context=context)
                        pos_category_pool.create(cr, uid, {'name': text, 'sequence': 3}, context=context)


        _logger.debug("completed 1")
        return True

    def test_import_size(self, cr, uid, context=None):

        product_attribute_pool = self.pool.get('product.attribute')

        attribute_values = []
        attribute_dict = {}

        filename = "E:\\Temporary\\size.csv"

        with open(filename, 'rb') as csvfile:
            spamreader = csv.DictReader(csvfile, delimiter=',')
            for row in spamreader:
                #print ', '.join(row)
                text = row['Size']
                _logger.debug(text)
                if row:
                    _logger.debug('add row size')

                    if text in attribute_dict:
                        #duplocate
                        _logger.debug('duplicate key: ' + text)
                    else:
                        attribute_dict[text] = 1
                        attribute_values.append((0, 0, {'name': text}))

        #add all this to new attribute
        product_attribute_pool.create(cr, uid, {'name': "Size", 'value_ids': attribute_values}, context=context)
        _logger.debug("completed")
        return True

    def test_import_colour(self, cr, uid, context=None):

        product_attribute_pool = self.pool.get('product.attribute')

        attribute_values = []
        attribute_dict = {}

        filename = "E:\\Temporary\\colour.csv"

        with open(filename, 'rb') as csvfile:
            spamreader = csv.DictReader(csvfile, delimiter=',')
            for row in spamreader:
                #print ', '.join(row)
                text = row['Colour']
                _logger.debug(text)
                if row:
                    _logger.debug('add row colour')

                    if text in attribute_dict:
                        #duplocate
                        _logger.debug('duplicate key: ' + text)
                    else:
                        attribute_dict[text] = 1
                        attribute_values.append((0, 0, {'name': text}))

        #add all this to new attribute
        product_attribute_pool.create(cr, uid, {'name': "Colour", 'value_ids': attribute_values}, context=context)
        _logger.debug("completed")
        return True

    def test_import_product_data(self, cr, uid, context=None):

        product_brand_pool = self.pool.get('product.brand')
        product_attribute_pool = self.pool.get('product.attribute')
        product_attribute_value_pool = self.pool.get('product.attribute.value')
        product_attribute_line_pool = self.pool.get('product.attribute.line')
        product_template_pool = self.pool.get('product.template')
        product_product_pool = self.pool.get('product.product')
        pos_category_pool = self.pool.get('pos.category')
        stock_change_pool = self.pool.get('stock.change.product.qty')

        size = None
        color = None

        size_id = product_attribute_pool.search(cr, uid, [['name', '=', 'Size']], context=context)
        for record in product_attribute_pool.browse(cr, uid, size_id, context=context):
            #_logger.debug("size found: " + record.name)
            #_logger.debug("value ids: %s", record.value_ids)
            size = record

        color_id = product_attribute_pool.search(cr, uid, [['name', '=', 'Colour']], context=context)
        for record in product_attribute_pool.browse(cr, uid, color_id, context=context):
            #_logger.debug("color found: " + record.name)
            #_logger.debug("type of value ids: %s", type(record.value_ids))
            #for id in record.value_ids:
            #    _logger.debug("name: %s", id.name)
            color = record

        filename = "E:\\Temporary\\product.csv"

        with open(filename, 'rb') as csvfile:
            #spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
            reader = csv.DictReader(csvfile, delimiter=',')
            for row in reader:
                #Brand,Model,Size,Colour,Serial No,Quantity,Cost,Selling Price,Image
                #print ', '.join(row)
                #text = ''.join(row)
                #_logger.debug(text)
                temp_brand = row['Brand']
                temp_name = row['Model']
                temp_size = row['Size']
                temp_color = row['Colour']
                temp_quantity = row['Quantity']
                temp_list_price = row['Selling Price']
                new_variant = False

                # check if product exist ald, if exist then its adding variant

                existing_prod_id = product_template_pool.search(cr, uid, [['name', '=', temp_name]], context=context)

                # add project template
                if not existing_prod_id:

                    existing_prod_id = product_template_pool.create(cr, uid, {'name': temp_name,
                                                                              'type': 'product',
                                                                              'list_price': temp_list_price}, context=context)

                    brand_id = None
                    pos_category_id = None
                    if temp_brand:
                        brand_id = product_brand_pool.search(cr, uid, [['name', '=', temp_brand]], context=context)
                        pos_category_id = pos_category_pool.search(cr, uid, [['name', '=', temp_brand]], context=context)

                    if brand_id:
                        _logger.debug("adding brand, create new product %s", existing_prod_id)
                        product_template_pool.write(cr, uid, existing_prod_id, {'product_brand_id': brand_id[0],
                                                                                'pos_categ_id': pos_category_id[0]}, context=context)
                    new_variant = True
                else:
                    existing_prod_id = existing_prod_id[0]

                # add variant size
                temp_size_id = None
                temp_color_id = None

                if temp_size:
                    temp_size_id = product_attribute_value_pool.search(cr, uid, [['name', '=', temp_size], ['attribute_id', '=', size.id]])

                    if temp_size_id:
                        _logger.debug("Add size variant - temp_size_id 2")
                        line_id = product_attribute_line_pool.search(cr, uid, [['product_tmpl_id', '=', existing_prod_id], ['attribute_id', '=', size.id]])

                        if line_id:
                            _logger.debug("existing id exist")
                            product_attribute_line_pool.write(cr, uid, line_id, {'value_ids': [(4, temp_size_id[0])]}, context=context)
                        else:
                            _logger.debug("new size variant")
                            product_attribute_line_pool.create(cr, uid, {'product_tmpl_id': existing_prod_id,
                                                                        'attribute_id': size.id,
                                                                        'value_ids': [(4, temp_size_id[0])]}, context=context)

                if temp_color:
                    temp_color_id = product_attribute_value_pool.search(cr, uid, [['name', '=', temp_color], ['attribute_id', '=', color.id]])

                    if temp_color_id:
                        _logger.debug("Add color variant - temp_size_id 3")
                        line_id = product_attribute_line_pool.search(cr, uid, [['product_tmpl_id', '=', existing_prod_id], ['attribute_id', '=', color.id]])

                        if line_id:
                            _logger.debug("existing color id exist")
                            product_attribute_line_pool.write(cr, uid, line_id, {'value_ids': [(4, temp_color_id[0])]}, context=context)
                        else:
                            _logger.debug("new color variant")
                            product_attribute_line_pool.create(cr, uid, {'product_tmpl_id': existing_prod_id,
                                                                        'attribute_id': color.id,
                                                                        'value_ids': [(4, temp_color_id[0])]}, context=context)

                product_product_id = None

                if new_variant:
                    #add new product_product
                    product_product_id = product_product_pool.search(cr, uid, [['product_tmpl_id', '=', existing_prod_id]], context=context)
                    _logger.debug('found existing product %s', product_product_id)
                    product_product_id = product_product_id[0]

                else:
                    #update existing product_product
                    product_product_id = product_product_pool.create(cr, uid, {'product_tmpl_id': existing_prod_id}, context=context)

                #add variant
                attribute_values = []

                if temp_size_id:
                    attribute_values.append(temp_size_id[0])

                if temp_color_id:
                    attribute_values.append(temp_color_id[0])

                if attribute_values:
                    _logger.debug('update product with attribute values %s', attribute_values)
                    product_product_pool.write(cr, uid, product_product_id, {'attribute_value_ids': [(6, 0, attribute_values)]}, context=context)

                #update quantities
                stock_ids = stock_change_pool.create(cr, uid, {'product_id': product_product_id, 'location_id': 12, 'new_quantity': 1}, context=context)
                stock_change_pool.change_product_qty(cr, uid, stock_ids, context=context)


                #prod_id = product_template_pool.create(cr, uid, {'name': temp_name}, context=context)

                #write
                #_logger.debug("prod id: %s", prod_id)
                #temp_color_id  =
                #product_template_pool.write(cr, uid, existing_prod_id, {'product_brand_id': brand_id[0]}, context=context)

                _logger.debug("quantity completed product id: %s", existing_prod_id)

    def generate_integration_file(self, cr, uid, context=None):

        #todo: status => whether file being transported

        _logger.debug('Generate Integration File 1')
        yesterday = date.today() - timedelta(days=1)
        today = date.today()
        _logger.debug('Yesterday %s', yesterday)
        _logger.debug('Today Date %s', today)

        #today = time.strftime("%Y%m%d")
        #temp_today = time.strftime("%d-%m-%Y")

        pos_pool = self.pool.get('pos.order')
        config_pool = self.pool.get('ir.config_parameter')

        tenant_id = config_pool.get_param(cr, uid, "mall.asiamall.mall_tenant_id", default=None, context=context)
        local_directory = config_pool.get_param(cr, uid, "mall.asiamall.temporary_folder", default=None, context=context)

        if not tenant_id:
            tenant_id = 'None'

        if not local_directory:
            local_directory = 'E:\\Temporary'

        _logger.debug("Tenant ID: %s", tenant_id)

        #search by order date, and pos etc
        #bigger than yesterday, smaller than today (remove time)
        ids = pos_pool.search(cr, uid, [("date_order", '<=', yesterday.strftime("%Y-%m-%d")),
                                        ("date_order", ">=", yesterday.strftime("%Y-%m-%d"))], context=context)

        noOfRecord = 0
        totalSales = 0.0
        totalSalesTax = 0.0

        for record in pos_pool.browse(cr, uid, ids, context=context):
            _logger.debug("pos orders: %s", record)
            noOfRecord += 1
            totalSales += record.amount_total
            totalSalesTax += record.amount_tax

        #_logger.debug("total sales: %s", totalSales)
        #self.create({'file_name': today})
        #two jobs => 1 create file, one more to transfer file

        #create file
        temp_file_name = tenant_id + yesterday.strftime("%Y%m%d") + ".txt"
        temp = os.path.join(local_directory, temp_file_name)
        temp_output = "{0}|{1}|{2}|{3}|{4}".format(totalSales, totalSales + totalSalesTax, totalSalesTax, noOfRecord, yesterday.strftime("%Y%m%d"))

        #_logger.debug("temp output: %s", temp_output)
        #_logger.debug("temp file name: %s", temp_file_name)
        #_logger.debug("temp directory: %s", local_directory)

        #_logger.debug("writing")
        with open(temp, mode="w") as f:
            f.write(temp_output)

        # write
        new_ids = None
        self.create(cr, uid, {'file_name': temp_file_name, 'value_date': yesterday, 'status': 'Pending'} , context=context)

        return True

    def ftp_upload_file(self, cr, uid, context=None):
        _logger.debug('FTP Upload File 1')

        config_pool = self.pool.get('ir.config_parameter')

        #tenant_id = config_pool.get_param(cr, uid, "mall.asiamall.mall_tenant_id", default=None, context=context)
        local_directory = config_pool.get_param(cr, uid, "mall.asiamall.temporary_folder", default=None, context=context)
        ftp_id = config_pool.get_param(cr, uid, "mall.asiamall.ftp_user_id", default=None, context=context)
        ftp_address = config_pool.get_param(cr, uid, "mall.asiamall.ftp_address", default=None, context=context)
        ftp_password = config_pool.get_param(cr, uid, "mall.asiamall.ftp_password", default=None, context=context)


        pending_ids = self.search(cr, uid, [('status', '=', 'Pending')], context=context)
        updated_ids = []

        if pending_ids:
            #set up ftblib
            try:
                ftp = ftplib.FTP(ftp_address)
                ftp.login(ftp_id, ftp_password)
                pending_records = self.browse(cr, uid, pending_ids, context=context)

                for record in pending_records:
                    try:
                        temp = os.path.join(local_directory, record.file_name)
                        ftp.storlines("STOR " + record.file_name, open(temp))
                        updated_ids.append(record.id)
                    except:
                        _logger.error('Unable to upload file %s &s'. temp, sys.exc_info()[0])

                #update uploaded files
                self.write(cr, uid, updated_ids, {'status': 'Uploaded'}, context=context)

            except:
                _logger.error('Unable to connect to ftp library: %s', sys.exc_info()[0])





    # => need POS id, then generate files
    # => get tenant id from files
    #mall_tenant_id = self.pool.get("ir.config_parameter").get_param(cr, uid, "mall.asiamall.mall_tenant_id", default=None, context=context)

class MallUploadFileGenerationWizard(models.TransientModel):

    _name = "mall.mall_integration.dailyfile.wizard"

    value_date = fields.Date(string='Value Date', help="Value date of this file", required=True)

    @api.multi
    def generate(self):
        _logger.debug("selected value date %s", self.value_date)

        yesterday = self.value_date
        yesterday_obj = datetime.strptime(yesterday, '%Y-%m-%d')

        pos_pool = self.env['pos.order']
        config_pool = self.env['ir.config_parameter']

        tenant_id = config_pool.get_param("mall.asiamall.mall_tenant_id")
        local_directory = config_pool.get_param("mall.asiamall.temporary_folder")

        if not tenant_id:
            tenant_id = 'None'

        if not local_directory:
            local_directory = 'E:\\Temporary'

        _logger.debug("Tenant ID: %s", tenant_id)

        #search by order date, and pos etc
        #bigger than yesterday, smaller than today (remove time)
        ids = pos_pool.search([("date_order", '<=', yesterday),
                            ("date_order", ">=", yesterday)])

        noOfRecord = 0
        totalSales = 0.0
        totalSalesTax = 0.0

        for record in ids:
            _logger.debug("pos orders: %s", record)
            noOfRecord += 1
            totalSales += record.amount_total
            totalSalesTax += record.amount_tax

        #_logger.debug("total sales: %s", totalSales)
        #self.create({'file_name': today})
        #two jobs => 1 create file, one more to transfer file

        #create file
        temp_file_name = tenant_id + yesterday_obj.strftime("%Y%m%d") + ".txt"
        temp = os.path.join(local_directory, temp_file_name)
        temp_output = "{0}|{1}|{2}|{3}|{4}".format(totalSales, totalSales + totalSalesTax, totalSalesTax, noOfRecord, yesterday_obj.strftime("%Y%m%d"))

        #_logger.debug("temp output: %s", temp_output)
        #_logger.debug("temp file name: %s", temp_file_name)
        #_logger.debug("temp directory: %s", local_directory)

        #_logger.debug("writing")
        with open(temp, mode="w") as f:
            f.write(temp_output)

        # write
        new_ids = None
        #self.create(cr, uid, {'file_name': temp_file_name, 'value_date': yesterday, 'status': 'Pending'} , context=context)
        self.env['mall.mall_integration.dailyfile'].create({'file_name': temp_file_name, 'value_date': yesterday, 'status': 'Pending'})

        return {}

class MallUploadWizard(models.TransientModel):

    _name = "mall.mall_integration.upload.wizard"

    @api.multi
    def upload(self):
        _logger.debug("upload file")

        #look for files without correct uploadstatus and upload it
        config_pool = self.env['ir.config_parameter']

        local_directory = config_pool.get_param("mall.asiamall.temporary_folder")
        ftp_id = config_pool.get_param("mall.asiamall.ftp_user_id")
        ftp_address = config_pool.get_param("mall.asiamall.ftp_address")
        ftp_password = config_pool.get_param("mall.asiamall.ftp_password")

        daily_pool = self.env['mall.mall_integration.dailyfile']

        pending_ids = daily_pool.search([('status', '=', 'Pending')])
        updated_ids = []

        if pending_ids:
            #set up ftblib
            try:
                ftp = ftplib.FTP(ftp_address)
                ftp.login(ftp_id, ftp_password)

                for record in pending_ids:
                    try:
                        temp = os.path.join(local_directory, record.file_name)
                        ftp.storlines("STOR " + record.file_name, open(temp))
                        updated_ids.append(record.id)
                    except:
                        _logger.error('Unable to upload file %s &s'. temp, sys.exc_info()[0])

                #update uploaded files
                pending_ids.write( {'status': 'Uploaded', 'uploaded_date': datetime.now()})

            except:
                _logger.error('Unable to connect to ftp library: %s', sys.exc_info()[0])


        return {}



