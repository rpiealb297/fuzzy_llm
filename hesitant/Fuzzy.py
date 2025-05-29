from typing import List, Set, Dict, Callable
from statistics import mean

class Fuzzy:

    #Estos son los valores linguisticos que el sistema va a utilizar para valorar los textos
    VALORES_LINGUISTICOS = [
        "Perfecto", "Muy bien", "Bien", "Aceptable", "Regular", "Malo", "Muy malo", "Incorrecto"
    ]

    # Asignamos valores difusos entre 0 y 1 manualmente
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

    def __init__(self):
        pass


    # Función de fuzzificación para obtener un valor del 0 al 1 desde un texto
    # @texto: Es el texto que se desea fuzzificar.
    # @return: Devuelve el valor difuso asociado al texto
    def MapaDifuso(self, texto):
        return self.MAPA_DIFUSO.get(texto, None)

    #Función r, necesaria para calcular el peso de los expertos
    #@experto: Es el peso dado por el experto
    #@base: Es el peso de la base
    #@return: Es el peso que el experto dará asociado con la base.
    def r(self, experto, base):
        return 0.5 * ((base - experto) + 1.0)

    #Función de conjunto difuso
    #@Son los valores a devolver el mapadifuso    
    def GetConjuntoDifuso(self, valores):
        items = set()
        for index in range(len(valores)):
            item = self.MapaDifuso(valores[index])
            items.add(item)
        return items
