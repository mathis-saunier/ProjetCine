import sys
import os

# Ajoute le répertoire parent au sys.path pour permettre l'importation juste en dessous (mrc GPT4o)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scenePackage.scene import Scene

class Film():
    nomFilm = None
    scenes = []
    
    def __init__(self, nomFilm):
        self.nomFilm = nomFilm
    
    def ajouterScene(scene):
        self.scenes.append(scene)
    
    def tirageScene():
        scenesExistantes = copy(Scene.scenesExistantes)
        