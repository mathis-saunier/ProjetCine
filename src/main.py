# A faire : lire le cours sur les exceptions et faire ça proprement
# On faire ajouter du typage de variable dans les déclarations : https://docs.python.org/fr/3.10/library/typing.html
from copy import deepcopy
import tkinter as tk
from tkinter import simpledialog

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

class MainApplication:
    def __init__(self, master):
        self.master = master
        self.master.title("Movie Management System")
        self.master.geometry("400x250")

        self.create_widgets()

        # Set up the window close event
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_widgets(self):
        tk.Label(self.master, text="Choose an action:", font=("Arial", 14)).pack(pady=10)

        tk.Button(self.master, text="Create/Edit Movie Scenes", command=self.launch_movie_manager).pack(pady=5)
        tk.Button(self.master, text="Generate Scripts", command=self.generate_scripts).pack(pady=5)

    def launch_movie_manager(self):
        self.master.withdraw()  # Hide the main window
        movie_manager_window = tk.Toplevel(self.master)
        movie_manager = js.MovieManager(movie_manager_window)
        movie_manager_window.protocol("WM_DELETE_WINDOW", lambda: self.on_movie_manager_close(movie_manager_window))

    def on_movie_manager_close(self, window):
        window.destroy()
        self.on_closing()  # Close the entire application

    def generate_scripts(self):
        texte = simpledialog.askstring("Input Text", "Enter the JSON filename:")
        if texte:
            nombre = simpledialog.askinteger("Input Number", "Enter the number of scripts to generate:")
            if nombre:
                self.create_scripts(texte, nombre)
            else:
                print("No number was entered.")
        else:
            print("No text was entered.")

    def create_scripts(self, json_filename, num_scripts):
        with open("scripts.txt", "w") as fichier:
            test = fi.Film("filmToto", 'A')
            for _ in range(num_scripts):
                test.creerFilmDepuisJSON(json_filename, "1")
                fichier.write(test.obtenirScript() + "\n\n")
        print(f"{num_scripts} scripts have been generated and saved in 'scripts.txt'.")

    def on_closing(self):
        self.master.quit()  # Stop the mainloop
        self.master.destroy()  # Destroy the window

def main():
    root = tk.Tk()
    app = MainApplication(root)
    root.mainloop()

if __name__ == "__main__":
    main()