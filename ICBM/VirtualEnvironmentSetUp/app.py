from flask import Flask, request, jsonify, abort
from waitress import serve

from ICBM.Simulations.gestion_de_simulation import *
from ICBM.BaseDeDonnees.database_querying import *

app = Flask(__name__)


@app.route('/api/icbm-bilan', methods=['POST'])
def post_simulation():
    data_request = request.get_json()
    response = __launch_icbm_simulation(data_request)
    return jsonify(response)


@app.route('/api/ajout-amendement', methods=['POST'])
def ajout_amendement():
    data_request = request.get_json()
    response = __ajout_amendement(data_request)
    return jsonify(response)


@app.route('/api/post-amendement-ajoute', methods=['POST'])
def post_amendement():
    data_request = request.get_json()
    response = __ajout_amendements(data_request)
    return jsonify(response)


@app.route('/api/get-parametres-defauts-culture_principale', methods=['POST'])
def get_parametres_defauts_culture_principale():
    data_request = request.get_json()
    rendement = __get_rendement_defaut_municipalite(data_request["culture_principale"], data_request["municipalite"])
    coefficient_culture_principale = get_coefficients_des_residus_de_culture(data_request["culture_principale"])
    response = {"rendement": rendement,
                "pourcentage_tige_exportee": coefficient_culture_principale.pourcentage_des_tiges_exportees,
                "pourcentage_humidite": coefficient_culture_principale.pourcentage_humidite,
                "travail_du_sol_defaut": coefficient_culture_principale.travail_du_sol_defaut}
    return jsonify(response)


@app.route('/api/get-municipalite', methods=['GET'])
def get_municipalite():
    response = get_municipalites_supportees()
    response = {"municipalites_supportees": response}
    return jsonify(response)


@app.route('/api/get-groupe_textural', methods=['GET'])
def get_groupe_textural():
    response = get_groupes_texturaux_supportees()
    response = {"groupes_texturaux_supportees": response}
    return jsonify(response)


@app.route('/api/get-classe_de_drainage', methods=['GET'])
def get_classe_de_drainage():
    response = get_classes_de_drainage_supportees()
    response = {"classes_de_drainage_supportees": response}
    return jsonify(response)


@app.route('/api/get-culture_principale', methods=['GET'])
def get_culture_principale():
    response = get_cultures_principales_supportees()
    response = {"cultures_principales_supportees": response}
    return jsonify(response)


@app.route('/api/get-travail_du_sol', methods=['GET'])
def get_travail_du_sol():
    response = get_types_travail_du_sol_supportes()
    response = {"types_travail_du_sol_supportes": response}
    return jsonify(response)


@app.route('/api/get-culture_secondaire', methods=['GET'])
def get_culture_secondaire():
    response = get_cultures_secondaires_supportees()
    response = {"cultures_secondaires_supportees": response}
    return jsonify(response)


@app.route('/api/get-amendement', methods=['GET'])
def get_amendement():
    response = get_amendements_supportees()
    response = {"amendements_supportees": response}
    return jsonify(response)


@app.route('/api/get-amendement-ajoute', methods=['GET'])
def get_amendement_ajoutes():
    response = get_added_amendment()
    amendements = []
    for amendement in response:
        amendements.append(
            {"amendement": amendement.amendement, "pourcentage_humidite": (100 - amendement.matiere_seche),
             "carbon_total": amendement.carbon_total})
    response = {"amendements_ajoutes": amendements}
    return jsonify(response)


def is_decimal_number(string):
    if "." not in string and string.isdigit():
        return True
    if "." in string:
        decimal_parts = string.split(".")
        if len(decimal_parts) == 2 and decimal_parts[0].isdigit() and (
                decimal_parts[1].isdigit() or decimal_parts[1] == ""):
            return True
        else:
            return False
    return False


def __launch_icbm_simulation(data):
    gestion_simulation = __simulation_mapping(data["simulations"])
    return gestion_simulation.generer_les_bilans_pour_les_simulations_de_l_entreprise_agricole()


def __ajout_amendement(data):
    try:
        amendement = data["amendement"]
        amendement = amendement.split(" ")
        for amendement_parts in amendement:
            assert amendement_parts.isalnum()
    except AssertionError:
        message_erreur = data[
                             "amendement"] + " n'est pas un amendement valide. Uniquement caractères alphanumériques acceptés."
        abort(400, message_erreur)
    try:
        assert is_decimal_number(data["pourcentage_humidite"])
    except AssertionError:
        message_erreur = data[
                             "pourcentage_humidite"] + " n'est pas un pourcentage d'humidité valide. Uniquement caractères numériques et le \".\" acceptés."
        abort(400, message_erreur)
    try:
        if is_decimal_number(data["pourcentage_humidite"]):
            assert 0 <= float(data["pourcentage_humidite"]) <= 100
    except AssertionError:
        message_erreur = data[
                             "pourcentage_humidite"] + " n'est pas un pourcentage d'humidité valide. Doit être un réel dans l'intervalle [0-100]."
        abort(400, message_erreur)
    try:
        assert is_decimal_number(data["carbon_total"])
    except AssertionError:
        message_erreur = data[
                             "carbon_total"] + " n'est pas un total d'azote valide. Uniquement caractères numériques et le \".\" acceptés."
        abort(400, message_erreur)
    add_amendment(data)


def __ajout_amendements(data):
    for amendement in data["amendements_ajoutes"]:
        try:
            assert amendement["amendement"].isalnum()
        except AssertionError:
            message_erreur = amendement[
                                 "amendement"] + " n'est pas un amendement valide. Uniquement caractères alphanumériques acceptés."
            abort(400, message_erreur)
        try:
            assert isinstance(amendement["pourcentage_humidite"], float) and 0 <= float(
                amendement["pourcentage_humidite"]) <= 100
        except AssertionError:
            message_erreur = str(amendement[
                                     "pourcentage_humidite"]) + " n'est pas un pourcentage d'humidité valide. Doit être un réel dans l'intervalle [0-100]."
            abort(400, message_erreur)
        try:
            assert isinstance(amendement["carbon_total"], float)
        except AssertionError:
            message_erreur = str(amendement[
                                     "carbon_total"]) + " n'est pas un total d'azote valide. Uniquement caractères numériques et le \".\" acceptés."
            abort(400, message_erreur)
        add_amendment(amendement)


def __simulation_mapping(data):
    gestion_simulation = GestionSimulation()
    for simulation in data:
        annee_initiale = simulation["annee_initiale_projection"]
        annee_finale = simulation["annee_finale_projection"]
        nom_simulation = simulation["nom_simulation"]

        try:
            assert isinstance(annee_initiale, int)
        except AssertionError:
            message_erreur = str(annee_initiale) + " n'est pas une annee initiale valide. Voir documentation API."
            abort(400, message_erreur)

        try:
            assert isinstance(annee_finale, int)
        except AssertionError:
            message_erreur = str(annee_finale) + " n'est pas un nom d'entreprise valide. Voir documentation API."
            abort(400, message_erreur)

        entreprise_agricole = __entreprise_agricole_mapping(simulation["entreprise_agricole"])

        gestion_simulation.ajouter_une_simulation(Simulation(annee_initiale, annee_finale, entreprise_agricole, nom_simulation))
    return gestion_simulation


def __entreprise_agricole_mapping(data):
    entreprise_nom = data["nom"]
    champs = __champs_mapping(data["champs"])

    try:
        assert isinstance(entreprise_nom, str)
    except AssertionError:
        message_erreur = str(entreprise_nom) + " n'est pas un nom d'entreprise valide. Voir documentation API."
        abort(400, message_erreur)

    return EntrepriseAgricole(entreprise_nom, champs)


def __champs_mapping(data):
    liste_champs = []
    for champs in data:
        nom_champs = champs["nom"]
        zones_de_gestion = __zone_de_gestion_mapping(champs["zones_de_gestion"])

        try:
            assert isinstance(nom_champs, str)
        except AssertionError:
            message_erreur = str(nom_champs) + " n'est pas un nom d'entreprise valide. Voir documentation API."
            abort(400, message_erreur)

        liste_champs.append(Champs(nom_champs, zones_de_gestion))
    return liste_champs


def __zone_de_gestion_mapping(data):
    liste_zone_de_gestion = []
    groupes_texturaux_supportees = get_groupes_texturaux_supportees()
    classe_de_drainage_supportees = get_classes_de_drainage_supportees()
    for zone_de_gestion in data:
        taux_matiere_organique = zone_de_gestion["taux_matiere_organique"]
        municipalite = zone_de_gestion["municipalite"]
        groupe_textural = zone_de_gestion["groupe_textural"]
        superficie_de_la_zone = zone_de_gestion["superficie_de_la_zone"]
        classe_de_drainage = zone_de_gestion["classe_de_drainage"]
        masse_volumique_apparente = zone_de_gestion["masse_volumique_apparente"]
        profondeur = zone_de_gestion["profondeur"]
        regies_sol_et_culture_projection = __regie_sol_et_culture_mapping(
            zone_de_gestion["regies_sol_et_culture_projection"], municipalite)
        regies_sol_et_culture_historique = __regie_sol_et_culture_mapping(
            zone_de_gestion["regies_sol_et_culture_historique"], municipalite)

        try:
            assert groupe_textural in groupes_texturaux_supportees
        except AssertionError:
            message_erreur = str(groupe_textural) + " n'est pas un groupe textural supportée."
            abort(400, message_erreur)

        try:
            assert isinstance(taux_matiere_organique, (float, int))
        except AssertionError:
            message_erreur = str(
                taux_matiere_organique) + " n'est pas un taux de matière organique valide. Voir documentation API."
            abort(400, message_erreur)
        try:
            assert isinstance(municipalite, str)
        except AssertionError:
            message_erreur = str(municipalite) + " n'est pas une municipalité valide. Voir documentation API."
            abort(400, message_erreur)

        try:
            assert municipalite in get_municipalites_supportees()
        except AssertionError:
            message_erreur = str(municipalite) + " n'est pas une municipalité supportée."
            abort(400, message_erreur)

        try:
            assert isinstance(superficie_de_la_zone, (float, int)) and superficie_de_la_zone > 0
        except AssertionError:
            message_erreur = str(
                superficie_de_la_zone) + " n'est pas une taille de la zone de gestion valide. Voir documentation API."
            abort(400, message_erreur)

        try:
            assert classe_de_drainage in classe_de_drainage_supportees
        except AssertionError:
            message_erreur = str(
                classe_de_drainage) + " n'est pas une classe de drainage supportée."
            abort(400, message_erreur)

        try:
            assert isinstance(masse_volumique_apparente, (float, int)) or masse_volumique_apparente is None
            if masse_volumique_apparente is not None:
                assert masse_volumique_apparente > 0
        except AssertionError:
            message_erreur = str(
                masse_volumique_apparente) + " n'est pas une nom masse_volumique_apparente valide. Voir documentation API."
            abort(400, message_erreur)

        try:
            assert isinstance(profondeur, (float, int)) or profondeur is None
            if profondeur is not None:
                assert profondeur > 0
        except AssertionError:
            message_erreur = str(profondeur) + " n'est pas une profondeur valide. Voir documentation API."
            abort(400, message_erreur)

        liste_zone_de_gestion.append(
            ZoneDeGestion(taux_matiere_organique, municipalite, groupe_textural, classe_de_drainage,
                          masse_volumique_apparente, profondeur, superficie_de_la_zone,
                          regies_sol_et_culture_projection, regies_sol_et_culture_historique))
    return liste_zone_de_gestion


def __regie_sol_et_culture_mapping(data, municipalite):
    liste_regies = []
    cultures_fourrageres = get_cultures_fourrageres()
    iterateur_annee = 0
    postion_derniere_annee_de_simulation = len(data) - 1
    while iterateur_annee < len(data):
        if data[iterateur_annee] is None:
            liste_regies.append(None)
        else:
            if data[iterateur_annee]["culture_principale"] in cultures_fourrageres:
                culture_annee_suivante = data[iterateur_annee + 1]["culture_principale"]
                if iterateur_annee == postion_derniere_annee_de_simulation or culture_annee_suivante not in cultures_fourrageres:
                    culture_principale = __culture_principale_mapping(data[iterateur_annee]["culture_principale"], True,
                                                                      municipalite)
                else:
                    culture_principale = __culture_principale_mapping(data[iterateur_annee]["culture_principale"],
                                                                      False,
                                                                      municipalite)
            else:
                culture_principale = __culture_principale_mapping(data[iterateur_annee]["culture_principale"], False,
                                                                  municipalite)
            culture_secondaire = __culture_secondaire_mapping(data[iterateur_annee]["culture_secondaire"])
            amendements = __amendements_mapping(data[iterateur_annee]["amendements"])
            travail_du_sol = __travail_du_sol_mapping(data[iterateur_annee]["travail_du_sol"])
            liste_regies.append(
                RegieDesSolsEtCultures(culture_principale, culture_secondaire, amendements, travail_du_sol))
        iterateur_annee += 1
    return liste_regies


def __travail_du_sol_mapping(data):
    travail_du_sol = data["travail_du_sol"]
    types_travail_du_sol_supportee = get_types_travail_du_sol_supportes()

    try:
        assert travail_du_sol in types_travail_du_sol_supportee
    except AssertionError:
        message_erreur = str(travail_du_sol) + " n'est pas un travail du sol supporté."
        abort(400, message_erreur)

    return TravailDuSol(travail_du_sol)


def __amendements_mapping(data):
    liste_amendement = []
    for amendement in data:
        if amendement["amendement"] is None and amendement["apport"] is None:
            liste_amendement.append(Amendement(amendement["amendement"], amendement["apport"]))
        else:
            try:
                assert isinstance(amendement["apport"], (float, int))
            except AssertionError:
                message_erreur = str(amendement["apport"]) + " n'est pas un apport valide. Voir documentation API."
                abort(400, message_erreur)

            try:
                assert amendement["amendement"] in get_amendements_supportees()
            except AssertionError:
                message_erreur = str(amendement["amendement"]) + " n'est pas un amendement supporté."
                abort(400, message_erreur)

            liste_amendement.append(Amendement(amendement["amendement"], amendement["apport"]))
    return Amendements(liste_amendement)


def __culture_principale_mapping(data, est_derniere_annee_rotation_culture_fourragere, municipalite):
    culture_principale = data["culture_principale"]
    cultures_supportees = get_cultures_principales_supportees()
    try:
        assert culture_principale in cultures_supportees
    except AssertionError:
        message_erreur = str(culture_principale) + " n'est pas une culture principale supportée."
        abort(400, message_erreur)

    if data["rendement"] is None:
        rendement = __get_rendement_defaut_municipalite(culture_principale, municipalite)

    else:
        rendement = data["rendement"]
    produit_non_recolte = data["produit_recolte"]
    pourcentage_tige_exporte = data["pourcentage_tige_exporte"]
    pourcentage_humidite = data["pourcentage_humidite"]

    try:
        assert isinstance(rendement, (float, int)) and rendement >= 0
    except AssertionError:
        message_erreur = str(rendement) + " n'est pas un rendement valide. Voir documentation API."
        abort(400, message_erreur)

    try:
        assert isinstance(produit_non_recolte, bool)
    except AssertionError:
        message_erreur = str(produit_non_recolte) + " n'est pas une produit non récolté valide. Voir documentation API."
        abort(400, message_erreur)

    try:
        assert (isinstance(pourcentage_tige_exporte,
                           (float, int)) and 0 <= pourcentage_tige_exporte <= 100) or pourcentage_tige_exporte is None
    except AssertionError:
        message_erreur = str(
            pourcentage_tige_exporte) + " n'est pas une pourcentage tige exporte valide. Voir documentation API."
        abort(400, message_erreur)

    try:
        assert isinstance(pourcentage_humidite, (float, int)) or pourcentage_humidite is None
        if pourcentage_humidite is not None:
            assert pourcentage_humidite > 0
    except AssertionError:
        message_erreur = str(
            pourcentage_humidite) + " n'est pas un pourcentage d'humidité valide. Voir documentation API."
        abort(400, message_erreur)

    if pourcentage_humidite is None:
        return CulturePrincipale(culture_principale, rendement, pourcentage_tige_exporte, produit_non_recolte,
                                 est_derniere_annee_rotation_culture_fourragere)
    else:
        return CulturePrincipale(culture_principale, rendement, pourcentage_tige_exporte, produit_non_recolte,
                                 est_derniere_annee_rotation_culture_fourragere, pourcentage_humidite)


def __get_rendement_defaut_municipalite(culture_principale, municipalite):
    rendements = get_rendement_et_propriete_municipalite(municipalite)
    if culture_principale == "Avoine":
        rendement = rendements.rendement_avoine
    elif culture_principale == "Blé":
        rendement = rendements.rendement_ble
    elif culture_principale == "Maïs fourrager":
        rendement = rendements.rendement_mais_fourrager
    elif culture_principale == "Orge":
        rendement = rendements.rendement_orge
    elif culture_principale == "Maïs grain":
        rendement = rendements.rendement_mais_grain
    elif culture_principale == "Soya":
        rendement = rendements.rendement_soya
    elif culture_principale == "Haricot":
        rendement = rendements.rendement_haricot
    elif culture_principale == "Pommes de terre - semence":
        rendement = rendements.rendement_pomme_de_terre_de_semence
    elif culture_principale == "Pommes de terre - table":
        rendement = rendements.rendement_pomme_de_terre_de_table
    elif culture_principale == "Pommes de terre - transformation":
        rendement = rendements.rendement_pomme_de_terre_de_transformation
    elif culture_principale == "Seigle":
        rendement = rendements.rendement_seigle
    elif culture_principale == "Triticale":
        rendement = rendements.rendement_triticale
    elif culture_principale == "Canola":
        rendement = rendements.rendement_canola
    else:
        rendement = rendements.rendement_foin
    return rendement


def __culture_secondaire_mapping(data):
    culture_secondaire = data["culture_secondaire"]
    rendement = data["rendement"]

    if culture_secondaire is None and rendement is None:
        return CultureSecondaire(culture_secondaire, 0)

    try:
        assert culture_secondaire in get_cultures_secondaires_supportees()
    except AssertionError:
        message_erreur = str(culture_secondaire) + " n'est pas une culture secondaire supportée."
        abort(400, message_erreur)

    try:
        assert isinstance(rendement, float)
    except AssertionError:
        message_erreur = str(
            rendement) + " n'est pas une période d'implantation valide. Voir documentation API."
        abort(400, message_erreur)

    return CultureSecondaire(culture_secondaire, rendement)


if __name__ == '__main__':
    serve(app, host="127.0.0.1", port=5000)
