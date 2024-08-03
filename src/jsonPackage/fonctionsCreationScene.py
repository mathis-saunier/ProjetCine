import json

def lire_scenes(fichier_json):
    try:
        with open(fichier_json, 'r', encoding='utf-8') as file:
            data = json.load(file)
            
            scenes = data.get("scenes", [])
            
            if not isinstance(scenes, list):
                raise ValueError("Le contenu de 'scenes' doit être une liste.")
            
            for scene in scenes:
                if not isinstance(scene, dict):
                    raise ValueError(f"Chaque scène doit être un objet JSON. Erreur à la scène {index}.")
                
                print(f"Scene:")
                info = scene.get('info', {})
                
                if not isinstance(info, dict):
                    raise ValueError(f"Le bloc 'info' doit être un objet JSON. Erreur à la scène {index}.")
                
                print("  Info:")
                for key, value in info.items():
                    if isinstance(value, list):
                        print(f"    {key}: {', '.join(value)}")
                    else:
                        print(f"    {key}: {value}")
                
                conditions = scene.get('conditions', [])
                
                if not isinstance(conditions, list):
                    raise ValueError(f"Le bloc 'conditions' doit être une liste. Erreur à la scène {index}.")
                
                if conditions:
                    print("  Conditions:")
                    for condition in conditions:
                        if not isinstance(condition, dict):
                            raise ValueError(f"Chaque condition doit être un objet JSON. Erreur à la scène {index}.")
                        for key, value in condition.items():
                            if isinstance(value, list):
                                print(f"    {key}: {', '.join(value)}")
                            else:
                                print(f"    {key}: {value}")
                else:
                    print("  No conditions")
                print("\n")
                
    except FileNotFoundError:
        print(f"Le fichier {fichier_json} n'a pas été trouvé.")
    except json.JSONDecodeError:
        print(f"Le fichier {fichier_json} n'est pas un JSON valide.")
    except ValueError as ve:
        print(f"Erreur de format: {ve}")
    except Exception as e:
        print(f"Une erreur est survenue: {e}")

# Exemple d'utilisation
lire_scenes('toto.json')
