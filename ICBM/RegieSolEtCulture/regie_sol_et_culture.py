from ICBM.CoefficientDocumentation import database_querying

class RegieDesSolsEtCultures:
    def __init__(self, culture_pricipale, culture_secondaire, amendements, travail_du_sol):
        self.__annee_de_culture = None
        self.__culture_principale = culture_pricipale
        self.__culture_secondaire = culture_secondaire
        self.__amendements = amendements
        self.__travail_du_sol = travail_du_sol

    def calculer_apport_annuel_en_carbone_de_la_regie(self):
        return self.__culture_principale.calculer_apport_en_carbone_culture_principale() \
               + self.__culture_secondaire.calculer_apport_en_carbone_culture_secondaire() \
               + self.__amendements.calculer_apport_en_carbone_amendements() \
               + self.__travail_du_sol.calculer_apport_en_carbone_travail_du_sol()

    def set_annee_de_culture(self, annee_de_culture):
        self.__annee_de_culture = annee_de_culture


class CulturePrincipale:
    def __init__(self, type_de_culture_principale, rendement, recolte_residu):
        self.__type_de_culture_principale = type_de_culture_principale
        self.__rendement = rendement
        self.__recolte_residu = recolte_residu

    def calculer_apport_en_carbone_culture_principale(self):
        instance = database_querying.get_coefficients_des_residus_de_culture(self.__type_de_culture_principale)
        print(instance)


class CultureSecondaire:
    def __init__(self, type_de_culture_secondaire, periode_implantation):
        self.__type_de_culture_secondaire = type_de_culture_secondaire
        self.__periode_implantation = periode_implantation

    def calculer_apport_en_carbone_culture_secondaire(self):
        pass  # TODO: calculer l'apport en carbone de la culture secondaire


class Amendements:
    def __init__(self, amendements):
        self.__amendements = amendements

    def calculer_apport_en_carbone_amendements(self):
        total_carbone_amendements = 0
        if self.__amendements.size() != 0:
            for amendement in self.__amendements:
                total_carbone_amendements += amendement.calculer_apport_en_carbone()
            return total_carbone_amendements


class Amendement:
    def __init__(self, type_amendement):
        self.__type_amendement = type_amendement
        self.__taux_apport_specifique = None
        self.__taux_humidite = None

    def calculer_apport_en_carbone(self):
        pass  # TODO: calculer l'apport en carbone de l'amendement


class TravailDuSol:
    def __init__(self, type_de_travail_du_sol, profondeur_maximale_du_travail):
        self.__type_de_travail_du_sol = type_de_travail_du_sol
        self.__profondeur_maximale_du_travail = profondeur_maximale_du_travail

    def calculer_apport_en_carbone_travail_du_sol(self):
        pass  # TODO: calculer l'apport en carbone du trravail du sol


if __name__ == '__main__':
    cp = CulturePrincipale('Avoine', 1, True)
    cp.calculer_apport_en_carbone_culture_principale()
