from ICBM.BaseDeDonnees.data_tables import *
from ICBM.database_setup import *


def get_facteur_climatique(region):
    session = Session()
    query_result = session.query(FacteurClimatique).filter(FacteurClimatique.region == region).one()
    session.close()
    return query_result


def get_facteur_classe_texturale(classe_texturale):
    session = Session()
    query_result = session.query(FacteurClasseTexturale).filter(FacteurClasseTexturale.classe_texturale == classe_texturale).one()
    session.close()
    return query_result


def get_classes_texturales_supportees():
    session = Session()
    query_result = []
    for classe_texturale in session.query(FacteurClasseTexturale.classe_texturale).all():
        query_result.append(classe_texturale.classe_texturale)
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
    query_result = session.query(CoefficientDesAmendements).filter(
        CoefficientDesAmendements.amendement == amendement).one()
    session.close()
    return query_result


def get_amendements_supportees():
    session = Session()
    query_result = []
    for amendement in session.query(CoefficientDesAmendements.amendement).all():
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


def get_rendement_par_municipalite(municipalite):
    session = Session()
    query_result = session.query(TableDesRendements).filter(TableDesRendements.municipalite == municipalite).one()
    session.close()
    return query_result


def get_municipalites_supportees():
    session = Session()
    query_result = []
    for municipalite in session.query(TableDesRendements.municipalite).all():
        query_result.append(municipalite.municipalite)
    session.close()
    return query_result
