class Transition:
    """
    Classe représentant une transition entre deux scènes dans le graphe du film.
    
    Attributs:
        depart (int): L'identifiant de la scène de départ
        arrivee (int): L'identifiant de la scène d'arrivée
        nomCondition (str): Le nom de la condition qui génère cette transition
        priorite (int): La priorité de cette transition (défaut: 0)
    """
    
    def __init__(self, depart, arrivee, nomCondition, priorite=0):
        """
        Constructeur de la classe Transition.
        
        Args:
            depart (int): L'identifiant de la scène de départ
            arrivee (int): L'identifiant de la scène d'arrivée
            nomCondition (str): Le nom de la condition qui génère cette transition
            priorite (int): La priorité de cette transition (défaut: 0)
        """
        self.depart = depart
        self.arrivee = arrivee
        self.nomCondition = nomCondition
        self.priorite = priorite
    
    def to_graphviz(self):
        """
        Retourne la transition au format compatible avec GraphViz (format DOT).
        
        Returns:
            str: Une ligne au format DOT pour GraphViz
        """
        # Format: "scene1" -> "scene2" [label="condition_name"];
        label = f"{self.nomCondition} (p:{self.priorite})"
        return f'"{self.depart}" -> "{self.arrivee}" [label="{label}"];'
    
    def __repr__(self):
        return f"Transition({self.depart} -> {self.arrivee}, '{self.nomCondition}', p={self.priorite})"
    
    def __str__(self):
        return f"Scène {self.depart} → Scène {self.arrivee} ({self.nomCondition})"
