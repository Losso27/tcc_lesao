from .extensions import db
from sqlalchemy.dialects.postgresql import ARRAY, TIMESTAMP


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
    largura_lesao                   = db.Column(db.Float)
    comprimento_lesao               = db.Column(db.Float)                
    temperatura                     = db.Column(db.String(255))                   
    tipo                            = db.Column(db.String(255))
    venosa                          = db.Column(db.Float)
    arterial                        = db.Column(db.Float)
    peso                            = db.Column(db.Float)
    altura                          = db.Column(db.Float)
    imc                             = db.Column(db.Float)
    cod_sus                         = db.Column(db.String(255))
    data_exame                      = db.Column(TIMESTAMP)
    nome                            = db.Column(db.String(255))
    tipo_tecido                     = db.Column(db.String(255))
    tratamento_remocao              = db.Column(db.Text)
    tratamento_terapia_topica       = db.Column(db.Text)
    tratamento_cobertura            = db.Column(db.Text)
    tratamento_adjuvante            = db.Column(db.Text)
    dor_num                         = db.Column(db.Float)
    exsudato_volume_num             = db.Column(db.Float)


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
            "comprimento_lesao": self.comprimento_lesao,
            "largura_lesao": self.largura_lesao,                
            "temperatura": self.temperatura,                             
            "peso": self.peso,                    
            "altura": self.altura,                     
            "imc": self.imc,                          
            "cod_sus": self.cod_sus,                      
            "data_exame": self.data_exame,               
            "nome": self.nome,
            'tipo': tipo,
            'probabilidade': probabilidade,
            'probabilidade_risco': probabilidade_risco,
            'risco': risco,
            "tipo_tecido": self.tipo_tecido,                            
            "tratamento_remocao": self.tratamento_remocao,              
            "tratamento_terapia_topica": self.tratamento_terapia_topica,
            "tratamento_cobertura": self.tratamento_cobertura,          
            "tratamento_adjuvante": self.tratamento_adjuvante,
            "dor_num" : self.dor_num,
            "exsudato_volume_num": self.exsudato_volume_num    
        }