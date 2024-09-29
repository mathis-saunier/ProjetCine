from copy import deepcopy
import tkinter as tk
from tkinter import simpledialog

import scenePackage as sc
import planPackage as pl
import filmPackage as fi
import conditionPackage as co
import jsonPackage as js

with open("scriptsTest.txt", "w") as fichier:
            test = fi.Film("filmToto", 'A')
            for _ in range(1):
                test.creerFilmDepuisJSON("exampleSansVoies.json", choixPremiereScene="1")
                fichier.write(test.obtenirScript() + "\n\n")