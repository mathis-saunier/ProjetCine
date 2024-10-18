class DonneesNarration:
    """
    Classe qui représente les données narratives d'une scène.
    
    Attributs:
        voies (list[str]): La liste des voies possibles pour la scène
        actes (list[str]): La liste des actes possibles pour la scène
    """
    voies = []
    actes = []
    
    def __init__(self, voies, actes):
        """
        Constructeur de la classe DonneesNarration.
        
        Args:
            voies (list[str]): La liste des voies possibles pour la scène
            actes (list[str]): La liste des actes possibles pour la scène
        """
        self.voies = voies
        self.actes = actes