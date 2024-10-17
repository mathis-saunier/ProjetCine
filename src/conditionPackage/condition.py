from abc import ABC, abstractmethod

from .valeurCondition import ValeurCondition

# Classe abstraite
class Condition:
    """
    Condition est une classe abstraite qui représente les conditions que peuvent posséder une SceneAvecCondition.
    """
    valeurCondition = None
    
    @abstractmethod
    def __init__(self, valeurCondition):
        """
        Constructeur abstrait de la classe Condition.
        """
        pass
    
    @abstractmethod
    def verifierCondition(self, scene):
        """
        Méthode abstraite permettant de vérifier si la scene passée en argument vérifie la Condition.

        Retourne un élément de l'énumération ValeurCondition (SUCCES ou ECHEC).
        """
        pass
