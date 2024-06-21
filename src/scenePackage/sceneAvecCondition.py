from .scene import Scene

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
    def verifierToutesLesConditions(self, film):
        conditionsAVerif = copy(film.scenes)
        for c in self.conditions:
            conditionsAVerif.append(c)
        for c in conditionsAVerif:
            if (c.verifierCondition(film) == ValeurCondition.ECHEC):
                return ValeurCondition.ECHEC
        return ValeurCondition.SUCCES
    