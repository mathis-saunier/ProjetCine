from copy import deepcopy
import random as rd

from scenePackage.scene import Scene
from conditionPackage.condition import Condition
from conditionPackage.valeurCondition import ValeurCondition

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
        self.acteActuel = 1
    
    def ajouterScene(self, scene):
        self.scenes.append(scene)
    
    def tirerUneScene(self):
        scenesPossibles = self.recupererScenesPossibles(self.acteActuel, self.voieActuelle)
        # On retire egalement les scenes qui sont deja dans le film
        for s in scenesPossibles:
            if s in self.scenes:
                scenesPossibles.remove(s)
        # Faire une erreur en bonne et due forme
        if (len(scenesPossibles) == 0):
            return f"Erreur, il n'y a pas de scènes restantes dans l'acte {self.acteActuel} pour la voie {self.voieActuelle}"
        else:
            while len(scenesPossibles) != 0:
                # Faire une erreur en bonne et due forme et TROUVER UNE MEILLEURE MANIERE DE FAIRE CE CODE
                if (len(scenesPossibles) == 0):
                    return "Erreur, il n'y a aucune scene qui respecte toutes les conditions"
                choix = rd.randrange(0, len(scenesPossibles))
                sceneChoisie = scenesPossibles[choix]
                # Maintenant que l'on a une scene possible, on vérifie qu'elle respecte les conditions
                if (sceneChoisie.verifierToutesLesConditions(self) == ValeurCondition.SUCCES):
                    return sceneChoisie
                else:
                    scenesPossibles.remove(sceneChoisie)    
        
    def recupererScenesPossibles(self, acteActuel, voieActuelle):
        scenesExistantes = deepcopy(Scene.scenesExistantes)
        for s in scenesExistantes:
            if ((acteActuel not in s.actes) or (voieActuelle not in s.voies)):
                scenesExistantes.remove(s)
        return scenesExistantes
        
    def recupererConditions(self):
        res = []
        for s in self.scenes:
            for c in s.conditions:
                res.append(c)
        return res
        
        
        