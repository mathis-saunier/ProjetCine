class DonneesContenu:
    """
    Classe qui représente les différents contenus d'une scène comme le texte qui lui est associé.
    
    Attributs:
        urlTexte (str): L'url du texte associé à la scène
        resume (str): Un résumé court, affiché au survol du nœud dans le graphe
        ATTENTION, pour l'instant urlTexte représente le texte en lui-même
    """

    def __init__(self, urlTexte, resume: str = ""):
        """
        Constructeur de la classe DonneesContenu.
        
        Args:
            urlTexte (str): L'url du texte associé à la scène
            resume (str): Un résumé court de la scène (défaut: chaîne vide)
        """
        self.urlTexte = urlTexte
        self.resume = resume or ""
