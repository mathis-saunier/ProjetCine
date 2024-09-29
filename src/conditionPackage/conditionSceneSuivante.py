from .condition import Condition
from .valeurCondition import ValeurCondition
from scenePackage.scene import Scene

class ConditionSceneSuivante(Condition):
    idScenesSuivantesPossibles = []
    
    def __init__(self, idScenesSuivantesPossibles):
        if (type(idScenesSuivantesPossibles) is list):
            self.idScenesSuivantesPossibles = idScenesSuivantesPossibles
        else:
            self.idScenesSuivantesPossibles.append(idScenesSuivantesPossibles)
            
    def verifierCondition(self, scene):
        idSceneAVerif = scene.idScene
        # On verifie si la scene passee en argument verifie la ConditionSceneSuivante
        if scene.idScene in self.idScenesSuivantesPossibles:
            return ValeurCondition.SUCCES
        else:
            return ValeurCondition.ECHEC