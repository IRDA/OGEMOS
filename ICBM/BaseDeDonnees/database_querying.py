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
    sesion = Session()
    query_result = []
    for culture in sesion.query(CoefficientDesResidusDeCulture).filter(
            CoefficientDesResidusDeCulture.est_culture_fourragere.is_(True)):
        query_result.append(culture.culture_principale)
    sesion.close()
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
