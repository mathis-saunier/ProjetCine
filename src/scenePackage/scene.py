# A faire : Changer le nom de interieurExterieur

class Scene:
    """
    Classe représentant une scène d'un film.
    
    Attributs:
        idScene (int): L'identifiant de la scène
        lieu (str): Le lieu où se déroule la scène
        personnages (list[str]): La liste des personnages présents dans la scène
        interieurExterieur (str): Le type de lieu où se déroule la scène (intérieur ou extérieur)
        urlTexte (str): L'url du texte associé à la scène
        voies (list[str]): La liste des voies possibles pour la scène
        actes (list[str]): La liste des actes possibles pour la scène
    """
    idScene = None
    
    # Donnees description
    lieu = None
    personnages = None
    interieurExterieur = None
    # Donnees contenu
    urlTexte = None
    # Donnees narration
    voies = []
    actes = []
    
    
    def __init__(self, idScene, lieu, personnages, interieurExterieur, urlTexte, voies, actes):
        """
        Constructeur de la classe Scene.
        
        Args:
            idScene (int): L'identifiant de la scène
            lieu (str): Le lieu où se déroule la scène
            personnages (list[str]): La liste des personnages présents dans la scène
            interieurExterieur (str): Le type de lieu où se déroule la scène (intérieur ou extérieur)
            urlTexte (str): L'url du texte associé à la scène
            voies (list[str]): La liste des voies possibles pour la scène
            actes (list[str]): La liste des actes possibles pour la scène
        """
        self.idScene = idScene
        
        # Initialisation des donnees de description
        self.lieu = lieu
        self.personnages = personnages
        self.interieurExterieur = interieurExterieur
        
        # Initialisation des donnees de contenu
        self.urlTexte = urlTexte
        
        # Initialisation des donnees de narration
        self.voies = voies
        self.actes = actes
        
    # La surchage de constructeurs en python est impossible et l'on doit donc utiliser d'autres méthodes
    # Pour ma part, je vais utiliser le décorateur @classmethod qui me permettra d'appeler une méthode de classe
    # qui fera l'instanciation à ma place (ce sera ma "surchage de __init__")
    # Lien vers le site d'où vient la solution https://www.delftstack.com/fr/howto/python/overload-constructors-in-python/
    @classmethod
    def constructeurParDonnees(self, idScene, donneesDescription, donneesContenu, donneesNarration):
        """
        Second constructeur de la classe Scene à partir d'instances de classes DonneesDescription, DonneesContenu et DonneesNarration.
        
        Args:
            idScene (int): L'identifiant de la scène
            donneesDescription (DonneesDescription): Les données de description de la scène
            donneesContenu (DonneesContenu): Les données de contenu de la scène
            donneesNarration (DonneesNarration): Les données de narration de la scène
        """
        return Scene(idScene,
                     donneesDescription.lieu,
                     donneesDescription.personnages,
                     donneesDescription.interieurExterieur,
                     donneesContenu.urlTexte,
                     donneesNarration.voies,
                     donneesNarration.actes)

    def __str__(self):
        return f"idScene : {self.idScene}"

    def __repr__(self):
        return f"Scene({self.idScene}, '{self.lieu}', {str(self.personnages)}, {self.interieurExterieur}, '{self.urlTexte}', {str(self.voies)}, {str(self.actes)})"
    
    def __eq__(self, other):
        return self.idScene == other.idScene
        
    
    
        
