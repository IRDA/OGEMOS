from ICBM.BaseDeDonnees.database_querying import *


class EntrepriseAgricole:
    def __init__(self, nom_entreprise_agricole, champs):
        self.__nom_entreprise_agricole = nom_entreprise_agricole
        self.__champs = champs
        self.__taille_entreprise = self.__calculer_la_taille_de_l_entreprise()

    def appliquer_les_regies_pour_la_duree_de_la_simulation(self, annee_initiale, annee_finale):
        for champs in self.__champs:
            champs.appliquer_les_regies_pour_la_duree_de_la_simulation(annee_initiale, annee_finale)

    def __calculer_moyenne_ponderee_entreprise_via_superficie_champs(self, bilans_des_champs):
        bilan_annuel_moyen_ponderee_entreprise = []
        for bilan_du_champs in bilans_des_champs:
            bilan_annuel_moyen_ponderee_champs = bilan_du_champs["bilan_champs_pondere"]
            ponderation_champs = bilan_du_champs["taille_du_champs"] / self.__taille_entreprise
            annee = 0
            while annee < len(bilan_annuel_moyen_ponderee_champs):
                if len(bilan_annuel_moyen_ponderee_entreprise) < len(bilan_annuel_moyen_ponderee_champs):
                    bilan_annuel_moyen_ponderee_entreprise.append(
                        bilan_annuel_moyen_ponderee_champs[annee] * ponderation_champs)
                else:
                    bilan_annuel_moyen_ponderee_entreprise[annee] += bilan_annuel_moyen_ponderee_champs[annee] * ponderation_champs
                annee += 1
        return bilan_annuel_moyen_ponderee_entreprise

    def __calculer_la_taille_de_l_entreprise(self):
        taille_de_l_entreprise = 0
        for champs in self.__champs:
            taille_de_l_entreprise += champs.get_taille_du_champs()
        return taille_de_l_entreprise

    def generer_le_bilan_entreprise(self):
        bilans_des_champs = []
        for champs in self.__champs:
            bilans_des_champs.append(champs.generer_le_bilan_des_champs())
        bilan_entreprise_ponderee = self.__calculer_moyenne_ponderee_entreprise_via_superficie_champs(bilans_des_champs)
        return {"bilan_entreprise_ponderee": bilan_entreprise_ponderee, "bilans_des_champs": bilans_des_champs}


class Champs:
    def __init__(self, nom_champs, zones_de_gestion):
        self.__nom_champs = nom_champs
        self.__zones_de_gestion = zones_de_gestion
        self.__taille_du_champs = self.__calculer_la_taille_du_champs()

    def appliquer_les_regies_pour_la_duree_de_la_simulation(self, annee_initiale, annee_finale):
        for zone_de_gestion in self.__zones_de_gestion:
            zone_de_gestion.appliquer_les_regies_pour_la_duree_de_la_simulation(annee_initiale, annee_finale)

    def __calculer_moyenne_ponderee_champs_via_superficie_zone_de_gestion(self, bilan_des_zones):
        bilan_annuel_moyen_ponderee_champs = []
        for bilan_de_zone in bilan_des_zones:
            bilan_annuel_zone = bilan_de_zone["bilan_carbone_de_la_zone_pour_la_simulation"]
            ponderation_zone = bilan_de_zone["taille_de_la_zone"] / self.__taille_du_champs
            annee = 0
            while annee < len(bilan_annuel_zone):
                if len(bilan_annuel_moyen_ponderee_champs) < len(bilan_annuel_zone):
                    bilan_annuel_moyen_ponderee_champs.append(bilan_annuel_zone[annee] * ponderation_zone)
                else:
                    bilan_annuel_moyen_ponderee_champs[annee] += bilan_annuel_zone[annee] * ponderation_zone
                annee += 1
        return bilan_annuel_moyen_ponderee_champs

    def __calculer_la_taille_du_champs(self):
        taille_du_champs = 0
        for zone in self.__zones_de_gestion:
            taille_du_champs += zone.get_taille_de_la_zone()
        return taille_du_champs

    def get_taille_du_champs(self):
        return self.__taille_du_champs

    def generer_le_bilan_des_champs(self):
        bilans_des_zones = []
        for zone_de_gestion in self.__zones_de_gestion:
            bilans_des_zones.append(zone_de_gestion.generer_le_bilan_de_zone())
        bilan_champs_ponderee = self.__calculer_moyenne_ponderee_champs_via_superficie_zone_de_gestion(
            bilans_des_zones)
        return {"bilans_des_zones": bilans_des_zones, "bilan_champs_pondere": bilan_champs_ponderee,
                "taille_du_champs": self.__taille_du_champs, "nom_du_champs": self.__nom_champs,
                "nombre_de_zone_de_gestion": len(self.__zones_de_gestion)}


class ZoneDeGestion:
    """
    :param taux_matiere_organique: taux de matière organique (%)
    :param masse_volumique_apparente: masse volumique apparente  1.318 par défaut(g/cm3)
    :param profondeur: profondeur donnée pour le calcul de la masse de carbone organique du sol (cm)
    :param municipalite: municipalite dans laquelle se trouve la zone de gestion
    :param classe_texturale: classe texturale de la zone de gestion
    :param classe_de_drainage: classe de drainage de la zone de gestion
    :param regies_sol_et_culture_projection: Régies des sols constitué des cultures, amendement, etc, pour les quelques années
    qui correspondent à une rotation
    """

    def __init__(self, taux_matiere_organique, municipalite, classe_texturale, classe_de_drainage,
                 masse_volumique_apparente, profondeur, taille_de_la_zone, regies_sol_et_culture_projection,
                 regies_sol_et_culture_historique):
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
        self.__classe_texturale = classe_texturale
        self.__classe_de_drainage = classe_de_drainage
        self.__coefficient_mineralisation_pool_jeune = self.__calculer_coefficient_mineralisation_pool_jeune()
        self.__coefficient_mineralisation_pool_vieux = self.__calculer_coefficient_mineralisation_pool_vieux()
        self.__facteur_climatique = self.__calculer_facteur_climatique()
        self.__regies_sol_et_culture_projection = regies_sol_et_culture_projection
        if regies_sol_et_culture_historique is None:
            self.__regies_sol_et_culture_historique = []
        else:
            self.__regies_sol_et_culture_historique = regies_sol_et_culture_historique
        self.__regies_sol_et_culture_pour_la_duree_de_la_simulation = []
        self.__carbone_organique_initial_du_sol = self.__calculer_carbone_organique_initial_du_sol()
        self.__taille_de_la_zone_de_gestion = taille_de_la_zone

    def appliquer_les_regies_pour_la_duree_de_la_simulation(self, annee_initiale, annee_finale):
        if len(self.__regies_sol_et_culture_historique) != 0:
            annee_courante = annee_initiale - len(self.__regies_sol_et_culture_historique)
            compteur_annee = 0
            while annee_courante < annee_initiale:
                regie_annee_courante = self.__regies_sol_et_culture_historique[compteur_annee]
                regie_annee_courante.set_annee_de_culture(annee_courante)
                self.__regies_sol_et_culture_pour_la_duree_de_la_simulation.append(regie_annee_courante)
                annee_courante += 1
                compteur_annee += 1
        if len(self.__regies_sol_et_culture_projection) != 0:
            annee_courante = annee_initiale
            compteur_annee = 0
            while annee_courante <= annee_finale:
                regie_annee_courante = self.__regies_sol_et_culture_projection[
                    compteur_annee % len(self.__regies_sol_et_culture_projection)]
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
        facteur_conversion_de_matiere_organique_a_carbone_organique_du_sol = 1 / self.FACTEUR_CONVERSION_MATIERE_ORGANIQUE_CARBONE_ORGANIQUE_SOL
        return self.__masse_volumique_apparente * self.__profondeur * \
               (
                       self.__taux_matiere_organique / conversion_pourcentage_taux_matiere_organique) * facteur_conversion_de_matiere_organique_a_carbone_organique_du_sol * facteur_conversion_de_g_cm2_a_kg_m2

    def __calculer_carbone_organique_du_sol_pour_la_duree_de_la_simulation(self):
        carbone_organique_du_sol_pour_la_duree_de_la_simulation = []
        apport_carbone_culture_principale = []
        apport_carbone_culture_secondaire = []
        apport_carbone_amendements = []
        if len(self.__regies_sol_et_culture_pour_la_duree_de_la_simulation) != 0:
            pool_carbone_jeune_initial = self.__calculer_pool_carbone_jeune_initial()
            pool_carbone_vieux_initial = self.__calculer_pool_carbone_vieux_initial(pool_carbone_jeune_initial)
            regie_annee_calcule, *regie_annee_simulation_restante = self.__regies_sol_et_culture_pour_la_duree_de_la_simulation
            carbone_organique_du_sol_pour_la_duree_de_la_simulation.append(
                pool_carbone_jeune_initial + pool_carbone_vieux_initial)
            carbone_total_annee_initiale = self.__regies_sol_et_culture_pour_la_duree_de_la_simulation[0].calculer_apport_annuel_en_carbone_de_la_regie()
            apport_carbone_culture_principale.append(carbone_total_annee_initiale[1])
            apport_carbone_culture_secondaire.append(carbone_total_annee_initiale[2])
            apport_carbone_amendements.append(carbone_total_annee_initiale[3])
            for regie_annee_de_simulation in regie_annee_simulation_restante:
                apports_annuel_de_carbone = regie_annee_de_simulation.calculer_apport_annuel_en_carbone_de_la_regie()
                apport_annuel_total_a_la_regie = apports_annuel_de_carbone[0]
                apport_carbone_culture_principale.append(apports_annuel_de_carbone[1])
                apport_carbone_culture_secondaire.append(apports_annuel_de_carbone[2])
                apport_carbone_amendements.append(apports_annuel_de_carbone[3])
                carbone_organique_du_sol = apport_annuel_total_a_la_regie / (
                        self.__facteur_climatique * (
                        (1 / self.__coefficient_mineralisation_pool_jeune) + (
                        regie_annee_de_simulation.calculer_coefficient_humification_residus_culture() / self.__coefficient_mineralisation_pool_vieux)))
                carbone_organique_du_sol_pour_la_duree_de_la_simulation.append(carbone_organique_du_sol)
            return carbone_organique_du_sol_pour_la_duree_de_la_simulation, \
                   apport_carbone_culture_principale, \
                   apport_carbone_culture_secondaire, \
                   apport_carbone_amendements

    def __calculer_pool_carbone_jeune_initial(self):
        if len(self.__regies_sol_et_culture_pour_la_duree_de_la_simulation):
            return self.__regies_sol_et_culture_pour_la_duree_de_la_simulation[
                       0].calculer_apport_annuel_en_carbone_de_la_regie()[0] / (
                           self.__facteur_climatique * self.__coefficient_mineralisation_pool_jeune)
        else:
            return 0

    def __calculer_pool_carbone_vieux_initial(self, pool_carbone_jeune_initial):
        return self.__carbone_organique_initial_du_sol - pool_carbone_jeune_initial

    def __calculer_coefficient_mineralisation_pool_jeune(self):
        return get_facteur_classe_texturale(self.__classe_texturale).coefficient_mineralisation_pool_jeune

    def __calculer_coefficient_mineralisation_pool_vieux(self):
        return get_facteur_classe_texturale(self.__classe_texturale).coefficient_mineralisation_pool_vieux

    def __calculer_facteur_climatique(self):
        facteur_climatique = get_facteur_climatique(self.__municipalite)
        return facteur_climatique.facteur_temperature_sol * facteur_climatique.facteur_humidite_sol

    def __calculer_bilan_annuel_moyen(self, carbone_organique_du_sol_pour_la_duree_de_la_simulation):
        somme_des_bilan_annuel = 0
        for annee in carbone_organique_du_sol_pour_la_duree_de_la_simulation:
            somme_des_bilan_annuel += annee
        if len(carbone_organique_du_sol_pour_la_duree_de_la_simulation) > 0:
            return somme_des_bilan_annuel / len(carbone_organique_du_sol_pour_la_duree_de_la_simulation)

    def __calculer_teneur_finale_projetee(self, carbone_organique_du_sol_pour_la_duree_de_la_simulation):
        return carbone_organique_du_sol_pour_la_duree_de_la_simulation[
            len(carbone_organique_du_sol_pour_la_duree_de_la_simulation) - 1]

    def __calculer_difference_entre_teneur_initiale_et_finale(self,
                                                              carbone_organique_du_sol_pour_la_duree_de_la_simulation,
                                                              teneur_finale_projetee):
        return teneur_finale_projetee - carbone_organique_du_sol_pour_la_duree_de_la_simulation[0]

    def __calculer_moyenne_de_chaque_annee_de_rotation_dans_la_projection(self,
                                                                          carbone_organique_de_sol_pour_la_duree_de_la_simulation):
        moyenne_de_chaque_annee_de_rotation = []
        nombre_de_repetition_de_annee_de_rotation = []
        for index_annee in range(len(self.__regies_sol_et_culture_historique), len(carbone_organique_de_sol_pour_la_duree_de_la_simulation)):
            if index_annee < len(self.__regies_sol_et_culture_projection):
                moyenne_de_chaque_annee_de_rotation.append(
                    carbone_organique_de_sol_pour_la_duree_de_la_simulation[index_annee])
                nombre_de_repetition_de_annee_de_rotation.append(1)
            else:
                moyenne_de_chaque_annee_de_rotation[index_annee % len(self.__regies_sol_et_culture_projection)] += \
                    carbone_organique_de_sol_pour_la_duree_de_la_simulation[index_annee]
                nombre_de_repetition_de_annee_de_rotation[
                    index_annee % len(self.__regies_sol_et_culture_projection)] += 1
        for index_annee in range(len(moyenne_de_chaque_annee_de_rotation)):
            moyenne_de_chaque_annee_de_rotation[index_annee] = moyenne_de_chaque_annee_de_rotation[index_annee] / \
                                                               nombre_de_repetition_de_annee_de_rotation[index_annee]

        return moyenne_de_chaque_annee_de_rotation

    def get_taille_de_la_zone(self):
        return self.__taille_de_la_zone_de_gestion

    def generer_le_bilan_de_zone(self):
        bilan_carbon_pour_la_simulation_et_apport = self.__calculer_carbone_organique_du_sol_pour_la_duree_de_la_simulation()
        bilan_carbon_pour_la_simulation = bilan_carbon_pour_la_simulation_et_apport[0]
        bilan_apports_cultures_principales = bilan_carbon_pour_la_simulation_et_apport[1]
        bilan_apports_cultures_secondaires = bilan_carbon_pour_la_simulation_et_apport[2]
        bilan_apports_amendements = bilan_carbon_pour_la_simulation_et_apport[3]
        bilan_annuel_moyen = self.__calculer_bilan_annuel_moyen(bilan_carbon_pour_la_simulation)
        teneur_finale_projetee = self.__calculer_teneur_finale_projetee(bilan_carbon_pour_la_simulation)
        difference_entre_teneur_initiale_et_finale = self.__calculer_difference_entre_teneur_initiale_et_finale(
            bilan_carbon_pour_la_simulation, teneur_finale_projetee)
        moyenne_de_chaque_annee_de_rotation = self.__calculer_moyenne_de_chaque_annee_de_rotation_dans_la_projection(
            bilan_carbon_pour_la_simulation)
        bilan_des_regies_projections = []
        bilan_des_regies_historiques = []
        for regie_projection in self.__regies_sol_et_culture_projection:
            bilan_des_regies_projections.append(regie_projection.generer_bilan_regie())
        for regie_historique in self.__regies_sol_et_culture_historique:
            bilan_des_regies_historiques.append(regie_historique.generer_bilan_regie())
        return {
            "bilan_carbone_de_la_zone_pour_la_simulation": bilan_carbon_pour_la_simulation,
            "bilan_apports_cultures_principales": bilan_apports_cultures_principales,
            "bilan_apports_cultures_secondaires": bilan_apports_cultures_secondaires,
            "bilan_apports_amendements": bilan_apports_amendements,
            "bilan_annuel_moyen_pour_la_zone": bilan_annuel_moyen, "teneur_finale_projetee": teneur_finale_projetee,
            "difference_entre_la_teneur_finale_et_la_zone": difference_entre_teneur_initiale_et_finale,
            "moyenne_de_chaque_annee_de_rotation": moyenne_de_chaque_annee_de_rotation,
            "taille_de_la_zone": self.__taille_de_la_zone_de_gestion,
            "taux_de_matiere_organique_initial": self.__taux_matiere_organique,
            "classe_texturale": self.__classe_texturale,
            "classe_de_drainage": self.__classe_de_drainage,
            "bilan_des_regies_projections": bilan_des_regies_projections,
            "bilan_des_regies_historiques": bilan_des_regies_historiques}
