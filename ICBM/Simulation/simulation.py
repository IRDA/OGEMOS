class Simulation:
    def __init__(self, entreprise_agricole, regies_sol_et_culture, annee_itiniale, annee_finale):
        self.__entreprise_agricole = entreprise_agricole
        self.__regies_sol_et_culture = regies_sol_et_culture
        self.__annee_initiale = annee_itiniale
        self.__annee_finale = annee_finale
        self.__regies_applique_pour_la_duree_de_la_simulation = self.__regies_applique_pour_la_duree_de_la_simulation()
        self.__carbone_organique_du_sol_initial = self.__calculer_carbone_organique_du_sol_initial()

    def __appliquer_les_regies_pour_la_duree_de_la_simulation(self):
        regies_applique_pour_la_duree_de_la_simulation = []
        annee_courante = self.__annee_initiale
        compteur_annee = 0
        while annee_courante < self.__annee_finale:
            regie_annee_courante = self.__regies_sol_et_culture[compteur_annee % self.__regies_sol_et_culture.size()]
            regie_annee_courante.set_annee_culture(annee_courante)
            regies_applique_pour_la_duree_de_la_simulation.append(regie_annee_courante)
            annee_courante += 1
            compteur_annee += 1
        return regies_applique_pour_la_duree_de_la_simulation

    def __calculer_carbone_organique_du_sol_initial(self):
        pass  # TODO: calculer carbone organique du sol initial

    def calculer_carbone_organique_du_sol_pour_la_duree_de_la_simulation(self):
        pass  # TODO: calculer carbone organique du sol pour la duree de la simulation
