from hesitant.Experto import Experto
from hesitant.Fuzzy import Fuzzy

baselines = {
    "T_max": {0.8, 0.9},
    "RainProb": {0.7},
    "PhysCons": {0.6}
}
'''
valores_expertos = [
    {"T_max": ["Bien", "Regular"], "RainProb": ["Perfecto"], "PhysCons": ["Perfecto"]},
    {"T_max": ["Muy bien"], "RainProb": ["Regular"], "PhysCons": ["Perfecto"]},
    {"T_max": ["Perfecto"], "RainProb": ["Malo"], "PhysCons": ["Muy malo"]}
]
'''

# Asignamos valores difusos entre 0 y 1 manualmente
    '''
    MAPA_DIFUSO = {
        "Perfecto": 0.95,
        "Muy bien": 0.85,
        "Bien": 0.7,
        "Aceptable": 0.6,
        "Regular": 0.5,
        "Malo": 0.4,
        "Muy malo": 0.3,
        "Incorrecto": 0.0
    }
    '''
 
valores_expertos = [
    {"T_max": ["Bien", "Aceptable"], "RainProb": ["Perfecto"], "PhysCons": ["Perfecto"]},
    {"T_max": ["Perfecto", "Muy bien"], "RainProb": ["Bien", "Aceptable", "Regular"], "PhysCons": ["Perfecto"]},
    {"T_max": ["Perfecto", "Muy bien"], "RainProb": ["Malo"], "PhysCons": ["Muy malo"]}
]


fuzzy = Fuzzy()
experto = Experto()

experts = []
for i in range(3):
    set_expertos = {}
    set_expertos["T_max"] = fuzzy.GetConjuntoDifuso(valores_expertos[i]["T_max"])
    set_expertos["RainProb"] = fuzzy.GetConjuntoDifuso(valores_expertos[i]["RainProb"])
    set_expertos["PhysCons"] = fuzzy.GetConjuntoDifuso(valores_expertos[i]["PhysCons"])
    experts.append(set_expertos)

print(*valores_expertos)
print(experts)

W = experto.evaluaVariosExpertos(baselines, experts)
print("-------------- RESULTADO -----------------------")
print("Global␣score:", W, "", "ACCEPTED" if experto.esAceptable(W) else "REJECTED")

'''
accepted, W, w_i = evaluate_text(experts, baselines)
'''