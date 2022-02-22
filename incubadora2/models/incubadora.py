from odoo import models, fields, api
import random
from datetime import datetime, timedelta
from odoo.exceptions import ValidationError

class incubadora(models.Model):
    _name = 'res.partner'
  #  _description = 'incubadora.incubadora'
    _inherit='res.partner'

#  name = fields.Char(required=True,string="Nom") 
    is_player = fields.Boolean(default=False,string="Es un jugador?")
    is_premium= fields.Boolean(default=False)
    description= fields.Text()
    money = fields.Float(default=100000, string="Diners")
    company_value = fields.Float(compute="_get_value")
    start_day =fields.Date(string= "Data d'inici partida",default=lambda self: fields.Date.today())
    employees = fields.Many2many('incubadora.employee', domain="[('incubadora','=',False)]")
    quantityofemployees=fields.Integer(compute="_get_employees")
    #debts= fields.Many2many("incubadora.bank", string="Cantidad endeudada")#
    proyectsonboard=fields.One2many('incubadora.startproyect','incubadora', string="Projectes Actuals:")
    incubadoresCourses=fields.One2many('incubadora.courses_wizard','incubadores')
    loaninprocess=fields.Char(string="Prestamo Actual:")
    loan=fields.Float(default=0,string="Cantidad prestado")


    def _apply_premium(self):
        for p in self:
            if(p.is_premium!=True):
                p.is_premium=True

    def _get_value(self):
        for v in self:
            if(v.is_premium!=True):
                v.company_value=0
            else:
                v.company_value=5
    

    def _get_money(self):
        for m in self:
            if(m.is_premium==True):
               m.money=m.money+100000

    @api.depends("employees")
    def _get_employees(self):
         for e in self:
          e.quantityofemployees=len(e.employees)


    def short_term(self):
         for s in self:
            if(s.is_premium!=True):
                s.loan=50000
                s.loaninprocess="Corto Plazo"
            else:
                s.loan=100000
                s.loaninprocess="Corto Plazo"

          
    def long_term(self):
         for s in self:
            if(s.is_premium!=True): 
                s.loan=150000
                s.loaninprocess="Largo Plazo"
            else:
              s.loan=200000
              s.loaninprocess="Largo Plazo"

          
    def half_term(self):
         for s in self:
            if(s.is_premium!=True): 
                s.loan=100000
                s.loaninprocess="Medio Plazo"
            else:
                s.loan=150000
                s.loaninprocess="Medio Plazo"

    @api.constrains("loan")
    def _check_loans(self):
         for e in self:
          if(e.loan>0):
              raise ValidationError('Ya estas pagando un préstamo')

    salary_employees=fields.Float(compute="_get_salary")


    @api.depends("employees")
    def _get_salary(self):
         for e in self:
            if(e.quantityofemployees>0):
             for s in e.employees:
                e.salary_employees=e.salary_employees+s.salary
            else:
                e.salary_employees=0


class product_premium(models.Model):
    _name = 'product.template'
    _inherit = 'product.template'

    is_premium = fields.Boolean(default=False)

class sale_premium(models.Model):
    _name = 'sale.order'
    _inherit = 'sale.order'

    premium_applied= fields.Boolean(default=False)

    def apply_premium(self):
         premium_products = self.order_line.filtered(lambda p: p.product_id.is_premium == True )
         print("hola",premium_products)
         for p in premium_products:
             self.partner_id.is_premium=True

    
    def write(self,values):
        super(sale_premium,self).write(values)
        self.apply_premium()

    @api.model
    def create(self,values):
        record = super(sale_premium,self).create(values)
        record.apply_premium()
        return record