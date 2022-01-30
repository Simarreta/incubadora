# -*- coding: utf-8 -*-

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
    description= fields.Text()
    money = fields.Float(default=100000, string="Diners")
    company_value = fields.Float(default=0)
    start_day =fields.Date(string= "data d'inici",default=lambda self: fields.Date.today())
    employees = fields.Many2many('incubadora.employee', domain="[('incubadora','=',False)]")
    quantityofemployees=fields.Integer(compute="_get_employees")
    #debts= fields.Many2many("incubadora.bank", string="Cantidad endeudada")#
    proyectsonboard=fields.One2many('incubadora.startproyect','incubadora', string="Projectes Actuals:")
    loaninprocess=fields.Char(string="Prestamo Actual:")
    loan=fields.Float(default=0,string="Cantidad prestado")
    products=fields.Many2many(compute="_get_products")

    def _get_products(self):
        for e in self:
         #productes=self.env['product.product'] millorar
         e.products=10

    @api.depends("employees")
    def _get_employees(self):
         for e in self:
          e.quantityofemployees=len(e.employees)


    def short_term(self):
         for s in self:
          s.loan=50000
          s.loaninprocess="Corto Plazo"

          
    def long_term(self):
         for s in self:
          s.loan=150000
          s.loaninprocess="Largo Plazo"

          
    def half_term(self):
         for s in self:
          s.loan=100000
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


class incubadora_premium(models.Model):
    _name="res.partner"
    _inherit="res.partner"

    company_value = fields.Float(default=5)
    money = fields.Float(default=200000, string="Diners")
    loan=fields.Float(default=0,string="Cantidad prestado")

    def short_term(self):
         for s in self:
          s.loan=100000
          s.loaninprocess="Corto Plazo"

          
    def long_term(self):
         for s in self:
          s.loan=200000
          s.loaninprocess="Largo Plazo"

          
    def half_term(self):
         for s in self:
          s.loan=150000
          s.loaninprocess="Medio Plazo"



class startproyect(models.Model):
    _name = 'incubadora.startproyect'
    _description = 'Comença'

    name=fields.Char(compute="_get_name")
    incubadora=fields.Many2one('res.partner', ondelete="restrict",domain=[('is_player','=',True)])
    proyects=fields.Many2one('incubadora.proyect', ondelete="restrict")
    quantityofdays=fields.Integer(compute="_get_time")
    quantityofemployees=fields.Integer(compute="_get_employees", string="quantitat treballadors")
    #whoemployees=fields.Many2many("incubadora.employee",related="incubadora.employees")
    moneytowaste = fields.Float(compute="_get_salary",string="Cost",help="Els diners que et costarà el projecte")
    whoemployees=fields.Many2many("incubadora.employee")
    begginingday=fields.Datetime(string= "data d'inici",default=lambda self: fields.Date.today())
    finishday=fields.Date(compute="_get_end", string="data final")
    progressitobar=fields.Float(string="Progressio", compute="_get_progress")
    state=fields.Selection([('preparation','En preparació'),('inprogress','En procés'),('finished','Finalitzat')],default="preparation")

    @api.depends("whoemployees")
    def _get_salary(self):
        for e in self:
            e.moneytowaste=0
            for s in e.whoemployees:
                e.moneytowaste=e.moneytowaste+s.salary
                print("Diners que gastar",e.moneytowaste)
                print("Salari",s.salary)

            if(e.moneytowaste>0):
               # e.moneytowaste=0 PER A QUAN EXPLOTA
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
            else:
                f.write({'state':'inprogress'})
                
class startproyect_wizard(models.TransientModel):
    _name = 'incubadora.startproyect_wizard'
    _description = 'Wizard of travels'    

    name=fields.Char(compute="_get_name")
    incubadora=fields.Many2one('res.partner', ondelete="restrict",domain=[('is_player','=',True)])
    proyects=fields.Many2one('incubadora.proyect', ondelete="restrict")
    quantityofdays=fields.Integer(compute="_get_time")
    quantityofemployees=fields.Integer(compute="_get_employees", string="quantitat treballadors")
    moneytowaste = fields.Float(compute="_get_salary",string="Cost",help="Els diners que et costarà el projecte")
    whoemployees=fields.Many2many("incubadora.employee")
    begginingday=fields.Datetime(string= "data d'inici",default=lambda self: fields.Date.today())
    finishday=fields.Date(compute="_get_end", string="data final")
    state = fields.Selection([('nom','Nom'),('employees','Employees'),('dies','Dies'),('diners','Diners')], default = 'nom')

    def next(self):
        state = self.state
        if state == 'nom':
            self.state = 'employees'
        elif state == 'employees':
            self.state = 'dies'
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
            'incubadora':self.incubadora.id,
            'quantityofdays':self.quantityofdays.id,
            'quantityofemployees':self.quantityofemployees,
            'state': 'preparation',
            'moneytowaste':self.moneytowaste,
            'whoemployees':self.whoemployees.ids,
            'begginingday':self.begginingday,
            'finishday':self.finishday
        })
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
                print("Diners que gastar",e.moneytowaste)
                print("Salari",s.salary)

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

    @api.depends("proyects")
    def _get_name(self):
        for e in self:
            e.name=e.proyects.name


class product_premium(models.Model):
    _name = 'product.template'
    _inherit = 'product.template'

    is_premium = fields.Boolean(default=False)

    
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

class employee(models.Model):
    _name = 'incubadora.employee'
    _description = 'employees'

    def _generate_name(self):
        lastname=["Aguilar","Alonso","Alvarez","Arias","Benitez","Blanco","Blesa","Bravo",
            "Caballero","Cabrera","Calvo","Cambil","Campos","Cano","Carmona","Carrasco",
            "Castillo","Castro","Cortes","Crespo","Cruz","Delgado","Diaz","Diez","Dominguez",
            "Duran","Esteban","Fernandez","Ferrer","Flores","Fuentes","Gallardo","Gallego",
            "Garcia","Garrido","Gil","Gimenez","Gomez","Gonzalez","Guerrero","Gutierrez",
            "Hernandez","Herrera","Herrero","Hidalgo","Iglesias","Jimenez","Leon","Lopez",
            "Lorenzo","Lozano","Marin","Marquez","Martin","Martinez","Medina","Mendez",
            "Molina","Montero","Montoro","Mora","Morales","Moreno","Moya","Navarro","Nieto",
            "Ortega","Ortiz","Parra","Pascual","Pastor","Perez","Prieto","Ramirez","Ramos",
            "Rey","Reyes","Rodriguez","Roman","Romero","Rubio","Ruiz","Saez","Sanchez",
            "Santana","Santiago","Santos","Sanz","Serrano","Soler","Soto","Suarez",
            "Torres","Vargas","Vazquez","Vega","Velasco","Vicente","Vidal"
        ]
        firstname = ["Adela","Adelaida","Alba","Albina","Alejandra","Almudena","Amelia","Ana",
            "Anastasia","Andrea","Angela","Ananias","Antonia","Araceli","Ariadna",
            "Ascension","Asuncion","Aurea","Aurelia","Aurora","Barbara","Beatriz",
            "Belen","Bernarda","Blanca","Borja","Candida","Carina","Carmen","Carolina",
            "Catalina","Cecilia","Celia","Celina","Clara","Claudia","Clotilde",
            "Concepcion","Consuelo","Cristina","Dorotea","Elena","Elisa","Elvira",
            "Emilia","Epifania","Esperanza","Ester","Esther","Eugenia","Eulalia",
            "Eva","Fabiola","Fatima","Francisca","Gema","Genoveva","Gertrudis",
            "Gisela","Gloria","Guadalupe","Hildegarda","Ines","Inmaculada","Irene",
            "Isabel","Josefa","Josefina","Juana","Laura","Leocadia","Lidia","Liduvina",
            "Lorena","Lucia","Lucrecia","Luisa","Magdalena","Manuela","Margarita",
            "Marina","Marta","Matilde","Mercedes","Milagros","Miriam","Monica",
            "Montserrat","Natalia","Natividad","Nieves","Noelia","Nuria","Olga",
            "Otilia","Patricia","Paula","Petronila","Pilar","Priscila","Purificacion",
            "Raquel","Rebeca","Remedios","Rita","Rosa","Rosalia","Rosario","Salome",
            "Sandra","Sara","Silvia","Sofia","Soledad","Sonia","Susana","Tania","Teofila",
            "Teresa","Trinidad","Ursula","Vanesa","Veronica","Vicenta","Victoria",
            "Vidal","Virginia","Yolanda","Aaron","Abdon","Abel","Abelardo","Abrahan","Absalon","Acacio","Adalberto",
            "Adan","Adolfo","Adon","Adrian","Agustin","Aitor","Albert","Alberto","Alejandro",
            "Alejo","Alfonso","Alfredo","Alicia","Alipio","Alonso","Alvaro","Amadeo","Amaro",
            "Ambrosio","Amparo","Anatolio","Andres","Angel","Angeles","Aniano","Anna","Anselmo",
            "Antero","Antonio","Aquiles","Aranzazu","Arcadio","Aresio","Aristides","Arnaldo",
            "Artemio","Arturo","Atanasio","Augusto","Aureliano","Aurelio","Baldomero","Balduino",
            "Baltasar","Bartolome","Basileo","Beltran","Benedicto","Benigno","Benito","Benjamin",
            "Bernabe","Bernardo","Blas","Bonifacio","Bruno","Calixto","Camilo","Carlos","Carmelo",
            "Casiano","Casimiro","Casio","Cayetano","Cayo","Ceferino","Celso","Cesar","Cesareo",
            "Cipriano","Cirilo","Cirino","Ciro","Claudio","Cleofas","Colombo","Columba","Columbano",
            "Conrado","Constancio","Constantino","Cosme","Cristian","Cristobal","Daciano","Dacio",
            "Damaso","Damian","Daniel","Dario","David","Democrito","Diego","Dimas","Dolores","Domingo",
            "Donato","Edgar","Edmundo","Eduardo","Eduvigis","Efren","Elias","Eliseo","Emiliano",
            "Emilio","Encarnacion","Enrique","Erico","Ernesto","Esdras","Esiquio","Esteban","Eugenio",
            "Eusebio","Evaristo","Ezequiel","Fabian","Fabio","Facundo","Faustino","Fausto","Federico",
            "Feliciano","Felipe","Felix","Fermin","Fernando","Fidel","Fortunato","Francesc","Francisco",
            "Fulgencio","Gabriel","Gerardo","German","Godofredo","Gonzalo","Gregorio","Guido","Guillermo",
            "Gustavo","Guzman","Hector","Heliodoro","Heraclio","Heriberto","Hilarion","Homero","Honorato",
            "Honorio","Hugo","Humberto","Ifigenia","Ignacio","Ildefonso","Inocencio","Ireneo","Isaac",
            "Isaias","Isidro","Ismael","Ivan","Jacinto","Jacob","Jacobo","Jaime","Jaume","Javier","Jeremias",
            "Jeronimo","Jesus","Joan","Joaquim","Joaquin","Joel","Jonas","Jonathan","Jordi",
            "Jorge","Josafat","Jose","Josep","Josue","Juan","Julia","Julian","Julio","Justino",
            "Juvenal","Ladislao","Laureano","Lazaro","Leandro","Leon","Leonardo","Leoncio","Leonor",
            "Leopoldo","Lino","Lorenzo","Lourdes","Lucano","Lucas","Luciano","Luis","Luz",
            "Macario","Manuel","Mar","Marc","Marcelino","Marcelo","Marcial","Marciano","Marcos",
            "Maria","Mariano","Mario","Martin","Mateo","Matias","Mauricio","Maximiliano","Melchor",
            "Miguel","Miqueas","Mohamed","Moises","Narciso","Nazario","Nemesio","Nicanor",
            "Nicodemo","Nicolas","Nicomedes","Noe","Norberto","Octavio","Odon","Onesimo","Orestes",
            "Oriol","Oscar","oscar","Oseas","Oswaldo","Oto","Pablo","Pancracio","Pascual","Patricio",
            "Pedro","Pio","Poncio","Porfirio","Primo","Probo","Rafael","Raimundo","Ramiro","Ramon",
            "Raul","Reinaldo","Renato","Ricardo","Rigoberto","Roberto","Rocio","Rodrigo","Rogelio",
            "Roman","Romualdo","Roque","Rosendo","Ruben","Rufo","Ruperto","Salomon","Salvador",
            "Salvio","Samuel","Sanson","Santiago","Sebastian","Segismundo","Sergio","Severino",
            "Simeon","Simon","Siro","Sixto","Tadeo","Tarsicio","Teodora","Teodosia","Teofanes",
            "Timoteo","Tito","Tobias","Tomas","Tomas","Toribio","Ubaldo","Urbano","Valentin","Valeriano",
            "Velerio","Venancio","Vicente","Victor","Victorino","Victorio","Virgilio","Vladimiro","Wilfredo",
            "Xavier","Zacarias","Zaqueo"]
        return random.choice(firstname)+" "+random.choice(lastname)

    name = fields.Char(default=_generate_name)
    incubadora = fields.Many2many('res.partner')
    caffeine=fields.Float(default=50)
    happiness=fields.Float(default=100)
    tiredness=fields.Float(default=0)
    salary=fields.Float(compute="_get_salary")
    salaryview=fields.Float()
    intelligencestatic=fields.Float(compute="_get_intelligence")
    proyectonboard=fields.Many2many("incubadora.startproyect")
    intelligence=fields.Float(default=lambda r: random.randint(90,150))
    image = fields.Image(max_width=200, max_height=200)
    quantityofjobs=fields.Integer(compute="_get_job")
    programar=fields.Integer(default=lambda r: random.randint(0,5))
    marketing=fields.Integer(default=lambda r: random.randint(0,5))
    network=fields.Integer(default=lambda r: random.randint(0,5))
    laws=fields.Integer(default=lambda r: random.randint(0,5))
    betterskill=fields.Char(compute="_get_skill")
    quantityofprojects=fields.Integer(compute="_get_project")

    
    def _get_skill(self):
        for s in self:
            s.betterskill="No té cap habilitat"
            if(s.programar>s.network):
                if(s.programar>s.laws):
                    if(s.programar>s.marketing):
                        s.betterskill="programar"

            if(s.network>s.programar):
                if(s.network>s.laws):
                    if(s.network>s.marketing):
                        s.betterskill="network"

            if(s.laws>s.programar):
                if(s.laws>s.network):
                    if(s.laws>s.marketing):
                        s.betterskill="laws"
                        
            if(s.marketing>s.programar):
                if(s.marketing>s.network):
                    if(s.marketing>s.laws):
                        s.betterskill="marketing"
               



    @api.depends('intelligence')
    def _get_intelligence(self):
        for i in self:
            i.intelligencestatic=i.intelligence


    @api.depends('incubadora')
    def _get_job(self):
        for j in self:
            j.quantityofjobs=len(j.incubadora)

    @api.depends('proyectonboard')
    def _get_project(self):
        for j in self:
            j.quantityofprojects=len(j.proyectonboard)

   
    def give_caffeine(self):
        for c in self:
            c.caffeine=c.caffeine+25
            c.happiness=c.happiness+10
            c.tiredness=c.tiredness-15
            c.incubadora.money=c.incubadora.money-250

            if(c.happiness>100):
                c.happiness=100

            if(c.tiredness<0):
                c.tiredness=0
            

    @api.constrains('caffeine')
    def _check_caffeine(self):
         for e in self:
          if(e.caffeine>100):
              e.caffeine=100
              raise ValidationError('Demasiado café. Relajate')

            
            
   
    
    @api.depends('intelligence')
    def _get_salary(self):
        for s in self:
            if(s.intelligence>115):
                s.salary= random.randint(1500,3000)
                s.salaryview=s.salary
            else:
                s.salary= random.randint(900,1500)
                s.salaryview=s.salary


    @api.model
    def update_life(self):
        print("HEy")
        working= self.search([])
        print("Buenas")
        for s in working:
           if(s.quantityofjobs>0):
             if(s.quantityofprojects>0):
              s.happiness=s.happiness-1
              s.caffeine=s.caffeine-5
              s.tiredness=s.tiredness+5
             else:
              s.happiness=s.happiness-2
              s.caffeine=s.caffeine-5
              s.tiredness=s.tiredness+5

           if(s.tiredness>100):
               s.happiness=s.happiness-2
               s.tiredness=100
               s.caffeine=s.caffeine-10

           if(s.caffeine<0):
               s.tiredness=s.tiredness+10
               s.caffeine=100

           print("Hola")
           if(s.happiness<0):
              s.write({'incubadora':[(5,0,0)]})
              s.happiness=100
              s.caffeine=50
              s.tiredness=0

        
class courses_wizard(models.TransientModel):
    _name = 'incubadora.courses_wizard'
    _description = 'Wizard of travels'    

    name=fields.Selection([('programar','Programar'),('marketing','Marketing'),('network','Network'),('laws','Laws')],default="programar")
    #employee=fields.Many2one('incubadora.employee')
    descriptionCourse=fields.Char(compute="_get_description",string="Descripció curs")
    price=fields.Float(default=0)
    state = fields.Selection([('nom','Nom'),('employees','Employees'),('dies','Dies'),('diners','Diners')], default = 'nom')

    def next(self):
        state = self.state
        if state == 'nom':
            self.state = 'employees'
        elif state == 'employees':
            self.state = 'dies'
        elif state == 'dies':
            self.state = 'diners'

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
        if state == 'employees':
            self.state = 'nom'
        elif state == 'dies':
            self.state = 'employees'
        elif state == 'diners':
            self.state = 'dies'
    
        return {
            'name': 'Incubadora courses wizard action',
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'new'
        }

    @api.depends('name')
    def _get_name(self):
        for n in self:
            if (n.name=='programar'):
                n.programar+=1
            if (n.name=='marketing'):
                n.marketing+=1
            if(n.name=='network'):
                n.network+=1
            if(n.name=='laws'):
                n.laws+=1
        
        

    @api.depends('name')
    def _get_description(self):
        for n in self:
            n.descriptionCourse=""
            if (n.name=='rogramar'):
                n.descriptionCourse="Aumenta 1 punt en l'habilitat de Programar"
            if (n.name=='marketing'):
                n.descriptionCourse="Aumenta 1 punt en l'habilitat de Marketing"
            if(n.name=='network'):
                n.descriptionCourse="Aumenta 1 punt en l'habilitat de Network"
            if(n.name=='laws'):
                n.descriptionCourse="Aumenta 1 punt en l'habilitat de Laws"

    def _get_origin(self):
        employee = self.env.context.get('employee_context')
        return employee

    def _get_player(self):
        incubadora = self.env.context.get('incubadora_context')
        return incubadora

      