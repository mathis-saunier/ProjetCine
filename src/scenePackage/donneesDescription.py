class DonneesDescription:
    """
    Classe qui permet de stocker les données de description d'une scène tels que le lieu où se déroule cette dernière, les personnages présents ...
    
    Attributs:
        lieu (str): Le lieu où se déroule la scène
        personnages (list[str]): La liste des personnages présents dans la scène
        interieurExterieur (str): Le type de lieu où se déroule la scène (intérieur ou extérieur)
    """
    lieu = None
    personnages = []
    interieurExterieur = None
    
    def __init__(self, lieu, personnages, interieurExterieur):
        """
        Constructeur de la classe DonneesDescription
        
        Args:
            lieu (str): Le lieu où se déroule la scène
            personnages (list[str]): La liste des personnages présents dans la scène
            interieurExterieur (str): Le type de lieu où se déroule la scène (intérieur ou extérieur)
        """
        self.lieu = lieu
        self.personnages = personnages
        self.interieurExterieur = interieurExterieur