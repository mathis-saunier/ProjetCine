from scenePackage import scene as sc

def initialisationScene(numScene):
    idScene = numScene
    # Donnees description
    lieu = "lieu"+str(numScene)
    personnages = ["homme"+str(numScene), "femme"+str(numScene)]
    interieurExterieur = ((numScene %2) == 0)
    # Donnees contenu
    urlTexte = "urlTexteScene"+str(numScene)
    # Donnees narration
    if ((numScene %2) == 0):
        voies = ["A"]
        actes = [1]
    else:
        voies = ["B"]
        actes = [2]
        
    return sc.Scene(numScene, lieu, personnages, interieurExterieur, urlTexte, voies, actes)

scene0 = initialisationScene(0)
scene1 = initialisationScene(1)
print(scene0)
print(scene1)