class DonneesContenu:
    """
    Classe qui représente les différents contenus d'une scène comme le texte qui lui est associé.
    
    Attributs:
        urlTexte (str): L'url du texte associé à la scène
        ATTENTION, pour l'instant urlTexte représente le texte en lui-même"""
    urlTexte = None

    def __init__(self, urlTexte):
        """
        Constructeur de la classe DonneesContenu.
        
        Args:
            urlTexte (str): L'url du texte associé à la scène
        """
        self.urlTexte = urlTexte