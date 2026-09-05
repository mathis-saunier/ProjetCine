"""
Application FastAPI : couche de présentation web de ProjetCine.
"""

from pathlib import Path

from fastapi import FastAPI, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from jsonPackage import ChargementJSONException
import filmPackage as fi

from .serviceFilm import (
    FilmIntrouvableException,
    FilmNonModifiableException,
    IdentifiantFilmInvalideException,
    TropDeScriptsException,
    chargerDocumentFilm,
    creerFilmVide,
    dupliquerFilm,
    enregistrerDocumentFilm,
    estUnExemple,
    genererScriptsEtGraphe,
    listerFilms,
    validerIdentifiant,
)

REPERTOIRE_PACKAGE = Path(__file__).resolve().parent


def creerApplication() -> FastAPI:
    """
    Construit l'application FastAPI, avec les pages HTML et les routes JSON.

    Returns:
        FastAPI: L'application prête à être servie par Uvicorn
    """
    application = FastAPI(title="ProjetCine", docs_url=None, redoc_url=None)
    gabarits = Jinja2Templates(directory=str(REPERTOIRE_PACKAGE / "templates"))
    application.mount(
        "/static",
        StaticFiles(directory=str(REPERTOIRE_PACKAGE / "static")),
        name="static",
    )

    def rendre(requete: Request, nomGabarit: str, contexte: dict | None = None) -> HTMLResponse:
        """
        Rend un gabarit Jinja avec le contexte de la requête.

        Args:
            requete (Request): La requête HTTP en cours
            nomGabarit (str): Le nom du fichier de gabarit
            contexte (dict | None): Les variables supplémentaires du gabarit

        Returns:
            HTMLResponse: La page HTML
        """
        donnees = contexte or {}
        return gabarits.TemplateResponse(requete, nomGabarit, donnees)

    @application.get("/", response_class=HTMLResponse)
    def accueil(requete: Request) -> HTMLResponse:
        """
        Affiche la liste des films et le formulaire de création.

        Args:
            requete (Request): La requête HTTP

        Returns:
            HTMLResponse: La page d'accueil
        """
        return rendre(requete, "accueil.html", {"films": listerFilms()})

    @application.post("/films")
    def creerFilm(idFilm: str = Form(...)) -> RedirectResponse:
        """
        Crée un film vide dans data/ et redirige vers l'éditeur.

        Args:
            idFilm (str): L'identifiant saisi dans le formulaire

        Returns:
            RedirectResponse: Redirection vers l'éditeur du nouveau film
        """
        try:
            creerFilmVide(idFilm.strip())
        except (IdentifiantFilmInvalideException, ChargementJSONException) as erreur:
            raise HTTPException(status_code=400, detail=str(erreur)) from erreur
        return RedirectResponse(url=f"/films/{idFilm.strip()}/editer", status_code=303)

    @application.post("/films/{idFilm}/dupliquer")
    def dupliquer(idFilm: str, idFilmCible: str = Form(...)) -> RedirectResponse:
        """
        Duplique un film (exemple ou utilisateur) vers un nouvel identifiant.

        Args:
            idFilm (str): L'identifiant du film source
            idFilmCible (str): L'identifiant du film créé

        Returns:
            RedirectResponse: Redirection vers l'éditeur de la copie
        """
        try:
            dupliquerFilm(idFilm, idFilmCible.strip())
        except (IdentifiantFilmInvalideException, FilmIntrouvableException,
                ChargementJSONException, FilmNonModifiableException) as erreur:
            statut = 404 if isinstance(erreur, FilmIntrouvableException) else 400
            raise HTTPException(status_code=statut, detail=str(erreur)) from erreur
        return RedirectResponse(url=f"/films/{idFilmCible.strip()}/editer", status_code=303)

    @application.get("/films/{idFilm}/editer", response_class=HTMLResponse)
    def editer(requete: Request, idFilm: str) -> HTMLResponse:
        """
        Affiche l'éditeur de scènes d'un film.

        Args:
            requete (Request): La requête HTTP
            idFilm (str): L'identifiant du film

        Returns:
            HTMLResponse: La page d'édition
        """
        try:
            validerIdentifiant(idFilm)
            document = chargerDocumentFilm(idFilm)
        except IdentifiantFilmInvalideException as erreur:
            raise HTTPException(status_code=400, detail=str(erreur)) from erreur
        except FilmIntrouvableException as erreur:
            raise HTTPException(status_code=404, detail=str(erreur)) from erreur
        except ChargementJSONException as erreur:
            raise HTTPException(status_code=400, detail=str(erreur)) from erreur
        return rendre(requete, "editeur.html", {
            "idFilm": idFilm,
            "document": document,
            "estModifiable": not estUnExemple(idFilm),
        })

    @application.put("/films/{idFilm}")
    def enregistrer(idFilm: str, document: dict) -> JSONResponse:
        """
        Enregistre le document JSON d'un film modifiable.

        Args:
            idFilm (str): L'identifiant du film
            document (dict): Le corps JSON {scenes: [...]}

        Returns:
            JSONResponse: Confirmation de l'enregistrement
        """
        try:
            enregistrerDocumentFilm(idFilm, document)
        except IdentifiantFilmInvalideException as erreur:
            raise HTTPException(status_code=400, detail=str(erreur)) from erreur
        except FilmNonModifiableException as erreur:
            raise HTTPException(status_code=403, detail=str(erreur)) from erreur
        except ChargementJSONException as erreur:
            raise HTTPException(status_code=400, detail=str(erreur)) from erreur
        return JSONResponse({"ok": True})

    @application.get("/films/{idFilm}/generer", response_class=HTMLResponse)
    def pageGeneration(requete: Request, idFilm: str) -> HTMLResponse:
        """
        Affiche le formulaire de génération de scripts.

        Args:
            requete (Request): La requête HTTP
            idFilm (str): L'identifiant du film

        Returns:
            HTMLResponse: La page de génération
        """
        try:
            validerIdentifiant(idFilm)
            chargerDocumentFilm(idFilm)
        except IdentifiantFilmInvalideException as erreur:
            raise HTTPException(status_code=400, detail=str(erreur)) from erreur
        except FilmIntrouvableException as erreur:
            raise HTTPException(status_code=404, detail=str(erreur)) from erreur
        return rendre(requete, "generation.html", {
            "idFilm": idFilm,
            "scripts": None,
            "grapheComplet": None,
            "erreur": None,
        })

    @application.post("/films/{idFilm}/generer", response_class=HTMLResponse)
    def lancerGeneration(
        requete: Request,
        idFilm: str,
        nombre: int = Form(1),
        graine: str = Form(""),
    ) -> HTMLResponse:
        """
        Génère des scripts et affiche le résultat, y compris le graphe.

        Args:
            requete (Request): La requête HTTP
            idFilm (str): L'identifiant du film
            nombre (int): Le nombre de scripts demandés
            graine (str): Graine optionnelle, chaîne vide si absente

        Returns:
            HTMLResponse: La page de résultat
        """
        erreur = None
        scripts = None
        grapheComplet = None
        try:
            graineEntiere = int(graine) if graine.strip() else None
            resultat = genererScriptsEtGraphe(idFilm, nombre, graineEntiere)
            scripts = resultat["scripts"]
            grapheComplet = resultat["grapheComplet"]
        except ValueError:
            erreur = "La graine doit être un entier."
        except (IdentifiantFilmInvalideException, TropDeScriptsException,
                ChargementJSONException, fi.AucuneSceneDeDebutException,
                fi.ZeroSceneRestanteException, fi.SceneInexistanteException) as exc:
            erreur = str(exc)
        except FilmIntrouvableException as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc
        return rendre(requete, "generation.html", {
            "idFilm": idFilm,
            "scripts": scripts,
            "grapheComplet": grapheComplet,
            "erreur": erreur,
            "nombre": nombre,
            "graine": graine,
        })

    return application


app = creerApplication()
