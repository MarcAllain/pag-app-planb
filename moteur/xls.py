# ----------------------------------------------------------------------------------------------------------------------
# PACKAGES
# ----------------------------------------------------------------------------------------------------------------------

import pandas as pnd
from moteur.fic import Fic

# ----------------------------------------------------------------------------------------------------------------------
# CLASSE "Xls" : gestion des fichiers Excel
# ----------------------------------------------------------------------------------------------------------------------

class Xls(Fic):

# Attributs


# Constructeur

    def __init__(self, sUrl=""):
        super().__init__(sUrl=sUrl)

# Méthodes

    def mOuvrirOnglet(self, sOnglet=""):
        self.sOnglet = sOnglet
        return pnd.read_excel(self.sUrl, sheet_name=sOnglet)
