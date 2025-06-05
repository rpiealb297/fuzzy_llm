from hesitant.Experto import Experto
from hesitant.Fuzzy import Fuzzy
from hesitant.Files import Files

import os


def perform_files(baselines, valores_expertos):
    fuzzy = Fuzzy()
    experto = Experto()

    experts = []
    for i in range(3):
        set_expertos = {}
        set_expertos["precision"] = fuzzy.GetConjuntoDifuso(valores_expertos[i]["precision"])
        set_expertos["adecuacion"] = fuzzy.GetConjuntoDifuso(valores_expertos[i]["adecuacion"])
        set_expertos["cohesion"] = fuzzy.GetConjuntoDifuso(valores_expertos[i]["cohesion"])
        experts.append(set_expertos)

    #print(*valores_expertos)
    #print(experts)

    W = experto.evaluaVariosExpertos(baselines, experts)
    #print("Global␣score:", W, "", "ACCEPTED" if experto.esAceptable(W) else "REJECTED")
    return W, experto.esAceptable(W)

fileReader = Files()
fileReader.loadBaseLines("data/baselines.json")
baselines = fileReader.baselines

exitos = 0
#Aqui vamos a leer todos los expertos uno a uno, primero cargamos los que son correctos
for filename in os.listdir("data/experts/accepted"):
    #print("Fichero ACEPTADO:", filename)
    fileReader.loadExperts("data/experts/accepted/"+filename)
    valores_expertos = fileReader.experts
    W, is_accepted = perform_files(baselines, valores_expertos)
    exitos += 1 if is_accepted else 0
    print("Fichero ", filename, " es CORRECTO y los expertos indican que es ", "CORRECTO" if is_accepted else "INCORRECTO")

for filename in os.listdir("data/experts/rejected"):
    #print("Fichero RECHAZADO:", filename)
    fileReader.loadExperts("data/experts/rejected/"+filename)
    valores_expertos = fileReader.experts
    W, is_accepted = perform_files(baselines, valores_expertos)
    exitos += 1 if not is_accepted else 0
    print("Fichero ", filename, " INCORRECTO y los expertos indica que es ", "CORRECTO" if is_accepted else "INCORRECTO")

print("Total de expertos correctos:", exitos, "de", len(os.listdir("data/experts/accepted")) + len(os.listdir("data/experts/rejected")))



    
