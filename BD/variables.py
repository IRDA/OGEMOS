#
#
############################################################################
# Module:      variables
# Purpose:     Contient les dictionnaires permettant de définir les variables
# Author(s):   David Dugré - IRDA
# Created:     25-04-2019 v1
# Copyright:   Copyright (c) 2018 Gouvernement du Québec

#              This program is free software under the LiliQ-R-1.1 License.
#              Read the file COPYING that comes with OGEMOS for details.
# Python vers.:3.7
##############################################################################

class variables():
    '''Cette classe est dédié à initialiser les variables selon les différents choix effectués'''

    def f_soil_table(self):
        '''
        Facteur de sol (%)
        :return: la liste des choix de sol
        '''
        # fsoil = {
        #     'Argile et argile lourde': 1.0,
        #     'Sable acide': 1.0,
        #     'Limon': 1.2,
        #     'Argile limoneuse et autres': 1.3,
        #     'Loam Argileux': 1.5,
        #     'Loam': 1.6,
        #     'Loam sableux et autres': 2.0,
        #     'Sable': 2.5,
        #     'Sols organiques': 3.0
        # }
        fsoil = ['Argile et argile lourde', 'Sable acide', 'Limon', 'Argile limoneuse et autres',
                 'Loam Argileux', 'Loam', 'Loam sableux et autres', 'Sable', 'Sols organiques']
        return fsoil

    def f_climat_table(self):
        '''
        Facteur climatique selon le quadrillage en UTM
        :return: la liste des choix de région pour la définition du climat
        '''
        # fclimat = {
        #     'Saguenay Lac Saint-Jean (UTM : <2000)': 1.0,
        #     'Centre-du-Québec (UTM : 2000-2500' : 1.15,
        #     'Bases-terres du Saint-Laurent (UTM: >2500)' : 1.3
        # }
        fclimat = ['Saguenay Lac Saint-Jean (UTM : <2000)',
                   'Centre-du-Québec (UTM : 2000-2500)',
                   'Bases-terres du Saint-Laurent (UTM: >2500)']
        return fclimat

    def ammend_org_table(self):
        '''
        Ammendement organique (K1) en pourcentage (%)
        :return: la liste des options d'amendement organique
        '''
        # ammendorg = {
        #     'Aucun': 0,
        #     'Biosolides': 20,
        #     'Boues de station d\'épuration': 20,
        #     'Compost': 40,
        #     'Fumier bien décomposé': 50,
        #     'Fumier moyenement décompsé': 40,
        #     'Fumier peu décomposé (pailleux)': 25,
        #     'Humus industriel': 50,
        #     'Lisier de boivins': 15,
        #     'Lisier de porcs': 10,
        #     'Lisier de volailles': 10,
        #     'Paille sèche': 15,
        #     'Paille de céréales récoltées': -15,
        #     'Purin de bovin': 5,
        #     'Tiges de maïs récoltées': -12
        # }
        ammendorg = ['Aucun', 'Biosolides','Boues de station d\'épuration','Compost', 'Fumier bien décomposé',
                     'Fumier moyenement décompsé','Fumier peu décomposé (pailleux)','Humus industriel',
                     'Lisier de boivins','Lisier de porcs','Lisier de volailles', 'Paille sèche',
                     'Paille de céréales récoltées', 'Purin de bovin','Tiges de maïs récoltées']
        return ammendorg

    def travail_sol_table(self):
        '''
        facteur relié au travail du sol
        :return: la liste des travaux de sol possible
        '''
        # ftravail = {
        #     '1 Sarclage': 1.05,
        #     '2 Sarclages': 1.10,
        #     'Cultures pérennes': 1.00,
        #     'Jachère': 1.05,
        #     'Labour': 1.00,
        #     'Travail minimum': 0.90,
        #     'Semis direct': 0.65
        # }
        ftravail = ['1 Sarclage','2 Sarclages', 'Cultures pérennes','Jachère','Labour',
                    'Travail minimum','Semis direct']
        return ftravail

    def culture_table(self):
        '''
        Matière organique selon  (%)
        :return: liste des cultures
        '''
        # ammendorg = {
        #     'Avoine': dict(Rp=31.9, Rs=28.3, Rr=24.1, Re=15.7, k1t=15, k1r=15),
        #     'Blé': dict(Rp=32.2, Rs=48.2, Rr=11.8, Re=7.8, k1t=15, k1r=15),
        #     'Canola': dict(Rp=27.6, Rs=53.4, Rr=11.5, Re=7.5, k1t=15, k1r=15),
        #     'Maïs fourrager': dict(Rp=73.2, Rs=4.0, Rr=13.8, Re=9.0, k1t=15, k1r=15),
        #     'Maïs grain': dict(Rp=38.6, Rs=38.7, Rr=13.8, Re=8.9, k1t=12, k1r=15),
        #     'Orge': dict(Rp=29.0, Rs=25.7, Rr=27.4, Re=17.9, k1t=15, k1r=15),
        #     'Pâturage - en production': dict(Rp=39.4, Rs=9.8, Rr=30.8, Re=20.0, k1t=12, k1r=20),
        #     'Pâturage - din de rotation': dict(Rp=39.4, Rs=9.8, Rr=30.8, Re=20.0, k1t=12, k1r=20),
        #     'Pomme de terre': dict(Rp=64.5, Rs=16.1, Rr=11.7, Re=7.7, k1t=5, k1r=15),
        #     'Prairie - fin de rotation': dict(Rp=39.4, Rs=9.8, Rr=30.8, Re=20.0, k1t=12, k1r=20),
        #     'Prairie/Pâturage - entretien': dict(Rp=39.4, Rs=9.8, Rr=30.8, Re=20.0, k1t=12, k1r=20),
        #     'Prairie/Pâturage - semis': dict(Rp=39.4, Rs=9.8, Rr=30.8, Re=20.0, k1t=12, k1r=20),
        #     'Soya': dict(Rp=30.4, Rs=45.5, Rr=14.6, Re=9.5, k1t=8, k1r=15),
        #     'Triticale': dict(Rp=26.0, Rs=50.5, Rr=14.3, Re=9.1, k1t=15, k1r=15)
        # }
        ammendorg = ['Avoine','Blé', 'Canola','Maïs fourrager','Maïs grain','Orge','Pâturage - en production',
                     'Pâturage - din de rotation', 'Pomme de terre', 'Prairie - fin de rotation',
                     'Prairie/Pâturage - entretien','Prairie/Pâturage - semis','Soya','Triticale']
        return ammendorg