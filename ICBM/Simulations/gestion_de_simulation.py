from ICBM.RegieSolEtCulture.regie_sol_et_culture import *
from ICBM.Organisation.organisation import *


class GestionSimulation:
    def __init__(self):
        self.__simulations = []

    def generer_les_bilans_pour_les_simulations_de_l_entreprise_agricole(self):
        bilan_des_simulations = []
        for simulation in self.__simulations:
            bilan_des_simulations.append(simulation.generer_le_bilan_pour_la_simulation())
        return {"bilans_des_simulations": bilan_des_simulations}

    def ajouter_une_simulation(self, simulation):
        self.__simulations.append(simulation)


class Simulation:
    def __init__(self, annee_itiniale, annee_finale, entreprise_agricole, nom_simulation):
        self.__entreprise_agricole = entreprise_agricole
        self.__nom_simulation = nom_simulation
        self.__appliquer_les_regies_pour_la_duree_de_la_simulation(annee_itiniale, annee_finale)

    def __appliquer_les_regies_pour_la_duree_de_la_simulation(self, annee_initiale, annee_finale):
        self.__entreprise_agricole.appliquer_les_regies_pour_la_duree_de_la_simulation(annee_initiale, annee_finale)

    def generer_le_bilan_pour_la_simulation(self):
        bilan_simulation = self.__entreprise_agricole.generer_le_bilan_entreprise()
        bilan_simulation["nom_simulation"] = self.__nom_simulation
        return bilan_simulation
