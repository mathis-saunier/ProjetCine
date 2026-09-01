class DonneesNarration:
    """
    Classe qui représente les données narratives d'une scène.
    
    Attributs:
        voies (list[str]): La liste des voies possibles pour la scène
        actes (list[str]): La liste des actes possibles pour la scène
        estDebut (bool): Indique si la scène peut ouvrir un script
        estFin (bool): Indique si la scène peut clore un script
    """
    
    def __init__(self, voies, actes, estDebut: bool = False, estFin: bool = False):
        """
        Constructeur de la classe DonneesNarration.
        
        Args:
            voies (list[str]): La liste des voies possibles pour la scène
            actes (list[str]): La liste des actes possibles pour la scène
            estDebut (bool): Indique si la scène peut ouvrir un script (défaut: False)
            estFin (bool): Indique si la scène peut clore un script (défaut: False)
        """
        self.voies = voies
        self.actes = actes
        self.estDebut = estDebut
        self.estFin = estFin
