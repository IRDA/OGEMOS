from flask import Flask, request, jsonify, abort
from ICBM.Simulations.gestion_de_simulation import *

app = Flask(__name__)


@app.route('/api/icbm-bilan', methods=['POST'])
def add():
    data = request.get_json()
    __launch_icbm_simulation(data)
    return jsonify(data)


def __launch_icbm_simulation(data):
    gestion_simulation = __simulation_mapping(data["simulations"])
    gestion_simulation.effectuer_les_simulations_pour_l_entreprise_agricole()


def __simulation_mapping(data):
    gestion_simulation = GestionSimulation()
    for simulation in data:
        annee_initiale = simulation["annee_initiale"]
        annee_finale = simulation["annee_finale"]
        entreprise_agricole = __entreprise_agricole_mapping(simulation["entreprise_agricole"])
        gestion_simulation.ajouter_une_simulation(Simulation(annee_initiale, annee_finale, entreprise_agricole))
    return gestion_simulation


def __entreprise_agricole_mapping(data):
    entreprise_nom = data["nom"]
    champs = __champs_mapping(data["champs"])
    return EntrepriseAgricole(entreprise_nom, champs)


def __champs_mapping(data):
    liste_champs = []
    for champs in data:
        nom_champs = champs["nom"]
        zones_de_gestion = __zone_de_gestion_mapping(champs["zones_de_gestion"])
        liste_champs.append(Champs(nom_champs, zones_de_gestion))
    return liste_champs


def __zone_de_gestion_mapping(data):
    liste_zone_de_gestion = []
    series_de_sol_supportees = get_series_de_sol_supportees()
    for zone_de_gestion in data:
        taux_matiere_organique = zone_de_gestion["taux_matiere_organique"]
        municipalite = zone_de_gestion["municipalite"]
        serie_de_sol = zone_de_gestion["serie_de_sol"]
        taille_de_la_zone = zone_de_gestion["taille_de_la_zone"]

        try:
            assert serie_de_sol in series_de_sol_supportees
        except AssertionError:
            message_erreur = serie_de_sol + " n'est pas une série de sol supportée."
            abort(400, message_erreur)

        classe_de_drainage = zone_de_gestion["classe_de_drainage"]
        masse_volumique_apparente = zone_de_gestion["masse_volumique_apparente"]
        profondeur = zone_de_gestion["profondeur"]
        regies_sol_et_culture = __regie_sol_et_culture_mapping(zone_de_gestion["regies_sol_et_culture"])
        liste_zone_de_gestion.append(
            ZoneDeGestion(taux_matiere_organique, municipalite, serie_de_sol, classe_de_drainage,
                          masse_volumique_apparente, profondeur, regies_sol_et_culture, taille_de_la_zone))
    return liste_zone_de_gestion


def __regie_sol_et_culture_mapping(data):
    liste_regies = []
    cultures_fourrageres = get_cultures_fourrageres()
    iterateur_annee = 0
    postion_derniere_annee_de_simulation = len(data) - 1
    while iterateur_annee < len(data):
        if data[iterateur_annee]["culture_principale"] in cultures_fourrageres:
            culture_annee_suivante = data[iterateur_annee + 1]["culture_principale"]
            if iterateur_annee == postion_derniere_annee_de_simulation or culture_annee_suivante not in cultures_fourrageres:
                culture_principale = __culture_principale_mapping(data[iterateur_annee]["culture_principale"], True)
            else:
                culture_principale = __culture_principale_mapping(data[iterateur_annee]["culture_principale"], False)
        else:
            culture_principale = __culture_principale_mapping(data[iterateur_annee]["culture_principale"], False)
        culture_secondaire = __culture_secondaire_mapping(data[iterateur_annee]["culture_secondaire"])
        amendements = __amendements_mapping(data[iterateur_annee]["amendements"])
        travail_du_sol = __travail_du_sol_mapping(data[iterateur_annee]["travail_du_sol"])
        liste_regies.append(RegieDesSolsEtCultures(culture_principale, culture_secondaire, amendements, travail_du_sol))
        iterateur_annee += 1
    return liste_regies


def __travail_du_sol_mapping(data):
    travail_du_sol = data["travail_du_sol"]
    profondeur_du_travail = data["profondeur_du_travail"]
    types_travail_du_sol_supportee = get_types_travail_du_sol_supportes()

    try:
        assert travail_du_sol in types_travail_du_sol_supportee
    except AssertionError:
        message_erreur = travail_du_sol + " n'est pas un travail du sol supporté."
        abort(400, message_erreur)

    return TravailDuSol(travail_du_sol, profondeur_du_travail)


def __amendements_mapping(data):
    liste_amendement = []
    for amendement in data:
        liste_amendement.append(Amendement(amendement["amendement"], amendement["apport"]))
    return Amendements(liste_amendement)


def __culture_principale_mapping(data, est_derniere_annee_rotation_culture_fourragere):
    culture_principale = data["culture_principale"]
    rendement = data["rendement"]
    produit_non_recolte = data["produit_non_recolte"]
    proportion_tige_exporte = data["proportion_tige_exporte"]
    taux_matiere_seche = data["taux_matiere_seche"]
    cultures_supportees = get_cultures_principales_supportees()

    try:
        assert culture_principale in cultures_supportees
    except AssertionError:
        message_erreur = culture_principale + " n'est pas une culture supportée."
        abort(400, message_erreur)

    if taux_matiere_seche is None:
        return CulturePrincipale(culture_principale, rendement, proportion_tige_exporte, produit_non_recolte,
                                 est_derniere_annee_rotation_culture_fourragere)
    else:
        return CulturePrincipale(culture_principale, rendement, proportion_tige_exporte, produit_non_recolte,
                                 est_derniere_annee_rotation_culture_fourragere, taux_matiere_seche)


def __culture_secondaire_mapping(data):
    culture_secondaire = data["culture_secondaire"]
    periode_implantation = data["periode_implantation"]
    return CultureSecondaire(culture_secondaire, periode_implantation)
