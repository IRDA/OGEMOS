from ICBM.RegieSolEtCulture.regie_sol_et_culture import *
from ICBM.Organisation.organisation import *


class GestionSimulation:
    def __init__(self):
        self.__simulations = []

    def effectuer_les_simulations_pour_l_entreprise_agricole(self):
        for simulation in self.__simulations:
            simulation.calculer_carbone_organique_du_sol_pour_entreprise_agricole_la_duree_de_la_simulation()

    def effectuer_les_simulations_pour_une_liste_de_champs(self, liste_nom_de_champs):
        for simulation in self.__simulations:
            simulation.calculer_carbone_organique_du_sol_pour_une_liste_de_champs_la_duree_de_la_simulation(
                liste_nom_de_champs)

    def ajouter_une_simulation(self, simulation):
        self.__simulations.append(simulation)


class Simulation:
    def __init__(self, annee_itiniale, annee_finale, entreprise_agricole):
        self.__entreprise_agricole = entreprise_agricole
        self.__appliquer_les_regies_pour_la_duree_de_la_simulation(annee_itiniale, annee_finale)

    def __appliquer_les_regies_pour_la_duree_de_la_simulation(self, annee_initiale, annee_finale):
        self.__entreprise_agricole.appliquer_les_regies_pour_la_duree_de_la_simulation(annee_initiale, annee_finale)

    def calculer_carbone_organique_du_sol_pour_entreprise_agricole_la_duree_de_la_simulation(self):
        self.__entreprise_agricole.calculer_carbone_organique_du_sol_pour_la_duree_de_la_simulation()

    def calculer_carbone_organique_du_sol_pour_une_liste_de_champs_la_duree_de_la_simulation(self, liste_nom_de_champs):
        self.__entreprise_agricole.calculer_carbone_organique_du_sol_pour_une_liste_de_champs_la_duree_de_la_simulation(
            liste_nom_de_champs)


if __name__ == '__main__':
    cp = CulturePrincipale('Maïs grain', 5.0, 5, True)
    cs = CultureSecondaire(0, 0)
    am = Amendement(0)
    ams = Amendements([am])
    ts = TravailDuSol(0, 0)
    regie = RegieDesSolsEtCultures(cp, cs, ams, ts)
    zg = ZoneDeGestion(3, 'Victoriaville', 'Limon', 'Ok', None, None, [regie])
    chmp = Champs("Joe's Field", [zg])
    ea = EntrepriseAgricole("Joe's Farm", [chmp])
    sim = Simulation(2015, 2020, ea)
    print(sim.calculer_carbone_organique_du_sol_pour_entreprise_agricole_la_duree_de_la_simulation())
