from abc import ABC, abstractmethod

from .valeurCondition import ValeurCondition

# Classe abstraite
class Condition(ABC):
    """
    Condition est une classe abstraite qui représente les conditions que peut posséder une scène.
    """
    
    @abstractmethod
    def verifierCondition(self, scene):
        """
        Méthode abstraite permettant de vérifier si la scene passée en argument vérifie la condition.
        Retourne un élément de l'énumération ValeurCondition (SUCCES ou ECHEC).

        Args:
            scene (Scene): scène à vérifier
        """
        pass
    
    @abstractmethod
    def genererTransitions(self, sceneDepart):
        """
        Méthode abstraite permettant de générer les transitions possibles à partir de la scène de départ.
        
        Args:
            sceneDepart (Scene): La scène de départ pour laquelle générer les transitions
            
        Returns:
            list[Transition]: La liste des transitions générées par cette condition
        """
        pass
