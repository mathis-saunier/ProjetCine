from copy import deepcopy
import random as rd

from scenePackage.scene import Scene
from conditionPackage.condition import Condition
from conditionPackage.valeurCondition import ValeurCondition
import jsonPackage as js

class SceneInexistanteException(Exception):
    """
    Exception levée lorsqu'une scène n'existe pas.
    """
    def __init__(self, id):
        self.id = id
        super().__init__(f"Erreur, la scènes d'id {id} n'existe pas")

class ZeroSceneRestanteException(Exception):
    """
    Exception levée lorsqu'il n'y a plus de scènes restantes dans un acte pour une voie donnée.
    """
    def __init__(self, acte, voie):
        self.acte = acte
        self.voie = voie
        super().__init__(f"Erreur, il n'y a pas de scènes restantes dans l'acte {acte} pour la voie {voie}")
        
class Film():
    """
    Classe représentant un Film.
    
    Attributs:
        nomFilm (str): Le nom du film
        scenesDuFilm (list[Scene]): La liste des scènes du film
        scenesDuScript (list[Scene]): La liste des scènes du script (les scènes du film qui ont été choisies pour le script)
        voieInitiale (str): La voie initiale du film
        voieActuelle (str): La voie actuelle du film
        acteActuel (str): L'acte actuel du film
    """
    nomFilm = None
    scenesDuFilm = []
    scenesDuScript = []
    voieInitiale = None
    voieActuelle = None
    acteActuel = None
    
    # Ajouter le choix de la voieInitiale dans le __init__
    def __init__(self, nomFilm, voieInitiale):
        """
        Constructeur de la classe Film.

        Args:
            nomFilm (str): Le nom du film
            voieInitiale (str): La voie initiale du film
        """
        self.nomFilm = nomFilm
        self.voieInitiale = voieInitiale
        self.voieActuelle = voieInitiale
        self.acteActuel = "1"
    
    def ajouterScene(self, scene):
        """
        Méthode permettant d'ajouter une scène au script.

        Args:
            scene (Scene): La scène à ajouter au script
        """
        self.scenesDuScript.append(scene)
    
    # Ne prendre pas en compte l'acte ou la voie actuel.le
    def recupererScenesPossibles(self, acte, voie):
        """
        Méthode permettant de récupérer les scènes possibles pour un acte et une voie donnée.

        ATTENTION: Pour le moment, cette méthode ne prend pas en compte l'acte ou la voie passés en arguement.

        Args:
            acte (str): L'acte pour lequel on souhaite récupérer les scènes possibles
            voie (str): La voie pour laquelle on souhaite récupérer les scènes possibles

        Returns:
            list[Scene]: La liste des scènes possibles
        """
        scenesExistantes = deepcopy(self.scenesDuFilm)
        return scenesExistantes
        
    def recupererConditions(self):
        """
        Méthode permettant de récupérer toutes les conditions des scènes du script.

        Returns:
            list[Condition]: La liste des conditions des scènes du script
        """
        res = []
        for s in self.scenesDuScript:
            for c in s.conditions:
                res.append(c)
        return res
    
    def tirerUneScene(self):
        """
        Méthode permettant de choisir aléatoirement une scène parmi les scènes possibles en vérifiant que la scène respecte toutes les conditions du script dans son état actuel.

        Returns:
            Scene: La scène choisie aléatoirement

        Raises:
            ZeroSceneRestanteException: Si il n'y a plus de scènes disponibles pour le tirage aléatoire. Les raisons peuvent être qu'aucune scène ne vérifie les conditions ou que toutes les scènes possibles ont déjà été choisies
        """
        scenesPossibles = self.recupererScenesPossibles(self.acteActuel, self.voieActuelle)
        # On retire egalement les scenesDuScript qui sont deja dans le script
        for s in scenesPossibles:
            if s in self.scenesDuScript:
                scenesPossibles.remove(s)
                
        rd.seed()
        while len(scenesPossibles) != 0:
            choix = rd.randrange(0, len(scenesPossibles))
            sceneChoisie = scenesPossibles[choix]
            print(f"Scene choisie avant condition : {sceneChoisie}")
            # Maintenant que l'on a une scene possible, on vérifie qu'elle respecte les conditions
            if (sceneChoisie.verifierToutesLesConditionsPrecedentes(self) == ValeurCondition.SUCCES):
                print("On choisit cette scene")
                return sceneChoisie
            else:
                scenesPossibles.remove(sceneChoisie)
                print("On ne choisit pas cette scene")
                   
        if (len(scenesPossibles) == 0):
            raise ZeroSceneRestanteException(self.acteActuel, self.voieActuelle)
        
    def creerFilmDepuisJSON(self, fichier_json):
        """
        Méthode permettant de créer un film à partir d'un fichier JSON.

        Args:
            fichier_json (str): Le nom du fichier JSON (ex: "film.json")
        """
        self.scenesDuFilm = js.creerScenesDepuisJSON(fichier_json)

    # nombre de tour est une variable temporaire. Il y a mieux à faire comme fonctionnement
    def creerScript(self, choixPremiereScene=None):
        """
        Méthode permettant de créer un script aléatoire à partir des scènes du film.

        Args:
            choixPremiereScene (str): L'identifiant de la première scène du script (optionnel)

        Returns:
            list[Scene]: La liste des scènes du script
        """
        # On reinitialise tout potentiel ancien script
        self.scenesDuScript = []
        
        nbTour = 8
        if choixPremiereScene != None:
            print("On force la première scène")
            for s in self.scenesDuFilm:
                if s.idScene == choixPremiereScene:
                    self.ajouterScene(s)
                    nbTour -= 1
                    print(s)
        print("Debut creation film")
        # Faire une vérif que l'attribut scenes est bien vide
        for loop in range(nbTour):
            print(loop)
            self.ajouterScene(self.tirerUneScene())
        return self.scenesDuScript
    
    def obtenirScript(self):
        """
        Méthode permettant d'obtenir le script du film sous un format texte.

        Returns:
            str: Le script du film sous un format texte
        """
        script = "Début du script\n"
        for s in self.scenesDuScript:
            script += s.idScene + " : " + s.urlTexte + "\n"
        return script
    

    def sceneDejaExistante(self, idScene):
        """
        Méthode permettant de vérifier si une scène existe déjà dans le film.

        Args:
            idScene (str): L'identifiant de la scène à vérifier

        Returns:
            bool: True si la scène existe déjà, False sinon
        """
        for scene in self.scenesDuFilm:
            if (idScene == scene.idScene):
                return True
        return False
    
    def obtenirSceneParId(self, id):
        """
        Méthode permettant de récupérer une scène par son identifiant.
        
        Args:
            id (str): Un identifiant de scène

        Returns:
            Scene: La scène correspondante à l'identifiant

        Raises:
            SceneInexistanteException: Si l'indentifiant de la scène n'existe pas
        """
        for s in self.scenesDuFilm:
            if (s.idScene == id):
                return s
        # Si l'on a pas trouvé de scene on lève une exception
        raise SceneInexistanteException(id)
        
        
        
        