# TODO: trouver un meilleur nom pour le fichier et le directory
class EntrepriseAgricole:
    def __init__(self, champs):
        self.__champs = champs


class Champs:
    def __init__(self, zones_de_gestion):
        self.__zones_de_gestion = zones_de_gestion


class ZonesDeGestion:
    def __init__(self, taux_matiere_organique, masse_volumique_apparente, region_agroclimaique, region_geographique,
                 pente, ordonnee, serie_de_sol, classe_de_drainage):
        self.__taux_matiere_organique = taux_matiere_organique
        self.__masse_volumique_apparentre = masse_volumique_apparente
        self.__region_agroclimatique = region_agroclimaique
        self.__region_geographique = region_geographique
        self.__pente = pente
        self.__ordonnee = ordonnee
        self.__serie_de_sol = serie_de_sol
        self.__classe_de_drainage = classe_de_drainage
        self.__coeffcicient_isohumique = self.__caculer_coefficient_isohumique()
        self.__facteur_climatique = self.__calculer_facteur_climatique()
        self.__taux_de_decomposition_du_carbone_organique_du_sol = \
            self.__calculer_taux_de_decomposition_du_carbone_organique_du_sol()

    def __caculer_coefficient_isohumique(self):
        pass  # TODO: caculer le coefficient isohumique

    def __calculer_facteur_climatique(self):
        pass # TODO: calculer le facteur climatique

    def __calculer_taux_de_decomposition_du_carbone_organique_du_sol(self):
        pass # TODO: calculer le taux de decomposition du carbone organique du sol