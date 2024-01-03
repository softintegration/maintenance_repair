# -*- coding: utf-8 -*-

import ast

from datetime import date, datetime, timedelta

from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import ValidationError
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT


class MaintenanceEquipment(models.Model):
    _inherit = 'maintenance.equipment'

    product_id = fields.Many2one('product.product',string='Product',index=True,domain=[('type','!=','service')])


class MaintenanceRequest(models.Model):
    _inherit = 'maintenance.request'

    repair_ids = fields.One2many('repair.order',compute='_compute_repair_ids')
    repair_ids_count = fields.Integer(compute='_compute_repair_ids_count')

    @api.depends('repair_ids')
    def _compute_repair_ids_count(self):
        for each in self:
            each.repair_ids_count = len(each.repair_ids)

    def _compute_repair_ids(self):
        domain = [('request_id','in',self.ids)]
        self.repair_ids = self.env['repair.order'].search(domain)

    def create_repair_order(self):
        self._check_creation()
        return self._create_repair_order()

    def _check_creation(self):
        for each in self:
            if not each.equipment_id or not each.equipment_id.product_id:
                raise ValidationError(_("Equipement related to product must be specified in order to create à Repair order!"))


    def _create_repair_order(self):
        repair_orders_dicts = []
        for each in self:
            repair_orders_dicts.append(each._prepare_repair_order())
        self.env['repair.order'].create(repair_orders_dicts)

    def _prepare_repair_order(self):
        self.ensure_one()
        # We should specify te default location
        warehouse = self.env['stock.warehouse'].search([('company_id', '=', self.company_id.id)], limit=1)
        return {
            'request_id':self.id,
            'product_id':self.equipment_id.product_id.id,
            'product_uom':self.equipment_id.product_id.uom_id.id,
            'location_id':warehouse.lot_stock_id.id
        }

