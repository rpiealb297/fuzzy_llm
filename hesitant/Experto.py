from typing import List, Set, Dict, Callable
from statistics import mean
from hesitant.Fuzzy import Fuzzy

class Experto:
    
    #Son las propiedades que hay que evaluar en el texto.
    propiedades = ["precision","adecuacion","cohesion"]

    #Representa el valor del filtro que se desea aplicar para ver si la media de los expertos consideran
    #que es una respuesta aceptable o no.
    filtro = 0.5

    #Ctor.
    # @Propiedades_texto_evaluar: Son las propiedades que se utilizan para evaluar los textos
    # @valor_filtro: Por defecto será 0.5, pero puede cambiarse al valor necesario para hacer que las alucinaciones desaparezcan.
    def __init__(self, propiedades_texto_evaluar = None, valor_filtro = 0.5):
        if propiedades_texto_evaluar != None:
            self.propiedades = propiedades_texto_evaluar
        self.filtro = valor_filtro
        self.fuzzy = Fuzzy()
   
    #Hace el cálculo de la evaluación de un experto para una propiedad de texto en concreto.
    #@bases: Son las líneas base, con todos los pesos de las propiedades.
    #@valoracion_expertos: Son los pesos de todas las propiedades de un experto en concreto.
    #@return: Es el valoración de todos los expertos
    def valoracion(self, bases, valoracion_expertos, propiedad):
        base = bases[propiedad]
        sumPropiedad = 0
        for valoracionExperto in valoracion_expertos[propiedad]:
            for valorBase in base:
                sumPropiedad += self.fuzzy.r(valorBase, valoracionExperto)
        return sumPropiedad

        #print("Para el experto:"+str(expert_info)+" y la propiedad: "+ property + " tenemos el valor:"+str(propertyExpertMeanProperty / len(baselineItem)))
        #return mediaPropiedad / len(base)

    #Devuelve la evaluación de todos los expertos
    #@bases: Son las líneas base, con todos los pesos de las propiedades.
    #@valoracion_expertos: Son los pesos de todas las propiedades de un experto en concreto.
    def evaluaVariosExpertos(self, bases, expertos):        
        numero_experto = 0 #solo tiene proposito de depuracion
        expert_evaluation = 0
        for experto in expertos:
            numero_experto += 1 #Solo tiene proposito de depuracion
            evaluation = 0
            #print("-------------- Experto"+str(numero_experto)+" ----------------")
            for property in self.propiedades:
                sumProperty = self.valoracion(bases, experto, property)
                mediaProperty = sumProperty / (len(bases[property]) * len(experto[property]))
                #print("Resultado propiedad:"+property+" es:", mediaProperty)
                evaluation += mediaProperty
            expert_evaluation += evaluation / len(expertos)
            
            #print("Evaluación del experto"+str(numero_experto)+" es:"+str(evaluation / len(self.propiedades)))
        return expert_evaluation / len(self.propiedades)

    #Regla que se aplica para indicar si el texto es aceptable o no. True si es aceptable
    #@peso: Es el peso que se va a evaluar.
    #@return: Devuelve True si es aceptable.
    def esAceptable(self, peso):
        return peso >= self.filtro