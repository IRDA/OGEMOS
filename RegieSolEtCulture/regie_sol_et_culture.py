class RegieDesSolsEtCultures:
    def __init__(self, travail_du_sol, profondeur_max_travail_du_sol, culture_pricipale, culture_secondaire):
        self._annee_de_culture = None
        self._culture_principale = culture_pricipale
        self._culture_secondaire = culture_secondaire
        self._travail_du_sol = travail_du_sol


class CulturePrincipale:
    def __init__(self, type_de_culture_principale, rendement, recolte_residu, hauteur_coupe=0):
        self._type_de_culture_principale = type_de_culture_principale
        self._rendement = rendement
        self._recolte_residu = recolte_residu
        self._hauteur_coupe = hauteur_coupe


class CultureSecondaire:
    def __init__(self, type_de_culture_secondaire, periode_implantation):
        self.type_de_culture_secondaire = type_de_culture_secondaire
        self.periode_implantation = periode_implantation


class Amendements:
    def __init__(self, amendements):
        self._amendements = amendements
    def calculerApportEnCarbonesAmendements(self):
        total_carbone_amendements = 0
        for amendement in self.amendements:
            pass


class Amendement:
    def __init__(self, type_amendement):
        self._type_amendement = type_amendement
        self._taux_apport_specifique = None
        self._taux_humidite = None
