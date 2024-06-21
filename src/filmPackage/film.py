from scenePackage.scene import Scene
from scenePackage.condition import Condition

class Film():
    nomFilm = None
    scenes = []
    voieInitiale = None
    voieActuelle = None
    acteActuel = None
    
    # Ajouter le choix de la voieInitiale dans le __init__
    def __init__(self, nomFilm):
        self.nomFilm = nomFilm
    
    def ajouterScene(self, scene):
        self.scenes.append(scene)
    
    def tirageScene(self):
        scenesPossibles = self.recupererScenesPossibles(self.acteActuel, self.voieActuelle)
        sceneTrouvee = False
        while not sceneTrouvee:
            choix = rd.randrange(0, len(scenesExistantes))
            Condition.verifierConditions()
            
        
    def recupererScenesPossibles(acteActuel, voieActuelle):
        scenesExistantes = copy(Scene.scenesExistantes)
        for s in scenesExistantes:
            if ((acteActuel not in s.actes) or (voieActuelle not in s.voies)):
                scenesExistantes.remove(s)
        return scenesExistantes
        
        
        
        
        