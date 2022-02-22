from odoo import models, fields, api
import random
from datetime import datetime, timedelta
from odoo.exceptions import ValidationError

class proyect(models.Model):
    _name = 'incubadora.proyect'
    _description = 'proyect'

    name = fields.Char(required=True,string="Nom del Projecte")
    kindofproyect = fields.Char(required=True,string="Tipus de projecte")
    moneytoearn = fields.Float(string="Benefici",help="Els diners que guanyaràs")
    quantityofemployees = fields.Integer(string="Treballadors necessaris")
    quantityoftime = fields.Integer(compute="_get_difficulty",string="Temps",help="Quants dies son necessaris",default="0")
    difficulty= fields.Selection([('1','Easy'),('2','Intermediate'),('3','Difficult')],default='0')

    @api.depends('difficulty')
    def _get_difficulty(self):
        for d in self:
           if (d.difficulty == "1"):
              d.quantityoftime= 90
              d.quantityofemployees= 5
           if (d.difficulty == "2"):
              d.quantityoftime= 60
              d.quantityofemployees= 4
           if (d.difficulty == "3"):
              d.quantityoftime= 30 
              d.quantityofemployees= 3  
    
    startsproject=fields.One2many('incubadora.startproyect','proyects')
