from copy import deepcopy

from .scene import Scene
from conditionPackage import ValeurCondition

class SceneAvecCondition(Scene):
    conditions = []
    
    def __init__(self, idScene, lieu, personnages, interieurExterieur, urlTexte, voies, actes, conditions):
        super().__init__(idScene, lieu, personnages, interieurExterieur, urlTexte, voies, actes)
        self.conditions = conditions
        
    # Surchage du constructeur avec le décorateur @classethod
    @classmethod
    def constructeurParDonnees(self, idScene, donneesDescription, donneesContenu, donneesNarration, conditions):
        return SceneAvecCondition(idScene,
                                  donneesDescription.lieu,
                                  donneesDescription.personnages,
                                  donneesDescription.interieurExterieur,
                                  donneesContenu.urlTexte,
                                  donneesNarration.voies,
                                  donneesNarration.actes,
                                  conditions)
        
    # Fonction __str__ déjà définie par héritage
    
    def __repr__(self):
        return f"Scene({self.idScene}, '{self.lieu}', {str(self.personnages)}, {self.interieurExterieur}, '{self.urlTexte}', {str(self.voies)}, {str(self.actes)}, {str(self.conditions)})"

        
    # Permet de vérifier que les conditions des scènes déjà ajoutées et de la scène actuelle ne
    # menent pas a un ECHEC
    def verifierToutesConditions(self, film):
        # On récupère les conditions des scènes déjà dans le film
        conditionsAVerif = film.recupererConditions()
        # On ajoute les conditions de cette scène
        for c in self.conditions:
            conditionsAVerif.append(c)
        # Pour chaque condition, on vérifie que la Scène que l'on souhaite ajouter retourne SUCCES
        for c in conditionsAVerif:
            if (c.verifierCondition(self) == ValeurCondition.ECHEC):
                return ValeurCondition.ECHEC
        return ValeurCondition.SUCCES
    