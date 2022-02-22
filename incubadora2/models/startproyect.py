from odoo import models, fields, api
import random
from datetime import datetime, timedelta
from odoo.exceptions import ValidationError

class startproyect(models.Model):
    _name = 'incubadora.startproyect'
    _description = 'Comença'

    name=fields.Char(compute="_get_name")
    incubadora=fields.Many2one('res.partner', ondelete="restrict",domain=[('is_player','=',True)])
    proyects=fields.Many2one('incubadora.proyect', ondelete="restrict", string="Projectes")
    quantityofdays=fields.Integer()
    quantityofemployees=fields.Integer(compute="_get_employees", string="quantitat treballadors")
    #whoemployees=fields.Many2many("incubadora.employee",related="incubadora.employees")
    moneytowaste = fields.Float(string="Cost",help="Els diners que et costarà el projecte")
    moneytoearn=fields.Float(default=0, string="Benefici", help="Els diners que guanyaras")
    total=fields.Float(compute="_get_total",string="Total")
    whoemployees=fields.Many2many("incubadora.employee")
    betterSkill=fields.Char(compute="_get_betterSkill")
    begginingday=fields.Datetime(string= "data d'inici",default=lambda self: fields.Date.today())
    finishday=fields.Date(compute="_get_end", string="data final")
    progressitobar=fields.Float(string="Progressio", compute="_get_progress")
    state=fields.Selection([('preparation','En preparació'),('inprogress','En procés'),('finished','Finalitzat')],default="preparation")

    @api.onchange("proyects")
    def _get_money(self):
        for m in self:
            m.moneytoearn=m.proyects.moneytoearn

    @api.depends("whoemployees")
    def _get_betterSkill(self):
        for s in self:
            p=0
            m=0
            n=0
            l=0
            s.betterSkill="No té cap habilitat"
            for b in s.whoemployees:
                p=p+b.programar
                m=m+b.marketing
                n=n+b.network
                l=l+b.laws

            if(p>n):
                if(p>l):
                    if(p>m):
                        s.betterSkill="programar"

            if(n>p):
                if(n>l):
                    if(n>m):
                        s.betterSkill="network"

            if(l>p):
                if(l>n):
                    if(l>m):
                        s.betterSkill="laws"
                        
            if(m>p):
                if(m>n):
                    if(m>l):
                        s.betterSkill="marketing"
            

    def _get_total(self):
        for t in self:
            t.total=t.moneytoearn-t.moneytowaste

    @api.depends("whoemployees")
    def _get_salary(self):
        for e in self:
            e.moneytowaste=0
            for s in e.whoemployees:
                e.moneytowaste=e.moneytowaste+s.salary
                print("Diners que gastar",e.moneytowaste)
                print("Salari",s.salary)

            if(e.moneytowaste>0):
               # e.moneytowaste=0 #PER A QUAN EXPLOTA
                if(e.quantityofdays==0):
                    e.moneytowaste=0
                else:
                    e.moneytowaste=e.moneytowaste/(e.quantityofdays/30)   
            if(e.moneytowaste<=0):
                e.moneytowaste=0
            

    @api.depends("proyects")
    def _get_employees(self):
        for e in self:
            e.quantityofemployees=e.proyects.quantityofemployees

    @api.depends("quantityofdays")
    def _get_end(self):
        for f in self:
            data = fields.Datetime.from_string(f.begginingday)
            data = data + timedelta(days=f.quantityofdays)
            f.finishday = fields.Datetime.to_string(data)
    
    @api.depends("proyects")
    def _get_time(self):
        for t in self:
            t.quantityofdays=t.proyects.quantityoftime

    @api.depends("proyects")
    def _get_name(self):
        for e in self:
            e.name=e.proyects.name

    @api.model
    def _get_progress(self):
        for f in self:
            hui=datetime.now()
            #print(hui-f.begginingday)
            #print(hui)
            dies=(hui-f.begginingday).total_seconds()/60/60/24
            #print(dies/f.quantityofdays*100)
            #f.progressitobar=dies/f.quantityofdays*100
            if(f.quantityofdays!=0):
                if((dies/f.quantityofdays*100)<100):
                    f.progressitobar=(dies/f.quantityofdays*100)
                else:
                    f.progressitobar=100
                    f.incubadora.money=f.incubadora.money+f.proyects.moneytoearn-f.moneytowaste
                    for s in f.whoemployees:
                        s.happiness=100
                        s.intelligence=s.intelligencestatic
                        
            if(f.progressitobar==0):
                f.write({'state':'preparation'})
            if(f.progressitobar==100):
                f.write({'state':'finished'})
                f.incubadora.company_value=f.incubadora.company_value+1
            else:
                f.write({'state':'inprogress'})

######PREMIUM#####

class startproyect_premium(models.Model):
    _name="sale.order"
    _inherit="sale.order"
   

    quantityofemployees=fields.Integer(compute="_get_employees", string="quantitat treballadors")
    proyects=fields.Many2one('incubadora.proyect', ondelete="restrict") 

    quantityofdays=fields.Integer(compute="_get_time")

    @api.depends("proyects")
    def _get_employees(self):
        for e in self:
            e.quantityofemployees=e.proyects.quantityofemployees-2

    @api.depends("proyects")
    def _get_time(self):
        for t in self:
            if(t.quantityofdays==90):
                 t.quantityofdays=t.proyects.quantityoftime-45
            if(t.quantityofdays==60):
                 t.quantityofdays=t.proyects.quantityoftime-30
            if(t.quantityofdays==30):
                 t.quantityofdays=t.proyects.quantityoftime-15


##############