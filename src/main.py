# A faire : lire le cours sur les exceptions et faire ça proprement
# On faire ajouter du typage de variable dans les déclarations : https://docs.python.org/fr/3.10/library/typing.html

import scenePackage as sc
import planPackage as pl
import filmPackage as fi
import conditionPackage as co

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

def testSecondConstructeur():
    scene = initialisationScene(0)
    dd = sc.DonneesDescription("lieu0", ["homme0", "femme0"] , True)
    dc = sc.DonneesContenu("urlTexteScene0")
    dn = sc.DonneesNarration(["A"], [1])
    sceneBis = sc.Scene.constructeurParDonnees(0, dd, dc ,dn)
    return (str(scene) == str(sceneBis))

scene0 = initialisationScene(0)
# print(repr(scene0))
scene0Bis = sc.SceneAvecCondition(1, 'lieu0', ['homme0', 'femme0'], True, 'urlTexteScene0', ['A'], [1], [])
print(repr(scene0Bis))


