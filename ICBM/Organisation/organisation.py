from ICBM.BaseDeDonnees.database_querying import *


# TODO: trouver un meilleur nom pour le fichier et le directory
class EntrepriseAgricole:
    def __init__(self, nom_entreprise_agricole, champs):
        self.__nom_entreprise_agricole = nom_entreprise_agricole
        self.__champs = champs

    def appliquer_les_regies_pour_la_duree_de_la_simulation(self, annee_initiale, annee_finale):
        for champs in self.__champs:
            champs.appliquer_les_regies_pour_la_duree_de_la_simulation(annee_initiale, annee_finale)

    def calculer_carbone_organique_du_sol_pour_la_duree_de_la_simulation(self):
        for champs in self.__champs:
            champs.calculer_carbone_organique_du_sol_pour_la_duree_de_la_simulation()

    def calculer_carbone_organique_du_sol_pour_une_liste_de_champs_la_duree_de_la_simulation(self, liste_nom_de_champs):
        for champs in self.__champs:
            if champs in liste_nom_de_champs:
                champs.calculer_carbone_organique_du_sol_pour_la_duree_de_la_simulation()


class Champs:
    def __init__(self, nom_champs, zones_de_gestion):
        self.__nom_champs = nom_champs
        self.__zones_de_gestion = zones_de_gestion

    def appliquer_les_regies_pour_la_duree_de_la_simulation(self, annee_initiale, annee_finale):
        for zone_de_gestion in self.__zones_de_gestion:
            zone_de_gestion.appliquer_les_regies_pour_la_duree_de_la_simulation(annee_initiale, annee_finale)

    def calculer_carbone_organique_du_sol_pour_la_duree_de_la_simulation(self):
        for zone_de_gestion in self.__zones_de_gestion:
            zone_de_gestion.calculer_carbone_organique_du_sol_pour_la_duree_de_la_simulation()


class ZoneDeGestion:
    """
    :param taux_matiere_organique: taux de matière organique (%)
    :param masse_volumique_apparente: masse volumique apparente  1.318 par défaut(g/cm3)
    :param profondeur: profondeur donnée pour le calcul de la masse de carbone organique du sol (cm)
    :param municipalite: municipalite dans laquelle se trouve la zone de gestion
    :param serie_de_sol: série de sol de la zone de gestion
    :param classe_de_drainage: classe de drainage de la zone de gestion
    :param regies_sol_et_culture: Régies des sols constitué des cultures, amendement, etc, pour les quelques années
    qui correspondent à une rotation
    """

    def __init__(self, taux_matiere_organique, municipalite, serie_de_sol, classe_de_drainage,
                 masse_volumique_apparente, profondeur, regies_sol_et_culture, taille_de_la_zone):
        self.FACTEUR_CONVERSION_MATIERE_ORGANIQUE_CARBONE_ORGANIQUE_SOL = 1.724
        if masse_volumique_apparente is None:
            self.__masse_volumique_apparente = 1.318
        else:
            self.__masse_volumique_apparente = masse_volumique_apparente
        if profondeur is None:
            self.__profondeur = 17
        else:
            self.__profondeur = profondeur
        self.__taux_matiere_organique = taux_matiere_organique
        self.__municipalite = municipalite
        self.__serie_de_sol = serie_de_sol
        self.__classe_de_drainage = classe_de_drainage
        self.__coefficient_mineralisation_pool_jeune = self.__caculer_coefficient_mineralisation_pool_jeune()
        self.__coefficient_mineralisation_pool_vieux = self.__calculer_coefficient_mineralisation_pool_vieux()
        self.__facteur_climatique = self.__calculer_facteur_climatique()
        self.__regies_sol_et_culture = regies_sol_et_culture
        self.__regies_sol_et_culture_pour_la_duree_de_la_simulation = []
        self.__carbone_organique_initial_du_sol = self.__calculer_carbone_organique_initial_du_sol()
        self.__carbone_organique_du_sol_pour_la_duree_de_la_simulation = []

    def appliquer_les_regies_pour_la_duree_de_la_simulation(self, annee_initiale, annee_finale):
        if len(self.__regies_sol_et_culture) != 0:
            annee_courante = annee_initiale
            compteur_annee = 0
            while annee_courante <= annee_finale:
                regie_annee_courante = self.__regies_sol_et_culture[compteur_annee % len(self.__regies_sol_et_culture)]
                regie_annee_courante.set_annee_de_culture(annee_courante)
                self.__regies_sol_et_culture_pour_la_duree_de_la_simulation.append(regie_annee_courante)
                annee_courante += 1
                compteur_annee += 1

    """
    :returns carbone organique du sol initial ou TTS (total carbon at steady state) (kg C/m2)
    """

    def __calculer_carbone_organique_initial_du_sol(self):
        facteur_conversion_de_g_cm2_a_kg_m2 = 1000 / 100 ** 2
        conversion_pourcentage_taux_matiere_organique = 100
        facteur_conversion_de_matiere_organique_a_carbone_organique_du_sol = 1 / 1.724
        return self.__masse_volumique_apparente * self.__profondeur * \
               (
                       self.__taux_matiere_organique / conversion_pourcentage_taux_matiere_organique) * facteur_conversion_de_matiere_organique_a_carbone_organique_du_sol * facteur_conversion_de_g_cm2_a_kg_m2

    def calculer_carbone_organique_du_sol_pour_la_duree_de_la_simulation(self):
        if len(self.__regies_sol_et_culture_pour_la_duree_de_la_simulation) != 0:
            pool_carbone_jeune_initial = self.__calculer_pool_carbone_jeune_initial()
            pool_carbone_vieux_initial = self.__calculer_pool_carbone_vieux_initial(pool_carbone_jeune_initial)
            regie_annee_calcule, *regie_annee_simulation_restante = self.__regies_sol_et_culture_pour_la_duree_de_la_simulation
            self.__carbone_organique_du_sol_pour_la_duree_de_la_simulation.append(
                pool_carbone_jeune_initial + pool_carbone_vieux_initial)
            for regie_annee_de_simulation in regie_annee_simulation_restante:
                carbone_organique_du_sol = regie_annee_de_simulation.calculer_apport_annuel_en_carbone_de_la_regie() / (
                        self.__facteur_climatique * (
                        (1 / self.__coefficient_mineralisation_pool_jeune) + (
                        regie_annee_de_simulation.calculer_coefficient_humidification_residus_culture() / self.__coefficient_mineralisation_pool_vieux)))
                self.__carbone_organique_du_sol_pour_la_duree_de_la_simulation.append(carbone_organique_du_sol)

    def __calculer_pool_carbone_jeune_initial(self):
        if len(self.__regies_sol_et_culture_pour_la_duree_de_la_simulation):
            return self.__regies_sol_et_culture_pour_la_duree_de_la_simulation[
                       0].calculer_apport_annuel_en_carbone_de_la_regie() / (
                           self.__facteur_climatique * self.__coefficient_mineralisation_pool_jeune)
        else:
            return 0

    def __calculer_pool_carbone_vieux_initial(self, pool_carbone_jeune_initial):
        return self.__carbone_organique_initial_du_sol - pool_carbone_jeune_initial

    def __caculer_coefficient_mineralisation_pool_jeune(self):
        return get_facteur_series_de_sol(self.__serie_de_sol).coefficient_mineralisation_pool_jeune

    def __calculer_coefficient_mineralisation_pool_vieux(self):
        return get_facteur_series_de_sol(self.__serie_de_sol).coefficient_mineralisation_pool_vieux

    def __calculer_facteur_climatique(self):
        facteur_climatique = get_facteur_climatique(self.__obtenir_region_climatique_a_partir_de_municipalite())
        return facteur_climatique.facteur_temperature_sol * facteur_climatique.facteur_humidite_sol

    def __calculer_bilan_annuel_moyen(self):
        somme_des_bilan_annuel = 0
        for annee in self.__carbone_organique_du_sol_pour_la_duree_de_la_simulation:
            somme_des_bilan_annuel += annee
        return somme_des_bilan_annuel/len(self.__carbone_organique_du_sol_pour_la_duree_de_la_simulation)

    def __calculer_teneur_finale_projetee(self):
        return self.__carbone_organique_du_sol_pour_la_duree_de_la_simulation[len(self.__carbone_organique_du_sol_pour_la_duree_de_la_simulation)-1]

    def __calculer_difference_entre_teneur_initiale_et_finale(self):
        return self.__carbone_organique_du_sol_pour_la_duree_de_la_simulation[0] - self.__calculer_teneur_finale_projetee()

    def __obtenir_region_climatique_a_partir_de_municipalite(self):
        # TODO: enelver la dummy version et faire la vrai fonction
        if self.__municipalite == 'Victoriaville':
            return 'Centre-du-Québec'
