# ----------------------------------------------------------------------------------------------------------------------
# PACKAGES
# ----------------------------------------------------------------------------------------------------------------------
import math
import os
import pandas as pnd    # manipulation et analyse

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '0'
"""     
0 = all messages are logged (default behavior)
1 = INFO messages are not printed
2 = INFO and WARNING messages are not printed 
3 = INFO, WARNING, and ERROR messages are not printed
"""

# ----------------------------------------------------------------------------------------------------------------------
# CLASSE "PB_Log" : gestion des logs
# ----------------------------------------------------------------------------------------------------------------------

class Log:

    # Attributs
    oFichier = ""

    # Constructeur
    def __init__(self, sUrl="default.log"):
        self.oFichier = open(sUrl, "w")


    # Méthodes



    def mFormatCelluleNum(self, dValeur, dMax=0, bNegatif=False, bPourcentage=False, iNbCar=20, iPrecision=2):

        dicFormatNum = {0: "%.0f", 1: "%.1f", 2: "%.2f", 3: "%.3f", 4: "%.4f", 5: "%.5f"}
        sRetour = ""

        if (bNegatif==False and dValeur<0) or (dMax>0 and dValeur>dMax):
            sRetour = "--.--"
        else:
            sRetour = dicFormatNum[iPrecision] % dValeur
        if bPourcentage:
            sRetour = sRetour + " %"

        sRetour = ((100*" ")+sRetour+" ")[-iNbCar:]
        return sRetour

    def mFormatCelluleTxt(self, sTexte, iNbCar=20):
        return (" "+sTexte[:iNbCar-2]+(100*" "))[:iNbCar]

    def mFormatListe(self, lstVals):
        sTexte = ""
        for val in lstVals:
            sTexte = sTexte + val + ", "
        sTexte = sTexte[0:-2]
        return sTexte

    # Saut de ligne (\n)
    def n(self):
        print("")
        self.oFichier.write("\n")

    # Ecriture d'une ligne (write)
    def w(self, sTexte, iIndent=0):
        if (iIndent == -1) | (iIndent == 0) | (iIndent == 1): self.n()

        if iIndent == -1:
            sTexte = ("*** " + sTexte + " " + (100 * "*"))[0:100]
        else :
            if iIndent == 0: sTexte = "> " + sTexte
            if iIndent == 1: sTexte = "- " + sTexte
            sTexte = (4 * iIndent)*" " + sTexte

        print(sTexte)
        self.oFichier.write("\n"+sTexte)

    # Affichage d'un tableau
    def tableau(self, dicCols, dtfData, bColIndex = False, sSeparateurV = "|", sSeparateurH = "-", iIndent=0,):

        # Ajout colonne index dans dtfData
        if bColIndex:
            dtfData = dtfData.reset_index()

        # suppression des colonnes non présentes dans la description (dicCols)
        lstCols = []
        for col in dtfData.columns:
            if col not in dicCols:
                lstCols.append(col)
        dtfData = dtfData.drop(columns=lstCols)

        # Construction ligne d'entête
        sLigne = ""
        iLong = 0
        for col in dicCols:
            sCentrage = int((dicCols[col]["long"]-len(col))/2)*" "
            sLigne = sLigne + self.mFormatCelluleTxt( sCentrage + col,dicCols[col]["long"]) + sSeparateurV
            iLong = iLong + dicCols[col]["long"] +1
        iLong = iLong - 1
        sLigne = sLigne[:len(sLigne)-1]

        # Entête
        self.n()
        self.w(iLong * sSeparateurH, iIndent=iIndent)
        self.w(sLigne, iIndent=iIndent)
        self.w(iLong * sSeparateurH, iIndent=iIndent)

        # Données
        for i in range(len(dtfData.index)):

            sLigne = ""
            j = 0

            for col in dicCols:

                if dicCols[col]["format"]=="txt":
                    sLigne = sLigne + self.mFormatCelluleTxt( dtfData.iloc[i,j],dicCols[col]["long"])
                elif dicCols[col]["format"]=="num":
                    sLigne = sLigne + self.mFormatCelluleNum(dtfData.iloc[i,j], iPrecision=dicCols[col]["precis"],iNbCar=dicCols[col]["long"])

                sLigne = sLigne + "|"
                j = j+1

            self.w(sLigne[:len(sLigne)-1], iIndent=iIndent)

        # Pied
        self.w(iLong * sSeparateurH, iIndent=iIndent)
        self.n()

