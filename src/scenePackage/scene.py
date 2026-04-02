# A faire : Changer le nom de interieurExterieur
from scenePackage.donneesContenu import DonneesContenu
from scenePackage.donneesDescription import DonneesDescription
from scenePackage.donneesNarration import DonneesNarration

class Scene:
    """
    Classe représentant une scène.
    
    Attributs:
        idScene (int): L'identifiant de la scène
        scenes (list[Scene]): La liste des scènes du film (attribut de classe)
        contenuScene (DonneesContenu): Les données de contenu de la scène
        descriptionScene (DonneesDescription): Les données de description de la scène
        narrationScene (DonneesNarration): Les données de narration de la scène
    """
    def __init__(self, idScene, contenuScene, descriptionScene, narrationScene):
        """
        Constructeur de la classe Scene.
        
        Args:
            idScene (int): L'identifiant de la scène
            contenuScene (DonneesContenu): Les données de contenu de la scène
            descriptionScene (DonneesDescription): Les données de description de la scène
            narrationScene (DonneesNarration): Les données de narration de la scène
        """
        self.idScene = idScene
        self.contenuScene = contenuScene
        self.descriptionScene = descriptionScene
        self.narrationScene = narrationScene

    # La surchage de constructeurs en python est impossible et l'on doit donc utiliser d'autres méthodes
    # Pour ma part, je vais utiliser le décorateur @classmethod qui me permettra d'appeler une méthode de classe
    # qui fera l'instanciation à ma place (ce sera ma "surchage de __init__")
    # Lien vers le site d'où vient la solution https://www.delftstack.com/fr/howto/python/overload-constructors-in-python/
    @classmethod
    def depuisDonneesBrutes(cls, idScene, lieu, personnages, interieurExterieur, urlTexte, voies, actes):
        """
        Second constructeur de la classe Scene à partir des infos brutes des classes DonneesDescription, DonneesContenu et DonneesNarration.
        
        Args:
            idScene (int): L'identifiant de la scène
            lieu (str): Le lieu où se déroule la scène
            personnages (list[str]): La liste des personnages présents dans la scène
            interieurExterieur (str): Le type de lieu où se déroule la scène (intérieur ou extérieur)
            urlTexte (str): L'url du texte associé à la scène
            voies (list[str]): La liste des voies possibles pour la scène
            actes (list[str]): La liste des actes possibles pour la scène
        """
        descriptionScene = DonneesDescription(lieu, personnages, interieurExterieur)
        contenuScene = DonneesContenu(urlTexte)
        narrationScene = DonneesNarration(voies, actes)
        return cls(idScene, contenuScene, descriptionScene, narrationScene)

    def __str__(self):
        return f"idScene : {self.idScene}"

    def __repr__(self):
        return f"Scene({self.idScene}, '{self.lieu}', {str(self.personnages)}, {self.interieurExterieur}, '{self.urlTexte}', {str(self.voies)}, {str(self.actes)})"
    
    def __eq__(self, other):
        return self.idScene == other.idScene
        
    
    
        
