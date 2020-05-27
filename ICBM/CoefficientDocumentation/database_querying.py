from ICBM.CoefficientDocumentation.data_tables import *
from ICBM.database_setup import *

session = Session()


def get_coefficients_des_residus_de_culture(culture_principale):
    return session.query(CoefficientDesResidusDeCulture).filter(
        CoefficientDesResidusDeCulture.culture_principale == culture_principale).first()


if __name__ == '__main__':
    print(get_coefficients_des_residus_de_culture('Avoine').culture_principale)
