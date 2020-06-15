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
    def __init__(self, annee_itiniale, annee_finale, entreprise_agricole):
        self.__entreprise_agricole = entreprise_agricole
        self.__appliquer_les_regies_pour_la_duree_de_la_simulation(annee_itiniale, annee_finale)

    def __appliquer_les_regies_pour_la_duree_de_la_simulation(self, annee_initiale, annee_finale):
        self.__entreprise_agricole.appliquer_les_regies_pour_la_duree_de_la_simulation(annee_initiale, annee_finale)

    def generer_le_bilan_pour_la_simulation(self):
        return self.__entreprise_agricole.generer_le_bilan_entreprise()


if __name__ == '__main__':
    cp = CulturePrincipale('Maïs grain', 5.0, 5, True)
    cs = CultureSecondaire(0, 0)
    am = Amendement(0)
    ams = Amendements([am])
    ts = TravailDuSol(0, 0)
    data = RegieDesSolsEtCultures(cp, cs, ams, ts)
    zg = ZoneDeGestion(3, 'Victoriaville', 'Limon', 'Ok', None, None, [data])
    chmp = Champs("Joe's Field", [zg])
    ea = EntrepriseAgricole("Joe's Farm", [chmp])
    sim = Simulation(2015, 2020, ea)
    #2print(sim.calculer_carbone_organique_du_sol_pour_entreprise_agricole_la_duree_de_la_simulation())
