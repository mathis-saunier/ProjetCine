from .condition import Condition
from .valeurCondition import ValeurCondition
from scenePackage.scene import Scene

class ConditionSceneSuivante(Condition):
    """
    ConditionSceneSuivante est une classe, héritant de la classe Condition, qui permet de d'indiquer quelles scènes pouvent succéder à la scène actuelle possédant la condition.

    Attributs:
        idScenesSuivantesPossibles (list[int]): liste des identifiants de scènes pouvant suivre la scène actuelle
    """
    idScenesSuivantesPossibles = []
    
    def __init__(self, idScenesSuivantesPossibles):
        """
        Constructeur de la classe ConditionSceneSuivante.

        Args:
            idScenesSuivantesPossibles (list[int]): liste des identifiants de scènes pouvant succéder à la scène possédant la condition
        """
        if (type(idScenesSuivantesPossibles) is list):
            self.idScenesSuivantesPossibles = idScenesSuivantesPossibles
        else:
            self.idScenesSuivantesPossibles.append(idScenesSuivantesPossibles)
            
    def verifierCondition(self, scene):
        """
        Méthode permettant de vérifier si la scène passée en argument vérifie la condition.

        Args:
            scene (Scene): scène à vérifier

        Returns:
            ValeurCondition.SUCCES ou ValeurCondition.ECHEC
        """
        idSceneAVerif = scene.idScene
        # On verifie si la scene passee en argument verifie la ConditionSceneSuivante
        if scene.idScene in self.idScenesSuivantesPossibles:
            return ValeurCondition.SUCCES
        else:
            return ValeurCondition.ECHEC