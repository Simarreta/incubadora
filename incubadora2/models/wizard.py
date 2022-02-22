from odoo import models, fields, api
import random
from datetime import datetime, timedelta
from odoo.exceptions import ValidationError

class startproyect_wizard(models.TransientModel):
    _name = 'incubadora.startproyect_wizard'
    _description = 'Wizard of travels'  

    def _get_incubadora(self):
        
        incubadora= self._context.get('incubadora_course_context')
        return incubadora

    name=fields.Char(related="proyects.name",store=True)
    incubadora=fields.Many2one('res.partner', domain="[('is_player','=',False)]",default=_get_incubadora)
    proyects=fields.Many2one('incubadora.proyect', ondelete="restrict")
    quantityofdays=fields.Integer(compute="_get_time")
    quantityofemployees=fields.Integer(compute="_get_employees", string="quantitat treballadors")
    moneytowaste = fields.Float(compute="_get_salary",string="Cost",help="Els diners que et costarà el projecte")
    total=fields.Float(compute="_get_total",string="Total")
    moneytoearn=fields.Float(related="proyects.moneytoearn")
    whoemployees=fields.Many2many("incubadora.employee")
    begginingday=fields.Datetime(string= "data d'inici",default=lambda self: fields.Date.today())
    finishday=fields.Date(compute="_get_end", string="data final")
    state = fields.Selection([('nom','Nom'),('employees','Employees'),('dies','Dies'),('diners','Diners')], default = 'nom')

    def _get_total(self):
        for t in self:
            t.total=t.moneytoearn-t.moneytowaste


    def next(self):
        state = self.state
        if state == 'nom':
            if len(self.proyects)!=0:
                print(self.proyects)
                self.state = 'employees'
            else:
                return {
               'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                'message': 'No has triat cap projecte',
                'type': 'danger',  #types: success,warning,danger,info
                'sticky': False,
                }
                }

        elif state == 'employees':
            if len(self.whoemployees)==self.quantityofemployees:
                print(self.whoemployees)
                print(self.quantityofemployees)
                self.state = 'dies'
            else:
                return {
               'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                'message': 'Falten treballadors',
                'type': 'danger',  #types: success,warning,danger,info
                'sticky': False,
                }
                }
        elif state == 'dies':
            self.state = 'diners'

        return {
            'name': 'Incubadora startproyect wizard action',
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'new'
        }

    def previous(self):
        state = self.state
        if state == 'employees':
            self.state = 'nom'
        elif state == 'dies':
            self.state = 'employees'
        elif state == 'diners':
            self.state = 'dies'
    
        return {
            'name': 'Incubadora startproyect wizard action',
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'new'
        }

    def create_proyect(self):
        proyect=self.env['incubadora.startproyect'].create({
            'name':self.name,
            'proyects':self.proyects.id,
            'incubadora':self.incubadora.id,
            'quantityofdays':self.quantityofdays,
            'quantityofemployees':self.quantityofemployees,
            'state': 'preparation',
            'moneytowaste':self.moneytowaste,
            'whoemployees':self.whoemployees.ids,
            'begginingday':self.begginingday,
            'finishday':self.finishday
        })
        print("Nom ",self.name)
        return {
            'name': 'Incubadora startproyect',
            'type': 'ir.actions.act_window',
            'res_model': 'incubadora.startproyect',
            'res_id': proyect.id,
            'view_mode': 'form',
            'target': 'current'
        }

    @api.depends("whoemployees")
    def _get_salary(self):
        for e in self:
            e.moneytowaste=0
            for s in e.whoemployees:
                e.moneytowaste=e.moneytowaste+s.salary
               # print("Diners que gastar",e.moneytowaste)
                #print("Salari",s.salary)

            if(e.moneytowaste>0):
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

    @api.constrains('nom')
    def check_things(self):
        for c in self:
            if (c.name ==""):
                raise ValidationError('Falta el nom')



class courses_wizard(models.TransientModel):
    _name = 'incubadora.courses_wizard'
    _description = 'Wizard of travels'  

    def _get_incubadora(self):
        incubadores= self.env.context.get('incubadora_context')
        return incubadores  
    
    def _get_employee(self):
        employee= self.env.context.get('employee_context')
        return employee 

    name=fields.Selection([('programar','Programar'),('marketing','Marketing'),('network','Network'),('laws','Laws'),('ningunCurs','Ningun Curs')],default="ningunCurs")
    incubadores=fields.Many2one('res.partner',domain="[('is_player','=',True)]",string="Incubadora",default=_get_incubadora)
    employee=fields.Many2one('incubadora.employee',default= _get_employee)
    programPoints=fields.Integer(default=0)
    netPoints=fields.Integer(default=0)
    lawsPoints=fields.Integer(default=0)
    markPoints=fields.Integer(default=0)
    descriptionCourse=fields.Char(compute="_get_description",string="Descripció curs")
    improve=fields.Integer(compute="_get_course")
    price=fields.Float(compute="_get_price",default=0)
    state = fields.Selection([('employees','Employees'),('course','Course'),('pay','Pay')], default = 'employees')
    cost=fields.Float(compute="_get_price")


    @api.onchange("employee")
    def _get_skills(self):
        for e in self:
            e.programPoints=e.employee.programar
            e.netPoints=e.employee.network
            e.lawsPoints=e.employee.laws
            e.markPoints=e.employee.marketing

    def _get_price(self):
         for p in self:
             p.cost=p.incubadores.money
             if(p.improve>0):
                 p.price=p.improve*1000
                 p.cost=p.cost-p.price
             else:
                 p.price=0
            
    def next(self):
        state = self.state
        if state == 'employees' :
            self.state = 'course'
        elif state == 'course':
            if self.name !='ningunCurs':
                 print(self.name)
                 self.state = 'pay'
            else:   
                return {
               'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                'message': 'No has triat cap curs',
                'type': 'danger',  #types: success,warning,danger,info
                'sticky': False,
                }
                }
                
            
        

        return {
            'name': 'Incubadora courses wizard action',
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'new'
        }

   

    def previous(self):
        state = self.state
        if state == 'course':
            self.state = 'employees'
        elif state == 'pay':
            self.state = 'course'
        
    
        return {
            'name': 'Incubadora courses wizard action',
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'new'
        }

    def create_course(self):
        self.employee.write({
            'programar':self.programPoints,
            'marketing':self.markPoints,
            'laws':self.lawsPoints,
            'network':self.netPoints            
        })
        self.incubadores.write({
            'money':self.cost
        })
        print(self.employee.programar,self.programPoints)
        return {
            'name': 'Incubadora course',
            'type': 'ir.actions.act_window',
            'res_model': 'incubadora.employee',
            'res_id': self.employee.id,
            'view_mode': 'form',
            'target': 'current'
        }

    @api.depends('name')
    def _get_course(self):
        for n in self:
                print("Primer ",n.programPoints)
                print(n.markPoints)
                print(n.netPoints)
                print("Primer ",n.lawsPoints)
                if (n.name=='ningunCurs'):
                    n.improve=0
                if (n.name=='programar'):
                    n.programPoints=n.programPoints+1
                    n.improve=n.programPoints
                if (n.name=='marketing'):
                    n.markPoints=n.markPoints+1
                    n.improve=n.markPoints
                if(n.name=='network'):
                    n.netPoints=n.netPoints+1
                    n.improve=n.netPoints
                if(n.name=='laws'):
                    n.lawsPoints=n.lawsPoints+1
                    n.improve=n.lawsPoints
                print(n.programPoints)
                print(n.markPoints)
                print(n.netPoints)
                print(n.lawsPoints)
        
        

    @api.depends('name')
    def _get_description(self):
        for n in self:
            n.descriptionCourse=""
            if (n.name=='programar'):
                n.descriptionCourse="Aumenta 1 punt en l'habilitat de Programar"
            if (n.name=='marketing'):
                n.descriptionCourse="Aumenta 1 punt en l'habilitat de Marketing"
            if(n.name=='network'):
                n.descriptionCourse="Aumenta 1 punt en l'habilitat de Network"
            if(n.name=='laws'):
                n.descriptionCourse="Aumenta 1 punt en l'habilitat de Laws"

  

      