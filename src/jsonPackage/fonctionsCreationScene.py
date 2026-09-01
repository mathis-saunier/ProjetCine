import json

from scenePackage import SceneAvecCondition
from conditionPackage import Condition, ConditionSceneSuivante


class ChargementJSONException(Exception):
    """
    Exception levée lorsqu'un fichier JSON de film ne peut pas être chargé.

    Attributs:
        fichierJson (str): Le nom du fichier JSON à l'origine de l'erreur
    """

    def __init__(self, fichierJson: str, message: str):
        """
        Constructeur de la classe ChargementJSONException.

        Args:
            fichierJson (str): Le nom du fichier JSON à l'origine de l'erreur
            message (str): La description de l'erreur rencontrée
        """
        self.fichierJson = fichierJson
        super().__init__(f"Erreur lors du chargement de {fichierJson} : {message}")


def creerConditionsDepuisJSON(conditions: list[dict]) -> list[Condition]:
    """
    Fonction permettant de créer les objets Condition correspondant au bloc 'conditions' d'une scène.

    Args:
        conditions (list[dict]): La liste des conditions décrites dans le JSON

    Returns:
        list[Condition]: La liste des conditions créées (vide si la scène n'a aucune condition)

    Raises:
        ValueError: Si une condition n'est pas un objet JSON ou si son type est inconnu
    """
    listeConditions = []
    for condition in conditions:
        if not isinstance(condition, dict):
            raise ValueError("Chaque condition doit être un objet JSON.")

        match condition["type"]:
            case "conditionSceneSuivante":
                listeConditions.append(ConditionSceneSuivante(condition["idScenesSuivantesPossibles"]))
            case _:
                raise ValueError(f"La condition '{condition['type']}' est inconnue.")
    return listeConditions


def creerScenesDepuisJSON(fichier_json: str) -> list[SceneAvecCondition]:
    """
    Fonction permettant de créer les scènes d'un film à partir d'un fichier JSON.

    Args:
        fichier_json (str): Le nom du fichier JSON décrivant le film (ex: "film.json")

    Returns:
        list[SceneAvecCondition]: La liste des scènes créées à partir du fichier

    Raises:
        ChargementJSONException: Si le fichier est introuvable, mal formé ou si son contenu ne respecte pas le format attendu
    """
    try:
        with open(fichier_json, 'r', encoding='utf-8') as file:
            data = json.load(file)
    except FileNotFoundError as e:
        raise ChargementJSONException(fichier_json, "le fichier n'a pas été trouvé") from e
    except json.JSONDecodeError as e:
        raise ChargementJSONException(fichier_json, "le fichier n'est pas un JSON valide") from e

    try:
        scenes = data.get("scenes", [])
        if not isinstance(scenes, list):
            raise ValueError("Le contenu de 'scenes' doit être une liste.")

        # On cree une liste qui stockera les scenes crees pour les retourner
        scenesCreesDepuisJSON = []
        for scene in scenes:
            if not isinstance(scene, dict):
                raise ValueError("Chaque scène doit être un objet JSON.")

            info = scene.get('info', {})
            if not isinstance(info, dict):
                raise ValueError("Le bloc 'info' doit être un objet JSON.")

            conditions = scene.get('conditions', [])
            if not isinstance(conditions, list):
                raise ValueError("Le bloc 'conditions' doit être une liste.")

            # On pourra utiliser **info pour créer une Scene, il manque juste les conditions
            # dont on s'occupe maintenant. La liste est propre à cette scène : la réutiliser
            # d'une scène à l'autre ferait hériter une scène sans condition de celles de la précédente.
            info.update({"conditions": creerConditionsDepuisJSON(conditions)})
            # On cree la scene et on l'ajoute a notre liste qui sera retournee
            scenesCreesDepuisJSON.append(SceneAvecCondition.depuisDonneesBrutes(**info))

        return scenesCreesDepuisJSON

    except (ValueError, KeyError, TypeError) as e:
        raise ChargementJSONException(fichier_json, f"format invalide ({e})") from e
