from abc import ABC, abstractmethod

from .valeurCondition import ValeurCondition

# Classe abstraite
class Condition:
    valeurCondition = None
    
    @abstractmethod
    def __init__(self, valeurCondition):
        pass
    
    # Retourne SUCCES si la scène est permise par la Condition, retourne ECHEC sinon
    # Exemple : si la scene est imcompatible avec les conditions déjà existantes alors ECHEC
    # Si la scene respecte toutes les conditions existantes et que les conditions de cette scène ne posent
    # pas non plus de problème alors SUCCES
    @abstractmethod
    def verifierCondition(self, film):
        pass
