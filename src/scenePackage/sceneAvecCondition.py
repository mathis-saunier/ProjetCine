from .scene import Scene
from conditionPackage import ValeurCondition, ConditionSceneSuivante

class SceneAvecCondition(Scene):
    """
    Classe représentant une scène possédant des conditions.
    
    Attributs:
        conditions (list[Condition]): La liste des conditions de la scène
    """
    conditions = []
    
    def __init__(self, idScene, lieu, personnages, interieurExterieur, urlTexte, voies, actes, conditions):
        """
        Constructeur de la classe SceneAvecCondition.

        Args:
            idScene (int): L'identifiant de la scène
            lieu (str): Le lieu où se déroule la scène
            personnages (list[str]): La liste des personnages présents dans la scène
            interieurExterieur (str): Le type de lieu où se déroule la scène (intérieur ou extérieur)
            urlTexte (str): L'url du texte de la scène
            voies (list[str]): La liste des voies possibles pour la scène
            actes (list[str]): La liste des actes possibles pour la scène
            conditions (list[Condition]): La liste des conditions de la scène
        """
        super().__init__(idScene, lieu, personnages, interieurExterieur, urlTexte, voies, actes)
        self.conditions = conditions
        
    # Surchage du constructeur avec le décorateur @classethod
    @classmethod
    def constructeurParDonnees(self, idScene, donneesDescription, donneesContenu, donneesNarration, conditions):
        """
        Second constructeur de la classe SceneCondition à partir d'instances de classes DonneesDescription, DonneesContenu et DonneesNarration.
        
        Args:
            idScene (int): L'identifiant de la scène
            donneesDescription (DonneesDescription): Les données de description de la scène
            donneesContenu (DonneesContenu): Les données de contenu de la scène
            donneesNarration (DonneesNarration): Les données de narration de la scène
            conditions (list[Condition]): La liste des conditions de la scène
        """
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

        
    # Verifie que les conditions des scenes deja ajoutees ne
    # menent pas a un ECHEC
    def verifierToutesLesConditionsPrecedentes(self, film):
        """
        Méthode permettant de vérifier toutes les conditions des scènes déjà ajoutées au script du film.
        
        Args:
            film (Film): Le film dont on souhaite vérifier les conditions par rapport à notre scène actuelle
            
        Returns:
            ValeurCondition: SUCCES si toutes les conditions sont vérifiées, ECHEC sinon
        """
        # On récupère les conditions des scènes déjà dans le film
        conditionsAVerif = film.recupererConditions()
        # Pour chaque condition, on vérifie que la Scène que l'on souhaite ajouter retourne SUCCES
        for c in conditionsAVerif:
            # Les conditions de SceneSuivantes dans ANCIENNES scenes n'ont pas lieu d'etre verifiees
            if not isinstance(c, ConditionSceneSuivante) or (c in (film.scenesDuScript[-1]).conditions):
                if (c.verifierCondition(self) == ValeurCondition.ECHEC):
                    return ValeurCondition.ECHEC
        return ValeurCondition.SUCCES
    