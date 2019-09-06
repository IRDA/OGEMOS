#
#
############################################################################
# Module:      dbmanagement
# Purpose:
# Author(s):   David Dugré - IRDA
# Created:     20-08-2019
# Copyright:   Copyright (c) 2018 Gouvernement du Québec

#              This program is free software under the LiliQ-R-1.1 License.
#              Read the file COPYING that comes with OGEMOS for details.
# Python vers.:3.7
##############################################################################

import sqlalchemy
from sqlalchemy import create_engine
from icbm.setup import setup
import os

class gen():
    '''outils généraux'''
    def list_files_names(self, directory, format):
        '''
        Procède à la création d'une liste des fichiers D'un certain format se trouvant dans un dossier ciblé
        :param directory: le parcours vers le dossier visé (ex: C:\\directory\\path\\and\\name)
        :param format: format des fichiers recherchés (ex: .pdf, .db, etc.)
        :return:  liste des fichiers du format défini présents dans le dossier visé
        '''''
        #Détermine le parcours principal et ajoute le dossier visé
        main_path = setup().def_path()
        path = os.path.join(main_path, directory)
        dirs = os.listdir(path)

        # Sélectionne que les fichiers correspondant au format recherché
        files_list = []
        for file in dirs:
            if file.endswith(format):
                files_list.append(file)
            else:
                pass

        return files_list

    def same_name(self, directory, name, format):
        '''
        vérifie si le nom est déjà utilisé pour un format de fichier précis
        :param directory: le parcours vers le dossier visé (ex: C:\\directory\\path\\and\\name)
        :param name: nom du fichier à créer
        :param format: format des fichiers recherchés (ex: .pdf, .db, etc.)
        :return: une valeur boolean qui est une indication pour définir si un fichier du même nom
                est présent ou non (True = présent, False = non présent)
        '''
        # fn = files names
        fn = gen().list_files_names(directory, format)
        new_file = name + format
        for i in fn:
            if new_file == fn[i]:
                return True
            else:
                pass
        return False


class sql():
    '''
    Classe permettant de procéder à la gestion des données
    :return:
    '''

    def connect(self, db):
        '''
        Permet de procéder à la connection d'une table existante ou futur
        (première étape obligatoire avant tout autre étape).
        :param path_db:  parcours sous format string (exemple pour une bd sqlite dans windows:
                         'sqlite://C:\\path\\to\\foo.db') de la base de données avec laquelle
                         la connection doit s'effectuer
        :return:
        '''
        path_db = 'sqlite:///' + db
        engine = create_engine(path_db, echo=False)
        return engine

    def get_data_dict(self, db, dbtable):
        '''
        Importe la table visée sous forme de dictionnaire
        :param db: nom de la base de donnée où se trouve les données recherchées (ex : 'BD\\variables.db')
        :param table: nom de la table de la base de donnée visée
        :return: la table visée sous format de dictionnaire
        '''
        # Cré le parcours de la base de données
        path = setup().def_path()
        path_db = os.path.join(path, db)

        # print('db : ', db)
        # print('dbtable : ', dbtable)
        # print('path_db : ', path_db)
        # print('db',path_db)
        # Connection à la base de données
        engine = sql().connect(path_db)

        # va chercher la donnée
        metadata = sqlalchemy.MetaData()
        data = sqlalchemy.Table(dbtable, metadata, autoload=True, autoload_with = engine)
        # Equivalent to 'SELECT * FROM table'
        query = sqlalchemy.select([data])

        # Procède à l'extraction de la table
        ResultProxy = engine.execute(query)
        ResultSet = ResultProxy.fetchall()
        dict_result = {}
        for i in ResultSet:
            d1 = dict(i)
            dict_result[d1['id']] = d1

        for j in dict_result:
            del dict_result[j]['id']
        #print(dict_result)
        return dict_result

    def cr_db(self, main_path, local_path, bd_name):
        '''Crée une base de données'''
        # if we error, we rollback automatically, else commit!
        db = main_path + local_path + db_name + '.db'
        sqlite3.connect(db)

    def cr_ent_db(self, main_path, local_path, bd_name):
        '''Crée une entrprise distincte'''

        # si l'entrprise existe déjà, demander un nouveau nom

    def list_ent_tab(self, main_path, local_path, bd_name):
        '''Crée une liste des entreprises créées'''

    def cr_fields_table(self, main_path, local_path, ent_name, champs_name):
        '''Crée une table qui représente un champs d'un nom donnée dans la base
        de donnée de l'entrpise correspondante du nom précisé'''

    def cr_table(self):
        '''Crée une table du nom choisi dans une base de données ciblée'''

        #si la table existe déjà, demander un nouveau nom

if __name__=='__main__':
    # Définit le parcours vers les bases de données
    db = 'BD\\variables2.db'
    sql().get_data_dict(db, 'fact_sol')