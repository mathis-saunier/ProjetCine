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

def testSecondConstructeur():
    scene = initialisationScene(0)
    dd = sc.DonneesDescription("lieu0", ["homme0", "femme0"] , True)
    dc = sc.DonneesContenu("urlTexteScene0")
    dn = sc.DonneesNarration(["A"], [1])
    sceneBis = sc.Scene.constructeurParDonnees(0, dd, dc ,dn)
    print(str(scene))
    print(str(sceneBis))
    return (str(scene) == str(sceneBis))

print(testSecondConstructeur())