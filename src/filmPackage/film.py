from copy import deepcopy
import random as rd

from scenePackage.scene import Scene
from conditionPackage.condition import Condition
from conditionPackage.valeurCondition import ValeurCondition
import jsonPackage as js

class ZeroSceneRestanteException(Exception):
    def __init__(self, acte, voie):
        self.acte = acte
        self.voie = voie
        super().__init__(f"Erreur, il n'y a pas de scènes restantes dans l'acte {acte} pour la voie {voie}")
        
class Film():
    nomFilm = None
    scenes = []
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
        self.scenes.append(scene)
    
    def recupererScenesPossibles(self, acteActuel, voieActuelle):
        scenesExistantes = deepcopy(Scene.scenesExistantes)
        for s in scenesExistantes:
            if (acteActuel not in s.actes):
                scenesExistantes.remove(s)
        return scenesExistantes
        
    def recupererConditions(self):
        res = []
        for s in self.scenes:
            for c in s.conditions:
                res.append(c)
        return res
    
    def tirerUneScene(self):
        scenesPossibles = self.recupererScenesPossibles(self.acteActuel, self.voieActuelle)
        # On retire egalement les scenes qui sont deja dans le film
        for s in scenesPossibles:
            if s in self.scenes:
                scenesPossibles.remove(s)
                
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
        
    def creerFilmDepuisJSON(self, fichier_json, choixPremiereScene=None):
        print("Creation scenes")
        js.creerScenesDepuisJSON(fichier_json)
        nbTour = 7
        if choixPremiereScene != None:
            print("On force la première scène")
            for s in Scene.scenesExistantes:
                if s.idScene == choixPremiereScene:
                    self.ajouterScene(s)
                    nbTour -= 1
                    print(s)
        print("Debut creation film")
        # Faire une vérif que l'attribut scenes est bien vide
        for loop in range(nbTour):
            print(loop)
            self.ajouterScene(self.tirerUneScene())
        return self.scenes
    
    def obtenirScript(self):
        script = "Début du script\n"
        for s in self.scenes:
            script += s.idScene + " : " + s.urlTexte + "\n"
        return script
        
        
        
        