

class Decisao:

    def avalia_tipo(bordas, temperatura, localizacao, claudicacao, pilificacao):
        
        avaliacao = {
            "arterial" : 0.0,
            "venosa" : 0.0,
            "tipo" : ""
        }

        if bordas == "regular":
            avaliacao["arterial"] += 0.6
        if bordas == "irregular":
            avaliacao["venosa"] += 0.7

        if claudicacao:
            avaliacao["arterial"] += 0.1
        if not claudicacao:
            avaliacao["venosa"] += 0.05

        if temperatura == "fria":
            avaliacao["arterial"] += 0.15
        if temperatura == "quente":
            avaliacao["venosa"] += 0.15
        
        if pilificacao == "sem pelo":
            avaliacao["arterial"] += 0.05
        if pilificacao == "escassa":
            avaliacao["arterial"] += 0.035 

        if "face anterior da perna" in localizacao:
            avaliacao["arterial"] += 0.02
            avaliacao["venosa"] += 0.08
        if "dorso do pe" in localizacao:
            avaliacao["arterial"] += 0.1
        if "face medial da perna" in localizacao:
            avaliacao["arterial"] += 0.02
            avaliacao["venosa"] += 0.08
        if "face lateral da perna" in localizacao:
            avaliacao["arterial"] += 0.02
            avaliacao["venosa"] += 0.08
        if "maleolos" in localizacao:
            avaliacao["arterial"] += 0.06
            avaliacao["venosa"] += 0.04
        if "regiao tendao calcaneo" in localizacao:
            avaliacao["venosa"] += 0.1

        if avaliacao["arterial"] > avaliacao["venosa"]:
            avaliacao["tipo"] = "arterial"
        else:
            avaliacao["tipo"] = "venosa"

        return avaliacao

    def avalia_risco(aspecto_pele, aspecto_unha, bordas, claudicacao, comorbidade, dor, dor_em_elevacao,
                     edema, enchimento_capilar, exsudato, exsudato_volume, idade, itb,                  
                     condicoes_clinicas_associadas, doppler, estilo_de_vida, etnia, pilificacao,
                     profundidade, pulso, sexo, tamanho_lesao):
        riscos = {
            "risco_alto_arterial" : 0.0,
            "risco_alto_venoso" : 0.0,
            "risco_moderado_arterial" : 0.0,
            "risco_moderado_venoso" : 0.0,
            "risco_baixo_arterial" : 0.0,
            "risco_baixo_venoso" : 0.0
        }

        if 1 in estilo_de_vida:
            riscos["risco_baixo_venoso"] += 0.075
        
        if 2 in estilo_de_vida or 3 in estilo_de_vida or 4 in estilo_de_vida:
            riscos["risco_baixo_arterial"] += 0.05
        
        if 2 in estilo_de_vida and 3 in estilo_de_vida and 4 in estilo_de_vida:
            riscos["risco_alto_arterial"] += 0.03

        if 5 in comorbidade or 7 in comorbidade or 8 in comorbidade or 10 in comorbidade:
            riscos["risco_moderado_venoso"] += 0.075
        
        if 8 in comorbidade or 9 in comorbidade or 10 in comorbidade or 12 in comorbidade:
            riscos["risco_moderado_arterial"] += 0.075

        if 6 in comorbidade:
            riscos["risco_alto_arterial"] += 0.03
        
        if 12 in comorbidade:
            riscos["risco_moderado_arterial"] += 0.075

        if 11 in comorbidade and 5 in comorbidade:
            riscos["risco_alto_venoso"] += 0.0375
        
        if 9 in comorbidade:
            riscos["risco_baixo_arterial"] += 0.05

        if 16 in etnia or 17 in etnia:
            riscos["risco_alto_venoso"] += 0.0375
            riscos["risco_alto_arterial"] += 0.03

        if 13 in etnia or 15 in etnia:
            riscos["risco_baixo_venoso"] += 0.075
            riscos["risco_baixo_arterial"] += 0.05

        if 14 in etnia:
            riscos["risco_moderado_venoso"] += 0.075    
            riscos["risco_alto_arterial"] += 0.03

        if claudicacao:
            riscos["risco_alto_arterial"] += 0.03
        
        if tamanho_lesao < 1:
            riscos["risco_baixo_arterial"] += 0.1167
            riscos["risco_baixo_venoso"] += 0.05

        if tamanho_lesao >= 1 and tamanho_lesao <= 3:
            riscos["risco_moderado_arterial"] += 0.0584
            riscos["risco_baixo_venoso"] += 0.05

        if tamanho_lesao > 3:
            riscos["risco_alto_arterial"] += 0.0584
            riscos["risco_moderado_venoso"] += 0.05

        if profundidade == "derme":
            riscos["risco_moderado_venoso"] += 0.05
            riscos["risco_alto_arterial"] += 0.0584
        
        if profundidade == "hipoderme":
            riscos["risco_alto_venoso"] += 0.07

        if tamanho_lesao < 1 and bordas == "regular" and profundidade == "epiderme":
            riscos["risco_baixo_arterial"] += 0.1166
        
        if tamanho_lesao < 1 and bordas == "irregular" and profundidade == "epiderme":
            riscos["risco_baixo_venoso"] += 0.05
        
        if tamanho_lesao < 1 and bordas == "regular" and profundidade == "derme":
            riscos["risco_alto_arterial"] += 0.0583

        if tamanho_lesao >= 1 and tamanho_lesao <= 3 and bordas == "regular" and profundidade == "derme":
            riscos["risco_alto_arterial"] += 0.0583
        
        if tamanho_lesao >= 1 and tamanho_lesao <= 3 and bordas == "irregular" and profundidade == "derme":
            riscos["risco_moderado_venoso"] += 0.0584
        
        if tamanho_lesao >= 1 and tamanho_lesao <= 3 and bordas == "regular" and profundidade == "hipoderme":
            riscos["risco_moderado_arterial"] += 0.0583

        if tamanho_lesao > 3 and bordas == "irregular" and profundidade == "hipoderme":
            riscos["risco_alto_venoso"] += 0.07

        if exsudato == 24 and (exsudato_volume == "minimo" or exsudato_volume == "pouco"):
            riscos["risco_baixo_venoso"] += 0.05

        if exsudato == 24 and exsudato_volume == "moderado":
            riscos["risco_moderado_venoso"] += 0.05
        
        if exsudato == 24 and exsudato_volume == "intenso":
            riscos["risco_alto_venoso"] += 0.07

        if (exsudato == 26 or exsudato == 27) and (exsudato_volume == "minimo" or exsudato_volume == "pouco"):
            riscos["risco_moderado_venoso"] += 0.5

        if exsudato == 26 and (exsudato_volume == "moderado" or exsudato_volume == "pouco"):
            riscos["risco_moderado_venoso"] += 0.05
            riscos["risco_moderado_arterial"] += 0.0583

        if exsudato == 25:
            riscos["risco_alto_venoso"] += 0.07
            riscos["risco_alto_arterial"] += 0.0583

        if edema == "Grau I":
            riscos["risco_baixo_venoso"] += 0.05
            riscos["risco_baixo_arterial"] += 0.125

        if edema == "Grau II":
            riscos["risco_moderado_venoso"] += 0.0834
            riscos["risco_moderado_arterial"] += 0.0357

        if edema == "Grau III" or edema == "Grau IV":
            riscos["risco_moderado_venoso"] += 0.125
            riscos["risco_moderado_arterial"] += 0.0357

        if aspecto_pele == "natural":
            riscos["risco_baixo_venoso"] += 0.05
        
        if aspecto_pele == "fina e brilhante":
            riscos["risco_baixo_venoso"] += 0.05
            riscos["risco_moderado_arterial"] += 0.0357

        if aspecto_pele == "cianotica":
            riscos["risco_alto_venoso"] += 0.125
            riscos["risco_alto_arterial"] += 0.0625

        if aspecto_pele == "seca":
            riscos["risco_moderado_venoso"] += 0.0834
            riscos["risco_moderado_arterial"] += 0.0357

        if pulso == "cheio":
            riscos["risco_baixo_arterial"] += 0.125

        if pulso == "fino":
            riscos["risco_baixo_venoso"] += 0.05
            riscos["risco_moderado_arterial"] += 0.0357

        if pulso == "ausente":
            riscos["risco_alto_arterial"] += 625
        
        if pilificacao == "sem pelos":
            riscos["risco_alto_arterial"] += 0.0625

        if pilificacao == "escassa":
            riscos["risco_moderado_arterial"] += 0.0357
        
        if aspecto_unha == "quebradica":
            riscos["risco_alto_arterial"] += 0.0625
            riscos["risco_baixo_venoso"] += 0.05
        
        if aspecto_unha == "espessada":
            riscos["risco_moderado_arterial"] += 0.0357
            riscos["risco_moderado_venoso"] += 0.0834

        if 28 in condicoes_clinicas_associadas or 29 in condicoes_clinicas_associadas or 32 in condicoes_clinicas_associadas or 34 in condicoes_clinicas_associadas:
            riscos["risco_alto_venoso"] += 0.025
        
        if 30 in condicoes_clinicas_associadas or 31 in condicoes_clinicas_associadas:
            riscos["risco_alto_arterial"] += 0.0334
            riscos["risco_alto_venoso"] += 0.025
        
        if 35 in condicoes_clinicas_associadas:
            riscos["risco_alto_arterial"] += 0.0334
            riscos["risco_alto_venoso"] += 0.025
        
        if 34 in condicoes_clinicas_associadas:
            riscos["risco_alto_arterial"] += 0.0334
            riscos["risco_alto_venoso"] += 0.025

        if 33 in condicoes_clinicas_associadas:
            riscos["risco_moderado_arterial"] += 0.1
            riscos["risco_moderado_venoso"] += 0.1

        if enchimento_capilar == "alterado":
            riscos["risco_alto_arterial"] += 0.0334

        if 36 in doppler and (38 in doppler or 39 in doppler):
            riscos["risco_alto_venoso"] += 0.1

        if 40 in doppler or 41 in doppler:
            riscos["risco_alto_arterial"] += 0.0333

        if 36 in doppler:
            riscos["risco_moderado_venoso"] += 0.1
        
        if itb > 1.3 or (itb < 0.9 and itb > 0.5):
            riscos["risco_moderado_arterial"] += 0.1
        
        if itb < 0.5:
            riscos["risco_alto_arterial"] += 0.0333
        
        if itb < 1 and itb > 0.9:
            riscos["risco_baixo_arterial"] += 0.1

        if dor == "leve":
            riscos["risco_baixo_venoso"] += 0.05

        if dor == "leve/moderada":
            riscos["risco_moderado_venoso"] += 0.05
            riscos["risco_baixo_arterial"] += 0.1166
        
        if dor == "moderada":
            riscos["risco_moderado_arterial"] += 0.0583
        
        if dor == "moderada/intensa":
            riscos["risco_alto_venoso"] += 0.07
        
        if dor == "intensa":
            riscos["risco_alto_arterial"] += 0.0583
        
        if dor_em_elevacao == "aumento":
            riscos["risco_moderado_arterial"] += 0.0583

        if dor_em_elevacao == "alivio":
            riscos["risco_baixo_venoso"] += 0.05

        if idade >= 30 and idade <= 39:
            riscos["risco_baixo_arterial"] += 0.025
            riscos["risco_baixo_venoso"] += 0.025
        
        if idade >= 40 and idade <= 49:
            riscos["risco_moderado_arterial"] += 0.025
            riscos["risco_moderado_venoso"] += 0.05

        if idade >= 50:
            riscos["risco_alto_arterial"] += 0.05
            riscos["risco_alto_venoso"] += 0.025
        
        if sexo == "Masculino":
            riscos["risco_baixo_venoso"] += 0.025
            riscos["risco_moderado_arterial"] += 0.025

        if sexo == "Feminino":
            riscos["risco_baixo_arterial"] += 0.025
            riscos["risco_alto_venoso"] += 0.025

        return riscos