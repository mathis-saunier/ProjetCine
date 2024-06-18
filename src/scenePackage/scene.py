# A faire : Changer le nom de interieurExterieur
# On faire ajouter du typage de variable dans les déclarations : https://docs.python.org/fr/3.10/library/typing.html

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
        # Faire une exception pour gerer la création d'une scene avec un ID deja existant
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
    # Le premier élément cls fait référence à la classe elle-même (un peu comme le self de ce que j'ai compris)
    def constructeurParDonnees(cls, idScene, donneesDescription, donneesContenu, donneesNarration):
        return Scene(idScene,
                     donneesDescription.lieu,
                     donneesDescription.personnages,
                     donneesDescription.interieurExterieur,
                     donneesContenu.urlTexte,
                     donneesNarration.voies,
                     donneesNarration.actes)

    def __str__(self):
        res = "idScene :" + str(self.idScene) + "\nDonnees description :\n " + "lieu : " + self.lieu + ", personnages : " + str(self.personnages) + ", interieurExterieur : " + str(self.interieurExterieur) + "\nDonnees contenu :\n urlTexte : " + self.urlTexte + "\nDonnees narration :\n voies : " + str(self.voies) + ", actes : " + str(self.actes)

        return res
        



# On met tous les attributs dans Scene mais il pourrait rester intéressant
# de séparer par type de données et faire un autre constructeur de Scene avec
# ces types de données 
class DonneesDescription:
    lieu = None
    personnages = []
    interieurExterieur = None
    
    def __init__(self, lieu, personnages, interieurExterieur):
        self.lieu = lieu
        self.personnages = personnages
        self.interieurExterieur = interieurExterieur


class DonneesContenu:
    urlTexte = None

    def __init__(self, urlTexte):
        self.urlTexte = urlTexte
        
        
class DonneesNarration:
    voies = []
    actes = []
    
    def __init__(self, voies, actes):
        self.voies = voies
        self.actes = actes

    