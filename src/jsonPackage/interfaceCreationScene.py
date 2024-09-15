import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk
import json
import os

class MovieManager:
    def __init__(self, master):
        self.master = master
        self.master.title("Movie Manager")
        self.master.geometry("300x150")

        self.filename_label = tk.Label(master, text="Enter file name:")
        self.filename_label.pack(pady=5)

        self.filename_entry = tk.Entry(master, width=30)
        self.filename_entry.pack(pady=5)

        self.button_frame = tk.Frame(master)
        self.button_frame.pack(pady=10)

        self.new_movie_button = tk.Button(self.button_frame, text="New movie", command=self.new_movie)
        self.new_movie_button.pack(side=tk.LEFT, padx=5)

        self.resume_edit_button = tk.Button(self.button_frame, text="Resume the edit", command=self.resume_edit)
        self.resume_edit_button.pack(side=tk.RIGHT, padx=5)

    def new_movie(self):
        filename = self.filename_entry.get()
        if not filename.endswith('.json'):
            filename += '.json'
        
        if os.path.exists(filename):
            messagebox.showerror("Error", f"The file '{filename}' already exists.")
        else:
            self.open_data_window(filename, is_new=True)

    def resume_edit(self):
        filename = self.filename_entry.get()
        if not filename.endswith('.json'):
            filename += '.json'
        
        if not os.path.exists(filename):
            messagebox.showerror("Error", f"The file '{filename}' does not exist.")
        else:
            self.open_data_window(filename, is_new=False)

    def open_data_window(self, filename, is_new):
        self.master.withdraw()  # Hide the main window
        self.data_window = tk.Toplevel(self.master)
        self.data_window.title("Enter Movie Data")
        self.data_window.geometry("600x800")

        self.filename = filename
        self.is_new = is_new
        self.scenes = []
        self.current_scene = {}

        self.create_widgets()

        if not is_new:
            self.load_existing_data()
        else:
            self.clear_fields()  # Ensure fields are clear for a new movie

    def create_widgets(self):
        main_frame = tk.Frame(self.data_window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.canvas = tk.Canvas(main_frame)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.canvas.bind('<Configure>', self.update_scrollregion)

        self.inner_frame = tk.Frame(self.canvas)
        self.canvas_window = self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")

        labels = ["idScene", "lieu", "interieurExterieur", "urlTexte"]
        self.entries = {}

        for label in labels:
            tk.Label(self.inner_frame, text=label).pack(pady=5)
            self.entries[label] = tk.Entry(self.inner_frame, width=50)
            self.entries[label].pack(pady=5)

        self.create_section("personnages")
        self.create_section("voies")
        self.create_section("actes")
        self.create_conditions_section()

        button_frame = tk.Frame(self.inner_frame)
        button_frame.pack(pady=10, fill=tk.X)

        self.next_scene_button = tk.Button(button_frame, text="Next Scene", command=self.next_scene)
        self.next_scene_button.pack(side=tk.LEFT, padx=5)

        self.save_movie_button = tk.Button(button_frame, text="Save Movie", command=self.save_movie)
        self.save_movie_button.pack(side=tk.LEFT, padx=5)

    def create_section(self, section_name):
        section_frame = tk.Frame(self.inner_frame)
        section_frame.pack(pady=10, fill=tk.X)
        
        tk.Label(section_frame, text=section_name.capitalize()).pack(pady=5)
        
        add_button = tk.Button(section_frame, text=f"Add {section_name}", 
                               command=lambda: self.add_entry(section_frame, section_name))
        add_button.pack(pady=5)
        
        setattr(self, f"{section_name}_frame", section_frame)
        setattr(self, f"{section_name}_entries", [])

    def update_scrollregion(self, event=None):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def add_entry(self, parent_frame, section_name):
        entry_frame = tk.Frame(parent_frame)
        entry_frame.pack(fill=tk.X, pady=2)
        
        entry = tk.Entry(entry_frame, width=40)
        entry.pack(side=tk.LEFT, padx=(0, 5))
        
        delete_button = tk.Button(entry_frame, text="Delete", 
                                  command=lambda f=entry_frame: self.delete_entry(f, section_name))
        delete_button.pack(side=tk.LEFT)
        
        getattr(self, f"{section_name}_entries").insert(0, entry)
        
        # Move the new entry frame to the top of the section
        entry_frame.pack_forget()
        entry_frame.pack(in_=parent_frame, after=parent_frame.winfo_children()[1], fill=tk.X, pady=2)

        self.update_scrollregion()

    def delete_entry(self, entry_frame, section_name):
        entries = getattr(self, f"{section_name}_entries")
        entry = entry_frame.winfo_children()[0]
        entries.remove(entry)
        entry_frame.destroy()
        self.update_scrollregion()

    def create_conditions_section(self):
        self.conditions_frame = tk.Frame(self.inner_frame)
        self.conditions_frame.pack(pady=10, fill=tk.X)
        
        tk.Label(self.conditions_frame, text="Conditions").pack(pady=5)
        
        self.add_condition_button = tk.Button(self.conditions_frame, text="Add a condition", command=self.add_condition)
        self.add_condition_button.pack(pady=5)

        self.condition_frames = []

    def add_condition(self):
        condition_frame = tk.Frame(self.conditions_frame)
        condition_frame.pack(fill=tk.X, pady=5)

        condition_var = tk.StringVar()
        condition_dropdown = ttk.Combobox(condition_frame, textvariable=condition_var, 
                                          values=["conditionSceneSuivante"])
        condition_dropdown.pack(side=tk.LEFT, padx=5)
        condition_dropdown.set("Select Condition")

        delete_condition_button = tk.Button(condition_frame, text="Delete Condition", 
                                            command=lambda: self.delete_condition(condition_frame))
        delete_condition_button.pack(side=tk.LEFT, padx=5)

        idscene_button_frame = tk.Frame(condition_frame)
        idscene_button_frame.pack(fill=tk.X, pady=2)

        add_idscene_button = tk.Button(idscene_button_frame, text="Add IdScene", 
                                       command=lambda: self.add_idscene(condition_frame))
        
        def on_condition_select(event):
            if condition_var.get() == "conditionSceneSuivante":
                add_idscene_button.pack(side=tk.LEFT, padx=5)
            else:
                add_idscene_button.pack_forget()

        condition_dropdown.bind("<<ComboboxSelected>>", on_condition_select)

        self.condition_frames.append((condition_frame, condition_var, [], idscene_button_frame))
        
        condition_frame.pack_forget()
        condition_frame.pack(in_=self.conditions_frame, side=tk.BOTTOM, fill=tk.X, pady=5)

        self.update_scrollregion()

    def add_idscene(self, parent_frame):
        for condition_frame, _, idscene_entries, idscene_button_frame in self.condition_frames:
            if condition_frame == parent_frame:
                idscene_frame = tk.Frame(parent_frame)
                idscene_frame.pack(fill=tk.X, pady=2)
                
                entry = tk.Entry(idscene_frame, width=40)
                entry.pack(side=tk.LEFT, padx=(0, 5))
                
                delete_button = tk.Button(idscene_frame, text="Delete", 
                                          command=lambda f=idscene_frame, p=parent_frame: self.delete_idscene(f, p))
                delete_button.pack(side=tk.LEFT)
                
                idscene_entries.append(entry)
                
                # Move the new IdScene entry just below the "Add IdScene" button
                idscene_frame.pack_forget()
                idscene_frame.pack(in_=parent_frame, after=idscene_button_frame, fill=tk.X, pady=2)
                
                self.update_scrollregion()
                break

    def delete_idscene(self, idscene_frame, parent_frame):
        for condition_frame, _, idscene_entries, _ in self.condition_frames:
            if condition_frame == parent_frame:
                entry = idscene_frame.winfo_children()[0]
                idscene_entries.remove(entry)
                break
        idscene_frame.destroy()
        self.update_scrollregion()

    def delete_condition(self, condition_frame):
        self.condition_frames = [cf for cf in self.condition_frames if cf[0] != condition_frame]
        condition_frame.destroy()
        self.update_scrollregion()

    def save_current_scene(self):
        scene_data = {
            "info": {
                label: self.entries[label].get() for label in self.entries
            },
            "conditions": []
        }
        
        scene_data["info"].update({
            "personnages": [entry.get() for entry in self.personnages_entries],
            "voies": [entry.get() for entry in self.voies_entries],
            "actes": [entry.get() for entry in self.actes_entries]
        })

        for _, condition_var, idscene_entries, _ in self.condition_frames:
            if condition_var.get() != "Select Condition":
                condition = {
                    "type": condition_var.get(),
                    "idScenesSuivantesPossibles": [entry.get() for entry in idscene_entries]
                }
                scene_data["conditions"].append(condition)

        return scene_data

    def next_scene(self):
        self.scenes.append(self.save_current_scene())
        self.clear_fields()

    def clear_fields(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)
        
        for section in ["personnages", "voies", "actes"]:
            section_frame = getattr(self, f"{section}_frame")
            for child in section_frame.winfo_children()[2:]:  # Skip label and add button
                child.destroy()
            setattr(self, f"{section}_entries", [])
        
        for condition_frame, _, _, _ in self.condition_frames:
            condition_frame.destroy()
        self.condition_frames.clear()

    def save_movie(self):
        current_scene = self.save_current_scene()
        if any(current_scene["info"].values()) or current_scene["conditions"]:
            self.scenes.append(current_scene)
        
        movie_data = {"scenes": self.scenes}
        
        with open(self.filename, 'w') as f:
            json.dump(movie_data, f, indent=4)
        
        messagebox.showinfo("Success", f"Movie data saved to {self.filename}")
        self.data_window.destroy()
        self.master.destroy()

    def load_existing_data(self):
        with open(self.filename, 'r') as f:
            movie_data = json.load(f)
        
        self.scenes = movie_data.get("scenes", [])
        
        # Start with empty fields for a new scene
        self.clear_fields()

def lancerInterfaceGraphique():
    root = tk.Tk()
    app = MovieManager(root)
    root.mainloop()

if __name__ == "__main__":
    lancerInterfaceGraphique()
