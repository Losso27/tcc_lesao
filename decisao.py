from random import choice
from experta import *

class DataInput(Fact):
    pass

class Decisao(KnowledgeEngine):

    def __init__(self):

        self.riscos = {
            "risco_alto_arterial" : 0.0,
            "risco_alto_venoso" : 0.0,
            "risco_moderado_arterial" : 0.0,
            "risco_moderado_venoso" : 0.0,
            "risco_baixo_arterial" : 0.0,
            "risco_baixo_venoso" : 0.0
        }

        self.avaliacao = {
            "arterial" : 0.0,
            "venosa" : 0.0,
            "tipo" : ""
        }
        super().__init__()

    @Rule(DataInput(bordas='regular'))
    def se_bordas_regulares(self):
        self.avaliacao["arterial"] += 0.6

    @Rule(DataInput(bordas='irregular'))
    def se_bordas_irregulares(self):
        self.avaliacao["venosa"] += 0.7

    @Rule(DataInput(claudicacao=True))
    def se_claudicacao(self):
        self.avaliacao["arterial"] += 0.1
        self.riscos["risco_alto_arterial"] += 0.03

    @Rule(DataInput(claudicacao=False))
    def se_nao_claudicacao(self):
        self.avaliacao["venosa"] += 0.05

    @Rule(DataInput(temperatura="fria"))
    def se_fria(self):
        self.avaliacao["arterial"] += 0.15

    @Rule(DataInput(temperatura="quente"))
    def se_quente(self):
        self.avaliacao["venosa"] += 0.15
    
    @Rule(DataInput(pilificacao ="sem pelo"))
    def se_pilificacao_sem_pelo(self):
        self.avaliacao["arterial"] += 0.05

    @Rule(DataInput(pilificacao = "escassa"))
    def se_pilificacao_escassa(self):
        self.avaliacao["arterial"] += 0.035 

    @Rule(DataInput(localizacao = CONTAINS("face anterior da perna")))
    def se_localizacao_face_anterior_da_perna(self):
        self.avaliacao["arterial"] += 0.02
        self.avaliacao["venosa"] += 0.08

    @Rule(DataInput(localizacao = CONTAINS("dorso do pe")))
    def se_localizacao_dorso_do_pe(self):
        self.avaliacao["arterial"] += 0.1

    @Rule(DataInput(localizacao = CONTAINS("face lateral da perna")))
    def se_localizacao_face_lateral_da_perna(self):
        self.avaliacao["arterial"] += 0.02
        self.avaliacao["venosa"] += 0.08
    
    @Rule(DataInput(localizacao = CONTAINS("maleolos")))
    def se_localizacao_maleolos(self):
            self.avaliacao["arterial"] += 0.06
            self.avaliacao["venosa"] += 0.04
    
    @Rule(DataInput(localizacao = CONTAINS("regiao tendao calcaneo")))
    def se_localizacao_regiao_tendao_calcaneo(self):
            self.avaliacao["venosa"] += 0.1

    @Rule(DataInput(estilo_de_vida = CONTAINS(1)))
    def se_estilo_de_vida_1(self):
            self.riscos["risco_baixo_venoso"] += 0.075

    @Rule(DataInput(estilo_de_vida = CONTAINS(2) | CONTAINS(3) | CONTAINS(4)))
    def se_estilo_de_vida_2_ou_3_ou_4(self):
            self.riscos["risco_baixo_arterial"] += 0.05
    
    @Rule(DataInput(estilo_de_vida = CONTAINS(2) & CONTAINS(3) & CONTAINS(4)))
    def se_estilo_de_vida_2_e_3_e_4(self):
            self.riscos["risco_alto_arterial"] += 0.03

    @Rule(DataInput(comorbidade = CONTAINS(5) | CONTAINS(7) | CONTAINS(8) | CONTAINS(10)))
    def se_comorbidade_5_ou_7_ou_8_ou_10 (self):
        self.riscos["risco_moderado_venoso"] += 0.075
    
    @Rule(DataInput(comorbidade = CONTAINS(8) | CONTAINS(9) | CONTAINS(10) | CONTAINS(12)))
    def se_comorbidade_8_ou_9_ou_10_ou_12 (self):
        self.riscos["risco_moderado_arterial"] += 0.075

    @Rule(DataInput(comorbidade = CONTAINS(6)))
    def se_comorbidade_6 (self):
        self.riscos["risco_alto_arterial"] += 0.03
        
    @Rule(DataInput(comorbidade = CONTAINS(12)))
    def se_comorbidade_12 (self):
        self.riscos["risco_moderado_arterial"] += 0.075

    @Rule(DataInput(comorbidade = CONTAINS(11) & CONTAINS(5)))
    def se_comorbidade_11_e_5 (self):
            self.riscos["risco_alto_venoso"] += 0.0375
        
    @Rule(DataInput(comorbidade = CONTAINS(9)))
    def se_comorbidade_9 (self):
        self.riscos["risco_baixo_arterial"] += 0.05

    @Rule(DataInput(comorbidade = CONTAINS(16) | CONTAINS(17)))
    def se_etnia_16_ou_17 (self):
        self.riscos["risco_alto_venoso"] += 0.0375
        self.riscos["risco_alto_arterial"] += 0.03
    
    @Rule(DataInput(comorbidade = CONTAINS(13) | CONTAINS(15)))
    def se_etnia_13_ou_15 (self):
        self.riscos["risco_baixo_venoso"] += 0.075
        self.riscos["risco_baixo_arterial"] += 0.05

    @Rule(DataInput(comorbidade = CONTAINS(14)))
    def se_etnia_14 (self):
        self.riscos["risco_moderado_venoso"] += 0.075    
        self.riscos["risco_alto_arterial"] += 0.03

    @Rule(DataInput(tamanho_lesao = LT(1)))
    def se_tamanho_menor_1 (self):
        self.riscos["risco_baixo_arterial"] += 0.1167
        self.riscos["risco_baixo_venoso"] += 0.05

    @Rule(DataInput(tamanho_lesao = GT(1) & LT(3)))
    def se_tamanho_entre_1_e_3 (self):
        self.riscos["risco_moderado_arterial"] += 0.0584
        self.riscos["risco_baixo_venoso"] += 0.05

    @Rule(DataInput(tamanho_lesao = GT(3)))
    def se_tamanho_maior_3 (self):
        self.riscos["risco_moderado_arterial"] += 0.0584
        self.riscos["risco_baixo_venoso"] += 0.05

    @Rule(DataInput(profundidade = "derme"))
    def se_profundidade_derme (self):
        self.riscos["risco_moderado_venoso"] += 0.05
        self.riscos["risco_alto_arterial"] += 0.0584
        
    @Rule(DataInput(profundidade = "hipoderme"))
    def se_profundidade_hipoderme (self):
        self.riscos["risco_alto_venoso"] += 0.07

    @Rule(DataInput(tamanho_lesao = LT(1), bordas = "regular", profundidade = "epiderme"))
    def se_comb_1 (self):
        self.riscos["risco_baixo_arterial"] += 0.1166

    @Rule(DataInput(tamanho_lesao = LT(1), bordas = "irregular", profundidade = "epiderme"))
    def se_comb_2 (self):
        self.riscos["risco_baixo_venoso"] += 0.05
    
    @Rule(DataInput(tamanho_lesao = LT(1), bordas = "regular", profundidade = "derme"))
    def se_comb_3 (self):
        self.riscos["risco_alto_arterial"] += 0.0583

    @Rule(DataInput(tamanho_lesao = GT(1) & LT(3), bordas = "regular", profundidade = "derme"))
    def se_comb_4 (self):
        self.riscos["risco_alto_arterial"] += 0.0583

    @Rule(DataInput(tamanho_lesao = GT(1) & LT(3), bordas = "irregular", profundidade = "derme"))
    def se_comb_5 (self):
        self.riscos["risco_moderado_venoso"] += 0.0584
    
    @Rule(DataInput(tamanho_lesao = GT(1) & LT(3), bordas = "regular", profundidade = "hipoderme"))
    def se_comb_6 (self):
        self.riscos["risco_moderado_arterial"] += 0.0583

    @Rule(DataInput(tamanho_lesao = GT(3), bordas = "irregular", profundidade = "hipoderme"))
    def se_comb_7 (self):
         self.riscos["risco_alto_venoso"] += 0.07

    @Rule(DataInput(exsudato = 24, exsudato_volume = L("minimo") | L("pouco")))
    def se_exsudato_24_e_volume_minimo_ou_pouco (self):
        self.riscos["risco_baixo_venoso"] += 0.05

    @Rule(DataInput(exsudato = 24, exsudato_volume = "moderado"))
    def se_exsudato_24_e_volume_moderado (self):
            self.riscos["risco_moderado_venoso"] += 0.05
        
    @Rule(DataInput(exsudato = 24, exsudato_volume = "intenso"))
    def se_exsudato_24_e_volume_intenso (self):
        self.riscos["risco_alto_venoso"] += 0.07

    @Rule(DataInput(exsudato = 26 | 27, exsudato_volume = L("minimo") | L("pouco")))
    def se_exsudato_26_ou_27_e_volume_minimo_ou_pouco (self):
        self.riscos["risco_moderado_venoso"] += 0.5

    @Rule(DataInput(exsudato = 26, exsudato_volume = L("pouco") | L("moderado")))
    def se_exsudato_26_e_volume_pouco_ou_moderado (self): 
        self.riscos["risco_moderado_venoso"] += 0.05
        self.riscos["risco_moderado_arterial"] += 0.0583

    @Rule(DataInput(exsudato = 25))
    def se_exsudato_25 (self): 
        self.riscos["risco_alto_venoso"] += 0.07
        self.riscos["risco_alto_arterial"] += 0.0583

    @Rule(DataInput(edema = "Grau I"))
    def se_edema_grau_I (self):
        self.riscos["risco_baixo_venoso"] += 0.05
        self.riscos["risco_baixo_arterial"] += 0.125 

    @Rule(DataInput(edema = "Grau II"))
    def se_edema_grau_II (self):
        self.riscos["risco_moderado_venoso"] += 0.0834
        self.riscos["risco_moderado_arterial"] += 0.0357

    @Rule(DataInput(edema = L("Grau III") | L("Grau IV")))
    def se_edema_grau_III_ou_IV (self):
        self.riscos["risco_moderado_venoso"] += 0.125
        self.riscos["risco_moderado_arterial"] += 0.0357

    @Rule(DataInput(aspecto_pele = "natural"))
    def se_aspecto_pele_natural(self):
        self.riscos["risco_baixo_venoso"] += 0.05

    @Rule(DataInput(aspecto_pele = "fina e brilhante"))
    def se_aspecto_pele_fina_e_brilhante(self):    
        self.riscos["risco_baixo_venoso"] += 0.05
        self.riscos["risco_moderado_arterial"] += 0.0357

    @Rule(DataInput(aspecto_pele = "cianotica"))
    def se_aspecto_pele_cianotica(self):
        self.riscos["risco_alto_venoso"] += 0.125
        self.riscos["risco_alto_arterial"] += 0.0625

    @Rule(DataInput(aspecto_pele = "seca"))
    def se_aspecto_pele_seca(self):
        self.riscos["risco_moderado_venoso"] += 0.0834
        self.riscos["risco_moderado_arterial"] += 0.0357

    @Rule(DataInput(pulso = "cheio"))
    def se_pulso_cheio(self):
        self.riscos["risco_baixo_arterial"] += 0.125

    @Rule(DataInput(pulso = "fino"))
    def se_pulso_fino(self):
        self.riscos["risco_baixo_venoso"] += 0.05
        self.riscos["risco_moderado_arterial"] += 0.0357
    
    @Rule(DataInput(pulso = "ausente"))
    def se_pulso_ausente(self):
        self.riscos["risco_alto_arterial"] += 0.0625

    @Rule(DataInput(pilificacao = "sem pelos"))
    def se_pilificacao_sem_pelos(self):
        self.riscos["risco_alto_arterial"] += 0.0625

    @Rule(DataInput(pilificacao = "escassa"))
    def se_pilificacao_escassa(self):
        self.riscos["risco_moderado_arterial"] += 0.0357
    
    @Rule(DataInput(aspecto_unha = "quebradica"))
    def se_aspecto_unha_quebradica(self):
        self.riscos["risco_alto_arterial"] += 0.0625
        self.riscos["risco_baixo_venoso"] += 0.05
    
    @Rule(DataInput(aspecto_unha = "espessada"))
    def se_aspecto_unha_espessada(self):
        self.riscos["risco_moderado_arterial"] += 0.0357
        self.riscos["risco_moderado_venoso"] += 0.0834

    @Rule(DataInput(condicoes_clinicas_associadas = CONTAINS(28) | CONTAINS(29) | CONTAINS(32) | CONTAINS(34)))
    def se_condicoes_clinicas_associadas_28_ou_29_ou_32_ou_34(self):    
        self.riscos["risco_alto_venoso"] += 0.025

    @Rule(DataInput(condicoes_clinicas_associadas = CONTAINS(30) | CONTAINS(31)))
    def se_condicoes_clinicas_associadas_30_ou_31(self):    
        self.riscos["risco_alto_arterial"] += 0.0334
        self.riscos["risco_alto_venoso"] += 0.025
    
    @Rule(DataInput(condicoes_clinicas_associadas = CONTAINS(35)))
    def se_condicoes_clinicas_associadas_35(self):
        self.riscos["risco_alto_arterial"] += 0.0334
        self.riscos["risco_alto_venoso"] += 0.025

    @Rule(DataInput(condicoes_clinicas_associadas = CONTAINS(34)))
    def se_condicoes_clinicas_associadas_34(self):    
        self.riscos["risco_alto_arterial"] += 0.0334
        self.riscos["risco_alto_venoso"] += 0.025

    @Rule(DataInput(condicoes_clinicas_associadas = CONTAINS(33)))
    def se_condicoes_clinicas_associadas_33(self):  
        self.riscos["risco_moderado_arterial"] += 0.1
        self.riscos["risco_moderado_venoso"] += 0.1

    @Rule(DataInput(enchimento_capilar = "alterado"))
    def se_enchimento_capilar_alterado(self):
        self.riscos["risco_alto_arterial"] += 0.0334

    @Rule(DataInput(doppler = 36 & (38 | 39)))
    def se_doppler_36_e_38_ou_39(self):
        self.riscos["risco_alto_venoso"] += 0.1

    @Rule(DataInput(doppler = 40 | 41))
    def se_doppler_40_ou_41(self):
        self.riscos["risco_alto_arterial"] += 0.0333
    
    @Rule(DataInput(doppler = 36))
    def se_doppler_36(self):
        self.riscos["risco_moderado_venoso"] += 0.1

    @Rule(DataInput(itb= GT(1.3) | BETWEEN(0.5, 0.9)))
    def se_itb_maior_1_3_ou_entre_0_5_e_0_9(self):
        self.riscos["risco_moderado_arterial"] += 0.1
    
    @Rule(DataInput(itb= LT(0.5)))
    def se_itb_menor_0_5(self):
        self.riscos["risco_alto_arterial"] += 0.0333
    
    @Rule(DataInput(itb= BETWEEN(0.9, 1)))
    def se_itb_entre_0_9_e_1(self):
        self.riscos["risco_baixo_arterial"] += 0.1

    @Rule(DataInput(dor = "leve"))
    def se_dor_leve(self):
        self.riscos["risco_baixo_venoso"] += 0.05

    @Rule(DataInput(dor = "leve/moderada"))
    def se_dor_leve_moderada(self):
        self.riscos["risco_moderado_venoso"] += 0.05
        self.riscos["risco_baixo_arterial"] += 0.1166
    
    @Rule(DataInput(dor = "moderada"))
    def se_dor_moderada(self):
        self.riscos["risco_moderado_arterial"] += 0.0583
    
    @Rule(DataInput(dor = "moderada/intensa"))
    def se_dor_moderada_intensa(self):
        self.riscos["risco_alto_venoso"] += 0.07

    @Rule(DataInput(dor = "intensa"))
    def se_dor_intensa(self):
        self.riscos["risco_alto_arterial"] += 0.0583

    @Rule(DataInput(dor_em_elevacao = "aumento"))
    def se_dor_em_elevacao_aumento(self):
        self.riscos["risco_moderado_arterial"] += 0.0583

    @Rule(DataInput(dor_em_elevacao = "alivio"))
    def se_dor_em_elevacao_alivio(self):
        self.riscos["risco_baixo_venoso"] += 0.05

    @Rule(DataInput(idade=BETWEEN(30,39)))
    def se_idade_entre_30_e_39(self):
        self.riscos["risco_baixo_arterial"] += 0.025
        self.riscos["risco_baixo_venoso"] += 0.025
    
    @Rule(DataInput(idade=BETWEEN(40,49)))
    def se_idade_entre_40_e_49(self):
        self.riscos["risco_moderado_arterial"] += 0.025
        self.riscos["risco_moderado_venoso"] += 0.05
    
    @Rule(DataInput(idade=GE(50)))
    def se_idade_maior_ou_igual_a_50(self):
        self.riscos["risco_alto_arterial"] += 0.05
        self.riscos["risco_alto_venoso"] += 0.025
    
    @Rule(DataInput(sexo="Masculino"))
    def se_sexo_masculino(self):
        self.riscos["risco_baixo_venoso"] += 0.025
        self.riscos["risco_moderado_arterial"] += 0.025

    @Rule(DataInput(sexo="Feminino"))
    def se_sexo_feminino(self): 
        self.riscos["risco_baixo_arterial"] += 0.025
        self.riscos["risco_moderado_venoso"] += 0.015
        self.riscos["risco_alto_venoso"] += 0.01
    
def avaliacao(aspecto_pele, aspecto_unha, bordas, claudicacao, comorbidade, dor, dor_em_elevacao,
                     edema, enchimento_capilar, exsudato, exsudato_volume, idade, itb,                  
                     condicoes_clinicas_associadas, doppler, estilo_de_vida, etnia, pilificacao,
                     profundidade, pulso, sexo, tamanho_lesao, temperatura, localizacao):
    engine = Decisao()
    engine.reset()
    engine.declare(DataInput(aspecto_pele=aspecto_pele, aspecto_unha=aspecto_unha, bordas=bordas, claudicacao=claudicacao, 
                             comorbidade=comorbidade, dor=dor, dor_em_elevacao=dor_em_elevacao, edema = edema,
                             enchimento_capilar = enchimento_capilar, exsudato = exsudato, exsudato_volume = exsudato_volume, 
                             idade = idade, itb = itb, condicoes_clinicas_associadas = condicoes_clinicas_associadas, doppler = doppler,
                             estilo_de_vida = estilo_de_vida, etnia = etnia, pilificacao = pilificacao,
                             profundidade = profundidade, pulso = pulso, sexo = sexo, tamanho_lesao = tamanho_lesao,
                             temperatura = temperatura, localizacao = localizacao))
    engine.run()
    return get_avaliacao_tipo(engine.avaliacao), engine.riscos

def get_avaliacao_tipo(avaliacao):
    if avaliacao["arterial"] > avaliacao["venosa"]:
            avaliacao["tipo"] = "arterial"
    else:
        avaliacao["tipo"] = "venosa"

    return avaliacao
