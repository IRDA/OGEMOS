from ICBM.BaseDeDonnees.database_querying import *
import copy
import math


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
                    bilan_annuel_moyen_ponderee_entreprise[annee] += bilan_annuel_moyen_ponderee_champs[
                                                                         annee] * ponderation_champs
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
        return {"nom_entreprise": self.__nom_entreprise_agricole,
                "bilan_entreprise_ponderee": bilan_entreprise_ponderee, "bilans_des_champs": bilans_des_champs}


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
        return {"nom_champs": self.__nom_champs, "bilans_des_zones": bilans_des_zones,
                "bilan_champs_pondere": bilan_champs_ponderee,
                "taille_du_champs": self.__taille_du_champs, "nom_du_champs": self.__nom_champs,
                "nombre_de_zone_de_gestion": len(self.__zones_de_gestion)}


class ZoneDeGestion:

    def __init__(self, taux_matiere_organique, municipalite, groupe_textural, classe_de_drainage,
                 masse_volumique_apparente, profondeur, taille_de_la_zone, regies_sol_et_culture_projection,
                 regies_sol_et_culture_historique):
        self.FACTEUR_CONVERSION_MATIERE_ORGANIQUE_CARBONE_ORGANIQUE_SOL = 1.724
        self.COEFFICIENT_MINERALISATION_POOL_JEUNE = 0.8
        self.COEFFICIENT_MINERALISATION_POOL_STABLE = 0.006
        self.COEFFICIENT_HUMIFICATION_AMENDEMENT = 0.3
        self.COEFFICIENT_HUMIFICATION_AERIEN = 0.1
        self.COEFFICIENT_HUMIFICATION_RACINNAIRE = 0.3

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
        self.__groupe_textural = groupe_textural
        self.__classe_de_drainage = classe_de_drainage
        self.__facteur_climatique = self.__calculer_facteur_climatique()
        self.__regies_sol_et_culture_projection = regies_sol_et_culture_projection
        if regies_sol_et_culture_historique is None:
            self.__regies_sol_et_culture_historique = []
        else:
            self.__regies_sol_et_culture_historique = regies_sol_et_culture_historique
        self.__regies_sol_et_culture_pour_la_duree_de_la_simulation = []
        self.__carbone_organique_initial_du_sol = self.__calculer_carbone_organique_initial_du_sol()
        self.__taille_de_la_zone_de_gestion = taille_de_la_zone
        self.__regies_sol_et_culture_historique_pour_initialisation = []

    def appliquer_les_regies_pour_la_duree_de_la_simulation(self, annee_initiale, annee_finale):
        if len(self.__regies_sol_et_culture_historique) != 0:
            annee_courante = annee_initiale - len(self.__regies_sol_et_culture_historique)
            compteur_annee = 0
            while annee_courante < annee_initiale:
                regie_annee_courante = copy.deepcopy(self.__regies_sol_et_culture_historique[compteur_annee])
                regie_annee_courante.set_annee_de_culture(annee_courante)
                self.__regies_sol_et_culture_historique_pour_initialisation.append(regie_annee_courante)
                annee_courante += 1
                compteur_annee += 1
        if len(self.__regies_sol_et_culture_projection) != 0:
            annee_courante = annee_initiale
            compteur_annee = 0
            while annee_courante <= annee_finale:
                regie_annee_courante = copy.deepcopy(self.__regies_sol_et_culture_projection[
                                                         compteur_annee % len(self.__regies_sol_et_culture_projection)])
                regie_annee_courante.set_annee_de_culture(annee_courante)
                self.__regies_sol_et_culture_pour_la_duree_de_la_simulation.append(regie_annee_courante)
                annee_courante += 1
                compteur_annee += 1

    def __calculer_carbone_organique_initial_du_sol(self):
        facteur_conversion_de_g_cm2_a_kg_m2 = 1000 / 100 ** 2
        conversion_pourcentage_taux_matiere_organique = 100
        facteur_conversion_de_matiere_organique_a_carbone_organique_du_sol = 1 / self.FACTEUR_CONVERSION_MATIERE_ORGANIQUE_CARBONE_ORGANIQUE_SOL
        return self.__masse_volumique_apparente * self.__profondeur * \
               (
                       self.__taux_matiere_organique / conversion_pourcentage_taux_matiere_organique) * facteur_conversion_de_matiere_organique_a_carbone_organique_du_sol * facteur_conversion_de_g_cm2_a_kg_m2

    def __calculer_carbone_organique_du_sol_pour_la_duree_de_la_simulation(self):
        carbone_organique_du_sol_pour_la_duree_de_la_simulation = []
        matiere_organique_du_sol_pour_la_duree_de_la_simulation = []
        apport_carbone_culture_principale = []
        apport_carbone_culture_secondaire = []
        apport_carbone_amendements = []
        apport_carbone_culture_principale_aerienne = []
        apport_carbone_culture_principale_racinaire = []
        apport_carbone_culture_secondaire_aerienne = []
        apport_carbone_culture_secondaire_racinaire = []
        etats_pool_jeune_amendements = []
        etats_pool_jeune_aerien = []
        etats_pool_jeune_racinnaire = []
        etats_pool_jeune_total = []
        etats_pool_stable = []
        pool_humification = ({"Amendements": {"coefficient_humification": self.COEFFICIENT_HUMIFICATION_AMENDEMENT,
                                              "etat_pool_annee_precedente": 0}},
                             self.COEFFICIENT_HUMIFICATION_AERIEN,
                             self.COEFFICIENT_HUMIFICATION_RACINNAIRE)
        if len(self.__regies_sol_et_culture_pour_la_duree_de_la_simulation) != 0:
            pools_carbone_jeune_initiaux = self.__calculer_pool_carbone_jeune_initial()
            pool_jeune_initial = 0
            for pool in pools_carbone_jeune_initiaux:
                pool_jeune_initial += pool
            pool_carbone_stable_initial = self.__calculer_pool_carbone_stable_initial(pool_jeune_initial)
            pool_humification[0]["Amendements"]["etat_pool_annee_precedente"] = pools_carbone_jeune_initiaux[0]
            regie_annee_simulation = self.__regies_sol_et_culture_pour_la_duree_de_la_simulation
            carbone_total_annee_initiale = self.__regies_sol_et_culture_pour_la_duree_de_la_simulation[
                0].calculer_apport_annuel_en_carbone_de_la_regie()
            apports_carbone = (carbone_total_annee_initiale[3],
                               carbone_total_annee_initiale[4] + carbone_total_annee_initiale[6],
                               carbone_total_annee_initiale[5] + carbone_total_annee_initiale[7])
            pools_carbone_jeune = pools_carbone_jeune_initiaux
            pool_carbone_stable = pool_carbone_stable_initial
            for regie_annee_de_simulation in regie_annee_simulation:
                amendements = regie_annee_de_simulation.generer_bilan_regie()["amendements"]["amendements"]
                amendements_dict = {}
                index = 0
                for amendement in amendements:
                    amendements_dict[amendement]: index
                    index += 1
                apports_annuel_de_carbone = regie_annee_de_simulation.calculer_apport_annuel_en_carbone_de_la_regie()
                apport_carbone_culture_principale.append(apports_annuel_de_carbone[1])
                apport_carbone_culture_secondaire.append(apports_annuel_de_carbone[2])
                apport_carbone_amendements.append(apports_annuel_de_carbone[3])
                apport_carbone_culture_principale_aerienne.append(apports_annuel_de_carbone[4])
                apport_carbone_culture_principale_racinaire.append(apports_annuel_de_carbone[5])
                apport_carbone_culture_secondaire_aerienne.append(apports_annuel_de_carbone[6])
                apport_carbone_culture_secondaire_racinaire.append(apports_annuel_de_carbone[7])
                pool_jeune_amendements = (apports_carbone[0] + pools_carbone_jeune[0]) * math.exp(
                    -self.COEFFICIENT_MINERALISATION_POOL_JEUNE * self.__facteur_climatique)
                pool_jeune_aerien = (apports_carbone[1] + pools_carbone_jeune[1]) * math.exp(
                    -self.COEFFICIENT_MINERALISATION_POOL_JEUNE * self.__facteur_climatique)
                pool_jeune_racinnaire = (apports_carbone[2] + pools_carbone_jeune[2]) * math.exp(
                    -self.COEFFICIENT_MINERALISATION_POOL_JEUNE * self.__facteur_climatique)
                pool_jeune_total = (pool_jeune_amendements +
                                    pool_jeune_aerien +
                                    pool_jeune_racinnaire)
                etats_pool_jeune_amendements.append(pool_jeune_amendements)
                etats_pool_jeune_aerien.append(pool_jeune_aerien)
                etats_pool_jeune_racinnaire.append(pool_jeune_racinnaire)
                etats_pool_jeune_total.append(pool_jeune_total)
                index_pools = 0
                for coefficient in pool_humification:
                    if index_pools == 0:
                        somme_pools_amendments = 0
                        index_amendement = 0
                        for amendement in coefficient.keys():
                            if amendement in amendements_dict.keys():
                                bilan_amendement = amendements[amendements_dict[amendement]]
                                apport_amendement = bilan_amendement["apport"]
                            else:
                                apport_amendement = apports_annuel_de_carbone[3]
                            somme_pools_amendments += coefficient[amendement]["coefficient_humification"] * (
                                    self.COEFFICIENT_MINERALISATION_POOL_JEUNE / (
                                    self.COEFFICIENT_MINERALISATION_POOL_STABLE - self.COEFFICIENT_MINERALISATION_POOL_JEUNE)) * (
                                                              apport_amendement + coefficient[amendement][
                                                          "etat_pool_annee_precedente"])
                            index_amendement += 1
                        pool_carbone_stable -= somme_pools_amendments
                    else:
                        pool_carbone_stable -= coefficient * (self.COEFFICIENT_MINERALISATION_POOL_JEUNE / (
                                self.COEFFICIENT_MINERALISATION_POOL_STABLE - self.COEFFICIENT_MINERALISATION_POOL_JEUNE)) * (
                                                       apports_carbone[index_pools] + pools_carbone_jeune[
                                                   index_pools])
                    index_pools += 1
                pool_carbone_stable = pool_carbone_stable * math.exp(
                    -self.COEFFICIENT_MINERALISATION_POOL_STABLE * self.__facteur_climatique)
                index_pools = 0
                for coefficient in pool_humification:
                    if index_pools == 0:
                        somme_pools_amendments = 0
                        index_amendement = 0
                        for amendement in coefficient.keys():
                            if amendement in amendements_dict.keys():
                                bilan_amendement = amendements[amendements_dict[amendement]]
                                apport_amendement = bilan_amendement["apport"]
                            else:
                                apport_amendement = apports_annuel_de_carbone[3]
                            somme_pools_amendments += coefficient[amendement]["coefficient_humification"] * (
                                    self.COEFFICIENT_MINERALISATION_POOL_JEUNE / (
                                    self.COEFFICIENT_MINERALISATION_POOL_STABLE - self.COEFFICIENT_MINERALISATION_POOL_JEUNE)) * (
                                                              apport_amendement + coefficient[amendement][
                                                          "etat_pool_annee_precedente"]) * math.exp(
                                -self.COEFFICIENT_MINERALISATION_POOL_JEUNE * self.__facteur_climatique)
                            index_amendement += 1
                        pool_carbone_stable += somme_pools_amendments
                    else:
                        pool_carbone_stable += coefficient * (self.COEFFICIENT_MINERALISATION_POOL_JEUNE / (
                                self.COEFFICIENT_MINERALISATION_POOL_STABLE - self.COEFFICIENT_MINERALISATION_POOL_JEUNE)) * (
                                                       apports_carbone[index_pools] + pools_carbone_jeune[
                                                   index_pools]) * math.exp(
                            -self.COEFFICIENT_MINERALISATION_POOL_JEUNE * self.__facteur_climatique)
                    index_pools += 1
                etats_pool_stable.append(pool_carbone_stable)
                carbone_organique_du_sol_pour_la_duree_de_la_simulation.append(pool_carbone_stable + pool_jeune_total)
                matiere_organique_du_sol_pour_la_duree_de_la_simulation.append((
                                                                                       pool_carbone_stable + pool_jeune_total) / self.FACTEUR_CONVERSION_MATIERE_ORGANIQUE_CARBONE_ORGANIQUE_SOL)
                apports_carbone = (apports_annuel_de_carbone[3],
                                   apports_annuel_de_carbone[4] + apports_annuel_de_carbone[6],
                                   apports_annuel_de_carbone[5] + apports_annuel_de_carbone[7])
                pools_carbone_jeune = (pool_jeune_amendements,
                                       pool_jeune_aerien,
                                       pool_jeune_racinnaire)
            return (carbone_organique_du_sol_pour_la_duree_de_la_simulation,
                    apport_carbone_culture_principale,
                    apport_carbone_culture_secondaire,
                    apport_carbone_amendements,
                    apport_carbone_culture_principale_aerienne,
                    apport_carbone_culture_principale_racinaire,
                    apport_carbone_culture_secondaire_aerienne,
                    apport_carbone_culture_secondaire_racinaire,
                    etats_pool_jeune_amendements,
                    etats_pool_jeune_aerien,
                    etats_pool_jeune_racinnaire,
                    etats_pool_jeune_total,
                    etats_pool_stable,
                    matiere_organique_du_sol_pour_la_duree_de_la_simulation)

    def __calculer_pool_carbone_jeune_initial(self):
        if len(self.__regies_sol_et_culture_historique_pour_initialisation):
            pool_jeune_amendements_initial = 0
            pool_jeune_aerien_culture_principale_initial = 0
            pool_jeune_racinaire_culture_principale_initial = 0
            pool_jeune_aerien_culture_secondaire_initial = 0
            pool_jeune_racinaire_culture_secondaire_initial = 0
            nombre_de_regie_historique = len(self.__regies_sol_et_culture_historique_pour_initialisation)
            for regie in self.__regies_sol_et_culture_historique_pour_initialisation:
                regie_annee_initial_apports = regie.calculer_apport_annuel_en_carbone_de_la_regie()
                pool_jeune_amendements_initial = pool_jeune_amendements_initial + (regie_annee_initial_apports[3] / (
                        self.__facteur_climatique * self.COEFFICIENT_MINERALISATION_POOL_JEUNE))
                pool_jeune_aerien_culture_principale_initial = pool_jeune_aerien_culture_principale_initial + (
                        regie_annee_initial_apports[4] / (
                        self.__facteur_climatique * self.COEFFICIENT_MINERALISATION_POOL_JEUNE))
                pool_jeune_racinaire_culture_principale_initial = pool_jeune_racinaire_culture_principale_initial + (
                        regie_annee_initial_apports[5] / (
                        self.__facteur_climatique * self.COEFFICIENT_MINERALISATION_POOL_JEUNE))
                pool_jeune_aerien_culture_secondaire_initial = pool_jeune_aerien_culture_secondaire_initial + (
                        regie_annee_initial_apports[6] / (
                        self.__facteur_climatique * self.COEFFICIENT_MINERALISATION_POOL_JEUNE))
                pool_jeune_racinaire_culture_secondaire_initial = pool_jeune_racinaire_culture_secondaire_initial + (
                        regie_annee_initial_apports[7] / (
                        self.__facteur_climatique * self.COEFFICIENT_MINERALISATION_POOL_JEUNE))
            return (pool_jeune_amendements_initial / nombre_de_regie_historique,
                    pool_jeune_aerien_culture_principale_initial / nombre_de_regie_historique,
                    pool_jeune_racinaire_culture_principale_initial / nombre_de_regie_historique,
                    pool_jeune_aerien_culture_secondaire_initial / nombre_de_regie_historique,
                    pool_jeune_racinaire_culture_secondaire_initial / nombre_de_regie_historique)
        else:
            pool_jeune_amendements_initial = 0
            pool_jeune_aerien_culture_principale_initial = 0
            pool_jeune_racinaire_culture_principale_initial = 0
            pool_jeune_aerien_culture_secondaire_initial = 0
            pool_jeune_racinaire_culture_secondaire_initial = 0
            nombre_de_regie_historique = len(self.__regies_sol_et_culture_projection)
            for regie in self.__regies_sol_et_culture_projection:
                regie_annee_initial_apports = regie.calculer_apport_annuel_en_carbone_de_la_regie()
                pool_jeune_amendements_initial = pool_jeune_amendements_initial + (regie_annee_initial_apports[3] / (
                        self.__facteur_climatique * self.COEFFICIENT_MINERALISATION_POOL_JEUNE))
                pool_jeune_aerien_culture_principale_initial = pool_jeune_aerien_culture_principale_initial + (
                        regie_annee_initial_apports[4] / (
                        self.__facteur_climatique * self.COEFFICIENT_MINERALISATION_POOL_JEUNE))
                pool_jeune_racinaire_culture_principale_initial = pool_jeune_racinaire_culture_principale_initial + (
                        regie_annee_initial_apports[5] / (
                        self.__facteur_climatique * self.COEFFICIENT_MINERALISATION_POOL_JEUNE))
                pool_jeune_aerien_culture_secondaire_initial = pool_jeune_aerien_culture_secondaire_initial + (
                        regie_annee_initial_apports[6] / (
                        self.__facteur_climatique * self.COEFFICIENT_MINERALISATION_POOL_JEUNE))
                pool_jeune_racinaire_culture_secondaire_initial = pool_jeune_racinaire_culture_secondaire_initial + (
                        regie_annee_initial_apports[7] / (
                        self.__facteur_climatique * self.COEFFICIENT_MINERALISATION_POOL_JEUNE))
            return (pool_jeune_amendements_initial / nombre_de_regie_historique,
                    pool_jeune_aerien_culture_principale_initial / nombre_de_regie_historique,
                    pool_jeune_racinaire_culture_principale_initial / nombre_de_regie_historique,
                    pool_jeune_aerien_culture_secondaire_initial / nombre_de_regie_historique,
                    pool_jeune_racinaire_culture_secondaire_initial / nombre_de_regie_historique)

    def __calculer_pool_carbone_stable_initial(self, pool_carbone_jeune_initial):
        return self.__carbone_organique_initial_du_sol - pool_carbone_jeune_initial

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
        for index_annee in range(len(self.__regies_sol_et_culture_historique),
                                 len(carbone_organique_de_sol_pour_la_duree_de_la_simulation)):
            if (index_annee - len(self.__regies_sol_et_culture_historique)) < len(
                    self.__regies_sol_et_culture_projection):
                moyenne_de_chaque_annee_de_rotation.append(
                    carbone_organique_de_sol_pour_la_duree_de_la_simulation[index_annee])
                nombre_de_repetition_de_annee_de_rotation.append(1)
            else:
                moyenne_de_chaque_annee_de_rotation[(index_annee - len(self.__regies_sol_et_culture_historique)) % len(
                    self.__regies_sol_et_culture_projection)] += \
                    carbone_organique_de_sol_pour_la_duree_de_la_simulation[index_annee]
                nombre_de_repetition_de_annee_de_rotation[
                    (index_annee - len(self.__regies_sol_et_culture_historique)) % len(
                        self.__regies_sol_et_culture_projection)] += 1
        for index_annee in range(len(moyenne_de_chaque_annee_de_rotation)):
            moyenne_de_chaque_annee_de_rotation[index_annee] = moyenne_de_chaque_annee_de_rotation[index_annee] / \
                                                               nombre_de_repetition_de_annee_de_rotation[index_annee]

        return moyenne_de_chaque_annee_de_rotation

    def __calculer_moyenne_des_apports_des_cultures_principales_pour_la_simulation(self,
                                                                                   apports_de_la_culture_principale_aerien,
                                                                                   apports_de_la_culture_principale_racinnaire):
        somme_apports_des_cultures_principales = 0
        for index_annee in range(len(self.__regies_sol_et_culture_historique),
                                 len(apports_de_la_culture_principale_aerien)):
            somme_apports_des_cultures_principales += apports_de_la_culture_principale_aerien[index_annee]
            somme_apports_des_cultures_principales += apports_de_la_culture_principale_racinnaire[index_annee]
        return somme_apports_des_cultures_principales / len(self.__regies_sol_et_culture_projection)

    def __calculer_moyenne_des_apports_des_cultures_secondaires_pour_la_simulation(self,
                                                                                   apports_de_la_culture_secondaire_aerien,
                                                                                   apports_de_la_culture_secondaire_racinnaire):
        somme_apports_des_cultures_secondaires = 0
        for index_annee in range(len(self.__regies_sol_et_culture_historique),
                                 len(apports_de_la_culture_secondaire_aerien)):
            somme_apports_des_cultures_secondaires += apports_de_la_culture_secondaire_aerien[index_annee]
            somme_apports_des_cultures_secondaires += apports_de_la_culture_secondaire_racinnaire[index_annee]
        return somme_apports_des_cultures_secondaires / len(self.__regies_sol_et_culture_projection)

    def __calculer_moyenne_des_apports_des_amendements_pour_la_simulation(self, apports_des_amendements):
        somme_apports_des_amendements = 0
        for index_annee in range(len(self.__regies_sol_et_culture_historique), len(apports_des_amendements)):
            somme_apports_des_amendements += apports_des_amendements[index_annee]
        return somme_apports_des_amendements

    def get_taille_de_la_zone(self):
        return self.__taille_de_la_zone_de_gestion

    def generer_le_bilan_de_zone(self):
        bilan_carbon_pour_la_simulation_et_apport = self.__calculer_carbone_organique_du_sol_pour_la_duree_de_la_simulation()
        bilan_carbon_pour_la_simulation = bilan_carbon_pour_la_simulation_et_apport[0]
        bilan_apports_cultures_principales = bilan_carbon_pour_la_simulation_et_apport[1]
        bilan_apports_cultures_secondaires = bilan_carbon_pour_la_simulation_et_apport[2]
        bilan_apports_amendements = bilan_carbon_pour_la_simulation_et_apport[3]
        bilan_apports_cultures_principales_aeriennes = bilan_carbon_pour_la_simulation_et_apport[4]
        bilan_apports_cultures_principales_racinaires = bilan_carbon_pour_la_simulation_et_apport[5]
        bilan_apports_cultures_secondaires_aeriennes = bilan_carbon_pour_la_simulation_et_apport[6]
        bilan_apports_cultures_secondaires_racinaires = bilan_carbon_pour_la_simulation_et_apport[7]
        bilan_etats_pool_jeune_amendements = bilan_carbon_pour_la_simulation_et_apport[8]
        bilan_etats_pool_jeune_aerien = bilan_carbon_pour_la_simulation_et_apport[9]
        bilan_etats_pool_jeune_racinaire = bilan_carbon_pour_la_simulation_et_apport[10]
        bilan_etats_pool_jeune_total = bilan_carbon_pour_la_simulation_et_apport[11]
        bilan_etats_pool_stable = bilan_carbon_pour_la_simulation_et_apport[12]
        bilan_matiere_orgagnique_pour_la_simulation = bilan_carbon_pour_la_simulation_et_apport[13]
        bilan_annuel_moyen = self.__calculer_bilan_annuel_moyen(bilan_carbon_pour_la_simulation)
        teneur_finale_projetee = self.__calculer_teneur_finale_projetee(bilan_carbon_pour_la_simulation)
        difference_entre_teneur_initiale_et_finale = self.__calculer_difference_entre_teneur_initiale_et_finale(
            bilan_carbon_pour_la_simulation, teneur_finale_projetee)
        moyenne_de_chaque_annee_de_rotation = self.__calculer_moyenne_de_chaque_annee_de_rotation_dans_la_projection(
            bilan_carbon_pour_la_simulation)
        moyenne_apports_cultures_principales = self.__calculer_moyenne_des_apports_des_cultures_principales_pour_la_simulation(
            bilan_apports_cultures_principales_aeriennes, bilan_apports_cultures_principales_racinaires)
        moyenne_apports_cultures_secondaire = self.__calculer_moyenne_des_apports_des_cultures_secondaires_pour_la_simulation(
            bilan_apports_cultures_secondaires_aeriennes, bilan_apports_cultures_secondaires_racinaires)
        moyenne_apports_amendements = self.__calculer_moyenne_des_apports_des_amendements_pour_la_simulation(
            bilan_apports_amendements)
        bilan_des_regies_projections = []
        bilan_des_regies_historiques = []
        bilan_des_regies_simulation = []
        for regie_projection in self.__regies_sol_et_culture_projection:
            bilan_des_regies_projections.append(regie_projection.generer_bilan_regie())
        for regie_historique in self.__regies_sol_et_culture_historique:
            bilan_des_regies_historiques.append(regie_historique.generer_bilan_regie())
        for regie_simulation in self.__regies_sol_et_culture_pour_la_duree_de_la_simulation:
            bilan_des_regies_simulation.append(regie_simulation.generer_bilan_regie())
        utm = get_facteur_climatique(self.__municipalite)
        percentile50 = get_percentile50(utm.utm, self.__groupe_textural)
        percentile90 = get_percentile90(utm.utm, self.__groupe_textural)
        difference_entre_teneur_finale_et_percentile50 = teneur_finale_projetee - percentile50.percentile50
        difference_entre_teneur_finale_et_percentile90 = teneur_finale_projetee - percentile90.percentile90
        return {
            "bilan_des_regies_pour_la_duree_de_la_simulation": bilan_des_regies_simulation,
            "bilan_carbone_de_la_zone_pour_la_simulation": bilan_carbon_pour_la_simulation,
            "bilan_apports_cultures_principales": bilan_apports_cultures_principales,
            "bilan_apports_cultures_secondaires": bilan_apports_cultures_secondaires,
            "bilan_apports_amendements": bilan_apports_amendements,
            "bilan_apports_cultures_principales_aeriennes": bilan_apports_cultures_principales_aeriennes,
            "bilan_apports_cultures_principales_racinaires": bilan_apports_cultures_principales_racinaires,
            "bilan_apports_cultures_secondaires_aeriennes": bilan_apports_cultures_secondaires_aeriennes,
            "bilan_apports_cultures_secondaires_racinaires": bilan_apports_cultures_secondaires_racinaires,
            "bilan_etats_pool_jeune_amendements": bilan_etats_pool_jeune_amendements,
            "bilan_etats_pool_jeune_aerien": bilan_etats_pool_jeune_aerien,
            "bilan_etats_pool_jeune_racinaire": bilan_etats_pool_jeune_racinaire,
            "bilan_etats_pool_jeune_total": bilan_etats_pool_jeune_total,
            "bilan_etats_pool_stable": bilan_etats_pool_stable,
            "bilan_matiere_orgagnique_pour_la_simulation": bilan_matiere_orgagnique_pour_la_simulation,
            "bilan_annuel_moyen_pour_la_zone": bilan_annuel_moyen, "teneur_finale_projetee": teneur_finale_projetee,
            "difference_entre_la_teneur_finale_et_la_zone": difference_entre_teneur_initiale_et_finale,
            "comparaison_percentile50": difference_entre_teneur_finale_et_percentile50,
            "comparaison_percentile90": difference_entre_teneur_finale_et_percentile90,
            "moyenne_de_chaque_annee_de_rotation": moyenne_de_chaque_annee_de_rotation,
            "moyenne_apports_cultures_principales": moyenne_apports_cultures_principales,
            "moyenne_apports_cultures_secondaires": moyenne_apports_cultures_secondaire,
            "moyenne_apports_amendements": moyenne_apports_amendements,
            "taille_de_la_zone": self.__taille_de_la_zone_de_gestion,
            "taux_de_matiere_organique_initial": self.__taux_matiere_organique,
            "groupe_textural": self.__groupe_textural,
            "classe_de_drainage": self.__classe_de_drainage,
            "bilan_des_regies_projections": bilan_des_regies_projections,
            "bilan_des_regies_historiques": bilan_des_regies_historiques}
