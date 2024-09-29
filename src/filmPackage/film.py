from copy import deepcopy
import random as rd

from scenePackage.scene import Scene
from conditionPackage.condition import Condition
from conditionPackage.valeurCondition import ValeurCondition
import jsonPackage as js

class SceneInexistanteException(Exception):
    def __init__(self, id):
        self.id = id
        super().__init__(f"Erreur, la scènes d'id {id} n'existe pas")

class ZeroSceneRestanteException(Exception):
    def __init__(self, acte, voie):
        self.acte = acte
        self.voie = voie
        super().__init__(f"Erreur, il n'y a pas de scènes restantes dans l'acte {acte} pour la voie {voie}")
        
class Film():
    nomFilm = None
    scenesDuFilm = []
    scenesDuScript = []
    voieInitiale = None
    voieActuelle = None
    acteActuel = None
    
    # Ajouter le choix de la voieInitiale dans le __init__
    def __init__(self, nomFilm, voieInitiale):
        self.nomFilm = nomFilm
        self.voieInitiale = voieInitiale
        self.voieActuelle = voieInitiale
        self.acteActuel = "1"
    
    def ajouterScene(self, scene):
        self.scenesDuScript.append(scene)
    
    # Ne prendre pas en compte l'acte ou la voie actuel.le
    def recupererScenesPossibles(self, acteActuel, voieActuelle):
        scenesExistantes = deepcopy(self.scenesDuFilm)
        return scenesExistantes
        
    def recupererConditions(self):
        res = []
        for s in self.scenesDuScript:
            for c in s.conditions:
                res.append(c)
        return res
    
    def tirerUneScene(self):
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
        self.scenesDuFilm = js.creerScenesDepuisJSON(fichier_json)

    # nombre de tour est une variable temporaire. Il y a mieux à faire comme fonctionnement
    def creerScript(self, choixPremiereScene=None):
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
        script = "Début du script\n"
        for s in self.scenesDuScript:
            script += s.idScene + " : " + s.urlTexte + "\n"
        return script
    

    def sceneDejaExistante(self, idScene):
        for scene in self.scenesDuFilm:
            if (idScene == scene.idScene):
                return True
        return False
    
    def obtenirSceneParId(self, id):
        for s in self.scenesDuFilm:
            if (s.idScene == id):
                return s
        # Si l'on a pas trouvé de scene on lève une exception
        raise SceneInexistanteException(id)
        
        
        
        