from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import ARRAY
from decisao import Decisao
from fuzzy import Fuzzy
import os

app = Flask(__name__)
list = []

# Define a model
class Paciente:

    def __init__(self,
    aspecto_pele, aspecto_unha, bordas, claudicacao, comorbidade, dor, dor_em_elevacao, edema,
    enchimento_capilar, exsudato, exsudato_volume, idade, itb, localizacao, condicoes_clinicas_associadas,
    doppler, estilo_de_vida, etnia, pilificacao, profundidade, pulso, risco_alto_arterial,
    risco_alto_venoso, risco_baixo_arterial, risco_baixo_venoso, risco_moderado_arterial,
    risco_moderado_venoso, sexo, tamanho_lesao, tempertura, tipo, venosa, arterial):
        id_count = len(list) + 1

        self.id                              = id_count                          
        self.aspecto_pele                    = aspecto_pele                 
        self.aspecto_unha                    = aspecto_unha                 
        self.bordas                          = bordas                       
        self.claudicacao                     = claudicacao                               
        self.comorbidade                     = comorbidade                          
        self.dor                             = dor                          
        self.dor_em_elevacao                 = dor_em_elevacao              
        self.edema                           = edema                                      
        self.enchimento_capilar              = enchimento_capilar           
        self.exsudato                        = exsudato                     
        self.exsudato_volume                 = exsudato_volume              
        self.idade                           = idade                                      
        self.itb                             = itb                          
        self.localizacao                     = localizacao                                    
        self.condicoes_clinicas_associadas   = condicoes_clinicas_associadas
        self.doppler                         = doppler                                         
        self.estilo_de_vida                  = estilo_de_vida               
        self.etnia                           = etnia                                              
        self.pilificacao                     = pilificacao                                    
        self.profundidade                    = profundidade                                  
        self.pulso                           = pulso                        
        self.risco_alto_arterial             = risco_alto_arterial           
        self.risco_alto_venoso               = risco_alto_venoso                  
        self.risco_baixo_arterial            = risco_baixo_arterial           
        self.risco_baixo_venoso              = risco_baixo_venoso               
        self.risco_moderado_arterial         = risco_moderado_arterial      
        self.risco_moderado_venoso           = risco_moderado_venoso          
        self.sexo                            = sexo                                                  
        self.tamanho_lesao                   = tamanho_lesao                          
        self.tempertura                      = tempertura                                      
        self.tipo                            = tipo                         
        self.venosa                          = venosa                       
        self.arterial                        = arterial                                        

    def __repr__(self):
        return f"<Paciente {self.id}>"

    def to_dict(self):
        return {
            'id': self.id,
            'venosa' : self.venosa,
            'arterial' : self.arterial,
            'tipo': self.tipo,
            'risco_alto_arterial': self.risco_alto_arterial,
            'risco_alto_venoso':self.risco_alto_venoso,
            'risco_moderado_arterial':self.risco_moderado_arterial,
            'risco_moderado_venoso':self.risco_moderado_venoso,
            'risco_baixo_arterial':self.risco_baixo_arterial,
            'risco_baixo_venoso':self.risco_baixo_venoso
        }

# Create an item
@app.route('/pacientes', methods=['POST'])
def create_item():
    data = request.get_json()

    aspecto_pele = data["aspecto_pele"]                 
    aspecto_unha = data["aspecto_unha"]                
    bordas = data["bordas"]                      
    claudicacao = data["claudicacao"]                  
    comorbidade = data["comorbidade"]                  
    dor = data["dor"]                          
    dor_em_elevacao = data['dor_em_elevacao']              
    edema = data["edema"]                        
    enchimento_capilar = data["enchimento_capilar"]           
    exsudato = data["exsudato"]                     
    exsudato_volume = data["exsudato_volume"]             
    idade = data["idade"]
    itb = data["itb"]                          
    localizacao = data["localizacao"]              
    condicoes_clinicas_associadas = data["condicoes_clinicas_associadas"]
    doppler = data["doppler"]                     
    estilo_de_vida = data ["estilo_de_vida"]               
    etnia = data["etnia"]                       
    pilificacao = data["pilificacao"]                  
    profundidade = data ["profundidade"]                
    pulso = data["pulso"]                                
    sexo = data["sexo"]                        
    tamanho_lesao = data ["tamanho_lesao"]                
    tempertura = data["temperatura"]                  
    
    dor = Fuzzy.avalia_dor(dor)
    exsudato_volume = Fuzzy.avalia_exudato(exsudato_volume)

    avaliacao = Decisao.avalia_tipo(bordas,tempertura, localizacao, claudicacao, pilificacao)

    riscos = Decisao.avalia_risco(aspecto_pele, aspecto_unha, bordas, claudicacao, comorbidade, dor,
                                  dor_em_elevacao, edema, enchimento_capilar, exsudato, exsudato_volume, idade,
                                  itb, condicoes_clinicas_associadas, doppler, estilo_de_vida, etnia, pilificacao,
                                  profundidade, pulso, sexo, tamanho_lesao)                       

    new_paciente = Paciente(
        aspecto_pele = aspecto_pele,
        aspecto_unha = aspecto_unha,
        bordas = bordas,
        claudicacao = claudicacao,
        comorbidade = comorbidade,
        dor=dor,
        dor_em_elevacao = dor_em_elevacao,
        edema=edema,
        enchimento_capilar=enchimento_capilar,
        exsudato=exsudato,
        exsudato_volume=exsudato_volume,
        idade=idade,
        itb = itb,
        condicoes_clinicas_associadas = condicoes_clinicas_associadas,
        doppler = doppler,
        estilo_de_vida = estilo_de_vida,
        etnia = etnia,
        pilificacao = pilificacao,
        profundidade = profundidade,
        pulso=pulso,
        sexo=sexo,
        tamanho_lesao=tamanho_lesao,
        tempertura = tempertura,
        localizacao= localizacao,
        tipo=avaliacao["tipo"],
        venosa= round(avaliacao["venosa"], 3),
        arterial= round(avaliacao["arterial"], 3),
        risco_alto_arterial= round(riscos["risco_alto_arterial"], 3),    
        risco_alto_venoso=round(riscos["risco_alto_venoso"], 3),      
        risco_baixo_arterial=round(riscos["risco_baixo_arterial"], 3),   
        risco_baixo_venoso=round(riscos["risco_baixo_venoso"], 3),     
        risco_moderado_arterial=round(riscos["risco_moderado_arterial"], 3),
        risco_moderado_venoso=round(riscos["risco_moderado_venoso"], 3) 
    )
    list.append(new_paciente)
    return jsonify(new_paciente.to_dict()), 201

# Read all items
@app.route('/pacientes', methods=['GET'])
def get_items():
    return jsonify([item.to_dict() for item in list])

# Read a single item
@app.route('/pacientes/<int:item_id>', methods=['GET'])
def get_item(item_id):
    itens_found = [p for p in list if p.id == item_id] 
    if len(itens_found) == 0:
        return "paciente inexistente", 404
    item = itens_found.pop(0)
    return jsonify(item.to_dict())

# Delete an item
@app.route('/pacientes/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    for p in list:
        if p.id == item_id:
            list.remove(p)
    return 'Paciente removido', 200

if __name__ == '__main__':
    app.run(debug=True)