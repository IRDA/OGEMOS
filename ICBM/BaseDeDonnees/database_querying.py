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


def get_coefficients_des_residus_de_culture(culture_principale):
    session = Session()
    query_result = session.query(CoefficientDesResidusDeCulture).filter(
        CoefficientDesResidusDeCulture.culture_principale == culture_principale).one()
    session.close()
    return query_result
