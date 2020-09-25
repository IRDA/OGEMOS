from ICBM.BaseDeDonnees.database_querying import *


class RegieDesSolsEtCultures:
    def __init__(self, culture_pricipale, culture_secondaire, amendements, travail_du_sol):
        self.__annee_de_culture = None
        self.__culture_principale = culture_pricipale
        self.__culture_secondaire = culture_secondaire
        self.__amendements = amendements
        self.__travail_du_sol = travail_du_sol

    def calculer_apport_annuel_en_carbone_de_la_regie(self):
        culture_principale = self.__culture_principale.get_coefficient_calcul()
        culture_secondaire = self.__culture_secondaire.get_coefficient_calcul()
        apport_culture_principale = self.__culture_principale.calculer_apport_en_carbone_culture_principale()
        apport_culture_secondaire = self.__culture_secondaire.calculer_apport_en_carbone_culture_secondaire()
        apport_amendements = self.__amendements.calculer_apport_en_carbone_amendements()
        apport_culture_principale_racinaire = apport_culture_principale / (
                culture_principale.biomasse_aerienne_sur_racinaire + 1)
        apport_culture_principale_aerienne = apport_culture_principale_racinaire * culture_principale.biomasse_aerienne_sur_racinaire
        apport_culture_secondaire_racinaire = apport_culture_secondaire / (
                culture_secondaire.biomasse_aerienne_sur_racinaire + 1)
        apport_culture_secondaire_aerienne = apport_culture_secondaire_racinaire * culture_secondaire.biomasse_aerienne_sur_racinaire
        return ((apport_culture_principale
                 + apport_culture_secondaire
                 + apport_amendements)
                * self.__travail_du_sol.calculer_facteur_apport_en_carbone_travail_du_sol(),
                apport_culture_principale,
                apport_culture_secondaire,
                apport_amendements,
                apport_culture_principale_aerienne,
                apport_culture_principale_racinaire,
                apport_culture_secondaire_aerienne,
                apport_culture_secondaire_racinaire)

    def set_annee_de_culture(self, annee_de_culture):
        self.__annee_de_culture = annee_de_culture

    def calculer_coefficient_humification_residus_culture(self):
        return self.__culture_principale.get_coefficient_calcul().coefficient_humification_residus_culture

    def generer_bilan_regie(self):
        return {"annee_culture": self.__annee_de_culture,
                "culture_principale": self.__culture_principale.generer_bilan_culture_principale(),
                "culture_secondaire": self.__culture_secondaire.generer_bilan_culture_secondaire(),
                "amendements": self.__amendements.generer_bilan_amendements()}


class CulturePrincipale:

    def __init__(self, type_de_culture_principale, rendement, proportion_tige_exporte, produit_non_recolte,
                 est_derniere_annee_rotation_plante_fourragere, taux_matiere_seche=None):
        self.__coefficient_des_residus_de_culture = get_coefficients_des_residus_de_culture(type_de_culture_principale)
        self.__type_de_culture_principale = type_de_culture_principale
        self.__rendement = rendement
        if proportion_tige_exporte is not None:
            self.__proportion_tige_exporte = proportion_tige_exporte
        else:
            self.__proportion_tige_exporte = self.__coefficient_des_residus_de_culture.proportion_des_tiges_exportees
        self.__produit_non_recolte = produit_non_recolte
        self.__est_derniere_annee_rotation_plante_fourragere = est_derniere_annee_rotation_plante_fourragere
        if taux_matiere_seche is not None:
            self.__taux_matiere_seche = taux_matiere_seche
        else:
            self.__taux_matiere_seche = self.__coefficient_des_residus_de_culture.taux_matiere_seche

    def calculer_apport_en_carbone_culture_principale(self):
        conversion_de_ton_ha_a_kg_m2 = 1000 / 10000
        proportion_tige_laissee_au_champs = (1 - self.__proportion_tige_exporte)
        coefficient_de_calcul = get_coefficients_des_residus_de_culture(self.__type_de_culture_principale)
        if self.__type_de_culture_principale not in get_cultures_fourrageres():
            quantite_carbone_partie_recolte = self.__rendement * conversion_de_ton_ha_a_kg_m2 * coefficient_de_calcul.taux_carbone_chaque_partie * self.__taux_matiere_seche
            quantite_carbone_partie_tige_non_recolte = quantite_carbone_partie_recolte * (
                    coefficient_de_calcul.ratio_partie_tige_non_recolte / coefficient_de_calcul.ratio_partie_recolte) * proportion_tige_laissee_au_champs
            quantite_carbone_partie_racinaire = quantite_carbone_partie_recolte * (
                    coefficient_de_calcul.ratio_partie_racinaire / coefficient_de_calcul.ratio_partie_recolte)
            quantite_carbone_partie_extra_racinaire = quantite_carbone_partie_recolte * (
                    coefficient_de_calcul.ratio_partie_extra_racinaire / coefficient_de_calcul.ratio_partie_recolte)
            if self.__produit_non_recolte:
                return quantite_carbone_partie_recolte + quantite_carbone_partie_tige_non_recolte + quantite_carbone_partie_racinaire + quantite_carbone_partie_extra_racinaire
            else:
                return quantite_carbone_partie_tige_non_recolte + quantite_carbone_partie_racinaire + quantite_carbone_partie_extra_racinaire
        else:
            quantite_carbone_partie_recolte = self.__rendement * conversion_de_ton_ha_a_kg_m2 * coefficient_de_calcul.taux_carbone_chaque_partie * self.__taux_matiere_seche * proportion_tige_laissee_au_champs
            quantite_carbone_partie_racinaire = quantite_carbone_partie_recolte * (
                    coefficient_de_calcul.ratio_partie_racinaire / coefficient_de_calcul.ratio_partie_recolte)
            quantite_carbone_partie_extra_racinaire = quantite_carbone_partie_recolte * (
                    coefficient_de_calcul.ratio_partie_extra_racinaire / coefficient_de_calcul.ratio_partie_recolte)
            if self.__est_derniere_annee_rotation_plante_fourragere:
                return proportion_tige_laissee_au_champs  #quantite_carbone_partie_recolte + quantite_carbone_partie_racinaire + quantite_carbone_partie_extra_racinaire
            else:
                return proportion_tige_laissee_au_champs  #quantite_carbone_partie_recolte + quantite_carbone_partie_extra_racinaire

    def get_coefficient_calcul(self):
        return get_coefficients_des_residus_de_culture(self.__type_de_culture_principale)

    def generer_bilan_culture_principale(self):
        return {"culture_principale": self.__type_de_culture_principale}


class CultureSecondaire:
    def __init__(self, type_de_culture_secondaire, rendement):
        self.__type_de_culture_secondaire = type_de_culture_secondaire
        self.__rendement = rendement

    def calculer_apport_en_carbone_culture_secondaire(self):
        if self.__type_de_culture_secondaire is None:
            return 0
        conversion_de_ton_ha_a_kg_m2 = 1000 / 10000
        coefficient_de_calcul = get_coefficients_culture_secondaire(self.__type_de_culture_secondaire)
        proportion_tige_laissee_au_champs = (1 - coefficient_de_calcul.proportion_des_tiges_exportees)
        quantite_carbone_partie_recolte = self.__rendement * conversion_de_ton_ha_a_kg_m2 * coefficient_de_calcul.taux_carbone_chaque_partie * coefficient_de_calcul.taux_matiere_seche
        quantite_carbone_partie_tige_non_recolte = quantite_carbone_partie_recolte * (
                coefficient_de_calcul.ratio_partie_tige_non_recolte / coefficient_de_calcul.ratio_partie_recolte) * proportion_tige_laissee_au_champs
        quantite_carbone_partie_racinaire = quantite_carbone_partie_recolte * (
                coefficient_de_calcul.ratio_partie_racinaire / coefficient_de_calcul.ratio_partie_recolte)
        quantite_carbone_partie_extra_racinaire = quantite_carbone_partie_recolte * (
                coefficient_de_calcul.ratio_partie_extra_racinaire / coefficient_de_calcul.ratio_partie_recolte)
        return quantite_carbone_partie_recolte + quantite_carbone_partie_tige_non_recolte + quantite_carbone_partie_racinaire + quantite_carbone_partie_extra_racinaire

    def get_coefficient_calcul(self):
        return get_coefficients_culture_secondaire(self.__type_de_culture_secondaire)

    def generer_bilan_culture_secondaire(self):
        return {"culture_secondaire": self.__type_de_culture_secondaire}


class Amendements:
    def __init__(self, amendements):
        self.__amendements = amendements

    def calculer_apport_en_carbone_amendements(self):
        total_carbone_amendements = 0
        if len(self.__amendements) != 0:
            for amendement in self.__amendements:
                total_carbone_amendements += amendement.calculer_apport_en_carbone()
        return total_carbone_amendements

    def generer_bilan_amendements(self):
        amendements = []
        for amendement in self.__amendements:
            amendements.append(amendement.generer_bilan_amendement())
        return {"amendements": amendements}


class Amendement:
    def __init__(self, type_amendement, apport):
        self.__type_amendement = type_amendement
        self.__apport = apport

    def calculer_apport_en_carbone(self):
        ha_to_m2 = 1/10000
        if self.__type_amendement is None:
            return 0
        coefficient_de_calcul = get_coefficient_des_amendements(self.__type_amendement)
        quantite_carbone_amendement = self.__apport * coefficient_de_calcul.nitrogen_total * coefficient_de_calcul.carbon_nitrogen * ha_to_m2
        return quantite_carbone_amendement

    def generer_bilan_amendement(self):
        return {"amendement": self.__type_amendement, "apport": self.__apport}


class TravailDuSol:
    def __init__(self, type_de_travail_du_sol, profondeur_maximale_du_travail):
        self.__type_de_travail_du_sol = type_de_travail_du_sol
        self.__profondeur_maximale_du_travail = profondeur_maximale_du_travail

    def calculer_facteur_apport_en_carbone_travail_du_sol(self):
        return get_facteur_travail_du_sol(self.__type_de_travail_du_sol).facteur_travail_du_sol
