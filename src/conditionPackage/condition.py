from abc import ABC, abstractmethod

from .valeurCondition import ValeurCondition

# Classe abstraite
class Condition:
    """
    Condition est une classe abstraite qui représente les conditions que peut posséder une scène.
    """
    valeurCondition = None
    
    @abstractmethod
    def __init__(self, valeurCondition):
        """
        Constructeur abstrait de la classe Condition.

        Args:
            valeurCondition (ValeurCondition): valeur à retourner si la condition est vérifiée
        """
        pass
    
    @abstractmethod
    def verifierCondition(self, scene):
        """
        Méthode abstraite permettant de vérifier si la scene passée en argument vérifie la condition.
        Retourne un élément de l'énumération ValeurCondition (SUCCES ou ECHEC).

        Args:
            scene (Scene): scène à vérifier
        """
        pass
