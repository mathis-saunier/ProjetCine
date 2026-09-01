"""
Tests de non-régression sur la base du projet : chargement JSON, intégrité des
conditions et cohérence narrative des scripts générés.

Lancement depuis la racine du dépôt : python3 -m unittest discover -s tests -p 'test*.py'
"""

import os
import sys
import unittest

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RACINE, "src"))

import filmPackage as fi
from conditionPackage import ConditionSceneSuivante
from jsonPackage import ChargementJSONException, creerScenesDepuisJSON

EXEMPLE_AVEC_VOIES = os.path.join(RACINE, "exampleAvecVoies.json")
EXEMPLE_SANS_VOIES = os.path.join(RACINE, "exampleSansVoies.json")


class TestChargementJSON(unittest.TestCase):
    """
    Tests portant sur la création des scènes à partir d'un fichier JSON.
    """

    def testLesDeuxExemplesSeChargent(self):
        """
        Vérifie que les deux fichiers d'exemple du dépôt produisent bien 19 scènes.
        """
        for fichier in (EXEMPLE_AVEC_VOIES, EXEMPLE_SANS_VOIES):
            with self.subTest(fichier=fichier):
                self.assertEqual(len(creerScenesDepuisJSON(fichier)), 19)

    def testSceneSansConditionNHeritePasDeLaPrecedente(self):
        """
        Vérifie qu'une scène dont le bloc 'conditions' est vide dans le JSON n'a
        aucune condition en mémoire. La scène 19 est la fin du récit : lui attribuer
        les conditions de la scène 18 créait une transition fantôme 19 -> 19.
        """
        scenes = creerScenesDepuisJSON(EXEMPLE_AVEC_VOIES)
        sceneFinale = next(s for s in scenes if s.idScene == "19")
        self.assertEqual(sceneFinale.conditions, [])

    def testChaqueSceneAUneListeDeConditionsDistincte(self):
        """
        Vérifie qu'aucune liste de conditions n'est partagée entre deux scènes.
        """
        scenes = creerScenesDepuisJSON(EXEMPLE_AVEC_VOIES)
        identifiants = [id(s.conditions) for s in scenes]
        self.assertEqual(len(identifiants), len(set(identifiants)))

    def testFichierIntrouvableLeveUneException(self):
        """
        Vérifie qu'un fichier absent lève une exception au lieu de renvoyer None.
        """
        with self.assertRaises(ChargementJSONException):
            creerScenesDepuisJSON(os.path.join(RACINE, "fichierQuiNExistePas.json"))

    def testConditionInconnueLeveUneException(self):
        """
        Vérifie qu'un type de condition non géré lève une exception explicite.
        """
        import json
        import tempfile

        contenu = {"scenes": [{"info": {"idScene": "1", "lieu": "", "personnages": [],
                                        "interieurExterieur": "", "urlTexte": "",
                                        "voies": [], "actes": []},
                               "conditions": [{"type": "conditionInventee"}]}]}
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as f:
            json.dump(contenu, f)
            chemin = f.name
        try:
            with self.assertRaises(ChargementJSONException):
                creerScenesDepuisJSON(chemin)
        finally:
            os.remove(chemin)


class TestRepresentationScene(unittest.TestCase):
    """
    Tests portant sur la représentation textuelle des scènes.
    """

    def testReprNeLevePasDException(self):
        """
        Vérifie que l'affichage d'une scène avec conditions ne lève plus d'AttributeError.
        """
        scenes = creerScenesDepuisJSON(EXEMPLE_AVEC_VOIES)
        self.assertIn("SceneAvecCondition", repr(scenes[0]))
        self.assertIsInstance(repr(scenes), str)


class TestGenerationScript(unittest.TestCase):
    """
    Tests portant sur la génération aléatoire de scripts.
    """

    def setUp(self):
        self.film = fi.Film("filmDeTest", "A")
        self.film.creerFilmDepuisJSON(EXEMPLE_AVEC_VOIES)

    def testScriptRespecteLesConditionsEtNaPasDeDoublon(self):
        """
        Vérifie sur 50 tirages que chaque enchaînement est autorisé par les conditions
        de la scène précédente et qu'aucune scène n'apparaît deux fois.
        """
        for _ in range(50):
            script = self.film.creerScript(choixPremiereScene="1")
            identifiants = [s.idScene for s in script]
            self.assertEqual(len(identifiants), len(set(identifiants)),
                             f"Scène en double dans le script {identifiants}")
            for scenePrecedente, sceneSuivante in zip(script, script[1:]):
                suivantesAutorisees = [idScene
                                       for c in scenePrecedente.conditions
                                       if isinstance(c, ConditionSceneSuivante)
                                       for idScene in c.idScenesSuivantesPossibles]
                if suivantesAutorisees:
                    self.assertIn(sceneSuivante.idScene, suivantesAutorisees,
                                  f"Enchaînement interdit dans le script {identifiants}")

    def testGrapheNeContientPasDeTransitionFantome(self):
        """
        Vérifie que le graphe exporté ne contient pas de boucle sur la scène finale.
        """
        import tempfile

        with tempfile.TemporaryDirectory() as dossier:
            graphe = self.film.genererGraphe(os.path.join(dossier, "graphe.dot"))
        self.assertNotIn('"19" -> "19"', graphe)


class TestSeparationMetierInterface(unittest.TestCase):
    """
    Tests portant sur l'indépendance du métier vis-à-vis de l'interface graphique.
    """

    def testLeMetierNImportePasTkinter(self):
        """
        Vérifie que charger le métier ne tire pas Tkinter, afin que le projet reste
        utilisable et testable sans interface graphique installée.
        """
        self.assertNotIn("tkinter", sys.modules)


if __name__ == "__main__":
    unittest.main()
