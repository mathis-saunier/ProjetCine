from .scene import Scene
from .donneesContenu import DonneesContenu
from .donneesDescription import DonneesDescription
from .donneesNarration import DonneesNarration
from conditionPackage import ValeurCondition, ConditionSceneSuivante

class SceneAvecCondition(Scene):
    """
    Classe représentant une scène possédant des conditions.
    
    Attributs:
        conditions (list[Condition]): La liste des conditions de la scène
    """
    
    def __init__(self, idScene, contenuScene, descriptionScene, narrationScene, conditions):
        """
        Constructeur de la classe SceneAvecCondition.

        Args:
            idScene (int): L'identifiant de la scène
            contenuScene (DonneesContenu): Les données de contenu de la scène
            descriptionScene (DonneesDescription): Les données de description de la scène
            narrationScene (DonneesNarration): Les données de narration de la scène
            conditions (list[Condition]): La liste des conditions de la scène
        """
        super().__init__(idScene, contenuScene, descriptionScene, narrationScene)
        self.conditions = conditions
        
    # Surchage du constructeur avec le décorateur @classethod
    @classmethod
    def depuisDonneesBrutes(cls, idScene, lieu, personnages, interieurExterieur, urlTexte, voies, actes, conditions,
                            estDebut: bool = False, estFin: bool = False, resume: str = ""):
        """
        Second constructeur de la classe SceneCondition à partir des infos brutes des classes DonneesDescription, DonneesContenu et DonneesNarration.
        
        Args:
            idScene (int): L'identifiant de la scène
            lieu (str): Le lieu où se déroule la scène
            personnages (list[str]): La liste des personnages présents dans la scène
            interieurExterieur (str): Le type de lieu où se déroule la scène (intérieur ou extérieur)
            urlTexte (str): L'url du texte associé à la scène
            voies (list[str]): La liste des voies possibles pour la scène
            actes (list[str]): La liste des actes possibles pour la scène
            conditions (list[Condition]): La liste des conditions de la scène
            estDebut (bool): Indique si la scène peut ouvrir un script (défaut: False)
            estFin (bool): Indique si la scène peut clore un script (défaut: False)
            resume (str): Un résumé court affiché au survol du graphe (défaut: chaîne vide)
        """
        return cls(idScene, DonneesContenu(urlTexte, resume), DonneesDescription(lieu, personnages, interieurExterieur), DonneesNarration(voies, actes, estDebut, estFin), conditions)
        
    # Fonction __str__ déjà définie par héritage
    
    def __repr__(self):
        return f"SceneAvecCondition({self.idScene}, {self.descriptionScene.lieu}, {self.descriptionScene.personnages}, {self.descriptionScene.interieurExterieur}, '{self.contenuScene.urlTexte}', {str(self.narrationScene.voies)}, {str(self.narrationScene.actes)}, {str(self.conditions)})"

        
    def possedeDesScenesSuivantes(self) -> bool:
        """
        Méthode indiquant si d'autres scènes peuvent succéder à celle-ci dans un script.

        La réponse est déduite des transitions générées par les conditions de la scène,
        ce qui évite au moteur de connaître les types concrets de conditions.

        Returns:
            bool: True si au moins une condition désigne une scène suivante, False sinon
        """
        return any(condition.genererTransitions(self) for condition in self.conditions)

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
    