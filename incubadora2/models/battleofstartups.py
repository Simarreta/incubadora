from sqlite3 import ProgrammingError
from odoo import models, fields, api
import random
from datetime import datetime, timedelta
from odoo.exceptions import ValidationError



class battleofstartups(models.Model):
    _name = 'incubadora.startproyect'
    _inherit='incubadora.startproyect'

    incubadoraPlayerOne=fields.Many2one('res.partner', string="Primera Incubadora:")
    incubadoraPlayerTwo=fields.Many2one('res.partner', string="Segona Incubadora:")
    

class battle_wizard(models.TransientModel):
    _name = 'incubadora.battleofstartups_wizard'
    _description = 'Wizard of battles'  

    def _get_incubadora(self):
        incubadores= self.env.context.get('incubadora_context')
        return incubadores 

    
    name=fields.Char(related="proyects.name",store=True)
    proyects=fields.Many2one('incubadora.proyect', ondelete="cascade")
    quantityofdays=fields.Integer(default=7,readonly=True,string="Quantitat de dies:")
    quantityofemployees=fields.Integer(default=3,readonly=True, string="quantitat treballadors")
    total=fields.Float(compute="_get_total",string="Total")
    moneytoearn=fields.Float(compute="_get_moneytoearn")
    begginingday=fields.Datetime(string= "data d'inici",default=lambda self: fields.Date.today(),readonly=True)
    finishday=fields.Date(compute="_get_end", string="data final")

    incubadoraPlayerOne=fields.Many2one('res.partner',domain="[('is_player','=',True)]",string="Incubadora Uno",default=_get_incubadora)
    quantityofdaysPlayerOne=fields.Integer(default=7,compute="_get_battle",string="Quantitat de dies:")
    employeesPlayerOne=fields.Many2many('incubadora.employee',string="Treballadors Incubadora Uno:")
    betterSkill=fields.Char(compute="_get_betterSkill", string="Millor habilitat")
    moneytoearnPlayerOne=fields.Float(compute="_get_battle")

    incubadoraPlayerTwo=fields.Many2one('res.partner',domain="[('is_player','=',True)]",string="Incubadora Dos")
    quantityofdaysPlayerTwo=fields.Integer(default=7,compute="_get_battle",string="Quantitat de dies:")
    betterSkill2=fields.Char(compute="_get_betterSkill2",string="Millor habilitat")
    moneytoearnPlayerTwo=fields.Float(compute="_get_battle")
    employeesPlayerTwo=fields.Many2many(comodel_name='incubadora.employee', # El model en el que es relaciona
                            relation='empleados_incubadorados', # (opcional) el nom del la taula en mig
                            column1='empleado', # (opcional) el nom en la taula en mig de la columna d'aquest model
                            column2='incubadora', # (opcional) el nom de la columna de l'altre model.
                            string="Treballadors Incubadora Dos:")
    
    state = fields.Selection([('proyect','Proyect'),('incubadorauno','IncubadoraUno'),('incubadorados','IncubadoraDos')], default = 'proyect')


    @api.onchange("incubadoraPlayerOne")
    def _onchange_playerOne(self):
        if(self.incubadoraPlayerOne):
            print("Hola")
            return{
                'domain':{
                    "employeesPlayerOne":[("id","in",self.incubadoraPlayerOne.employees.ids)]
                }

            }
    
    @api.onchange("incubadoraPlayerTwo")
    def _onchange_playerTwo(self):
        if(self.incubadoraPlayerTwo):
            return{
                'domain':{
                    "employeesPlayerTwo":[("id","in",self.incubadoraPlayerTwo.employees.ids)]
                }

            }

    @api.depends("employeesPlayerOne")
    def _get_betterSkill(self):
        for s in self:
            p=0
            m=0
            n=0
            l=0
            s.betterSkill="No té cap habilitat"
            for b in s.employeesPlayerOne:
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
            print("programar",p,"marketing",m,"network",n,"laws",l)
                

    @api.depends("employeesPlayerTwo")
    def _get_betterSkill2(self):
        for s in self:
            p=0
            m=0
            n=0
            l=0
            s.betterSkill2="No té cap habilitat"
            for b in s.employeesPlayerTwo:
                p=p+b.programar
                m=m+b.marketing
                n=n+b.network
                l=l+b.laws

            if(p>n):
                if(p>l):
                    if(p>m):
                        s.betterSkill2="programar"

            if(n>p):
                if(n>l):
                    if(n>m):
                        s.betterSkill2="network"

            if(l>p):
                if(l>n):
                    if(l>m):
                        s.betterSkill2="laws"
                        
            if(m>p):
                if(m>n):
                    if(m>l):
                        s.betterSkill2="marketing"
            print("programar",p,"marketing",m,"network",n,"laws",l)
        

    def _get_battle(self):
        for s in self:
            print("Entra")
            if(s.betterSkill=="programar"):
                    s.quantityofdaysPlayerOne=5
                    s.moneytoearnPlayerOne=s.moneytoearn
                    s.moneytoearnPlayerTwo=0
                    s.quantityofdaysPlayerTwo=s.quantityofdays
            if(s.betterSkill=="network"):
                    s.quantityofdaysPlayerTwo=9
                    s.quantityofdaysPlayerOne=s.quantityofdays
                    s.moneytoearnPlayerOne=s.moneytoearn
                    s.moneytoearnPlayerTwo=0
            if(s.betterSkill=="laws"):
                    s.moneytoearnPlayerTwo=s.moneytoearn-s.moneytoearn*0.20
                    s.moneytoearnPlayerOne=s.moneytoearn
                    s.quantityofdaysPlayerOne=s.quantityofdays
                    s.quantityofdaysPlayerTwo=s.quantityofdays
            if(s.betterSkill=="marketing"):
                    s.moneytoearnPlayerOne=s.moneytoearn+s.moneytoearn*0.20
                    s.moneytoearnPlayerTwo=s.moneytoearn 
                    s.quantityofdaysPlayerOne=s.quantityofdays
                    s.quantityofdaysPlayerTwo=s.quantityofdays      
            if(s.betterSkill2=="programar"):
                    s.quantityofdaysPlayerTwo=5
                    s.quantityofdaysPlayerOne=s.quantityofdays
                    s.moneytoearnPlayerOne=s.moneytoearn
                    s.moneytoearnPlayerTwo=s.moneytoearn
            if(s.betterSkill2=="network"):
                    s.quantityofdaysPlayerOne=9
                    s.quantityofdaysPlayerTwo=s.quantityofdays
                    s.moneytoearnPlayerOne=s.moneytoearn
                    s.moneytoearnPlayerTwo=s.moneytoearn
            if(s.betterSkill2=="laws"):
                    s.moneytoearnPlayerOne=s.moneytoearn-s.moneytoearn/0.20
                    s.moneytoearnPlayerTwo=s.moneytoearn
                    s.quantityofdaysPlayerOne=s.quantityofdays
                    s.quantityofdaysPlayerTwo=s.quantityofdays
            if(s.betterSkill2=="marketing"):
                    s.moneytoearnPlayerTwo=s.moneytoearn+s.moneytoearn*0.20
                    s.moneytoearnPlayerOne=s.moneytoearn
                    s.quantityofdaysPlayerOne=s.quantityofdays
                    s.quantityofdaysPlayerTwo=s.quantityofdays
        
        
        


    @api.depends("quantityofdays")
    def _get_end(self):
        for f in self:
            data = fields.Datetime.from_string(f.begginingday)
            data = data + timedelta(days=f.quantityofdays)
            f.finishday = fields.Datetime.to_string(data)

    @api.depends("proyects")
    def _get_moneytoearn(self):
        for e in self:
            print(e.proyects.moneytoearn)
            e.moneytoearn=e.proyects.moneytoearn+(e.proyects.moneytoearn*0.10)


    def next(self):
        
        state = self.state
        if state == 'proyect' :
            if len(self.proyects)>0:
                self.state = 'incubadorauno'
            else:
                return {
               'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                'message': 'No has triat cap proyecte',
                'type': 'danger',  #types: success,warning,danger,info
                'sticky': False,
                }
                }
        elif state == 'incubadorauno':
            if(len(self.incubadoraPlayerOne)>0)&(len(self.employeesPlayerOne)==self.quantityofemployees):
                print("Poyecto",self.incubadoraPlayerTwo)
                self.state = 'incubadorados'
            else:
                return {
               'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                'message': 'Falten treballadors o incubadora',
                'type': 'danger',  #types: success,warning,danger,info
                'sticky': False,
                }
                }
        return {
            'name': 'Incubadora battle wizard action',
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'new'
        }

    def previous(self):
        state = self.state
        if state == 'incubadorados':
            self.state = 'incubadorauno'
        elif state == 'incubadorauno':
            self.state = 'proyect'
        
    
        return {
            'name': 'Incubadora battle wizard action',
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'new'
        }
   

    def create_battle(self):
        if(len(self.incubadoraPlayerTwo)>0)&(len(self.employeesPlayerOne)==self.quantityofemployees):
            proyect=self.env['incubadora.startproyect'].create({
                'name':self.name,
                'proyects':self.proyects.id,
                'incubadora':self.incubadoraPlayerOne.id,
                'quantityofdays':self.quantityofdaysPlayerOne,
                'quantityofemployees':self.quantityofemployees,
                'state': 'preparation',
                'whoemployees':self.employeesPlayerOne.ids,
                'begginingday':self.begginingday,
                'moneytoearn':self.moneytoearnPlayerOne,
                'finishday':self.finishday
            })
            proyect=self.env['incubadora.startproyect'].create({
                'name':self.name,
                'proyects':self.proyects.id,
                'incubadora':self.incubadoraPlayerTwo.id,
                'quantityofdays':self.quantityofdaysPlayerTwo,
                'quantityofemployees':self.quantityofemployees,
                'state': 'preparation',
                'moneytoearn':self.moneytoearnPlayerTwo,
                'whoemployees':self.employeesPlayerTwo.ids,
                'begginingday':self.begginingday,
                'finishday':self.finishday
            })
            return {
                'name': 'Incubadora battleofstartups',
                'type': 'ir.actions.act_window',
                'res_model': 'incubadora.startproyect',
                'res_id': proyect.id,
                'view_mode': 'form',
                'target': 'current'
            }
        else:
            return {
               'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                'message': 'Falten incubadora o treballadors',
                'type': 'danger',  #types: success,warning,danger,info
                'sticky': False,
                }
                }