#
#
############################################################################
# Module:      ICBM *version 1*
# Purpose:     Procéder aux calculs de ICBM
# Author(s):   David Dugré - IRDA
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
    '''Version basée sur les calculs de la version excel de Marc-Olivier intitulé ICBM résidus_Martin'''

    # def __init__(self):
    #     self.climat =                 # climat présent
    #     self.sol =                    # type de sol présent dans la parcelle
    #     self.travail =                # type de travail du sol effectué
    #     self.culture1 =               # nom de la première culture se rapprochant le plus de celle cultivée pour l'année en cours
    #     self.culture2 =               # nom de la deuxième culture se rapprochant le plus de celle cultivée pour l'année en cours
    #     self.MO = 3                   # pourcentage de matière organique initial (%)
    #     self.prof = 0.17              # profondeur de sol qu'occupe les racines(m)
    #     self.mva = 1.31731402552353   # masse volumique apparente ()
    #     self.MS = 0.845               # masse sèche

    def MO (self,tss,  mva, prof):
        '''
        MO = Matière Organique
        :param mva: masse volumique apparente () - float
        :param prof: profondeur de sol qu'occupe les racines(m) - float
        :return: retourne un pourcentage de matière organique (%) - float
        '''
        mo = (tss* 1.724) / (1000 * mva * prof)
        return mo

    def tss(self, iCracines, iCtigesdispos, iCTigesrecoltes, r, k1, k2, fcult1):
        '''
        TSS =  i/r (1/k1+h/k2)
        :param iCracines: masse des racines (kg/m2) - float
        :param iCtigesdispos: masse des tiges disponibles (kg/m2) - float
        :param iCTigesrécoltés: masse des tiges récoltées (kg/m2) - float
        :param r: facteur climatique () - float
        :param k1: facteur relié au type de sol présent () - float
        :param k2: facteur relié au type de sol présent () - float
        :param fcult1: facteur relié à la culture principale () - float
        :return: retourne la masse de Tss (Totalt soil C at steady state) (kg/m2) - float
        '''

        tss = (((iCracines) + ((iCtigesdispos) - (iCTigesrecoltes)))/ (r)) * (1/(k1) + (fcult1)/(k2))
        return tss

    def iCracine (self, iCgrain, RreRp):
        '''

        :param iCgrain: apport C des grains (kg/m2) - float
        :param RreRp: ratio (%) - float
        :return: apport C des racines (kg/m2) - float
        '''
        iCracine = (iCgrain) * (RreRp)
        return iCracine

    def iCtiges (self, iCgrain, RreRp):
        '''

        :param iCgrain: apport C des grains (kg/m2) - float
        :param RreRp: ratio (%) - float
        :return: apport C des tiges pour l'année (kg/m2) - float
        '''
        iCtiges = (iCgrain) * (RreRp)
        return iCtiges

    def iCgrain(self, rendement, MS, CCulture):
        '''

        :param rendement: rendement de la culture (kg/m2) - float
        :param MS: masse sèche (%) - float
        :param CCulture: variable C relié à la culture - float
        :return: apport du grain pour l'année (kg/m2) - float
        '''
        iCgrain = 0.1 * (rendement) * (MS) * (CCulture)
        return iCgrain

    def cult_ratios(self, Rp, Rs, Rr, Re):
        '''
        cult_ratios = ratios reliés à la culture sélectionnée
        :param Rp: ratio de récolte (%) - float
        :param Rs: (%) - float
        :param Rr: (%) - float
        :param Re: (%) - float
        :return: ratios reliés à la culture sélectionnée
        '''
        RpRp = (Rp) / (Rp) # (%)
        RsRp = (Rs) / (Rp) # (%)
        RreRp = ((Rr) + (Re)) / (Rp) # (%)
        ReRp = (Re) / (Rp) # (%)
        RrRe = (Rr) / (Re) # (%)
        RatioRac = ((Rr) + (Re)) / (Rp) # ratio racine / récolte (%)
        IndRec = (Rp) / ((Rp) + (Rs)) # indice de récolte (%)
        BABR = ((Rp) + (Rs)) / (Rr)# biomasse aérienne (BA) / biomasse racinaire (BR)
        return RpRp, RsRp, RreRp, ReRp, RrRe, RatioRac, IndRec, BABR

    def BHp(self, k2, mCorg):
        '''
        BHp = Bilan Humique pertes (kg/m2)
        :param k2: facteur relié au type de sol présent () - float
        :param mCorg: masse de Carbone organique (kg/m2) - float
        :return: les pertes de mCorg par BH
        '''
        BHp = mCorg * k2
        return BHp

    def Corg(self, MOS):
        '''
        Corg = Carbone organique
        :param MOS: Matière organique solide (%) - float
        :return: Le carbone organique (Corg - %) et la masse correspondant (mCorg - kg/m2) - float
        '''
        Corg = MOS/1.724
        mCorg = (22.5*1.318*100*Corg)/1999
        return Corg, mCorg

    def TMS(self, k2, mCorg):
        '''
        BHp = Bilan Humique pertes (kg/m2)
        :param k2: facteur relié au type de sol présent () - float
        :param mCorg: masse de Carbone organique (kg/m2) - float
        :return:   1 Apport  Corg (kg/m2) pour 1 T MS avec BH
                   2 T MS residues necessaires pour maintenir le niveau de MOS avec BH
                   3 T MS residues necessaires pour maintenir le niveau de MOS avec ICBM
        '''
        BHp = icbm_MCO().BHp(k2, mCorg)
        AppCorg = (1000 * 0.85 * 0.45 * 0.15)/10000
        TMS_BH = BHp / AppCorg
        TMS_ICBM = ((mCorg * 0.8 * 0.00605) / 0.125) / (0.1 * 0.85 * 0.45)

        return AppCorg, TMS_BH, TMS_ICBM

    def calc_icbm_MCO(self, region, sol, trav_sol, culture, iCtigesrecoltes, Prof, MVA, rendement, MS):
        '''

        :param region: région climatique - string
        :param sol: type de sol présent - string
        :param trav_sol: travail du sol effectué - string
        :param culture: culture présente - - string
        :param iCtigesrecoltes: quantiqué de tiges récupérés (tonne/hectare)- float
        :param Prof: profondeur de sol avec des racines (m) - float
        :param MVA: masse volumique apparente (kg/m2) - float
        :param rendement: rendement de la culture (kg/m2) - float
        :param MS: masse sèche (%) - float
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
        iCtige = icbm_MCO().iCtiges(iCgrain, RreRp)
        iCracine = icbm_MCO().iCracine(iCgrain, RreRp)
        tss = icbm_MCO().tss(iCracine, iCtige, iCtigesrecoltes, r, k1, k2, CCulture)
        MO = icbm_MCO().MO(tss,  MVA, Prof)

        return iCgrain, iCtige, iCracine, tss, MO

class define_variables():
    '''Détermine les variables correspondantes aux choix de effectués'''
    def fact_climat(self, region):
        '''

        Défini la variable de climat selon la région correspondante
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
        Défini la variable de climat selon l'amendement organique correspondante
        :param amend_org: amendement organique
        :return: la valeur du fateur K1 correspondant à l'amendement sélectionnée
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
        Défini la variable de climat selon l'amendement organique correspondante
        :param culture: culture choisie
        :return: un dictionnaire des variables correspondant à la culture sélectionnée (Rp, Rs, Rr, Re, klt, klr)
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
        Défini la variable de climat selon l'amendement organique correspondante
        :param culture: culture choisie
        :return: un dictionnaire des variables correspondant à la culture sélectionnée (Rp, Rs, Rr, Re, klt, klr)
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
        Défini la variable de climat selon l'amendement organique correspondante
        :param culture: culture choisie
        :return: un dictionnaire des variables correspondant à la culture sélectionnée (Rp, Rs, Rr, Re, klt, klr)
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
        ''' Permet d'importer les listes des variables qui peuvent être choisis '''
        list_amen = var.ammend_org_table()
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
    iCtigesrecoltes = 0
    Prof = 0.17
    MVA = 1.31731402552353
    rendement = 5
    MS = 0.845
    k2 = 0.00605
    iCgrain, iCtige, iCRacines, tss, MO = icbm_MCO().calc_icbm_MCO(region, sol, trav_sol, culture1, iCtigesrecoltes, Prof, MVA, rendement, MS)
    print('region, sol, trav_sol, culture1, iCtigesrecoltes, Prof, MVA, rendement, MS')
    print(region, sol, trav_sol, culture1, iCtigesrecoltes, Prof, MVA, rendement, MS)
    print('+++---------+++')
    print('iCgrain, iCtige, iCRacines, tss, MO')
    print(iCgrain, iCtige, iCRacines, tss, MO)
    Corg, mCorg = icbm_MCO().Corg(MS)
    BHp = icbm_MCO().BHp(k2, mCorg)
    AppCorg, TMS_BH, TMS_ICBM = icbm_MCO().TMS(k2, mCorg)

    print('Corg, mCorg , BHp, AppCorg, TMS_BH, TMS_ICBM')
    print(Corg, mCorg , BHp, AppCorg, TMS_BH, TMS_ICBM)
