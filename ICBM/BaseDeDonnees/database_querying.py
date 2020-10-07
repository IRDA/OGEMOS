from ICBM.BaseDeDonnees.data_tables import *
from ICBM.database_setup import *


def get_facteur_climatique(municipalite):
    session = Session()
    query_result = session.query(TableDesMunicipalites).filter(
        TableDesMunicipalites.nom_municipalite == municipalite).one().utm
    session.close()
    return query_result


def get_facteur_groupe_textural(groupe_textural):
    session = Session()
    query_result = session.query(FacteurGroupeTextural).filter(
        FacteurGroupeTextural.groupe_textural == groupe_textural).one()
    session.close()
    return query_result


def get_groupes_texturaux_supportees():
    session = Session()
    query_result = []
    for groupe_textural in session.query(FacteurGroupeTextural.groupe_textural).all():
        query_result.append(groupe_textural.groupe_textural)
    session.close()
    return query_result


def get_coefficients_des_residus_de_culture(culture_principale):
    session = Session()
    query_result = session.query(CoefficientDesResidusDeCulture).filter(
        CoefficientDesResidusDeCulture.culture_principale == culture_principale).one()
    session.close()
    return query_result


def get_cultures_principales_supportees():
    session = Session()
    query_result = []
    for culture in session.query(CoefficientDesResidusDeCulture.culture_principale).all():
        query_result.append(culture.culture_principale)
    session.close()
    return query_result


def get_cultures_fourrageres():
    session = Session()
    query_result = []
    for culture in session.query(CoefficientDesResidusDeCulture).filter(
            CoefficientDesResidusDeCulture.est_culture_fourragere.is_(True)):
        query_result.append(culture.culture_principale)
    session.close()
    return query_result


def get_facteur_travail_du_sol(travail_du_sol):
    session = Session()
    query_result = session.query(FacteurTravailDuSol).filter(FacteurTravailDuSol.travail_du_sol == travail_du_sol).one()
    session.close()
    return query_result


def get_types_travail_du_sol_supportes():
    session = Session()
    query_result = []
    for travail in session.query(FacteurTravailDuSol.travail_du_sol).all():
        query_result.append(travail.travail_du_sol)
    session.close()
    return query_result


def get_coefficient_des_amendements(amendement):
    session = Session()
    query_result = session.query(CoefficientAmendements).filter(
        CoefficientAmendements.amendement == amendement).one()
    session.close()
    return query_result


def get_amendements_supportees():
    session = Session()
    query_result = []
    for amendement in session.query(CoefficientAmendements.amendement).all():
        query_result.append(amendement.amendement)
    session.close()
    return query_result


def get_classe_de_drainage(classe_de_drainage):
    session = Session()
    query_result = session.query(CoefficientClasseDeDrainage).filter(
        CoefficientClasseDeDrainage.classe_de_drainage == classe_de_drainage).one()
    session.close()
    return query_result


def get_classes_de_drainage_supportees():
    session = Session()
    query_result = []
    for classe_de_drainage in session.query(CoefficientClasseDeDrainage.classe_de_drainage).all():
        query_result.append(classe_de_drainage.classe_de_drainage)
    session.close()
    return query_result


def get_coefficients_culture_secondaire(culture_secondaire):
    session = Session()
    query_result = session.query(CoefficientDesCulturesSecondaires).filter(
        CoefficientDesCulturesSecondaires.culture_secondaire == culture_secondaire).one()
    session.close()
    return query_result


def get_cultures_secondaires_supportees():
    session = Session()
    query_result = []
    for cultures_secondaires in session.query(CoefficientDesCulturesSecondaires.culture_secondaire).all():
        query_result.append(cultures_secondaires.culture_secondaire)
    session.close()
    return query_result


def get_rendement_et_propriete_municipalite(municipalite):
    session = Session()
    query_result = session.query(TableDesMunicipalites).filter(
        TableDesMunicipalites.nom_municipalite == municipalite).one()
    session.close()
    return query_result


def get_municipalites_supportees():
    session = Session()
    query_result = []
    for municipalite in session.query(TableDesMunicipalites.nom_municipalite).all():
        query_result.append(municipalite.nom_municipalite)
    session.close()
    return query_result


def get_percentile50(utm, groupe_textural):
    session = Session()
    query_result = session.query(TablePercentile.percentile50).filter(
        TablePercentile.utm == utm, TablePercentile.groupe_textural == groupe_textural).one()
    session.close()
    return query_result


def get_percentile90(utm, groupe_textural):
    session = Session()
    query_result = session.query(TablePercentile.percentile90).filter(
        TablePercentile.utm == utm, TablePercentile.groupe_textural == groupe_textural).one()
    session.close()
    return query_result


def add_amendment(data):
    session = Session()
    nouvel_amendement = CoefficientAmendements(amendement=data["amendement"], matiere_seche=data["matiere_seche"],
                                               carbon_nitrogen=data["carbon_nitrogen"],
                                               nitrogen_total=data["nitrogen_total"],
                                               est_amendement_originel_ogemos=False)
    session.add(nouvel_amendement)
    session.commit()
