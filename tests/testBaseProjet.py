"""
Tests de non-régression sur la base du projet : chargement JSON, intégrité des
conditions et cohérence narrative des scripts générés.

Lancement depuis la racine du dépôt : python3 -m unittest discover -s tests -p 'test*.py'
"""

import json
import os
import random
import sys
import tempfile
import unittest

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RACINE, "src"))

import filmPackage as fi
from conditionPackage import ConditionSceneSuivante
from jsonPackage import ChargementJSONException, creerScenesDepuisJSON

EXEMPLE_AVEC_VOIES = os.path.join(RACINE, "exampleAvecVoies.json")
EXEMPLE_SANS_VOIES = os.path.join(RACINE, "exampleSansVoies.json")


def decrireScene(idScene, scenesSuivantes, estDebut=False, estFin=False):
    """
    Fonction utilitaire construisant la description JSON d'une scène de test.

    Args:
        idScene (str): L'identifiant de la scène
        scenesSuivantes (list[str]): Les identifiants des scènes pouvant lui succéder
        estDebut (bool): Indique si la scène peut ouvrir un script
        estFin (bool): Indique si la scène peut clore un script

    Returns:
        dict: La description de la scène au format attendu par creerScenesDepuisJSON
    """
    info = {"idScene": idScene, "lieu": "", "personnages": [], "interieurExterieur": "",
            "urlTexte": f"texte {idScene}", "voies": [], "actes": [],
            "estDebut": estDebut, "estFin": estFin}
    conditions = []
    if scenesSuivantes:
        conditions.append({"type": "conditionSceneSuivante",
                           "idScenesSuivantesPossibles": scenesSuivantes})
    return {"info": info, "conditions": conditions}


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

    def testGenerationReproductibleDepuisUneGraine(self):
        """
        Vérifie qu'une même graine aléatoire redonne les mêmes scripts, ce qui permet
        de rejouer une génération à l'identique.
        """
        def genererTroisScripts(graine):
            random.seed(graine)
            return [[s.idScene for s in self.film.creerScript()] for _ in range(3)]

        self.assertEqual(genererTroisScripts(42), genererTroisScripts(42))

    def testGrapheNeContientPasDeTransitionFantome(self):
        """
        Vérifie que le graphe exporté ne contient pas de boucle sur la scène finale.
        """
        import tempfile

        with tempfile.TemporaryDirectory() as dossier:
            graphe = self.film.genererGraphe(os.path.join(dossier, "graphe.dot"))
        self.assertNotIn('"19" -> "19"', graphe)


class TestFinDeRecit(unittest.TestCase):
    """
    Tests portant sur le début et la fin d'un script, déclarés par l'auteur via
    les marqueurs estDebut et estFin.
    """

    def setUp(self):
        self.dossier = tempfile.TemporaryDirectory()
        self.addCleanup(self.dossier.cleanup)

    def filmDepuisScenes(self, scenes, probabiliteArretSurFin=0.5):
        """
        Construit un film de test à partir de descriptions de scènes.

        Args:
            scenes (list[dict]): Les descriptions de scènes, construites avec decrireScene
            probabiliteArretSurFin (float): Probabilité de clore le script sur une scène de fin

        Returns:
            Film: Le film prêt à générer des scripts
        """
        chemin = os.path.join(self.dossier.name, f"film{len(os.listdir(self.dossier.name))}.json")
        with open(chemin, "w", encoding="utf-8") as fichier:
            json.dump({"scenes": scenes}, fichier)
        film = fi.Film("filmDeTest", "A", probabiliteArretSurFin)
        film.creerFilmDepuisJSON(chemin)
        return film

    def testLeScriptCommenceSurUnDebutEtFinitSurUneFin(self):
        """
        Vérifie que sans première scène imposée, le script part d'une scène de début
        et s'achève sur une scène de fin, ce qui échouait auparavant faute de savoir
        reconnaître la fin d'un récit.
        """
        film = fi.Film("filmDeTest", "A")
        film.creerFilmDepuisJSON(EXEMPLE_AVEC_VOIES)
        for _ in range(50):
            script = film.creerScript()
            self.assertTrue(script[0].narrationScene.estDebut)
            self.assertTrue(script[-1].narrationScene.estFin)

    def testUneFinAvecSuitesPeutCloreLeScript(self):
        """
        Vérifie qu'une scène de fin possédant encore des suites clôt le script
        lorsque le tirage désigne l'arrêt.
        """
        film = self.filmDepuisScenes(
            [decrireScene("A", ["B"], estDebut=True),
             decrireScene("B", ["C"], estFin=True),
             decrireScene("C", [], estFin=True)],
            probabiliteArretSurFin=1.0)
        self.assertEqual([s.idScene for s in film.creerScript()], ["A", "B"])

    def testUneFinAvecSuitesPeutPoursuivreLeScript(self):
        """
        Vérifie que la même scène de fin laisse le récit continuer lorsque le tirage
        désigne la poursuite : c'est ce qui produit des scripts de longueur variable.
        """
        film = self.filmDepuisScenes(
            [decrireScene("A", ["B"], estDebut=True),
             decrireScene("B", ["C"], estFin=True),
             decrireScene("C", [], estFin=True)],
            probabiliteArretSurFin=0.0)
        self.assertEqual([s.idScene for s in film.creerScript()], ["A", "B", "C"])

    def testFilmSansSceneDeDebutLeveUneException(self):
        """
        Vérifie qu'un film dont aucune scène n'ouvre le récit est signalé à l'auteur.
        """
        film = self.filmDepuisScenes([decrireScene("A", ["B"]), decrireScene("B", [], estFin=True)])
        with self.assertRaises(fi.AucuneSceneDeDebutException):
            film.creerScript()

    def testImpasseNonDeclareeCommeFinLeveUneException(self):
        """
        Vérifie qu'une scène sans suite et non déclarée comme fin est traitée comme
        une erreur de rédaction et non comme une fin implicite.
        """
        film = self.filmDepuisScenes([decrireScene("A", ["B"], estDebut=True), decrireScene("B", [])])
        with self.assertRaises(fi.ZeroSceneRestanteException):
            film.creerScript()

    def testLesMarqueursSontOptionnelsDansLeJSON(self):
        """
        Vérifie qu'un fichier JSON antérieur, dépourvu de estDebut et estFin,
        se charge toujours avec les valeurs par défaut.
        """
        chemin = os.path.join(self.dossier.name, "ancienFormat.json")
        ancienneScene = decrireScene("A", [])
        del ancienneScene["info"]["estDebut"]
        del ancienneScene["info"]["estFin"]
        with open(chemin, "w", encoding="utf-8") as fichier:
            json.dump({"scenes": [ancienneScene]}, fichier)

        scene = creerScenesDepuisJSON(chemin)[0]
        self.assertFalse(scene.narrationScene.estDebut)
        self.assertFalse(scene.narrationScene.estFin)

    def testUneSceneSansConditionNeMeneNullePart(self):
        """
        Vérifie que possedeDesScenesSuivantes distingue une scène qui désigne des
        suites d'une scène qui n'en désigne aucune.
        """
        scenes = creerScenesDepuisJSON(EXEMPLE_AVEC_VOIES)
        parId = {s.idScene: s for s in scenes}
        self.assertTrue(parId["1"].possedeDesScenesSuivantes())
        self.assertFalse(parId["19"].possedeDesScenesSuivantes())


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
