#
#
############################################################################
# Module:      setup
# Purpose:     Procède à la définition des éléments de base du système
# Author(s):   David Dugré - IRDA
# Created:     23-08-2019
# Copyright:   Copyright (c) 2018 Gouvernement du Québec

#              This program is free software under the LiliQ-R-1.1 License.
#              Read the file COPYING that comes with OGEMOS for details.
# Python vers.:3.7
##############################################################################

import os

class setup():
    '''Procède à la définition des éléments de base du système'''

    #def __init__:
    #    GEOMOS_path = self.def_path

    def def_path(self):
        '''Détermine le parcours de l'outil GEOMOS'''
        path = os.path.dirname(os.path.abspath(os.path.normpath('OGEMOS.py')))
        path1, path2 = os.path.split(path)
        if path == 'ICBM_IRDA':
            pass
        else:
            path = path1
        return path

