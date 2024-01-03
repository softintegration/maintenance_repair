# Part of Odoo. See LICENSE file for full copyright and licensing details.

from collections import defaultdict
from random import randint

from markupsafe import Markup

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare, is_html_empty
class Repair(models.Model):
    _inherit = 'repair.order'


    request_id = fields.Many2one('maintenance.request',string='Source document',index=True)
