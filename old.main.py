from typing import List, Set, Dict, Callable
from statistics import mean

valores_linguisticos = [
    "Perfecto", "Muy bien", "Bien", "Regular", "Malo", "Muy malo", "Incorrecto"
]

# Asignamos valores difusos entre 0 y 1 manualmente
fuzz_map = {
    "Perfecto": 0.95,
    "Muy bien": 0.9,
    "Bien": 0.75,
    "Regular": 0.5,
    "Malo": 0.25,
    "Muy malo": 0.1,
    "Incorrecto": 0.0
}

properties = ["T_max","RainProb","PhysCons"]

def pass_rule(W):
    return W >= 0.5

def r(x: float, y: float) -> float:
    return 0.5 * ((y - x) + 1.0)

def get_expert_evaluation(baselines, expert_info, property):
    propertyExpertItem = expert_info[property].pop()
    baselineItem = baselines[property]
    propertyExpertMeanProperty = 0

    for baselineValue in baselineItem:
        propertyExpertMeanProperty += r(baselineValue, propertyExpertItem)

    #print("Para el experto:"+str(expert_info)+" y la propiedad: "+ property + " tenemos el valor:"+str(propertyExpertMeanProperty / len(baselineItem)))
    return propertyExpertMeanProperty / len(baselineItem)

def evaluate_expert_text(baselines, expert_evals):
    
    expert_evaluation = 0

    for property in properties:
        evaluation = 0
        for expert in expert_evals:
            evaluation += get_expert_evaluation(baselines, expert, property)
        expert_evaluation += evaluation / len(expert_evals)
        print("Evaluación para la propiedad:"+property+" es:"+str(evaluation / len(expert_evals)))
    
    return expert_evaluation / len(properties)

# Función de fuzzificación
def fuzzimap(valor):
    return fuzz_map.get(valor, None)

def fuzzify_set(valores):
    items = set()
    for index in range(len(valores)):
        item = fuzzimap(valores[index])
        items.add(item)
    return items

# ---------- ejemplo rpido ----------
baselines = {
    "T_max": {0.8, 0.9},
    "RainProb": {0.7},
    "PhysCons": {0.6}
}


valores_expertos = [
    {"T_max": ["Bien", "Regular"], "RainProb": ["Perfecto"], "PhysCons": ["Perfecto"]},
    {"T_max": ["Muy bien"], "RainProb": ["Regular"], "PhysCons": ["Perfecto"]},
    {"T_max": ["Perfecto"], "RainProb": ["Malo"], "PhysCons": ["Muy malo"]}
]
'''
valores_expertos = [
    {"T_max": ["Perfecto"], "RainProb": ["Perfecto"], "PhysCons": ["Perfecto"]},
    {"T_max": ["Perfecto"], "RainProb": ["Perfecto"], "PhysCons": ["Perfecto"]},
    {"T_max": ["Perfecto"], "RainProb": ["Perfecto"], "PhysCons": ["Perfecto"]}
]
'''

experts = []
for i in range(3):
    set_expertos = {}
    set_expertos["T_max"] = fuzzify_set(valores_expertos[i]["T_max"])
    set_expertos["RainProb"] = fuzzify_set(valores_expertos[i]["RainProb"])
    set_expertos["PhysCons"] = fuzzify_set(valores_expertos[i]["PhysCons"])
    experts.append(set_expertos)


'''
experts = [
    {"T_max": {0.75, 0.8}, "RainProb": {0.6, 0.65}, "PhysCons": {0.55, 0.6}},
    {"T_max": {0.7}, "RainProb": {0.6}, "PhysCons": {0.5, 0.55}},
    {"T_max": {0.82}, "RainProb": {0.75, 0.8}, "PhysCons": {0.6, 0.65}}
]
'''

'''
experts = [
    {"T_max": {0.9, 0.95}, "RainProb": {0.9, 0.95}, "PhysCons": {0.95, 0.9}},
    {"T_max": {0.7}, "RainProb": {0.6}, "PhysCons": {0.5, 0.55}},
    {"T_max": {0.82}, "RainProb": {0.75, 0.8}, "PhysCons": {0.6, 0.65}}
]
'''

print(valores_expertos)
print(experts)

W = evaluate_expert_text(baselines, experts)
print("Global␣score:", W, "", "ACCEPTED" if pass_rule(W) else "REJECTED")

'''
accepted, W, w_i = evaluate_text(experts, baselines)
'''