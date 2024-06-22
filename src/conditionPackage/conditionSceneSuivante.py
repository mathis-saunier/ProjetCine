from .condition import Condition
from .valeurCondition import ValeurCondition

class ConditionSceneSuivante(Condition):
    scenesSuivantesPossibles = []
    
    def __init__(self, scenesSuivantesPossibles):
        if (type(scenesSuivantesPossibles) is list):
            self.scenesSuivantesPossibles = scenesSuivantesPossibles
        else:
            self.scenesSuivantesPossibles.append(scenesSuivantesPossibles)
            
    def verifierCondition(self, scene):
        idSceneAVerif = scene.idScene
        for s in self.scenesSuivantesPossibles:
            if (s.idScene == idSceneAVerif):
                return ValeurCondition.SUCCES
        return ValeurCondition.ECHEC