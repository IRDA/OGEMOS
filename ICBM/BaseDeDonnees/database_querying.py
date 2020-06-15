from ICBM.BaseDeDonnees.data_tables import *
from ICBM.database_setup import *


def get_facteur_climatique(region):
    session = Session()
    query_result = session.query(FacteurClimatique).filter(FacteurClimatique.region == region).one()
    session.close()
    return query_result


def get_facteur_series_de_sol(series_de_sol):
    session = Session()
    query_result = session.query(FacteurSerieDeSol).filter(FacteurSerieDeSol.serie_de_sol == series_de_sol).one()
    session.close()
    return query_result


def get_series_de_sol_supportees():
    session = Session()
    query_result = []
    for serie_de_sol in session.query(FacteurSerieDeSol.serie_de_sol).all():
        query_result.append(serie_de_sol.serie_de_sol)
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
