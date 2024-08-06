# A faire : lire le cours sur les exceptions et faire ça proprement
# On faire ajouter du typage de variable dans les déclarations : https://docs.python.org/fr/3.10/library/typing.html
from copy import deepcopy

import scenePackage as sc
import planPackage as pl
import filmPackage as fi
import conditionPackage as co
import jsonPackage as js

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

def testConditionSceneSuivante():
    conditionSS = co.ConditionSceneSuivante([0, 1])
    sDansFilm = sc.SceneAvecCondition(42, "", [], True, "", [], [],
                                      [co.ConditionSceneSuivante([0,1])])
    s0 = sc.SceneAvecCondition(0, "", [], True, "", [], [],[])
    s1 = sc.SceneAvecCondition(1, "", [], True, "", [], [],[])
    s2 = sc.SceneAvecCondition(2, "", [], True, "", [], [],[])
    film = fi.Film("FilmTest")
    film.ajouterScene(sDansFilm)
    print("Résultat attendu : SUCCES :")
    print(s0.verifierToutesConditions(film))
    print("Résultat attendu : SUCCES :")
    print(s1.verifierToutesConditions(film))
    print("Résultat attendu : ECHEC :")
    print(s2.verifierToutesConditions(film))

js.creerScenesDepuisJSON('toto.json')