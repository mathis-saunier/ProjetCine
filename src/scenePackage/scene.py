# A faire : Changer le nom de interieurExterieur
class Scene:
    idScene = None
    scenesExistantes = []
    
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
        # Faire une exception propre pour gerer la création d'une scene avec un ID deja existant
        if self.sceneDejaExistante(idScene):
            print("PROBLEME : l'id '"+str(idScene) + "' existe déjà pour une scène")
        self.idScene = idScene
        Scene.scenesExistantes.append(self)
        
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
    
    # A mettre en privé ?
    def sceneDejaExistante(self, idScene):
        for scene in Scene.scenesExistantes:
            if (idScene == scene.idScene):
                return True
        return False
    
    def obtenirSceneParId(self, id):
        for s in Scene.scenesExistantes:
            if (s.idScene == id):
                return s
        return None
        
