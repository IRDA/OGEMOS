#
#
############################################################################
# Module:      ICBM
# Purpose:     Procéder aux calculs de ICBM
# Author(s):   David Dugré, Arianne Blais Gagnon - IRDA
# Created:     25-04-2019 v1
# Copyright:   Copyright (c) 2018 Gouvernement du Québec

#              This program is free software under the LiliQ-R-1.1 License.
#              Read the file COPYING that comes with OGEMOS for details.
# Python vers.:3.7
##############################################################################


import math
from BD.dbmanagement import sql
from BD.variables import variables as var

class icbm_MCO():
    '''Version basée sur les calculs de la version excel de Marc-Olivier Gasser, intitulée ICBM résidus_Martin'''

    # def __init__(self):
    #     self.climat =                 # zone climatique
    #     self.sol =                    # type de sol présent dans la parcelle
    #     self.travail =                # type de travail du sol effectué
    #     self.culture1 =               # nom de la première culture se rapprochant le plus de celle cultivée pour l'année en cours
    #     self.culture2 =               # nom de la deuxième culture se rapprochant le plus de celle cultivée pour l'année en cours
    #     self.MO = 3                   # pourcentage de matière organique initiale (%)
    #     self.prof = 0.17              # profondeur de sol occupée par les racines (m)
    #     self.mva = 1.31731402552353   # masse volumique apparente ()
    #     self.MS = 0.845               # taux de matière sèche

    def MO (self,tss,  mva, prof):
        '''
        MO = Matière Organique
        :param tss:  () - float
        :param mva: masse volumique apparente () - float
        :param prof: profondeur de sol occupée par les racines(m) - float
        :facteur 1.724 : MOS = 1.724 COS
        :return: retourne un pourcentage de matière organique (%) - float
        '''
        mo = (tss* 1.724) / (1000 * mva * prof)
        return mo

    def tss(self, iCracines, iCtigesdispos, iCTigesrecoltees, r, k1, k2, fcult1):
        '''
        TSS =  i/r (1/k1+h/k2)
        :param iCracines: masse des racines (kg/m2) - float
        :param iCtigesdispos: masse des tiges disponibles (kg/m2) - float
        :param iCTigesrécoltées: masse des tiges récoltées (kg/m2) - float
        :param r: facteur climatique () - float
        :param k1: coefficient isohumique () - float
        :param k2: coefficient de minéralisation () - float
        :param fcult1: facteur relié à la culture principale () - float
        :return: retourne la masse de Tss (Total soil C at steady state) (kg/m2) - float
        '''

        tss = (((iCracines) + ((iCtigesdispos) - (iCTigesrecoltees)))/ (r)) * (1/(k1) + (fcult1)/(k2))
        return tss

    def iCracines (self, iCgrain, RreRp):
        '''

        :param iCgrain: apport en C des grains (kg/m2) - float
        :param RreRp: ratio (%) - float
        :return: apport en C des racines (kg/m2) - float
        '''
        iCracines = (iCgrain) * (RreRp)
        return iCracines

    def iCtigesdispos (self, iCgrain, RsRp):
        '''

        :param iCgrain: apport en C des grains (kg/m2) - float
        :param RsRp: ratio (%) - float
        :return: apport en C des tiges pour l'année (kg/m2) - float
        '''
        iCtigesdispos = (iCgrain) * (RsRp)
        return iCtigesdispos

    def iCgrain(self, rendement, MS, CCulture):
        '''

        :param rendement: rendement de la culture (tm/ha) - float
        :param MS: taux de matière sèche (%) - float
        :param CCulture: coefficient de culture - float
        :return: apport en C du grain pour l'année (kg/m2) - float
        '''
        iCgrain = 0.1 * (rendement) * (MS) * (CCulture)
        return iCgrain

    def cult_ratios(self, Rp, Rs, Rr, Re):
        '''
        cult_ratios = ratios reliés à la culture sélectionnée
        :param Rp: répartition de la partie récoltée (%) - float
        :param Rs: répartition de la partie tige non récoltée (%) - float
        :param Rr: répartition de la partie racinaire (%) - float
        :param Re: répartition de la partie extra-racinaire(%) - float
        :param RatioRac: ratio racines/récolte (%) - float
        :param IndRec: indice de récolte (%) - float
        :param BABR: ratio biomasse aérienne sur biomasse racinaire (%) - float
        :return: ratios reliés à la culture sélectionnée
        '''
        RpRp = (Rp) / (Rp)
        RsRp = (Rs) / (Rp)
        RreRp = ((Rr) + (Re)) / (Rp)
        ReRp = (Re) / (Rp)
        RrRe = (Rr) / (Re)
        RatioRac = ((Rr) + (Re)) / (Rp)
        IndRec = (Rp) / ((Rp) + (Rs))
        BABR = ((Rp) + (Rs)) / (Rr)
        return RpRp, RsRp, RreRp, ReRp, RrRe, RatioRac, IndRec, BABR

    def BHp(self, k2, mCorg):
        '''
        BHp = Bilan Humique pertes (kg/m2)
        :param k2: coefficient de minéralisation () - float
        :param mCorg: masse de carbone organique (kg/m2) - float
        :return: les pertes de mCorg par pour le bilan humique
        '''
        BHp = mCorg * k2/100
        return BHp

    def Corg(self, MOS):
        '''
        Corg = Carbone organique
        :param MOS: Matière organique solide (%) - float
        :facteur 1.724: facteur de conversion selon la littérature
        :facteur 22.5: épaisseur de la couche arable?
        :facteur 1.318: MVA ()
        :facteur 1999:
        :return: Le carbone organique (Corg - %) et la masse de carbone organique (mCorg - kg/m2) - float
        '''
        Corg = MOS/1.724
        mCorg = (22.5*1.318*100*Corg)/1999
        return Corg, mCorg

    def TMS(self, k2, mCorg):
        '''
        BHp = Bilan Humique pertes (kg/m2)
        :param k2: coefficient de minéralisation () - float
        :param mCorg: masse de Carbone organique (kg/m2) - float
        :facteur 0.85: taux de matière sèche ()
        :facteur 0.45:
        :facteur 0.15:
        :return:   1 Apport  Corg (kg/m2) pour 1 T MS avec BH
                   2 T MS residus necessaires pour maintenir le niveau de MOS avec BH
                   3 T MS residus necessaires pour maintenir le niveau de MOS avec ICBM
        '''
        BHp = icbm_MCO().BHp(k2, mCorg)
        AppCorg = (1000 * 0.85 * 0.45 * 0.15)/10000
        TMS_BH = BHp / AppCorg
        TMS_ICBM = ((mCorg * 0.8 * 0.00605) / 0.125) / (0.1 * 0.85 * 0.45)

        return AppCorg, TMS_BH, TMS_ICBM

    def calc_icbm_MCO(self, region, sol, trav_sol, culture, iCtigesrecoltees, Prof, MVA, rendement, MS):
        '''

        :param region: région climatique - string
        :param sol: type de sol présent - string
        :param trav_sol: travail du sol effectué - string
        :param culture: culture présente - - string
        :param iCtigesrecoltees: quantité de tiges récupérées (tm/ha)- float
        :param Prof: profondeur de sol avec des racines (m) - float
        :param MVA: masse volumique apparente (kg/m2) - float
        :param rendement: rendement de la culture (kg/m2) - float
        :param MS: taux de matière sèche (%) - float
        :return: % de matière organique produit (%)
        '''
        #importation des variables
        clim = define_variables().fact_climat(region)
        r = clim['r']
        fsol = define_variables().fact_sol(sol)
        print(fsol)
        k1 = fsol[0]
        k2 = fsol[1]
        ftravsol = define_variables().fact_travsol(trav_sol)
        fcult = define_variables().fact_culture(culture)

        #Définition de quelques variables
        Rp = fcult['Rp']
        Rs = fcult['Rs']
        Rr = fcult['Rr']
        Re = fcult['Re']
        CCulture = fcult['h']

        #Calcul des différents ratios de la culture
        RpRp, RsRp, RreRp, ReRp, RrRe, RatioRac, IndRec, BABR = icbm_MCO().cult_ratios(Rp, Rs, Rr, Re)

        # calcul des masses du C par les grains, tiges et racines et TSS
        iCgrain = icbm_MCO().iCgrain(rendement, MS, CCulture)
        iCtiges = icbm_MCO().iCtiges(iCgrain, RreRp)
        iCracines = icbm_MCO().iCracines(iCgrain, RreRp)
        tss = icbm_MCO().tss(iCracines, iCtiges, iCtigesrecoltees, r, k1, k2, CCulture)
        MO = icbm_MCO().MO(tss,  MVA, Prof)

        return iCgrain, iCtiges, iCracines, tss, MO

class define_variables():
    '''Détermine les variables correspondantes aux choix effectués'''
    def fact_climat(self, region):
        '''

        Définit la variable Climat selon la région correspondante
        :param region: région climatique
        :return: la valeur du fateur climatique correspondant à la région sélectionnée
        '''
        db = 'ICBM_IRDA\\BD\\variables.db'
        dbtable = 'fact_climate'
        dict = sql().get_data_dict(db, dbtable)
        for i in dict:
            if dict[i]['region'] == region:
                return dict[i]#['fclimat']
            else:
                pass

    def fact_amend(self, amend_org):
        '''
        Définit la variable Amendement organique
        :param amend_org: amendement organique
        :return: la valeur du fateur K1 correspondant à l'amendement sélectionné
        '''
        db = 'ICBM_IRDA\\BD\\variables.db'
        dbtable = 'amend_org'
        dict = sql().get_data_dict( db, dbtable)
        for i in dict:
            if dict[i]['amend_org'] == amend_org:
                return dict[i]#['K1']
            else:
                pass

    def fact_culture(self, culture):
        '''
        Définit la variable Culture
        :param culture: type de culture
        :return: un dictionnaire de variables correspondant à la culture sélectionnée (Rp, Rs, Rr, Re, klt, klr)
        '''
        db = 'ICBM_IRDA\\BD\\variables.db'
        dbtable = 'culture'
        dict = sql().get_data_dict(db, dbtable)
        for i in dict:
            if dict[i]['culture'] == culture:
                return dict[i]
            else:
                pass

    def fact_sol(self, sol):
        '''
        Définit la variable Sol
        :param sol: type de sol
        :return: un dictionnaire de variables correspondant au type de sol
        '''
        db = 'ICBM_IRDA\\BD\\variables.db'
        dbtable = 'fact_sol'
        dict = sql().get_data_dict(db, dbtable)
        for i in dict:
            if dict[i]['type_sol'] == sol:
                print (dict[i]['k1'], dict[i]['k2'])
                return dict[i]['k1'], dict[i]['k2']
            else:
                pass

    def fact_travsol(self, trav_sol):
        '''
        Définit la variable Travail de sol
        :param trav_sol: type de travail de sol
        :return: un dictionnaire de variables correspondant au type de travail de sol
        '''
        db = 'ICBM_IRDA\\BD\\variables.db'
        dbtable = 'travail_sol'
        dict = sql().get_data_dict(db, dbtable)
        for i in dict:
            if dict[i]['travail_sol'] == trav_sol:
                return dict[i]['fact_trav']
            else:
                pass

    def imp_selected_variable(self):
        ''' Permet d'importer les listes des variables qui peuvent être choisies '''
        list_amen = var.amend_org_table()
        list_cult = var.culture_table()
        list_clim = var.f_climat_table()
        list_soil = var.f_soil_table()
        list_trav = var.travail_sol_table()
        return list_amen, list_cult, list_clim, list_soil, list_trav



if __name__=='__main__':
    region = 'Saguenay Lac St-Jean'
    sol = 'Sable'
    trav_sol = '1 Sarclage'
    culture1 = 'Canola'
    iCtigesrecoltees = 0
    Prof = 0.17
    MVA = 1.31731402552353
    rendement = 5
    MS = 0.845
    k2 = 0.00605
    iCgrain, iCtiges, iCRacines, tss, MO = icbm_MCO().calc_icbm_MCO(region, sol, trav_sol, culture1, iCtigesrecoltees, Prof, MVA, rendement, MS)
    print('region, sol, trav_sol, culture1, iCtigesrecoltees, Prof, MVA, rendement, MS')
    print(region, sol, trav_sol, culture1, iCtigesrecoltees, Prof, MVA, rendement, MS)
    print('+++---------+++')
    print('iCgrain, iCtiges, iCRacines, tss, MO')
    print(iCgrain, iCtiges, iCRacines, tss, MO)
    Corg, mCorg = icbm_MCO().Corg(MS)
    BHp = icbm_MCO().BHp(k2, mCorg)
    AppCorg, TMS_BH, TMS_ICBM = icbm_MCO().TMS(k2, mCorg)

    print('Corg, mCorg , BHp, AppCorg, TMS_BH, TMS_ICBM')
    print(Corg, mCorg , BHp, AppCorg, TMS_BH, TMS_ICBM)