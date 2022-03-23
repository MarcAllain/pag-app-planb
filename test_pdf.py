import pandas as pnd
import datetime
import os
from moteur.log import Log
from moteur.xls import Xls
from moteur.pdf import Pdf

sDate = str(datetime.date.today().isoformat())
sFichier = "sources/test.xlsx"
log = Log(sUrl="log/trace_%s.log" % sDate)

if(sFichier.split(".")[-1]=="xlsx"):

    xls = Xls(sUrl=sFichier)
    dtfTest = xls.mOuvrirOnglet(sOnglet="simple")

    """log.w("DATAFRAME:", iIndent=1)
    log.tableau(dtfData=dtfTest, dicCols={  "1":    {"format":"txt", "long":10, "precis":0},
                                            "2":    {"format":"txt", "long":10,  "precis":0},
                                            "3":    {"format":"txt", "long":10, "precis":0},
                                            "4":    {"format":"txt", "long":10, "precis":0},
                                            "5":    {"format":"txt", "long":10, "precis":0}}, iIndent=2)
"""

    print("Type dtf :  %s" % type(dtfTest))
    data = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    print("Type data : %s" % type(data))
    data = dtfTest.values.tolist()
    print(data)
    print("Type data : %s" % type(data))

    pdf = Pdf(sUrl="cible/rapport.pdf")
    pdf.mAjouterEspace(iHaut=10)
    pdf.mAjouterTexte("Bla bla bla ...")
    pdf.mAjouterEspace(iHaut=40)
    pdf.mAjouterTableau(dtfTest.to_numpy())

    log.w("STRUCURE PDF:",iIndent=1)
    log.tableau(dtfData=pdf.dtfElements, dicCols={  "type":     {"format":"txt", "long":10, "precis":0},
                                                    "texte":    {"format":"txt", "long":50, "precis":0},
                                                    "url":      {"format":"txt", "long":100, "precis":0},
                                                    "largeur":  {"format":"num", "long":10, "precis":0},
                                                    "hauteur":  {"format":"num", "long":10, "precis":0}}, iIndent=2)


    pdf.mGenerer()
