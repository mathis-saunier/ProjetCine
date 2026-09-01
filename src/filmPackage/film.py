from copy import deepcopy
import random as rd

from scenePackage.scene import Scene
from conditionPackage.condition import Condition
from conditionPackage.valeurCondition import ValeurCondition
from conditionPackage.transition import Transition
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
        
class AucuneSceneDeDebutException(Exception):
    """
    Exception levée lorsqu'aucune scène du film n'est déclarée comme scène de début.
    """
    def __init__(self, nomFilm):
        self.nomFilm = nomFilm
        super().__init__(f"Erreur, aucune scène du film {nomFilm} n'est déclarée comme scène de début")

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
        probabiliteArretSurFin (float): Probabilité de clore le script lorsqu'une scène de fin possède encore des suites
    """
    
    # Ajouter le choix de la voieInitiale dans le __init__
    def __init__(self, nomFilm, voieInitiale, probabiliteArretSurFin: float = 0.5):
        """
        Constructeur de la classe Film.

        Args:
            nomFilm (str): Le nom du film
            voieInitiale (str): La voie initiale du film
            probabiliteArretSurFin (float): Probabilité, entre 0 et 1, de clore le script lorsque la dernière scène est une fin possédant encore des suites (défaut: 0.5)
        """
        self.nomFilm = nomFilm
        self.scenesDuFilm = []
        self.scenesDuScript = []
        self.voieInitiale = voieInitiale
        self.voieActuelle = voieInitiale
        self.acteActuel = "1"
        self.probabiliteArretSurFin = probabiliteArretSurFin
    
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
        # On retire egalement les scenesDuScript qui sont deja dans le script.
        # Filtrer par comprehension et non par remove() successifs : retirer des elements
        # d'une liste pendant qu'on l'itere en fait sauter certains.
        scenesPossibles = [s for s in scenesPossibles if s not in self.scenesDuScript]

        while len(scenesPossibles) != 0:
            choix = rd.randrange(0, len(scenesPossibles))
            sceneChoisie = scenesPossibles[choix]
            # Maintenant que l'on a une scene possible, on vérifie qu'elle respecte les conditions
            if (sceneChoisie.verifierToutesLesConditionsPrecedentes(self) == ValeurCondition.SUCCES):
                return sceneChoisie
            else:
                scenesPossibles.pop(choix)

        raise ZeroSceneRestanteException(self.acteActuel, self.voieActuelle)
        
    def creerFilmDepuisJSON(self, fichier_json):
        """
        Méthode permettant de créer un film à partir d'un fichier JSON.

        Args:
            fichier_json (str): Le nom du fichier JSON (ex: "film.json")

        Raises:
            ChargementJSONException: Si le fichier est introuvable, mal formé ou si son contenu ne respecte pas le format attendu
        """
        self.scenesDuFilm = js.creerScenesDepuisJSON(fichier_json)

    def tirerUneSceneDeDebut(self):
        """
        Méthode permettant de choisir aléatoirement une scène parmi celles déclarées comme scènes de début.

        Returns:
            Scene: La scène de début choisie aléatoirement

        Raises:
            AucuneSceneDeDebutException: Si aucune scène du film n'est déclarée comme scène de début
        """
        scenesDeDebut = [s for s in self.scenesDuFilm if s.narrationScene.estDebut]
        if not scenesDeDebut:
            raise AucuneSceneDeDebutException(self.nomFilm)
        return rd.choice(scenesDeDebut)

    def creerScript(self, choixPremiereScene=None):
        """
        Méthode permettant de créer un script aléatoire à partir des scènes du film.

        Le script démarre sur une scène de début et s'arrête sur une scène de fin.
        Lorsqu'une scène de fin possède encore des suites, la poursuite du récit est
        tirée au sort selon probabiliteArretSurFin, ce qui donne des scripts de longueur variable.

        Args:
            choixPremiereScene (str): L'identifiant de la première scène du script (optionnel, une scène de début est tirée au sort sinon)

        Returns:
            list[Scene]: La liste des scènes du script

        Raises:
            AucuneSceneDeDebutException: Si aucune première scène n'est imposée et qu'aucune scène de début n'est déclarée
            SceneInexistanteException: Si l'identifiant de première scène imposé n'existe pas
            ZeroSceneRestanteException: Si le récit s'interrompt sur une scène qui n'est pas une fin
        """
        # On reinitialise tout potentiel ancien script
        self.scenesDuScript = []

        if choixPremiereScene != None:
            self.ajouterScene(self.obtenirSceneParId(choixPremiereScene))
        else:
            self.ajouterScene(self.tirerUneSceneDeDebut())

        # Le generateur aleatoire n'est pas reamorce ici : un appelant peut ainsi
        # fixer une graine avec random.seed() pour rejouer une generation a l'identique.
        while True:
            derniereScene = self.scenesDuScript[-1]
            estUneFin = derniereScene.narrationScene.estFin

            if not derniereScene.possedeDesScenesSuivantes():
                # Le recit ne peut pas continuer : c'est une fin si l'auteur l'a voulu,
                # sinon le film est incomplet et il faut le signaler.
                if estUneFin:
                    return self.scenesDuScript
                raise ZeroSceneRestanteException(self.acteActuel, self.voieActuelle)

            if estUneFin and rd.random() < self.probabiliteArretSurFin:
                return self.scenesDuScript

            try:
                self.ajouterScene(self.tirerUneScene())
            except ZeroSceneRestanteException:
                # Aucune des suites declarees n'est disponible : acceptable seulement sur une fin
                if estUneFin:
                    return self.scenesDuScript
                raise
    
    def obtenirScript(self):
        """
        Méthode permettant d'obtenir le script du film sous un format texte.

        Returns:
            str: Le script du film sous un format texte
        """
        script = "Début du script\n"
        for s in self.scenesDuScript:
            script += s.idScene + " : " + s.contenuScene.urlTexte + "\n"
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
    
    def genererGraphe(self, nomFichier="graphe.dot"):
        """
        Génère un fichier GraphViz représentant le graphe de transitions entre les scènes du film.
        Le graphe inclut toutes les transitions basées sur les conditions des scènes.
        
        Args:
            nomFichier (str): Le nom du fichier de sortie (défaut: "graphe.dot")
            
        Returns:
            str: Le contenu du graphe au format DOT
        """
        # Début du graphe GraphViz
        contenuGraphe = "digraph Film{\n"
        contenuGraphe += f"    label=\"{self.nomFilm}\";\n"
        contenuGraphe += "    node [shape=box, style=filled, fillcolor=lightblue];\n"
        
        # Ensemble pour éviter les doublons
        transitionsAjoutees = set()
        
        # Parcourir toutes les scènes du film
        for scene in self.scenesDuFilm:
            # Vérifier si la scène a des conditions
            if hasattr(scene, 'conditions') and scene.conditions:
                # Générer les transitions pour chaque condition
                for condition in scene.conditions:
                    transitions = condition.genererTransitions(scene)
                    for transition in transitions:
                        # Créer une clé unique pour éviter les doublons
                        cleTransition = (transition.depart, transition.arrivee, transition.nomCondition)
                        if cleTransition not in transitionsAjoutees:
                            contenuGraphe += "    " + transition.to_graphviz() + "\n"
                            transitionsAjoutees.add(cleTransition)
        
        # Fin du graphe
        contenuGraphe += "}\n"
        
        # Écrire dans le fichier
        with open(nomFichier, 'w', encoding='utf-8') as f:
            f.write(contenuGraphe)
        
        return contenuGraphe
        
        
        