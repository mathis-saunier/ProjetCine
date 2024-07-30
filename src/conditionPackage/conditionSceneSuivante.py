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
        # il faut vérifier avant qu'il y a au moins une scene qui existe et qui est récupérable par obtenirSceneParId
        # sinon ça retourne None (ou une exception) et s.idScene ne marche pas A REFLECHIR
        for id in self.idScenesSuivantesPossibles:
            s = Scene.obtenirSceneParId(id)
            if (s.idScene == idSceneAVerif):
                return ValeurCondition.SUCCES
        return ValeurCondition.ECHEC