import pandas as pnd
import datetime
import os
from moteur.log import Log
from moteur.xls import Xls
from moteur.pdf import Pdf

sDossierRacine = "D:/Administratif/Plan B/scenarios/"
sScenario = "HORIZON_02"
sDate = str(datetime.date.today().isoformat())

dtfProjets = pnd.DataFrame()
dtfBilans = pnd.DataFrame()
dtfPlannings = pnd.DataFrame()

# Création du dossier cible
sDossier = sDossierRacine + sScenario + "/" + sDate
os.makedirs(sDossier, exist_ok=True)
log = Log(sUrl=sDossier+"/trace.log")

# Parcours du dossier source
sDossierSource = sDossierRacine + sScenario + "/sources"
log.w("Récupération des données sources (%s)" % sDossierSource)

for fichier in os.listdir(sDossierSource):

    if(fichier.split(".")[-1]=="xlsx"):

        xls = Xls(sUrl=sDossierSource + "/"+ fichier.title())
        log.w("Fichier %s" %xls.sUrl,iIndent=1)

        #Lecture onglet projet
        dtfProjet = xls.mOuvrirOnglet("PROJET")
        dtfProjet = dtfProjet.T
        dtfProjet.columns = dtfProjet.iloc[0]
        dtfProjet.drop(dtfProjet.head(1).index, inplace=True)
        dtfProjets = pnd.concat([dtfProjets,dtfProjet],ignore_index=True)

        # lecture onglet bilan
        dtfBilan = xls.mOuvrirOnglet("BILAN")
        dtfBilan['PROJET'] = dtfProjet['CODE'][0]
        dtfBilans = pnd.concat([dtfBilans,dtfBilan], ignore_index=True)

        # lecture onglet planning
        dtfPlanning = xls.mOuvrirOnglet("PLANNING")
        dtfPlanning['PROJET'] = dtfProjet['CODE'][0]
        dtfPlannings = pnd.concat([dtfPlannings,dtfPlanning], ignore_index=True)

# Affichage des résultats
log.n()
log.w("PROJETS:",iIndent=1)
dtfProjets.to_csv(sDossier+"/projets.csv")
log.tableau(dtfData=dtfProjets, dicCols={   "CODE":         {"format":"txt", "long":20, "precis":0},
                                            "TYPE":         {"format":"txt", "long":5,  "precis":0},
                                            "LIBELLE":      {"format":"txt", "long":50, "precis":0},
                                            "DATE_DEBUT":   {"format":"txt", "long":15, "precis":0},
                                            "DATE_FIN":     {"format":"txt", "long":15, "precis":0}}, iIndent=2)

dtfBilans[['GROUPE','SOUS_GROUPE','POSTE','SOUS_POSTE']] = dtfBilans[['GROUPE','SOUS_GROUPE','POSTE','SOUS_POSTE']].astype(str)
log.n()
log.w("BILAN:",iIndent=1)
dtfBilans.to_csv(sDossier+"/bilans.csv")
log.tableau(dtfData=dtfBilans, dicCols={    "GROUPE":       {"format":"txt", "long":20, "precis":0},
                                            "SOUS_GROUPE":  {"format":"txt", "long":20,  "precis":0},
                                            "POSTE":        {"format":"txt", "long":20, "precis":0},
                                            "SOUS_POSTE":   {"format":"txt", "long":20, "precis":0}}, iIndent=2)

log.n()
dtfPlannings = dtfPlannings.astype(str)
log.w("PLANNINGS:",iIndent=1)
log.tableau(dtfData=dtfPlannings, dicCols={ "ANNEE":        {"format":"txt", "long":10, "precis":0},
                                            "MOIS":         {"format":"txt", "long":10,  "precis":0},
                                            "PERSONNE":     {"format":"txt", "long":10, "precis":0},
                                            "TACHE":        {"format":"txt", "long":20, "precis":0},
                                            "JOUR":         {"format":"txt", "long":10, "precis":0},
                                            "HEURE_DEB":    {"format":"txt", "long":10, "precis":0},
                                            "HEURE_FIN":    {"format":"txt", "long":10, "precis":0},}, iIndent=2)

pdf = Pdf(sUrl=sDossier+"/rapport.pdf")
pdf.mAjouterImage(sUrl=sDossierSource+"/logo.png",iLarg=310,iHaut=110)
pdf.mAjouterImage(sUrl=sDossierSource+"/logo.png",iLarg=31,iHaut=11)
pdf.mAjouterEspace(iHaut=10)
pdf.mAjouterTexte("Description du Plan B, avec les diffénts projets embarqués dans le scénario...")
pdf.mAjouterEspace(iHaut=40)
pdf.mAjouterImage(sUrl=sDossierSource+"/logo.png",iLarg=31,iHaut=11)
pdf.mAjouterTableau(dtfProjets.to_numpy())

log.w("STRUCURE PDF:",iIndent=1)
log.tableau(dtfData=pdf.dtfElements, dicCols={  "type":     {"format":"txt", "long":10, "precis":0},
                                                "texte":    {"format":"txt", "long":50, "precis":0},
                                                "url":      {"format":"txt", "long":100, "precis":0},
                                                "largeur":  {"format":"num", "long":10, "precis":0},
                                                "hauteur":  {"format":"num", "long":10, "precis":0}}, iIndent=2)


pdf.mGenerer()
