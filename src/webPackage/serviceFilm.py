"""
Service de présentation : accès aux films JSON et génération de scripts.

Ce module ne contient aucun appel FastAPI. Il est utilisable par les routes
web et par les tests, sans serveur HTTP.
"""

import os
import random
import re

import filmPackage as fi
from jsonPackage import ChargementJSONException, creerScenesDepuisDonnees, creerScenesDepuisJSON

IDENTIFIANT_VALIDE = re.compile(r"^[A-Za-z0-9_-]+$")
NB_SCRIPTS_MAX = 20

SRC = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RACINE = os.path.dirname(SRC)

EXEMPLES = {
    "exampleAvecVoies": os.path.join(RACINE, "exampleAvecVoies.json"),
    "exampleSansVoies": os.path.join(RACINE, "exampleSansVoies.json"),
}


class IdentifiantFilmInvalideException(Exception):
    """
    Exception levée lorsqu'un identifiant de film n'est pas un nom sûr.

    Attributs:
        idFilm (str): L'identifiant refusé
    """

    def __init__(self, idFilm: str):
        """
        Constructeur de la classe IdentifiantFilmInvalideException.

        Args:
            idFilm (str): L'identifiant refusé
        """
        self.idFilm = idFilm
        super().__init__(
            f"Identifiant de film invalide : '{idFilm}'. "
            "Utilisez uniquement des lettres, chiffres, tirets et underscores."
        )


class FilmIntrouvableException(Exception):
    """
    Exception levée lorsqu'aucun film ne correspond à l'identifiant demandé.

    Attributs:
        idFilm (str): L'identifiant recherché
    """

    def __init__(self, idFilm: str):
        """
        Constructeur de la classe FilmIntrouvableException.

        Args:
            idFilm (str): L'identifiant recherché
        """
        self.idFilm = idFilm
        super().__init__(f"Aucun film nommé '{idFilm}' n'a été trouvé.")


class FilmNonModifiableException(Exception):
    """
    Exception levée lorsqu'on tente d'écrire un film d'exemple, en lecture seule.

    Attributs:
        idFilm (str): L'identifiant du film protégé
    """

    def __init__(self, idFilm: str):
        """
        Constructeur de la classe FilmNonModifiableException.

        Args:
            idFilm (str): L'identifiant du film protégé
        """
        self.idFilm = idFilm
        super().__init__(
            f"Le film '{idFilm}' est un exemple en lecture seule. "
            "Dupliquez-le pour l'éditer."
        )


class TropDeScriptsException(Exception):
    """
    Exception levée lorsqu'une génération demande trop de scripts d'un coup.

    Attributs:
        nombre (int): Le nombre demandé
    """

    def __init__(self, nombre: int):
        """
        Constructeur de la classe TropDeScriptsException.

        Args:
            nombre (int): Le nombre demandé
        """
        self.nombre = nombre
        super().__init__(
            f"Au plus {NB_SCRIPTS_MAX} scripts peuvent être générés à la fois "
            f"(reçu : {nombre})."
        )


def validerIdentifiant(idFilm: str) -> str:
    """
    Vérifie qu'un identifiant de film ne peut pas servir de chemin arbitraire.

    Args:
        idFilm (str): L'identifiant à contrôler

    Returns:
        str: L'identifiant validé

    Raises:
        IdentifiantFilmInvalideException: Si l'identifiant est vide ou contient un séparateur
    """
    if not idFilm or not IDENTIFIANT_VALIDE.fullmatch(idFilm):
        raise IdentifiantFilmInvalideException(idFilm)
    return idFilm


def repertoireData() -> str:
    """
    Retourne le dossier où sont stockés les films créés par les testeurs.

    Returns:
        str: Le chemin du dossier data
    """
    return os.environ.get("PROJETCINE_DATA", os.path.join(RACINE, "data"))


def cheminFilmUtilisateur(idFilm: str) -> str:
    """
    Construit le chemin d'un film enregistré dans data/.

    Args:
        idFilm (str): L'identifiant déjà validé

    Returns:
        str: Le chemin du fichier JSON
    """
    return os.path.join(repertoireData(), f"{idFilm}.json")


def estUnExemple(idFilm: str) -> bool:
    """
    Indique si l'identifiant désigne un film d'exemple livré avec le dépôt.

    Args:
        idFilm (str): L'identifiant du film

    Returns:
        bool: True si le film est un exemple en lecture seule
    """
    return idFilm in EXEMPLES


def listerFilms() -> list[dict]:
    """
    Liste les films disponibles : exemples du dépôt, puis films de data/.

    Returns:
        list[dict]: Des dictionnaires {idFilm, titre, estModifiable}
    """
    films = [
        {"idFilm": identifiant, "titre": identifiant, "estModifiable": False}
        for identifiant in EXEMPLES
        if os.path.isfile(EXEMPLES[identifiant])
    ]
    dossier = repertoireData()
    if os.path.isdir(dossier):
        for nomFichier in sorted(os.listdir(dossier)):
            if not nomFichier.endswith(".json"):
                continue
            identifiant = nomFichier[:-5]
            if not IDENTIFIANT_VALIDE.fullmatch(identifiant):
                continue
            films.append({"idFilm": identifiant, "titre": identifiant, "estModifiable": True})
    return films


def cheminLecture(idFilm: str) -> str:
    """
    Résout l'identifiant vers un fichier existant.

    Args:
        idFilm (str): L'identifiant du film

    Returns:
        str: Le chemin du fichier JSON

    Raises:
        IdentifiantFilmInvalideException: Si l'identifiant est dangereux
        FilmIntrouvableException: Si aucun fichier ne correspond
    """
    validerIdentifiant(idFilm)
    if estUnExemple(idFilm):
        chemin = EXEMPLES[idFilm]
        if os.path.isfile(chemin):
            return chemin
        raise FilmIntrouvableException(idFilm)
    chemin = cheminFilmUtilisateur(idFilm)
    if os.path.isfile(chemin):
        return chemin
    raise FilmIntrouvableException(idFilm)


def chargerDocumentFilm(idFilm: str) -> dict:
    """
    Charge le document JSON d'un film, sans instancier les scènes.

    Args:
        idFilm (str): L'identifiant du film

    Returns:
        dict: Le document {"scenes": [...]}

    Raises:
        ChargementJSONException: Si le fichier n'est pas un JSON valide
        FilmIntrouvableException: Si le film n'existe pas
        IdentifiantFilmInvalideException: Si l'identifiant est invalide
    """
    return _lireDocument(cheminLecture(idFilm))


def _lireDocument(chemin: str) -> dict:
    """
    Lit un fichier JSON de film.

    Args:
        chemin (str): Le chemin du fichier

    Returns:
        dict: Le document chargé

    Raises:
        ChargementJSONException: Si le fichier est illisible ou mal formé
    """
    import json

    try:
        with open(chemin, "r", encoding="utf-8") as fichier:
            data = json.load(fichier)
    except FileNotFoundError as e:
        raise ChargementJSONException(chemin, "le fichier n'a pas été trouvé") from e
    except json.JSONDecodeError as e:
        raise ChargementJSONException(chemin, "le fichier n'est pas un JSON valide") from e
    if not isinstance(data, dict):
        raise ChargementJSONException(chemin, "le document doit être un objet JSON")
    return data


def enregistrerDocumentFilm(idFilm: str, document: dict) -> None:
    """
    Enregistre un document JSON dans data/. Les exemples ne sont pas écrasés.

    Args:
        idFilm (str): L'identifiant du film à écrire
        document (dict): Le document {"scenes": [...]}

    Raises:
        IdentifiantFilmInvalideException: Si l'identifiant est invalide
        FilmNonModifiableException: Si l'identifiant est celui d'un exemple
        ChargementJSONException: Si le document ne peut pas produire de scènes
    """
    import json

    validerIdentifiant(idFilm)
    if estUnExemple(idFilm):
        raise FilmNonModifiableException(idFilm)
    if not isinstance(document, dict):
        raise ChargementJSONException(idFilm, "le document doit être un objet JSON")
    # Valide le contrat avant d'écrire, pour ne pas stocker un film ingénérable
    # pour une raison de format (un film sans début reste enregistrable).
    creerScenesDepuisDonnees(document, idFilm)
    os.makedirs(repertoireData(), exist_ok=True)
    with open(cheminFilmUtilisateur(idFilm), "w", encoding="utf-8") as fichier:
        json.dump(document, fichier, indent=4, ensure_ascii=False)
        fichier.write("\n")


def dupliquerFilm(idFilmSource: str, idFilmCible: str) -> None:
    """
    Copie un film existant vers un nouvel identifiant modifiable dans data/.

    Args:
        idFilmSource (str): L'identifiant du film à copier
        idFilmCible (str): L'identifiant du nouveau film

    Raises:
        IdentifiantFilmInvalideException: Si un identifiant est invalide
        FilmIntrouvableException: Si la source n'existe pas
        FilmNonModifiableException: Si la cible est un exemple
        ChargementJSONException: Si un film existe déjà sous cet identifiant
    """
    validerIdentifiant(idFilmCible)
    if estUnExemple(idFilmCible) or os.path.isfile(cheminFilmUtilisateur(idFilmCible)):
        raise ChargementJSONException(idFilmCible, "un film porte déjà cet identifiant")
    enregistrerDocumentFilm(idFilmCible, chargerDocumentFilm(idFilmSource))


def creerFilmVide(idFilm: str) -> None:
    """
    Crée un film sans scènes dans data/.

    Args:
        idFilm (str): L'identifiant du nouveau film

    Raises:
        IdentifiantFilmInvalideException: Si l'identifiant est invalide
        FilmNonModifiableException: Si l'identifiant est celui d'un exemple
        ChargementJSONException: Si un film existe déjà sous cet identifiant
    """
    validerIdentifiant(idFilm)
    if estUnExemple(idFilm) or os.path.isfile(cheminFilmUtilisateur(idFilm)):
        raise ChargementJSONException(idFilm, "un film porte déjà cet identifiant")
    enregistrerDocumentFilm(idFilm, {"scenes": []})


def genererScriptsEtGraphe(idFilm: str, nombre: int, graine: int | None = None) -> dict:
    """
    Génère des scripts et le graphe DOT d'un film, sans écrire de fichier à la racine.

    Args:
        idFilm (str): L'identifiant du film
        nombre (int): Le nombre de scripts à tirer
        graine (int | None): Graine optionnelle pour rejouer une génération

    Returns:
        dict: {scripts: list[dict], grapheComplet: str} chaque script contient
            texte, identifiants, grapheTirage et grapheSuperpose

    Raises:
        TropDeScriptsException: Si nombre est hors limites
        FilmIntrouvableException: Si le film n'existe pas
        ChargementJSONException: Si le JSON est invalide
        fi.AucuneSceneDeDebutException: Si aucune scène de début n'est déclarée
        fi.ZeroSceneRestanteException: Si le récit s'interrompt hors d'une fin
    """
    if not isinstance(nombre, int) or nombre < 1 or nombre > NB_SCRIPTS_MAX:
        raise TropDeScriptsException(nombre)

    chemin = cheminLecture(idFilm)
    film = fi.Film(idFilm, "A")
    film.chargerScenes(creerScenesDepuisJSON(chemin))

    if graine is not None:
        random.seed(graine)

    scripts = []
    for _ in range(nombre):
        film.creerScript()
        identifiants = [s.idScene for s in film.scenesDuScript]
        scripts.append({
            "texte": film.obtenirScript(),
            "identifiants": identifiants,
            "grapheTirage": film.donneesGrapheTirage(identifiants),
            "grapheSuperpose": film.donneesGrapheSuperpose(identifiants),
        })

    return {
        "scripts": scripts,
        "grapheComplet": film.donneesGrapheComplet(),
    }
