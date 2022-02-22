from odoo import models, fields, api
import random
from datetime import datetime, timedelta
from odoo.exceptions import ValidationError

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
    employeesCourses=fields.One2many('incubadora.courses_wizard','employee')

    def write(self,values):
        super(employee,self).write(values)
        print(values)

    
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
