from copy import deepcopy
import random as rd

from scenePackage.scene import Scene
from conditionPackage.condition import Condition
from conditionPackage.valeurCondition import ValeurCondition
from conditionPackage.transition import Transition
import jsonPackage as js

class SceneInexistanteException(Exception):
    """
    Exception levée lorsqu'une scène n'existe pas.
    """
    def __init__(self, id):
        self.id = id
        super().__init__(f"Erreur, la scènes d'id {id} n'existe pas")

class ZeroSceneRestanteException(Exception):
    """
    Exception levée lorsqu'il n'y a plus de scènes restantes dans un acte pour une voie donnée.
    """
    def __init__(self, acte, voie):
        self.acte = acte
        self.voie = voie
        super().__init__(f"Erreur, il n'y a pas de scènes restantes dans l'acte {acte} pour la voie {voie}")
        
class AucuneSceneDeDebutException(Exception):
    """
    Exception levée lorsqu'aucune scène du film n'est déclarée comme scène de début.
    """
    def __init__(self, nomFilm):
        self.nomFilm = nomFilm
        super().__init__(f"Erreur, aucune scène du film {nomFilm} n'est déclarée comme scène de début")

class Film():
    """
    Classe représentant un Film.
    
    Attributs:
        nomFilm (str): Le nom du film
        scenesDuFilm (list[Scene]): La liste des scènes du film
        scenesDuScript (list[Scene]): La liste des scènes du script (les scènes du film qui ont été choisies pour le script)
        voieInitiale (str): La voie initiale du film
        voieActuelle (str): La voie actuelle du film
        acteActuel (str): L'acte actuel du film
        probabiliteArretSurFin (float): Probabilité de clore le script lorsqu'une scène de fin possède encore des suites
    """
    
    # Ajouter le choix de la voieInitiale dans le __init__
    def __init__(self, nomFilm, voieInitiale, probabiliteArretSurFin: float = 0.5):
        """
        Constructeur de la classe Film.

        Args:
            nomFilm (str): Le nom du film
            voieInitiale (str): La voie initiale du film
            probabiliteArretSurFin (float): Probabilité, entre 0 et 1, de clore le script lorsque la dernière scène est une fin possédant encore des suites (défaut: 0.5)
        """
        self.nomFilm = nomFilm
        self.scenesDuFilm = []
        self.scenesDuScript = []
        self.voieInitiale = voieInitiale
        self.voieActuelle = voieInitiale
        self.acteActuel = "1"
        self.probabiliteArretSurFin = probabiliteArretSurFin
    
    def ajouterScene(self, scene):
        """
        Méthode permettant d'ajouter une scène au script.

        Args:
            scene (Scene): La scène à ajouter au script
        """
        self.scenesDuScript.append(scene)
    
    # Ne prendre pas en compte l'acte ou la voie actuel.le
    def recupererScenesPossibles(self, acte, voie):
        """
        Méthode permettant de récupérer les scènes possibles pour un acte et une voie donnée.

        ATTENTION: Pour le moment, cette méthode ne prend pas en compte l'acte ou la voie passés en arguement.

        Args:
            acte (str): L'acte pour lequel on souhaite récupérer les scènes possibles
            voie (str): La voie pour laquelle on souhaite récupérer les scènes possibles

        Returns:
            list[Scene]: La liste des scènes possibles
        """
        scenesExistantes = deepcopy(self.scenesDuFilm)
        return scenesExistantes
        
    def recupererConditions(self):
        """
        Méthode permettant de récupérer toutes les conditions des scènes du script.

        Returns:
            list[Condition]: La liste des conditions des scènes du script
        """
        res = []
        for s in self.scenesDuScript:
            for c in s.conditions:
                res.append(c)
        return res
    
    def tirerUneScene(self):
        """
        Méthode permettant de choisir aléatoirement une scène parmi les scènes possibles en vérifiant que la scène respecte toutes les conditions du script dans son état actuel.

        Returns:
            Scene: La scène choisie aléatoirement

        Raises:
            ZeroSceneRestanteException: Si il n'y a plus de scènes disponibles pour le tirage aléatoire. Les raisons peuvent être qu'aucune scène ne vérifie les conditions ou que toutes les scènes possibles ont déjà été choisies
        """
        scenesPossibles = self.recupererScenesPossibles(self.acteActuel, self.voieActuelle)
        # On retire egalement les scenesDuScript qui sont deja dans le script.
        # Filtrer par comprehension et non par remove() successifs : retirer des elements
        # d'une liste pendant qu'on l'itere en fait sauter certains.
        scenesPossibles = [s for s in scenesPossibles if s not in self.scenesDuScript]

        while len(scenesPossibles) != 0:
            choix = rd.randrange(0, len(scenesPossibles))
            sceneChoisie = scenesPossibles[choix]
            # Maintenant que l'on a une scene possible, on vérifie qu'elle respecte les conditions
            if (sceneChoisie.verifierToutesLesConditionsPrecedentes(self) == ValeurCondition.SUCCES):
                return sceneChoisie
            else:
                scenesPossibles.pop(choix)

        raise ZeroSceneRestanteException(self.acteActuel, self.voieActuelle)
        
    def creerFilmDepuisJSON(self, fichier_json):
        """
        Méthode permettant de créer un film à partir d'un fichier JSON.

        Args:
            fichier_json (str): Le nom du fichier JSON (ex: "film.json")

        Raises:
            ChargementJSONException: Si le fichier est introuvable, mal formé ou si son contenu ne respecte pas le format attendu
        """
        self.scenesDuFilm = js.creerScenesDepuisJSON(fichier_json)

    def chargerScenes(self, scenes: list) -> None:
        """
        Méthode permettant d'associer au film une liste de scènes déjà instanciées.

        Args:
            scenes (list[Scene]): Les scènes qui constituent le film
        """
        self.scenesDuFilm = list(scenes)

    def tirerUneSceneDeDebut(self):
        """
        Méthode permettant de choisir aléatoirement une scène parmi celles déclarées comme scènes de début.

        Returns:
            Scene: La scène de début choisie aléatoirement

        Raises:
            AucuneSceneDeDebutException: Si aucune scène du film n'est déclarée comme scène de début
        """
        scenesDeDebut = [s for s in self.scenesDuFilm if s.narrationScene.estDebut]
        if not scenesDeDebut:
            raise AucuneSceneDeDebutException(self.nomFilm)
        return rd.choice(scenesDeDebut)

    def creerScript(self, choixPremiereScene=None):
        """
        Méthode permettant de créer un script aléatoire à partir des scènes du film.

        Le script démarre sur une scène de début et s'arrête sur une scène de fin.
        Lorsqu'une scène de fin possède encore des suites, la poursuite du récit est
        tirée au sort selon probabiliteArretSurFin, ce qui donne des scripts de longueur variable.

        Args:
            choixPremiereScene (str): L'identifiant de la première scène du script (optionnel, une scène de début est tirée au sort sinon)

        Returns:
            list[Scene]: La liste des scènes du script

        Raises:
            AucuneSceneDeDebutException: Si aucune première scène n'est imposée et qu'aucune scène de début n'est déclarée
            SceneInexistanteException: Si l'identifiant de première scène imposé n'existe pas
            ZeroSceneRestanteException: Si le récit s'interrompt sur une scène qui n'est pas une fin
        """
        # On reinitialise tout potentiel ancien script
        self.scenesDuScript = []

        if choixPremiereScene != None:
            self.ajouterScene(self.obtenirSceneParId(choixPremiereScene))
        else:
            self.ajouterScene(self.tirerUneSceneDeDebut())

        # Le generateur aleatoire n'est pas reamorce ici : un appelant peut ainsi
        # fixer une graine avec random.seed() pour rejouer une generation a l'identique.
        while True:
            derniereScene = self.scenesDuScript[-1]
            estUneFin = derniereScene.narrationScene.estFin

            if not derniereScene.possedeDesScenesSuivantes():
                # Le recit ne peut pas continuer : c'est une fin si l'auteur l'a voulu,
                # sinon le film est incomplet et il faut le signaler.
                if estUneFin:
                    return self.scenesDuScript
                raise ZeroSceneRestanteException(self.acteActuel, self.voieActuelle)

            if estUneFin and rd.random() < self.probabiliteArretSurFin:
                return self.scenesDuScript

            try:
                self.ajouterScene(self.tirerUneScene())
            except ZeroSceneRestanteException:
                # Aucune des suites declarees n'est disponible : acceptable seulement sur une fin
                if estUneFin:
                    return self.scenesDuScript
                raise
    
    def obtenirScript(self):
        """
        Méthode permettant d'obtenir le script du film sous un format texte.

        Returns:
            str: Le script du film sous un format texte
        """
        script = "Début du script\n"
        for s in self.scenesDuScript:
            script += s.idScene + " : " + s.contenuScene.urlTexte + "\n"
        return script
    

    def sceneDejaExistante(self, idScene):
        """
        Méthode permettant de vérifier si une scène existe déjà dans le film.

        Args:
            idScene (str): L'identifiant de la scène à vérifier

        Returns:
            bool: True si la scène existe déjà, False sinon
        """
        for scene in self.scenesDuFilm:
            if (idScene == scene.idScene):
                return True
        return False
    
    def obtenirSceneParId(self, id):
        """
        Méthode permettant de récupérer une scène par son identifiant.
        
        Args:
            id (str): Un identifiant de scène

        Returns:
            Scene: La scène correspondante à l'identifiant

        Raises:
            SceneInexistanteException: Si l'indentifiant de la scène n'existe pas
        """
        for s in self.scenesDuFilm:
            if (s.idScene == id):
                return s
        # Si l'on a pas trouvé de scene on lève une exception
        raise SceneInexistanteException(id)
    
    def _identifiantDot(self, idScene) -> str:
        """
        Protège un identifiant de scène pour le format DOT.

        Args:
            idScene: L'identifiant brut de la scène

        Returns:
            str: L'identifiant entre guillemets, échappé
        """
        texte = str(idScene).replace("\\", "\\\\").replace('"', '\\"')
        return f'"{texte}"'

    def _couleurNoeud(self, scene) -> str:
        """
        Choisit la couleur d'un nœud selon son rôle narratif.

        Args:
            scene (Scene): La scène à colorer

        Returns:
            str: Une couleur GraphViz
        """
        debut = scene.narrationScene.estDebut
        fin = scene.narrationScene.estFin
        if debut and fin:
            return "gold"
        if debut:
            return "palegreen"
        if fin:
            return "lightcoral"
        return "lightblue"

    def _transitionsDuFilm(self) -> list:
        """
        Recense les transitions du film, sans doublon.

        Returns:
            list[Transition]: Les arêtes dérivées des conditions
        """
        transitionsAjoutees = []
        cles = set()
        for scene in self.scenesDuFilm:
            if not hasattr(scene, "conditions") or not scene.conditions:
                continue
            for condition in scene.conditions:
                for transition in condition.genererTransitions(scene):
                    cle = (transition.depart, transition.arrivee, transition.nomCondition)
                    if cle not in cles:
                        cles.add(cle)
                        transitionsAjoutees.append(transition)
        return transitionsAjoutees

    def _donneesNoeud(self, scene, couleur: str, surbrillance: bool) -> dict:
        """
        Construit la description d'un nœud de graphe, y compris son résumé.

        Args:
            scene (Scene): La scène représentée
            couleur (str): La couleur de remplissage
            surbrillance (bool): Indique si le nœud appartient au tirage

        Returns:
            dict: id, couleur, surbrillance, resume
        """
        resume = ""
        if hasattr(scene, "contenuScene") and scene.contenuScene.resume:
            resume = scene.contenuScene.resume
        return {
            "id": scene.idScene,
            "couleur": couleur,
            "surbrillance": surbrillance,
            "resume": resume,
        }

    def _sceneParIdOuAucune(self, idScene):
        """
        Retrouve une scène du film, ou None si elle n'existe pas.

        Args:
            idScene: L'identifiant recherché

        Returns:
            Scene | None: La scène, si elle existe
        """
        for scene in self.scenesDuFilm:
            if scene.idScene == idScene:
                return scene
        return None

    def donneesGrapheComplet(self) -> dict:
        """
        Décrit le graphe de toutes les possibilités, prêt à être dessiné en SVG.

        Returns:
            dict: {noeuds: list[dict], aretes: list[dict]}
        """
        noeuds = [
            self._donneesNoeud(scene, self._couleurNoeud(scene), False)
            for scene in self.scenesDuFilm
        ]
        aretes = [
            {"depart": t.depart, "arrivee": t.arrivee, "surbrillance": False}
            for t in self._transitionsDuFilm()
        ]
        return {"noeuds": noeuds, "aretes": aretes}

    def donneesGrapheTirage(self, identifiants: list) -> dict:
        """
        Décrit le graphe d'un script tiré.

        Args:
            identifiants (list[str]): Les identifiants des scènes du script, dans l'ordre

        Returns:
            dict: {noeuds: list[dict], aretes: list[dict]}
        """
        noeuds = []
        for identifiant in identifiants:
            scene = self._sceneParIdOuAucune(identifiant)
            if scene is None:
                noeuds.append({"id": identifiant, "couleur": "gold",
                               "surbrillance": True, "resume": ""})
            else:
                noeuds.append(self._donneesNoeud(scene, "gold", True))
        aretes = [{"depart": a, "arrivee": b, "surbrillance": True}
                  for a, b in zip(identifiants, identifiants[1:])]
        return {"noeuds": noeuds, "aretes": aretes}

    def donneesGrapheSuperpose(self, identifiants: list) -> dict:
        """
        Décrit le graphe complet avec le tirage mis en évidence.

        Args:
            identifiants (list[str]): Les identifiants des scènes du script, dans l'ordre

        Returns:
            dict: {noeuds: list[dict], aretes: list[dict]}
        """
        aretesDuTirage = set(zip(identifiants, identifiants[1:]))
        noeudsDuTirage = set(identifiants)
        noeuds = []
        for scene in self.scenesDuFilm:
            surbrillance = scene.idScene in noeudsDuTirage
            couleur = "gold" if surbrillance else self._couleurNoeud(scene)
            noeuds.append(self._donneesNoeud(scene, couleur, surbrillance))
        aretes = []
        for transition in self._transitionsDuFilm():
            surbrillance = (transition.depart, transition.arrivee) in aretesDuTirage
            aretes.append({
                "depart": transition.depart,
                "arrivee": transition.arrivee,
                "surbrillance": surbrillance,
            })
        return {"noeuds": noeuds, "aretes": aretes}

    def contenuGrapheComplet(self) -> str:
        """
        Construit le graphe de toutes les transitions possibles, sans écrire de fichier.

        Returns:
            str: Le graphe au format DOT
        """
        lignes = [
            "digraph Film {",
            '    bgcolor="white";',
            f'    label="{self.nomFilm} — toutes les possibilités";',
            '    node [shape=box, style=filled, fontname="Helvetica"];',
            '    edge [fontname="Helvetica"];',
        ]
        for scene in self.scenesDuFilm:
            lignes.append(
                f"    {self._identifiantDot(scene.idScene)} "
                f'[fillcolor={self._couleurNoeud(scene)}];'
            )
        for transition in self._transitionsDuFilm():
            lignes.append("    " + transition.to_graphviz())
        lignes.append("}\n")
        return "\n".join(lignes)

    def contenuGrapheTirage(self, identifiants: list) -> str:
        """
        Construit le graphe d'un script, c'est-à-dire la seule chaîne tirée.

        Args:
            identifiants (list[str]): Les identifiants des scènes du script, dans l'ordre

        Returns:
            str: Le graphe au format DOT
        """
        lignes = [
            "digraph Tirage {",
            '    bgcolor="white";',
            f'    label="{self.nomFilm} — tirage";',
            '    node [shape=box, style=filled, fillcolor=gold, fontname="Helvetica"];',
            '    edge [color="#b8860b", penwidth=2.5, fontname="Helvetica"];',
        ]
        for identifiant in identifiants:
            lignes.append(f"    {self._identifiantDot(identifiant)};")
        for depart, arrivee in zip(identifiants, identifiants[1:]):
            lignes.append(
                f"    {self._identifiantDot(depart)} -> {self._identifiantDot(arrivee)};"
            )
        lignes.append("}\n")
        return "\n".join(lignes)

    def contenuGrapheSuperpose(self, identifiants: list) -> str:
        """
        Superpose le chemin d'un script sur le graphe de toutes les possibilités.

        Args:
            identifiants (list[str]): Les identifiants des scènes du script, dans l'ordre

        Returns:
            str: Le graphe au format DOT
        """
        aretesDuTirage = set(zip(identifiants, identifiants[1:]))
        noeudsDuTirage = set(identifiants)
        lignes = [
            "digraph Superpose {",
            '    bgcolor="white";',
            f'    label="{self.nomFilm} — possibilités et tirage";',
            '    node [shape=box, style=filled, fontname="Helvetica"];',
            '    edge [fontname="Helvetica"];',
        ]
        for scene in self.scenesDuFilm:
            couleur = "gold" if scene.idScene in noeudsDuTirage else self._couleurNoeud(scene)
            epaisseur = ' penwidth=2.2' if scene.idScene in noeudsDuTirage else ""
            lignes.append(
                f"    {self._identifiantDot(scene.idScene)} "
                f"[fillcolor={couleur}{epaisseur}];"
            )
        for transition in self._transitionsDuFilm():
            if (transition.depart, transition.arrivee) in aretesDuTirage:
                extra = ' [color="#b8860b", penwidth=3.2]'
            else:
                extra = ' [color="#888888"]'
            lignes.append(
                f"    {self._identifiantDot(transition.depart)} -> "
                f"{self._identifiantDot(transition.arrivee)}{extra};"
            )
        lignes.append("}\n")
        return "\n".join(lignes)

    def genererGraphe(self, nomFichier="graphe.dot"):
        """
        Génère un fichier GraphViz représentant le graphe de transitions entre les scènes du film.
        Le graphe inclut toutes les transitions basées sur les conditions des scènes.
        
        Args:
            nomFichier (str): Le nom du fichier de sortie (défaut: "graphe.dot")
            
        Returns:
            str: Le contenu du graphe au format DOT
        """
        contenuGraphe = self.contenuGrapheComplet()
        with open(nomFichier, 'w', encoding='utf-8') as f:
            f.write(contenuGraphe)
        return contenuGraphe
        
        
        