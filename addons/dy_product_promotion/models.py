# -*- coding: utf-8 -*-

from openerp import models, fields, api

class ProductPromotion(models.Model):
    _name = 'dy_product_promotion.product_promotion'

    name = fields.Char(string="Promo Code", required=True)
    description = fields.Text()
    start_date = fields.Date(default=fields.Date.today)
    end_date = fields.Date()
    line_items = fields.One2many('dy_product_promotion.product_promotion_line_item', 'product_promotion_id', string='Line Item')

    total_price = fields.Float(compute='_calculate_total_price')

    @api.one
    @api.depends('line_items')
    def _calculate_total_price(self):
        self.total_price = 0
        for line_item in self.line_items:
            self.total_price += line_item.price

class ProductPromotionLineItem(models.Model):
    _name = 'dy_product_promotion.product_promotion_line_item'

    quantity = fields.Integer()
    price = fields.Float(digits=(6, 2), help="Total Price for this line item")
    product = fields.Many2one('product.product', string='Product', required=True)
    product_promotion_id = fields.Many2one('dy_product_promotion.product_promotion', string='Promotion', required=True)