from .condition import Condition
from .valeurCondition import ValeurCondition
from scenePackage.scene import Scene

class ConditionSceneSuivante(Condition):
    """
    ConditionSceneSuivante est une Condition qui permet de définir les Scenes pouvant suivre la Scene actuelle.

    Attributs:
        idScenesSuivantesPossibles: liste des id de Scenes pouvant suivre la scene actuelle
    """
    idScenesSuivantesPossibles = []
    
    def __init__(self, idScenesSuivantesPossibles):
        """
        Constructeur de la classe ConditionSceneSuivante.

        Args:
            idScenesSuivantesPossibles: liste des id de Scenes pouvant succéder à la Scene possédant cette ConditionSceneSuivante
        """
        if (type(idScenesSuivantesPossibles) is list):
            self.idScenesSuivantesPossibles = idScenesSuivantesPossibles
        else:
            self.idScenesSuivantesPossibles.append(idScenesSuivantesPossibles)
            
    def verifierCondition(self, scene):
        """
        Méthode permettant de vérifier si la scene passée en argument vérifie la ConditionSceneSuivante.

        Args:
            scene: Scene à vérifier

        Returns:
            ValeurCondition.SUCCES ou ValeurCondition.ECHEC
        """
        idSceneAVerif = scene.idScene
        # On verifie si la scene passee en argument verifie la ConditionSceneSuivante
        if scene.idScene in self.idScenesSuivantesPossibles:
            return ValeurCondition.SUCCES
        else:
            return ValeurCondition.ECHEC