import json

class Files:
    def __init__(self):
        self.baselines = {}
        self.experts = []

    def loadBaseLines(self, path):
        with open(path, "r", encoding="utf-8") as archivo:
            self.baselines = json.load(archivo)
        
    def loadExperts(self, path):
        with open(path, "r", encoding="utf-8") as archivo:
            self.experts = json.load(archivo)