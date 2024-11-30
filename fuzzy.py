import numpy as np
import skfuzzy as fuzz

class Fuzzy:

    def avalia_dor(dor):
        x_range = np.arange(0, 11, 1) 

        leve = fuzz.trapmf(x_range, [0, 0, 2, 3])
        moderada = fuzz.trapmf(x_range, [2, 3, 5, 6])
        intensa = fuzz.trapmf(x_range, [5, 6, 10, 10])

        grau_leve = fuzz.interp_membership(x_range, leve, dor)
        grau_moderado = fuzz.interp_membership(x_range, moderada, dor)
        grau_intenso = fuzz.interp_membership(x_range, intensa, dor)

        if grau_leve > grau_moderado and grau_leve > grau_intenso:
            return "leve"
        if grau_leve == grau_moderado and grau_leve > grau_intenso:
            return "leve/moderada"
        if grau_moderado > grau_leve and grau_moderado > grau_intenso:
            return "moderada"
        if grau_moderado == grau_intenso and grau_moderado > grau_leve:
            return "moderada/intensa"
        return "intensa"
    
    def avalia_exudato(volume):
        x_range = np.arange(0, 11, 1) 

        leve = fuzz.trapmf(x_range, [0, 0, 2, 3])
        pouco = fuzz.trapmf(x_range, [2.5, 3, 5.5, 6])
        moderada = fuzz.trapmf(x_range, [5.5, 6, 7, 8])
        intensa = fuzz.trapmf(x_range, [7, 8, 10, 10])

        grau_leve = fuzz.interp_membership(x_range, leve, volume)
        grau_pouco = fuzz.interp_membership(x_range, pouco, volume)
        grau_moderado = fuzz.interp_membership(x_range, moderada, volume)
        grau_intenso = fuzz.interp_membership(x_range, intensa, volume)

        if grau_leve > grau_moderado and grau_leve > grau_intenso and grau_leve > grau_pouco:
            return "leve"
        if grau_leve == grau_pouco and grau_leve > grau_intenso and grau_leve > grau_moderado:
            return "leve/pouco"
        if grau_pouco > grau_moderado and grau_pouco > grau_intenso and grau_pouco > grau_leve:
            return "pouco"
        if grau_pouco == grau_moderado and grau_pouco > grau_intenso and grau_pouco > grau_leve:
            return "pouco/moderado"
        if grau_moderado > grau_leve and grau_moderado > grau_intenso and grau_moderado > grau_pouco:
            return "moderado"
        if grau_moderado == grau_intenso and grau_moderado > grau_leve and grau_moderado > grau_pouco:
            return "moderado/intenso"
        return "intenso"

print(Fuzzy.avalia_exudato(5.9))