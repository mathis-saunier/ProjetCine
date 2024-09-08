# A faire : lire le cours sur les exceptions et faire ça proprement
# On faire ajouter du typage de variable dans les déclarations : https://docs.python.org/fr/3.10/library/typing.html
from copy import deepcopy
import tkinter as tk
from tkinter import simpledialog, messagebox

import scenePackage as sc
import planPackage as pl
import filmPackage as fi
import conditionPackage as co
import jsonPackage as js

# def initialisationScene(numScene):
#     idScene = numScene
#     # Donnees description
#     lieu = "lieu"+str(numScene)
#     personnages = ["homme"+str(numScene), "femme"+str(numScene)]
#     interieurExterieur = ((numScene %2) == 0)
#     # Donnees contenu
#     urlTexte = "urlTexteScene"+str(numScene)
#     # Donnees narration
#     if ((numScene %2) == 0):
#         voies = ["A"]
#         actes = [1]
#     else:
#         voies = ["B"]
#         actes = [2]
        
#     return sc.Scene(numScene, lieu, personnages, interieurExterieur, urlTexte, voies, actes)

# def testSecondConstructeur():
#     scene = initialisationScene(0)
#     dd = sc.DonneesDescription("lieu0", ["homme0", "femme0"] , True)
#     dc = sc.DonneesContenu("urlTexteScene0")
#     dn = sc.DonneesNarration(["A"], [1])
#     sceneBis = sc.Scene.constructeurParDonnees(0, dd, dc ,dn)
#     return (str(scene) == str(sceneBis))

# def testConditionSceneSuivante():
#     conditionSS = co.ConditionSceneSuivante([0, 1])
#     sDansFilm = sc.SceneAvecCondition(42, "", [], True, "", [], [],
#                                       [co.ConditionSceneSuivante([0,1])])
#     s0 = sc.SceneAvecCondition(0, "", [], True, "", [], [],[])
#     s1 = sc.SceneAvecCondition(1, "", [], True, "", [], [],[])
#     s2 = sc.SceneAvecCondition(2, "", [], True, "", [], [],[])
#     film = fi.Film("FilmTest")
#     film.ajouterScene(sDansFilm)
#     print("Résultat attendu : SUCCES :")
#     print(s0.verifierToutesConditions(film))
#     print("Résultat attendu : SUCCES :")
#     print(s1.verifierToutesConditions(film))
#     print("Résultat attendu : ECHEC :")
#     print(s2.verifierToutesConditions(film))

# js.creerScenesDepuisJSON('toto.json')
# print(sc.Scene.scenesExistantes)



        
def bouton_action(selection):
    if selection == 1:
        # Code pour le bouton 1 (if)
        js.lancerInterfaceGraphique()
        root.destroy()
    else:
        # Code pour le bouton 2 (else)
        ouvrir_fenetre_nombre_et_texte()


def ouvrir_fenetre_nombre_et_texte():
    # Nouvelle fenêtre pour demander un texte
    texte = simpledialog.askstring("Entrée du texte", "Entrez un texte:")
    
    if texte is not None:  # Si un texte est entré
        # Nouvelle fenêtre pour demander un nombre entier
        nombre = simpledialog.askinteger("Entrée du nombre", "Entrez un nombre entier:")
        
        if nombre is not None:  # Si un texte est entré
            with open("scripts.txt", "w") as fichier:
                test = fi.Film("filmToto", 'A')
                for loop in range(nombre):
                    test.creerFilmDepuisJSON(texte, "PF1")
                    fichier.write(test.obtenirScript()+"\n\n")
        else:
            print("Aucun nombre n'a été entré.")
    else:
        print("Aucun texte n'a été entré.")
    
    root.destroy()

# Création de la fenêtre principale
root = tk.Tk()
root.title("Menu avec 2 boutons")
root.geometry("300x200")

# Texte explicatif du bouton 1
texte1 = tk.Label(root, text="Pour lancer l'interface graphique qui permet d'enregistrer les caractéristiques des scènes d'un film (nouveau film ou film à compléter)")
texte1.pack()

# Bouton 1
bouton1 = tk.Button(root, text="Création de scènes", command=lambda: bouton_action(1))
bouton1.pack()

# Texte explicatif du bouton 2
texte2 = tk.Label(root, text="Pour lancer la création de plusieurs scripts à partir d'un fichier 'film.json'")
texte2.pack()

# Bouton 2
bouton2 = tk.Button(root, text="Création de script", command=lambda: bouton_action(2))
bouton2.pack()

# Lancement de la boucle principale
root.mainloop()
