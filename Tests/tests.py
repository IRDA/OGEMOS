from openpyxl import load_workbook
import requests
from GUI.fonction_utilitaire import is_valid_string

APPORT_DEFAUT = 10.0
CULTURE_SECONDAIRE_DEFAUT = 1.0
TRAVAIL_DU_SOL_DEFAUT = "Aucun"

wb = load_workbook(filename='C:\\Users\\Samuel\\Documents\\Stage IRDA\\FilesForTestingTheTestMapping.xlsx')
donnees_champs = wb['Données champs']
donnees_regies = wb['Données régies']
donnees_amendements = wb['Données amendements']

row_index = 1
column_index = 1
while donnees_amendements.cell(row=row_index, column=column_index).value is not None:
    id_amendement = donnees_amendements.cell(row=row_index, column=column_index).value
    print(id_amendement)
    column_index += 1
    pourcentage_humidite = donnees_amendements.cell(row=row_index, column=column_index).value
    column_index += 1
    carbon_total = donnees_amendements.cell(row=row_index, column=column_index).value
    column_index = 1
    row_index += 1
    if str(id_amendement).isalnum() and str(pourcentage_humidite).isalnum() and str(carbon_total).isalnum():
        amendement_dict = {"amendement": id_amendement,
                           "pourcentage_humidite": str(pourcentage_humidite),
                           "carbon_total": str(carbon_total)}
        # response = requests.post('http://localhost:5000/api/ajout-amendement', json=amendement_dict)
simulation = {"simulations": [{"nom_simulation": "Test OGEMOS", "duree_projection": 0, "annee_initiale_projection": 0,
                               "annee_finale_projection": 0,
                               "entreprise_agricole": {"nom": "Test OGEMOS", "champs": []}}]}
champ_dict = {}
row_index = 1
column_index = 1
while donnees_champs.cell(row=row_index, column=column_index).value is not None:
    id_champ = donnees_champs.cell(row=row_index, column=column_index).value
    column_index += 1
    centroide_champ = donnees_champs.cell(row=row_index, column=column_index).value
    column_index += 1
    taux_mos_initial = donnees_champs.cell(row=row_index, column=column_index).value
    column_index += 1
    annee_taux_mos_initial = donnees_champs.cell(row=row_index, column=column_index).value
    column_index += 1
    taux_mos_final = donnees_champs.cell(row=row_index, column=column_index).value
    column_index += 1
    annee_taux_mos_final = donnees_champs.cell(row=row_index, column=column_index).value
    column_index += 1
    municipalite = donnees_champs.cell(row=row_index, column=column_index).value
    column_index += 1
    code_postal = donnees_champs.cell(row=row_index, column=column_index).value
    column_index += 1
    serie_sol = donnees_champs.cell(row=row_index, column=column_index).value
    column_index += 1
    groupe_textural = donnees_champs.cell(row=row_index, column=column_index).value
    column_index += 1
    classe_de_drainage = donnees_champs.cell(row=row_index, column=column_index).value
    column_index += 1
    masse_volumique_apparente = donnees_champs.cell(row=row_index, column=column_index).value
    column_index += 1
    profondeur = donnees_champs.cell(row=row_index, column=column_index).value
    column_index = 1
    row_index += 1
    if is_valid_string(str(id_champ)):
        print("id_champ")
    if is_valid_string(str(centroide_champ)):
        print("centroide_champ")
    if is_valid_string(str(taux_mos_initial)):
        print("taux_mos_initial")
    if is_valid_string(str(annee_taux_mos_initial)):
        print("annee_taux_mos_initial")
    if is_valid_string(str(taux_mos_final)):
        print("taux_mos_final")
    if is_valid_string(str(annee_taux_mos_final)):
        print("annee_taux_mos_final")
    if is_valid_string(str(municipalite)):
        print("municipalite")
    if is_valid_string(str(code_postal)):
        print("code_postal")
    if is_valid_string(str(serie_sol)):
        print("serie_sol")
    if is_valid_string(str(groupe_textural)):
        print("groupe_textural")
    if is_valid_string(str(classe_de_drainage)):
        print("classe_de_drainage")
    if is_valid_string(str(masse_volumique_apparente)):
        print("masse_volumique_apparente")
    if is_valid_string(str(profondeur)):
        print("profondeur")
    if (is_valid_string(str(id_champ)) and is_valid_string(str(centroide_champ)) and is_valid_string(str(taux_mos_initial)) and is_valid_string(str(annee_taux_mos_initial)) and
            is_valid_string(str(taux_mos_final)) and is_valid_string(str(annee_taux_mos_final)) and is_valid_string(str(municipalite)) and is_valid_string(str(code_postal)) and
            is_valid_string(str(serie_sol)) and is_valid_string(str(groupe_textural)) and is_valid_string(str(classe_de_drainage)) and is_valid_string(str(masse_volumique_apparente)) and
            is_valid_string(str(profondeur))):
        if profondeur == -1:
            profondeur = 20
        if groupe_textural == -1:
            groupe_textural = "Groupe 2 (texture moyenne)"
        if classe_de_drainage == -1:
            classe_de_drainage = "Modérément bien drainé"
        champ = {"nom": id_champ,
                 "zone_de_gestion": [{"taux_matiere_organique": float(taux_mos_initial), "municipalite": municipalite,
                                      "groupe_textural": groupe_textural, "classe_de_drainage": classe_de_drainage,
                                      "masse_volumique_apparente": float(masse_volumique_apparente),
                                      "profondeur": float(profondeur),
                                      "superficie_de_la_zone": 1, "regies_sol_et_culture_projection": [],
                                      "regies_sol_et_culture_historique": []}]}
        print(champ)
        champ_dict[id_champ] = champ
print(champ_dict)
row_index = 1
column_index = 1
while donnees_regies.cell(row=row_index, column=column_index).value is not None:
    id_champ = donnees_regies.cell(row=row_index, column=column_index).value
    column_index += 1
    annee_culture = donnees_regies.cell(row=row_index, column=column_index).value
    column_index += 1
    culture_principale = donnees_regies.cell(row=row_index, column=column_index).value
    column_index += 1
    rendement_culture_principale = donnees_regies.cell(row=row_index, column=column_index).value
    column_index += 1
    pourcentage_tige_paille = donnees_regies.cell(row=row_index, column=column_index).value
    column_index += 1
    production_recoltee = donnees_regies.cell(row=row_index, column=column_index).value
    column_index += 1
    travail_du_sol = donnees_regies.cell(row=row_index, column=column_index).value
    column_index += 1
    culture_secondaire = donnees_regies.cell(row=row_index, column=column_index).value
    column_index += 1
    rendement_culture_secondaire = donnees_regies.cell(row=row_index, column=column_index).value
    column_index += 1
    id_amendement = donnees_regies.cell(row=row_index, column=column_index).value
    column_index += 1
    apport = donnees_regies.cell(row=row_index, column=column_index).value
    column_index = 1
    row_index += 1
    if (is_valid_string(str(id_champ)) and is_valid_string(str(annee_culture)) and is_valid_string(str(culture_principale)) and
            is_valid_string(str(pourcentage_tige_paille)) and
            is_valid_string(str(production_recoltee)) and is_valid_string(str(travail_du_sol)) and is_valid_string(str(culture_secondaire)) and
            is_valid_string(str(rendement_culture_secondaire)) and is_valid_string(str(id_champ)) and
            is_valid_string(str(apport))):
        if pourcentage_tige_paille == -1:
            pourcentage_tige_paille = None
        if travail_du_sol == -1:
            travail_du_sol = TRAVAIL_DU_SOL_DEFAUT
        if rendement_culture_principale == -1:
            rendement_culture_principale = None
        if production_recoltee == 1:
            production_recoltee = True
        else:
            production_recoltee = False
        if culture_secondaire != -1 and rendement_culture_secondaire != -1:
            pass
        elif culture_secondaire != -1 and rendement_culture_secondaire == -1:
            rendement_culture_secondaire = 1
        else:
            culture_secondaire = None
            rendement_culture_secondaire = None
        amendement_list = []
        if id_amendement != -1 and apport != -1:
            amendements = id_amendement.split(",")
            if "," in str(apport):
                apports = apport.split(",")
                index = 0
                for amendement in amendements:
                    amendement_list.append({"amendement": amendement,
                                            "apport": apports[index]})
                    index += 1
            else:
                amendement_list.append({"amendement": id_amendement,
                                        "apport": apport})

        elif id_amendement != -1 and apport == -1:
            amendements = id_amendement.split(",")
            for amendement in amendements:
                amendement_list.append({"amendement": amendement,
                                        "apport": APPORT_DEFAUT})
        else:
            amendement_list.append(({"amendement": None,
                                     "apport": None}))
        regie = {
            "culture_principale": {"culture_principale": culture_principale, "rendement": rendement_culture_principale,
                                   "pourcentage_tige_exporte": pourcentage_tige_paille,
                                   "produit_recolte": True,
                                   "pourcentage_humidite": None},
            "culture_secondaire": {"culture_secondaire": culture_secondaire, "rendement": rendement_culture_secondaire},
            "amendements": {"amendments": amendement_list}}
        champ_dict["id_champ"]["zone_de_gestion"][0]["regies_sol_et_culture_projection"].append(regie)
for champ in champ_dict:
    print(champ)
    simulation["simulations"][0]["entreprise_agricole"]["champs"].append(champ)
# test_response = requests.post("http://localhost:5000/api/icbm-bilan", json=simulation)
print(simulation)
print(champ_dict)
# print(test_response)
