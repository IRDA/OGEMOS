from ICBM.BaseDeDonnees.data_tables import *
from ICBM.database_setup import *

session = Session()


def get_facteur_climatique(region):
    return session.query(FacteurClimatique).filter(FacteurClimatique.region == region).one()


def get_facteur_series_de_sol(series_de_sol):
    return session.query(FacteurSerieDeSol).filter(FacteurSerieDeSol.serie_de_sol == series_de_sol).one()


def get_coefficients_des_residus_de_culture(culture_principale):
    return session.query(CoefficientDesResidusDeCulture).filter(
        CoefficientDesResidusDeCulture.culture_principale == culture_principale).one()

