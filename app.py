from flask import Flask, request, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import ARRAY, TIMESTAMP
import decisao
from sqlalchemy import desc
from fuzzy import Fuzzy
from pdf import create_pdf
import io
import os
import utils
from datetime import datetime

app = Flask(__name__)

# Configuration
db_user = os.environ.get('DB_USER')
db_password = os.environ.get('DB_PASSWORD')
db_port = os.environ.get('DB_PORT')
db_url = os.environ.get('DB_URL')
db_database = os.environ.get('DB_DATABASE')
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_user}:{db_password}@{db_url}:{db_port}/{db_database}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define a model
class Paciente(db.Model):
    __tablename__ = 'pacientes'

    id                              = db.Column(db.Integer, primary_key=True)
    aspecto_pele                    = db.Column(db.String(255))
    aspecto_unha                    = db.Column(db.String(255))
    bordas                          = db.Column(db.String(255))
    claudicacao                     = db.Column(db.Boolean)                 
    comorbidade                     = db.Column(ARRAY(db.Integer))            
    dor                             = db.Column(db.String(255))
    dor_em_elevacao                 = db.Column(db.String(255))
    edema                           = db.Column(db.Integer)                  
    enchimento_capilar              = db.Column(db.String(255))
    exsudato                        = db.Column(db.Integer)
    exsudato_volume                 = db.Column(db.String(255))
    idade                           = db.Column(db.Integer)                  
    itb                             = db.Column(db.Float)
    localizacao                     = db.Column(db.String(255))                  
    condicoes_clinicas_associadas   = db.Column(ARRAY(db.Integer))
    doppler                         = db.Column(ARRAY(db.Integer))                      
    estilo_de_vida                  = db.Column(ARRAY(db.Integer))               
    etnia                           = db.Column(ARRAY(db.Integer))                        
    pilificacao                     = db.Column(db.String(255))                  
    profundidade                    = db.Column(db.String(255))                 
    pulso                           = db.Column(db.String(255))
    risco                           = db.Column(db.Float)                        
    risco_alto_arterial             = db.Column(db.Float)       
    risco_alto_venoso               = db.Column(db.Float)            
    risco_baixo_arterial            = db.Column(db.Float)        
    risco_baixo_venoso              = db.Column(db.Float)          
    risco_moderado_arterial         = db.Column(db.Float)     
    risco_moderado_venoso           = db.Column(db.Float)        
    sexo                            = db.Column(db.String(255))                         
    tamanho_lesao                   = db.Column(db.Float)                
    tempertura                      = db.Column(db.String(255))                   
    tipo                            = db.Column(db.String(255))
    venosa                          = db.Column(db.Float)
    arterial                        = db.Column(db.Float)
    peso                            = db.Column(db.Float)
    altura                          = db.Column(db.Float)
    imc                             = db.Column(db.Float)
    cod_sus                         = db.Column(db.String(255))
    data_exame                      = db.Column(TIMESTAMP)
    nome                            = db.Column(db.String(255))


    def __repr__(self):
        return f"<Paciente {self.id}>"

    def to_dict(self):
        tipo = ""
        risco = ""
        probabilidade = 0.0
        probabilidade_risco = 0.0
        if self.tipo == "venosa":
            tipo = "Venosa"
            probabilidade = self.venosa
            if self.risco_alto_venoso > 0:
                risco = "Alto"
                probabilidade_risco = self.risco_alto_venoso
            elif self.risco_moderado_venoso > 0:
                risco = "Moderado"
                probabilidade_risco = self.risco_moderado_venoso
            elif self.risco_baixo_venoso > 0:
                risco = "Baixo"
                probabilidade_risco = self.risco_baixo_venoso
        if self.tipo == "arterial":
            tipo = "Arterial"
            probabilidade = self.arterial
            if self.risco_alto_arterial > 0:
                risco = "Alto"
                probabilidade_risco = self.risco_alto_arterial
            elif self.risco_moderado_arterial > 0:
                risco = "Moderado"
                probabilidade_risco = self.risco_moderado_arterial
            elif self.risco_baixo_arterial > 0:
                risco = "Baixo"
                probabilidade_risco = self.risco_baixo_arterial

        return {
            "id": self.id,                      
            "aspecto_pele": self.aspecto_pele,                 
            "aspecto_unha": self.aspecto_unha,   
            "bordas": self.bordas,
            "claudicacao": self.claudicacao,                 
            "comorbidade": self.comorbidade,            
            "dor": self.dor,                     
            "dor_em_elevacao": self.dor_em_elevacao,      
            "edema": self.edema,                        
            "enchimento_capilar": self.enchimento_capilar,      
            "exsudato": self.exsudato,                     
            "exsudato_volume": self.exsudato_volume,              
            "idade": self.idade,                        
            "itb": self.itb,                          
            "localizacao": self.localizacao,                  
            "condicoes_clinicas_associadas": self.condicoes_clinicas_associadas,
            "doppler": self.doppler,                      
            "estilo_de_vida": self.estilo_de_vida,              
            "etnia": self.etnia,                       
            "pilificacao": self.pilificacao,                  
            "profundidade": self.profundidade,      
            "pulso": self.pulso,     
            "sexo": self.sexo,                       
            "tamanho_lesao": self.tamanho_lesao,                
            "tempertura": self.tempertura,                             
            "peso": self.peso,                    
            "altura": self.altura,                     
            "imc": self.imc,                          
            "cod_sus": self.cod_sus,                      
            "data_exame": self.data_exame,               
            "nome": self.nome,
            'tipo': tipo,
            'probabilidade': probabilidade,
            'probabilidade_risco': probabilidade_risco,
            'risco': risco
        }

# Create an item
@app.route('/pacientes', methods=['POST'])
def create_item():
    data = request.get_json()

    aspecto_pele = data["aspecto_pele"]                 
    aspecto_unha = data["aspecto_unha"]                
    bordas = data["bordas"]                      
    claudicacao = utils.convert_string_to_boolean(data["claudicacao"])                  
    condicoes_clinicas_associadas = data["condicoes_clinicas_associadas"]
    comorbidade = data["comorbidade"]                  
    doppler = data["doppler"]                     
    dor = utils.convert_string_to_float(data["dor"])                          
    dor_em_elevacao = utils.convert_string_to_boolean(data['dor_em_elevacao'])              
    edema = data["edema"]                        
    estilo_de_vida = data ["estilo_de_vida"]               
    etnia = data["etnia"]                       
    enchimento_capilar = data["enchimento_capilar"]           
    exsudato = data["exsudato"]                     
    exsudato_volume = utils.convert_string_to_float(data["exsudato_volume"])            
    idade = utils.convert_string_to_age(data["data_nascimento"])
    itb = utils.convert_string_to_float(data["itb"])                     
    localizacao = data["localizacao"].split(", ")              
    pilificacao = data["pilificacao"]                  
    profundidade = data ["profundidade"]                
    pulso = data["pulso"]                                
    sexo = data["sexo"]                        
    tamanho_lesao = utils.convert_string_to_float(data["tamanho_lesao"])               
    temperatura = data["temperatura"]
    peso = utils.convert_string_to_float(data["peso"])
    altura = utils.convert_string_to_float(data["altura"])
    imc = peso / altura ** 2
    cod_sus = data["cod_sus"]
    data_exame = datetime.now()
    nome = data["nome"].title()
    
    dor = Fuzzy.avalia_dor(dor)
    exsudato_volume = Fuzzy.avalia_exudato(exsudato_volume)

    avaliacao, riscos = decisao.avaliacao(aspecto_pele, aspecto_unha, bordas, claudicacao, comorbidade, dor,
                     dor_em_elevacao, edema, enchimento_capilar, exsudato, exsudato_volume, idade,
                     itb, condicoes_clinicas_associadas, doppler, estilo_de_vida, etnia, pilificacao,
                     profundidade, pulso, sexo, tamanho_lesao, temperatura, localizacao)                   

    new_paciente = Paciente(
        aspecto_pele = aspecto_pele,
        aspecto_unha = aspecto_unha,
        bordas = bordas,
        claudicacao = claudicacao,
        comorbidade = comorbidade,
        condicoes_clinicas_associadas = condicoes_clinicas_associadas,
        dor=dor,
        dor_em_elevacao = dor_em_elevacao,
        edema=edema,
        enchimento_capilar=enchimento_capilar,
        exsudato=exsudato,
        exsudato_volume=exsudato_volume,
        idade=idade,
        itb = itb,
        doppler = doppler,
        estilo_de_vida = estilo_de_vida,
        etnia = etnia,
        pilificacao = pilificacao,
        profundidade = profundidade,
        pulso=pulso,
        sexo=sexo,
        tamanho_lesao=tamanho_lesao,
        tempertura = temperatura,
        localizacao= localizacao,
        tipo=avaliacao["tipo"],
        venosa= round(avaliacao["venosa"], 3),
        arterial= round(avaliacao["arterial"], 3),
        risco_alto_arterial= round(riscos["risco_alto_arterial"], 3),    
        risco_alto_venoso=round(riscos["risco_alto_venoso"], 3),      
        risco_baixo_arterial=round(riscos["risco_baixo_arterial"], 3),   
        risco_baixo_venoso=round(riscos["risco_baixo_venoso"], 3),     
        risco_moderado_arterial=round(riscos["risco_moderado_arterial"], 3),
        risco_moderado_venoso=round(riscos["risco_moderado_venoso"], 3),
        altura = altura,
        peso = peso,
        imc = imc,
        cod_sus = cod_sus,
        data_exame = data_exame,
        nome = nome
    )
    db.session.add(new_paciente)
    db.session.commit()
    return jsonify(new_paciente.to_dict()), 201

@app.route('/pdf', methods=['POST'])
def send_pdf():
    data = request.get_json()
    return send_file(
                     io.BytesIO(create_pdf(data)),
                     mimetype='application/pdf',
                     as_attachment=False
               )

@app.route('/discovery', methods=['POST'])
def discovery_json():
    print(request.data)
    return request.get_json(), 200

# Read all items
@app.route('/pacientes', methods=['GET'])
def get_items():
    items = Paciente.query.all()
    return jsonify([item.to_dict() for item in items])

# Read a single item
@app.route('/pacientes/<string:item_id>', methods=['GET'])
def get_item(item_id):
    item = Paciente.query.where(Paciente.cod_sus == item_id).order_by(desc(Paciente.data_exame)).first_or_404()
    return jsonify(item.to_dict()), 200

# Delete an item
@app.route('/pacientes/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    item = Paciente.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    return '', 204

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")