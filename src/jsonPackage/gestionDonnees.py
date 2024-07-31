""" Ce fichier a pour but de rassembler les fonctions qui serviront
au realisateur pour enregistrer les scenes qu'il veut mettre dans le programme """

import json

# Pour initier une scene on a besoin de ceci : idScene, lieu, personnages, interieurExterieur, urlTexte, voies, actes, conditions
# Le tout sera stocke dans un format JSON

import tkinter as tk
from tkinter import ttk

class SceneFormApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Formulaire de Scène")

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="ID Scene").grid(row=0, column=0, sticky=tk.W)
        self.id_scene_entry = tk.Entry(self.root)
        self.id_scene_entry.grid(row=0, column=1, sticky=tk.W)

        tk.Label(self.root, text="Lieu").grid(row=1, column=0, sticky=tk.W)
        self.lieu_entry = tk.Entry(self.root)
        self.lieu_entry.grid(row=1, column=1, sticky=tk.W)

        tk.Label(self.root, text="Intérieur/Extérieur").grid(row=2, column=0, sticky=tk.W)
        self.int_ext_entry = tk.Entry(self.root)
        self.int_ext_entry.grid(row=2, column=1, sticky=tk.W)

        tk.Label(self.root, text="URL Texte").grid(row=3, column=0, sticky=tk.W)
        self.url_texte_entry = tk.Entry(self.root)
        self.url_texte_entry.grid(row=3, column=1, sticky=tk.W)

        # Section pour les personnages
        tk.Label(self.root, text="Personnages").grid(row=4, column=0, sticky=tk.W)
        self.personnages_frame = tk.Frame(self.root)
        self.personnages_frame.grid(row=4, column=1, sticky=tk.W)
        self.add_personnage_button = tk.Button(self.personnages_frame, text="Ajouter Personnage", command=self.add_personnage)
        self.add_personnage_button.grid(row=0, column=0, sticky=tk.W)
        self.personnage_entries = []

        # Section pour les voies
        tk.Label(self.root, text="Voies").grid(row=5, column=0, sticky=tk.W)
        self.voies_frame = tk.Frame(self.root)
        self.voies_frame.grid(row=5, column=1, sticky=tk.W)
        self.add_voie_button = tk.Button(self.voies_frame, text="Ajouter Voie", command=self.add_voie)
        self.add_voie_button.grid(row=0, column=0, sticky=tk.W)
        self.voie_entries = []

        # Section pour les actes
        tk.Label(self.root, text="Actes").grid(row=6, column=0, sticky=tk.W)
        self.actes_frame = tk.Frame(self.root)
        self.actes_frame.grid(row=6, column=1, sticky=tk.W)
        self.add_acte_button = tk.Button(self.actes_frame, text="Ajouter Acte", command=self.add_acte)
        self.add_acte_button.grid(row=0, column=0, sticky=tk.W)
        self.acte_entries = []

        # Section pour les conditions
        tk.Label(self.root, text="Conditions").grid(row=7, column=0, sticky=tk.W)
        self.conditions_frame = tk.Frame(self.root)
        self.conditions_frame.grid(row=7, column=1, sticky=tk.W)
        self.add_condition_button = tk.Button(self.conditions_frame, text="Ajouter condition", command=self.add_condition)
        self.add_condition_button.grid(row=0, column=0, sticky=tk.W)
        self.condition_entries = []

        # Bouton de soumission
        self.submit_button = tk.Button(self.root, text="Soumettre", command=self.submit)
        self.submit_button.grid(row=8, column=1, sticky=tk.W)

    def add_personnage(self):
        frame = tk.Frame(self.personnages_frame)
        frame.grid(row=len(self.personnage_entries) + 1, column=0, sticky=tk.W)
        entry = tk.Entry(frame)
        entry.grid(row=0, column=0, sticky=tk.W)
        delete_button = tk.Button(frame, text="Supprimer", command=lambda: self.remove_entry(frame, self.personnage_entries))
        delete_button.grid(row=0, column=1, sticky=tk.W)
        self.personnage_entries.append(frame)

    def add_voie(self):
        frame = tk.Frame(self.voies_frame)
        frame.grid(row=len(self.voie_entries) + 1, column=0, sticky=tk.W)
        entry = tk.Entry(frame)
        entry.grid(row=0, column=0, sticky=tk.W)
        delete_button = tk.Button(frame, text="Supprimer", command=lambda: self.remove_entry(frame, self.voie_entries))
        delete_button.grid(row=0, column=1, sticky=tk.W)
        self.voie_entries.append(frame)

    def add_acte(self):
        frame = tk.Frame(self.actes_frame)
        frame.grid(row=len(self.acte_entries) + 1, column=0, sticky=tk.W)
        entry = tk.Entry(frame)
        entry.grid(row=0, column=0, sticky=tk.W)
        delete_button = tk.Button(frame, text="Supprimer", command=lambda: self.remove_entry(frame, self.acte_entries))
        delete_button.grid(row=0, column=1, sticky=tk.W)
        self.acte_entries.append(frame)

    def add_condition(self):
        condition_frame = tk.Frame(self.conditions_frame)
        condition_frame.grid(row=len(self.condition_entries) + 1, column=0, sticky=tk.W)
        
        condition_var = tk.StringVar()
        condition_menu = ttk.Combobox(condition_frame, textvariable=condition_var)
        condition_menu['values'] = ('conditionSceneSuivante', 'conditionAutre')
        condition_menu.grid(row=0, column=0, sticky=tk.W)
        condition_menu.bind('<<ComboboxSelected>>', lambda event, frame=condition_frame, var=condition_var: self.add_condition_fields(frame, var))
        
        delete_button = tk.Button(condition_frame, text="Supprimer", command=lambda: self.remove_entry(condition_frame, self.condition_entries))
        delete_button.grid(row=0, column=1, sticky=tk.W)
        
        self.condition_entries.append(condition_frame)

    def add_condition_fields(self, frame, var):
        if var.get() == 'conditionSceneSuivante':
            add_id_scene_button = tk.Button(frame, text="Ajouter idScene", command=lambda: self.add_id_scene(frame))
            add_id_scene_button.grid(row=1, column=0, sticky=tk.W)
        elif var.get() == 'conditionAutre':
            other_entry = tk.Entry(frame)
            other_entry.grid(row=1, column=0, sticky=tk.W)

    def add_id_scene(self, frame):
        id_scene_frame = tk.Frame(frame)
        id_scene_frame.grid(row=len(frame.winfo_children()), column=0, sticky=tk.W)
        id_scene_entry = tk.Entry(id_scene_frame)
        id_scene_entry.grid(row=0, column=0, sticky=tk.W)
        delete_button = tk.Button(id_scene_frame, text="Supprimer", command=lambda: self.remove_entry(id_scene_frame, frame.winfo_children()))
        delete_button.grid(row=0, column=1, sticky=tk.W)

    def remove_entry(self, frame, entries_list):
        frame.destroy()
        entries_list.remove(frame)

    def submit(self):
        data = {
            "idScene": self.id_scene_entry.get(),
            "lieu": self.lieu_entry.get(),
            "interieurExterieur": self.int_ext_entry.get(),
            "urlTexte": self.url_texte_entry.get(),
            "personnages": [entry.winfo_children()[0].get() for entry in self.personnage_entries],
            "voies": [entry.winfo_children()[0].get() for entry in self.voie_entries],
            "actes": [entry.winfo_children()[0].get() for entry in self.acte_entries],
            "conditions": self.get_conditions()
        }
        print(data)  # Vous pouvez changer ceci pour sauvegarder les données ailleurs

    def get_conditions(self):
        conditions = []
        for frame in self.condition_entries:
            widgets = frame.winfo_children()
            condition_type = widgets[0].get()
            if condition_type == 'conditionSceneSuivante':
                ids = [widget.winfo_children()[0].get() for widget in widgets[1:] if isinstance(widget, tk.Frame)]
                conditions.append({"type": condition_type, "ids": ids})
            elif condition_type == 'conditionAutre':
                other_text = widgets[1].get()
                conditions.append({"type": condition_type, "other": other_text})
        return conditions

if __name__ == "__main__":
    root = tk.Tk()
    app = SceneFormApp(root)
    root.mainloop()
