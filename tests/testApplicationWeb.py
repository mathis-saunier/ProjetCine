"""
Tests de la couche web : service de films (sans HTTP) et routes FastAPI.

Lancement depuis la racine du dépôt : python3 -m unittest discover -s tests -p 'test*.py'
"""

import json
import os
import sys
import tempfile
import unittest

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RACINE, "src"))

from jsonPackage import creerScenesDepuisDonnees
from webPackage.serviceFilm import (
    FilmIntrouvableException,
    FilmNonModifiableException,
    IdentifiantFilmInvalideException,
    TropDeScriptsException,
    chargerDocumentFilm,
    creerFilmVide,
    enregistrerDocumentFilm,
    genererScriptsEtGraphe,
    listerFilms,
    validerIdentifiant,
)


class TestChargementEnMemoire(unittest.TestCase):
    """
    Tests portant sur creerScenesDepuisDonnees, utilisé par l'éditeur web.
    """

    def testLeDocumentDOrigineNEstPasMute(self):
        """
        Vérifie que l'ajout interne de conditions au constructeur ne pollue
        pas le JSON, dont le contrat sépare info et conditions.
        """
        document = {
            "scenes": [{
                "info": {"idScene": "1", "lieu": "", "personnages": [],
                         "interieurExterieur": "", "urlTexte": "bonjour",
                         "voies": [], "actes": [], "estDebut": True, "estFin": True},
                "conditions": [],
            }]
        }
        scenes = creerScenesDepuisDonnees(document, "memoire")
        self.assertEqual(len(scenes), 1)
        self.assertNotIn("conditions", document["scenes"][0]["info"])
        self.assertEqual(document["scenes"][0]["conditions"], [])


class TestServiceFilm(unittest.TestCase):
    """
    Tests portant sur l'accès aux films et la génération, hors HTTP.
    """

    def setUp(self):
        self.dossier = tempfile.TemporaryDirectory()
        self.addCleanup(self.dossier.cleanup)
        os.environ["PROJETCINE_DATA"] = self.dossier.name
        self.addCleanup(os.environ.pop, "PROJETCINE_DATA", None)

    def testIdentifiantDangereuxEstRefuse(self):
        """
        Vérifie qu'un identifiant contenant un séparateur de chemin est rejeté.
        """
        for identifiant in ("../secret", "a/b", "film.json", "", "éé"):
            with self.subTest(identifiant=identifiant):
                with self.assertRaises(IdentifiantFilmInvalideException):
                    validerIdentifiant(identifiant)

    def testIdentifiantSimpleEstAccepte(self):
        """
        Vérifie les identifiants autorisés pour un testeur.
        """
        self.assertEqual(validerIdentifiant("mon_Film-2"), "mon_Film-2")

    def testLesExemplesSontListesEtLisibles(self):
        """
        Vérifie que les deux films d'exemple apparaissent et se chargent.
        """
        identifiants = {film["idFilm"] for film in listerFilms()}
        self.assertIn("exampleAvecVoies", identifiants)
        self.assertFalse(next(f for f in listerFilms() if f["idFilm"] == "exampleAvecVoies")["estModifiable"])
        document = chargerDocumentFilm("exampleAvecVoies")
        self.assertEqual(len(document["scenes"]), 19)

    def testUnExempleNePeutPasEtreEcrase(self):
        """
        Vérifie qu'on ne peut pas enregistrer par-dessus un film d'exemple.
        """
        with self.assertRaises(FilmNonModifiableException):
            enregistrerDocumentFilm("exampleAvecVoies", {"scenes": []})

    def testCreerEtGenererUnFilmUtilisateur(self):
        """
        Vérifie le cycle création → enregistrement → génération d'un script.
        """
        creerFilmVide("court")
        enregistrerDocumentFilm("court", {
            "scenes": [{
                "info": {"idScene": "A", "lieu": "", "personnages": [],
                         "interieurExterieur": "", "urlTexte": "ouverture",
                         "voies": [], "actes": [], "estDebut": True, "estFin": True},
                "conditions": [],
            }]
        })
        resultat = genererScriptsEtGraphe("court", 2, graine=1)
        self.assertEqual(len(resultat["scripts"]), 2)
        self.assertIn("ouverture", resultat["scripts"][0]["texte"])
        self.assertTrue(any(n["id"] == "A" for n in resultat["grapheComplet"]["noeuds"]))

    def testTropDeScriptsEstRefuse(self):
        """
        Vérifie le plafond de génération, pour éviter une charge abusive en ligne.
        """
        with self.assertRaises(TropDeScriptsException):
            genererScriptsEtGraphe("exampleAvecVoies", 21)

    def testFilmAbsentLeveUneException(self):
        """
        Vérifie qu'un identifiant inconnu mais sûr est signalé comme introuvable.
        """
        with self.assertRaises(FilmIntrouvableException):
            chargerDocumentFilm("inconnu")

    def testGenerationSurLExempleProduitUnGrapheSansBoucleFantome(self):
        """
        Vérifie qu'une génération web sur l'exemple ne réécrit pas la boucle 19→19.
        """
        resultat = genererScriptsEtGraphe("exampleAvecVoies", 1, graine=42)
        self.assertIn("Début du script", resultat["scripts"][0]["texte"])
        self.assertFalse(any(
            a["depart"] == "19" and a["arrivee"] == "19"
            for a in resultat["grapheComplet"]["aretes"]
        ))
        self.assertTrue(resultat["scripts"][0]["grapheTirage"]["noeuds"][0]["surbrillance"])
        self.assertTrue(any(a["surbrillance"] for a in resultat["scripts"][0]["grapheSuperpose"]["aretes"]))


class TestRoutesWeb(unittest.TestCase):
    """
    Tests portant sur les pages FastAPI, via le client de test.
    """

    def setUp(self):
        self.dossier = tempfile.TemporaryDirectory()
        self.addCleanup(self.dossier.cleanup)
        os.environ["PROJETCINE_DATA"] = self.dossier.name
        self.addCleanup(os.environ.pop, "PROJETCINE_DATA", None)

        from fastapi.testclient import TestClient
        from webPackage.applicationWeb import creerApplication

        self.client = TestClient(creerApplication())

    def testAccueilListeLesExemples(self):
        """
        Vérifie que la page d'accueil affiche les films d'exemple.
        """
        reponse = self.client.get("/")
        self.assertEqual(reponse.status_code, 200)
        self.assertIn("exampleAvecVoies", reponse.text)

    def testGenerationAfficheUnScript(self):
        """
        Vérifie qu'un POST de génération sur l'exemple renvoie un script.
        """
        reponse = self.client.post(
            "/films/exampleAvecVoies/generer",
            data={"nombre": "1", "graine": "42"},
        )
        self.assertEqual(reponse.status_code, 200)
        self.assertIn("Début du script", reponse.text)
        self.assertIn("graphe", reponse.text)

    def testCheminArbitraireEstRefuse(self):
        """
        Vérifie qu'une tentative de lecture hors data/ est rejetée.
        """
        reponse = self.client.get("/films/..%2FexampleAvecVoies/editer")
        self.assertIn(reponse.status_code, (400, 404, 422))

    def testCreationPuisEditionDUnFilm(self):
        """
        Vérifie qu'on peut créer un film puis l'enregistrer via l'API JSON.
        """
        creation = self.client.post("/films", data={"idFilm": "webTest"}, follow_redirects=False)
        self.assertEqual(creation.status_code, 303)
        edition = self.client.get("/films/webTest/editer")
        self.assertEqual(edition.status_code, 200)
        enregistrement = self.client.put("/films/webTest", json={
            "scenes": [{
                "info": {"idScene": "1", "lieu": "", "personnages": [],
                         "interieurExterieur": "", "urlTexte": "hello",
                         "voies": [], "actes": [], "estDebut": True, "estFin": True},
                "conditions": [],
            }]
        })
        self.assertEqual(enregistrement.status_code, 200)
        self.assertTrue(os.path.isfile(os.path.join(self.dossier.name, "webTest.json")))
