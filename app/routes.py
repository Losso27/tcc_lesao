from flask import Blueprint, request, jsonify, send_file, current_app
from .models import Paciente
from .decisao import avaliacao, avaliacao_tratamento
from sqlalchemy import desc
from .pdf import create_pdf
import io
from .fuzzy import Fuzzy
from .utils import convert_string_to_age, convert_string_to_boolean, convert_string_to_float
from datetime import datetime
from .extensions import db
from functools import wraps

pacientes = Blueprint("pacientes", __name__)

def require_token(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if request.headers.get("Authorization", "") != current_app.config["SECRET_KEY"]:
            return jsonify({"error": "Unauthorized"}), 403
        return f(*args, **kwargs)
    return decorated

# Create an item
@pacientes.route('/', methods=['POST'])
def create_item():
    data = request.get_json()

    aspecto_pele = data["aspecto_pele"]                 
    aspecto_unha = data["aspecto_unha"]                
    bordas = data["bordas"]                      
    claudicacao = convert_string_to_boolean(data["claudicacao"])                  
    condicoes_clinicas_associadas = data["condicoes_clinicas_associadas"]
    comorbidade = data["comorbidade"]                  
    doppler = data["doppler"]                     
    dor_num = convert_string_to_float(data["dor"])                          
    dor_em_elevacao = convert_string_to_boolean(data['dor_em_elevacao'])              
    edema = data["edema"]                        
    estilo_de_vida = data ["estilo_de_vida"]               
    etnia = data["etnia"]                       
    enchimento_capilar = data["enchimento_capilar"]           
    exsudato = data["exsudato"]                     
    exsudato_volume_num = convert_string_to_float(data["exsudato_volume"])            
    idade = convert_string_to_age(data["data_nascimento"])            
    localizacao = data["localizacao"].split(", ")              
    pilificacao = data["pilificacao"]                  
    profundidade = data ["profundidade"]                
    pulso = data["pulso"]                                
    sexo = data["sexo"]
    largura_lesao = convert_string_to_float(data["largura_lesao"])
    comprimento_lesao = convert_string_to_float(data["comprimento_lesao"])
    temperatura = data["temperatura"]
    peso = convert_string_to_float(data["peso"])
    altura = convert_string_to_float(data["altura"])
    imc = peso / altura ** 2
    cod_sus = data["cod_sus"]
    data_exame = datetime.now()
    nome = data["nome"].title()
    tipo_tecido = data["tipo_tecido"]
    itb = convert_string_to_float(data["itb"])

    dor = Fuzzy.avalia_dor(dor_num)
    exsudato_volume = Fuzzy.avalia_exudato(exsudato_volume_num)

    resultado_avaliacao, riscos = avaliacao(aspecto_pele, aspecto_unha, bordas, claudicacao, comorbidade, dor,
                     dor_em_elevacao, edema, enchimento_capilar, exsudato, exsudato_volume, idade,
                     itb, condicoes_clinicas_associadas, doppler, estilo_de_vida, etnia, pilificacao,
                     profundidade, pulso, sexo, largura_lesao * comprimento_lesao, temperatura, localizacao)

    tratamento = avaliacao_tratamento(tipo_tecido, exsudato_volume, itb, resultado_avaliacao["tipo"])           

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
        comprimento_lesao=comprimento_lesao,
        largura_lesao = largura_lesao,
        temperatura = temperatura,
        localizacao= localizacao,
        tipo=resultado_avaliacao["tipo"],
        venosa= round(resultado_avaliacao["venosa"], 3),
        arterial= round(resultado_avaliacao["arterial"], 3),
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
        nome = nome,
        tipo_tecido = tipo_tecido,              
        tratamento_remocao = tratamento["tratamento_remocao"],  
        tratamento_terapia_topica = tratamento["tratamento_terapia_topica"],
        tratamento_cobertura = tratamento["tratamento_cobertura"],
        tratamento_adjuvante = tratamento["tratamento_adjuvante"],
        dor_num = dor_num,
        exsudato_volume_num = exsudato_volume_num
    )
    db.session.add(new_paciente)
    db.session.commit()
    return jsonify(new_paciente.to_dict()), 201

# Read a single item
@pacientes.route('/pdf/<string:item_id>', methods=['GET'])
@require_token
def get_pdf(item_id):
    item = Paciente.query.where(Paciente.cod_sus == item_id).order_by(desc(Paciente.data_exame)).all()
    return send_file(
                 io.BytesIO(create_pdf(item)),
                 mimetype='application/pdf',
                 as_attachment=False
           )

@pacientes.route('/<string:item_id>', methods=['GET'])
@require_token
def get_item(item_id):
    item = Paciente.query.where(Paciente.cod_sus == item_id).order_by(desc(Paciente.data_exame)).first_or_404()
    return jsonify(item.to_dict()), 200


@pacientes.route('/discovery', methods=['POST'])
def discovery_json():
    print(request.data)
    return request.get_json(), 200