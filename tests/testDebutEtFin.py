"""
Tests dédiés aux scènes de début, aux scènes de fin et aux scripts de
longueur variable.

Complète tests/testBaseProjet.py, qui ne fait qu'effleurer ces comportements
sur les fichiers d'exemple et sur une chaîne A -> B -> C.

Lancement depuis la racine du dépôt : python3 -m unittest discover -s tests -p 'test*.py'
"""

import json
import os
import sys
import tempfile
import unittest

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RACINE, "src"))

import filmPackage as fi
import filmPackage.film as moduleFilm
from jsonPackage import creerScenesDepuisJSON

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


class FilmDeTest(unittest.TestCase):
    """
    Classe de base qui construit un film à partir de descriptions de scènes.

    Attributs:
        dossier (tempfile.TemporaryDirectory): Répertoire temporaire des JSON de test
    """

    def setUp(self):
        self.dossier = tempfile.TemporaryDirectory()
        self.addCleanup(self.dossier.cleanup)

    def filmDepuisScenes(self, scenes, probabiliteArretSurFin=0.5, nomFilm="filmDeTest"):
        """
        Construit un film de test à partir de descriptions de scènes.

        Args:
            scenes (list[dict]): Les descriptions de scènes, construites avec decrireScene
            probabiliteArretSurFin (float): Probabilité de clore le script sur une scène de fin
            nomFilm (str): Le nom du film créé

        Returns:
            Film: Le film prêt à générer des scripts
        """
        chemin = os.path.join(self.dossier.name, f"film{len(os.listdir(self.dossier.name))}.json")
        with open(chemin, "w", encoding="utf-8") as fichier:
            json.dump({"scenes": scenes}, fichier)
        film = fi.Film(nomFilm, "A", probabiliteArretSurFin)
        film.creerFilmDepuisJSON(chemin)
        return film

    def identifiantsDuScript(self, film, choixPremiereScene=None):
        """
        Génère un script et en retourne la liste des identifiants.

        Args:
            film (Film): Le film à partir duquel générer le script
            choixPremiereScene (str): L'identifiant de la première scène, ou None

        Returns:
            list[str]: Les identifiants des scènes du script généré
        """
        return [s.idScene for s in film.creerScript(choixPremiereScene)]


class TestScenesDeDebut(FilmDeTest):
    """
    Tests portant sur le tirage de la première scène parmi celles marquées estDebut.
    """

    def testTirerUneSceneDeDebutNeRenvoieQueDesDebuts(self):
        """
        Vérifie que, même avec plusieurs scènes éligibles, tirerUneSceneDeDebut
        ne renvoie jamais une scène qui n'est pas un début.
        """
        film = self.filmDepuisScenes([
            decrireScene("A", ["X"], estDebut=True),
            decrireScene("B", ["X"]),
            decrireScene("C", ["X"], estDebut=True),
            decrireScene("X", [], estFin=True),
        ])
        for _ in range(40):
            scene = film.tirerUneSceneDeDebut()
            self.assertIn(scene.idScene, ("A", "C"))
            self.assertTrue(scene.narrationScene.estDebut)

    def testLeScriptPartToujoursDUneSceneDeDebut(self):
        """
        Vérifie que creerScript, sans première scène imposée, ouvre le récit
        sur l'une des scènes déclarées comme débuts, et jamais sur une autre.
        """
        film = self.filmDepuisScenes([
            decrireScene("ouvertureA", ["fin"], estDebut=True),
            decrireScene("ouvertureB", ["fin"], estDebut=True),
            decrireScene("milieu", ["fin"]),
            decrireScene("fin", [], estFin=True),
        ])
        debutsObserves = set()
        for _ in range(40):
            script = film.creerScript()
            self.assertTrue(script[0].narrationScene.estDebut)
            self.assertIn(script[0].idScene, ("ouvertureA", "ouvertureB"))
            debutsObserves.add(script[0].idScene)
        self.assertEqual(debutsObserves, {"ouvertureA", "ouvertureB"})

    def testUneScenePeutEtreALaFoisDebutEtFin(self):
        """
        Vérifie qu'une scène unique, à la fois début et fin, produit un script
        d'une seule scène.
        """
        film = self.filmDepuisScenes([decrireScene("seule", [], estDebut=True, estFin=True)])
        self.assertEqual(self.identifiantsDuScript(film), ["seule"])

    def testPremiereSceneImposeeCourtCircuiteLeTirageDesDebuts(self):
        """
        Vérifie que choixPremiereScene force l'ouverture, y compris sur une
        scène qui n'est pas déclarée comme début.
        """
        film = self.filmDepuisScenes([
            decrireScene("debut", ["milieu"], estDebut=True),
            decrireScene("milieu", ["fin"]),
            decrireScene("fin", [], estFin=True),
        ])
        self.assertEqual(self.identifiantsDuScript(film, choixPremiereScene="milieu"),
                         ["milieu", "fin"])

    def testPremiereSceneInconnueLeveUneException(self):
        """
        Vérifie qu'imposer l'identifiant d'une scène absente est signalé
        explicitement, au lieu de tomber plus loin sur une liste vide.
        """
        film = self.filmDepuisScenes([
            decrireScene("debut", ["fin"], estDebut=True),
            decrireScene("fin", [], estFin=True),
        ])
        with self.assertRaises(fi.SceneInexistanteException):
            film.creerScript(choixPremiereScene="absente")

    def testFilmSansSceneDeDebutLeveUneException(self):
        """
        Vérifie qu'un film dont aucune scène n'ouvre le récit est refusé.
        """
        film = self.filmDepuisScenes(
            [decrireScene("A", ["B"]), decrireScene("B", [], estFin=True)],
            nomFilm="sansDebut")
        with self.assertRaises(fi.AucuneSceneDeDebutException) as contexte:
            film.creerScript()
        self.assertIn("sansDebut", str(contexte.exception))

    def testLesDeuxExemplesDeclarentBienUnDebut(self):
        """
        Vérifie que les fichiers d'exemple du dépôt portent estDebut sur la scène 1.
        """
        for fichier in (EXEMPLE_AVEC_VOIES, EXEMPLE_SANS_VOIES):
            with self.subTest(fichier=os.path.basename(fichier)):
                scenes = creerScenesDepuisJSON(fichier)
                debuts = [s.idScene for s in scenes if s.narrationScene.estDebut]
                self.assertEqual(debuts, ["1"])


class TestScenesDeFin(FilmDeTest):
    """
    Tests portant sur l'arrêt du script sur une scène marquée estFin.
    """

    def testLeScriptSArreteSurUneSceneDeFin(self):
        """
        Vérifie que le script se termine toujours sur une scène déclarée comme fin,
        et jamais sur une scène intermédiaire.
        """
        film = self.filmDepuisScenes([
            decrireScene("debut", ["gauche", "droite"], estDebut=True),
            decrireScene("gauche", ["finGauche"]),
            decrireScene("droite", ["finDroite"]),
            decrireScene("finGauche", [], estFin=True),
            decrireScene("finDroite", [], estFin=True),
        ])
        finsObservees = set()
        for _ in range(40):
            script = film.creerScript()
            self.assertTrue(script[-1].narrationScene.estFin)
            self.assertIn(script[-1].idScene, ("finGauche", "finDroite"))
            finsObservees.add(script[-1].idScene)
        self.assertEqual(finsObservees, {"finGauche", "finDroite"})

    def testImpasseNonDeclareeCommeFinLeveUneException(self):
        """
        Vérifie qu'une scène sans suite et non marquée estFin n'est pas
        interprétée comme une fin implicite.
        """
        film = self.filmDepuisScenes([
            decrireScene("debut", ["impasse"], estDebut=True),
            decrireScene("impasse", []),
        ])
        with self.assertRaises(fi.ZeroSceneRestanteException):
            film.creerScript()

    def testUneSceneDeDebutSansSuiteNiFinLeveUneException(self):
        """
        Vérifie qu'une scène d'ouverture isolée, non déclarée comme fin,
        est une erreur de rédaction et non un script d'une scène.
        """
        film = self.filmDepuisScenes([decrireScene("orpheline", [], estDebut=True)])
        with self.assertRaises(fi.ZeroSceneRestanteException):
            film.creerScript()

    def testUneFinDontLesSuitesSontDejaJoueesClotLeScript(self):
        """
        Vérifie qu'une scène de fin qui pointe vers une scène déjà présente
        dans le script s'arrête normalement, au lieu de lever une exception.
        """
        film = self.filmDepuisScenes([
            decrireScene("debut", ["fin"], estDebut=True),
            decrireScene("fin", ["debut"], estFin=True),
        ], probabiliteArretSurFin=0.0)
        self.assertEqual(self.identifiantsDuScript(film), ["debut", "fin"])

    def testLesDeuxExemplesDeclarentBienUneFin(self):
        """
        Vérifie que les fichiers d'exemple du dépôt portent estFin sur la scène 19.
        """
        for fichier in (EXEMPLE_AVEC_VOIES, EXEMPLE_SANS_VOIES):
            with self.subTest(fichier=os.path.basename(fichier)):
                scenes = creerScenesDepuisJSON(fichier)
                fins = [s.idScene for s in scenes if s.narrationScene.estFin]
                self.assertEqual(fins, ["19"])


class TestLongueurVariable(FilmDeTest):
    """
    Tests portant sur les scripts de longueur variable : une scène de fin
    qui possède encore des suites peut clore ou poursuivre le récit.
    """

    CHAINETTE = [
        decrireScene("A", ["B"], estDebut=True),
        decrireScene("B", ["C"], estFin=True),
        decrireScene("C", ["D"]),
        decrireScene("D", [], estFin=True),
    ]

    def testArretForceDesLaPremiereFin(self):
        """
        Vérifie qu'avec probabiliteArretSurFin à 1, le script s'arrête dès
        la première scène de fin rencontrée, même si elle a encore des suites.
        """
        film = self.filmDepuisScenes(self.CHAINETTE, probabiliteArretSurFin=1.0)
        self.assertEqual(self.identifiantsDuScript(film), ["A", "B"])

    def testPoursuiteForceeJusquaLaDerniereFin(self):
        """
        Vérifie qu'avec probabiliteArretSurFin à 0, le récit ignore les fins
        intermédiaires et s'arrête seulement quand plus aucune suite n'existe.
        """
        film = self.filmDepuisScenes(self.CHAINETTE, probabiliteArretSurFin=0.0)
        self.assertEqual(self.identifiantsDuScript(film), ["A", "B", "C", "D"])

    def testUneSceneQuiNestPasUneFinNePeutPasCloreLeScript(self):
        """
        Vérifie qu'une scène intermédiaire, même si le tirage voudrait s'arrêter,
        ne clôt jamais le récit : seule une scène estFin en a le droit.
        """
        film = self.filmDepuisScenes([
            decrireScene("A", ["B"], estDebut=True),
            decrireScene("B", ["C"]),
            decrireScene("C", [], estFin=True),
        ], probabiliteArretSurFin=1.0)
        self.assertEqual(self.identifiantsDuScript(film), ["A", "B", "C"])

    def testUneSceneDebutEtFinAvecSuitesPeutProduireDeuxLongueurs(self):
        """
        Vérifie qu'une scène à la fois début et fin, qui possède encore une suite,
        donne soit un script d'une scène, soit le récit complet, selon la
        probabilité d'arrêt.
        """
        scenes = [
            decrireScene("prologue", ["epilogue"], estDebut=True, estFin=True),
            decrireScene("epilogue", [], estFin=True),
        ]
        court = self.filmDepuisScenes(scenes, probabiliteArretSurFin=1.0)
        long = self.filmDepuisScenes(scenes, probabiliteArretSurFin=0.0)
        self.assertEqual(self.identifiantsDuScript(court), ["prologue"])
        self.assertEqual(self.identifiantsDuScript(long), ["prologue", "epilogue"])

    def testDeuxFinsSuccessivesOffrentTroisLongueursPossibles(self):
        """
        Vérifie qu'un récit A -> B(fin) -> C(fin) -> D(fin) peut s'arrêter
        à B, à C ou à D. Les extrêmes se forcent par la probabilité ; l'arrêt
        sur C s'obtient en contrôlant les deux tirages successifs.
        """
        scenes = [
            decrireScene("A", ["B"], estDebut=True),
            decrireScene("B", ["C"], estFin=True),
            decrireScene("C", ["D"], estFin=True),
            decrireScene("D", [], estFin=True),
        ]
        self.assertEqual(
            self.identifiantsDuScript(self.filmDepuisScenes(scenes, 1.0)),
            ["A", "B"])
        self.assertEqual(
            self.identifiantsDuScript(self.filmDepuisScenes(scenes, 0.0)),
            ["A", "B", "C", "D"])

        film = self.filmDepuisScenes(scenes, probabiliteArretSurFin=0.5)
        # Premier tirage (sur B) : 0.8 >= 0.5, le récit continue.
        # Second tirage (sur C) : 0.2 < 0.5, le récit s'arrête.
        reponses = iter([0.8, 0.2])
        aleaOriginal = moduleFilm.rd.random
        self.addCleanup(setattr, moduleFilm.rd, "random", aleaOriginal)
        moduleFilm.rd.random = lambda: next(reponses)
        self.assertEqual(self.identifiantsDuScript(film), ["A", "B", "C"])

    def testChaqueGenerationReinitialiseLeScriptPrecedent(self):
        """
        Vérifie que creerScript vide scenesDuScript avant de recommencer :
        un second tirage n'empile pas les scènes sur le script précédent.
        """
        film = self.filmDepuisScenes(self.CHAINETTE, probabiliteArretSurFin=1.0)
        premier = self.identifiantsDuScript(film)
        second = self.identifiantsDuScript(film)
        self.assertEqual(premier, ["A", "B"])
        self.assertEqual(second, ["A", "B"])
        self.assertEqual(len(film.scenesDuScript), 2)

    def testLesExemplesGardentUneLongueurDeHuitScenes(self):
        """
        Vérifie que les films d'exemple, dont tous les chemins ont la même
        profondeur, produisent toujours un script de 8 scènes commençant
        par 1 et finissant par 19.
        """
        for fichier in (EXEMPLE_AVEC_VOIES, EXEMPLE_SANS_VOIES):
            with self.subTest(fichier=os.path.basename(fichier)):
                film = fi.Film("exemple", "A")
                film.creerFilmDepuisJSON(fichier)
                for _ in range(20):
                    script = film.creerScript()
                    identifiants = [s.idScene for s in script]
                    self.assertEqual(identifiants[0], "1")
                    self.assertEqual(identifiants[-1], "19")
                    self.assertEqual(len(identifiants), 8)


if __name__ == "__main__":
    unittest.main()
