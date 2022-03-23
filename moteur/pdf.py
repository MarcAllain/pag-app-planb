# ----------------------------------------------------------------------------------------------------------------------
# PACKAGES
# ----------------------------------------------------------------------------------------------------------------------

import pandas as pnd
from moteur.fic import Fic
from reportlab.platypus import BaseDocTemplate, SimpleDocTemplate, PageTemplate, Frame, Paragraph, Spacer, PageBreak, Table, TableStyle, CondPageBreak, Image, ParagraphAndImage
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle as PS
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY

# ----------------------------------------------------------------------------------------------------------------------
# CLASSE "Pdf" : gestion des fichiers PDF
# ----------------------------------------------------------------------------------------------------------------------

class Pdf(Fic):

# Attributs



# Constructeur

    def __init__(self, sUrl=""):
        super().__init__(sUrl=sUrl)

# Méthodes

    def mGenerer(self):

        tElements = []

        for i in self.dtfElements.index:

            # Image
            if self.dtfElements["type"][i] == "IMG":
                tElements.append(Image(self.dtfElements["url"][i],width=self.dtfElements["largeur"][i], height=self.dtfElements["hauteur"][i], hAlign=TA_LEFT ))

            # Espace
            elif self.dtfElements["type"][i] == "ESP":
                tElements.append(Spacer(1, self.dtfElements["hauteur"][i]))

            # Texte
            elif self.dtfElements["type"][i] == "TXT":
                tElements.append(Paragraph(self.dtfElements["texte"][i], PS(   name='CORPS',
                                                                               fontName='Helvetica',
                                                                               fontSize=11,
                                                                               alignment=TA_LEFT)))

            # Tableau
            elif self.dtfElements["type"][i] == "TBL":
                #tElements.append(Table((self.dtfElements["data"][i])))
                print(">>> TYPE TABLE = %s" % type(self.dtfElements["data"][i]))
                data = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
                t = Table(data, len(data) * [2 * cm], len(data[0]) * [1 * cm])
                t.setStyle(TableStyle([('FONTSIZE', (0, 0), (-1, -1), 12),
                                       ('INNERGRID', (-1, -1), (0, 0), 0.5, colors.blue),
                                       ('BOX', (0, 0), (-1, -1), 0.5, colors.red)]))
                tElements.append(t)

        doc = SimpleDocTemplate(    self.sUrl,
                                    pagesize = A4,
                                    title = 'Plan B',
                                    author = 'PAG' )
        doc.build(tElements)

