import json
from scenePackage import SceneAvecCondition
from conditionPackage import ConditionSceneSuivante

def creerScenesDepuisJSON(fichier_json):
    try:
        with open(fichier_json, 'r', encoding='utf-8') as file:
            data = json.load(file)
            
            scenes = data.get("scenes", [])
            if not isinstance(scenes, list):
                raise ValueError("Le contenu de 'scenes' doit être une liste.")
            
            # On cree une liste qui stockera les scenes crees pour les retourner
            scenesCreesDepuisJSON = []
            for scene in scenes:
                if not isinstance(scene, dict):
                    raise ValueError(f"Chaque scène doit être un objet JSON.")
                
                info = scene.get('info', {})
                if not isinstance(info, dict):
                    raise ValueError(f"Le bloc 'info' doit être un objet JSON.")
                
                # On pourra utiliser **info pour créer une Scene, il manque juste les conditions
                # dont on s'occupe maintenant
                
                conditions = scene.get('conditions', [])
                if not isinstance(conditions, list):
                    raise ValueError(f"Le bloc 'conditions' doit être une liste.")
                
                if conditions: # Si l'on a récupéré des conditions
                    # Alors il faut créer les objets Conditions correspondants et les mettre dans une liste pour ensuite créer la Scene
                    listeConditions = []
                    for condition in conditions:
                        if not isinstance(condition, dict):
                            raise ValueError(f"Chaque condition doit être un objet JSON.")
                        
                        match condition["type"]:
                            case "conditionSceneSuivante":
                                listeConditions.append(ConditionSceneSuivante(condition["idScenesSuivantesPossibles"]))
                            case _:
                                raise ValueError(f"Cette condition est inconnue")
                    # On a parcouru et créer toutes les conditions. On peut les ajouter aux infos pour créer une scène
                
                info.update({"conditions": listeConditions})
                # On cree la scene et on l'ajoute a notre liste qui sera retourner
                scenesCreesDepuisJSON.append(SceneAvecCondition(**info))
                
            return scenesCreesDepuisJSON
        
    except FileNotFoundError:
        print(f"Le fichier {fichier_json} n'a pas été trouvé.")
    except json.JSONDecodeError:
        print(f"Le fichier {fichier_json} n'est pas un JSON valide.")
    except ValueError as ve:
        print(f"Erreur de format: {ve}")
    except Exception as e:
        print(f"Une erreur est survenue: {e}")

# Exemple d'utilisation
# creerScenesDepuisJSON('toto.json')
