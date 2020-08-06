import sqlite3
import sqlalchemy
import os


def add_column(database_name, table_name, column_name, data_type):
    connection = sqlite3.connect(database_name)
    cursor = connection.cursor()

    if data_type == "Integer":
        data_type_formatted = "INTEGER"
    elif data_type == "String":
        data_type_formatted = "VARCHAR(100)"

    base_command = ("ALTER TABLE '{table_name}' ADD column '{column_name}' '{data_type}'")
    sql_command = base_command.format(table_name=table_name, column_name=column_name, data_type=data_type_formatted)

    cursor.execute(sql_command)
    connection.commit()
    connection.close()


def change_column_name(database_name, table_name, column_name, new_column_name):
    connection = sqlite3.connect(database_name)
    cursor = connection.cursor()

    base_command = ("ALTER TABLE '{table_name}' RENAME column '{column_name}' TO '{new_column_name}'")
    sql_command = base_command.format(table_name=table_name, column_name=column_name, new_column_name=new_column_name)
    cursor.execute(sql_command)
    connection.commit()
    connection.close()


def drop_table(database_name, table_name):
    connection = sqlite3.connect(database_name)
    cursor = connection.cursor()

    base_command = ("DROP TABLE '{table_name}'")
    sql_command = base_command.format(table_name=table_name)
    cursor.execute(sql_command)
    connection.commit()
    connection.close()


def csv_to_db_municipalite():
    os.chdir("C:\\Users\\Samuel\\Documents\\Stage IRDA\\Table_rendement_et_UTM_terminée_+_métadonnées(1)")
    filename = "Copy of Table_rendement_UTM_sans_doublons.csv"
    entry_liste = []
    with open(filename) as file:
        index = 0
        for line in file:
            if index != 0:
                attributes = line.split(",")
                entry = TableDesMunicipalites(code_geographique_municipalite=str(attributes[0].replace("\"","")),
                                              nom_municipalite=attributes[1], rendement_avoine=float(attributes[2]),
                                              rendement_ble=float(attributes[3]), rendement_mais_fourrager=float(attributes[4]),
                                              rendement_orge=float(attributes[5]), rendement_mais_grain=float(attributes[6]),
                                              rendement_soya=float(attributes[7]), rendement_haricot=float(attributes[8]),
                                              rendement_pomme_de_terre_de_semence=float(attributes[9]),
                                              rendement_pomme_de_terre_de_table=float(attributes[10]),
                                              rendement_pomme_de_terre_de_transformation=float(attributes[11]),
                                              utm_principal=int(attributes[12].replace("\"", "")))
                entry_liste.append(entry)
            index += 1
    return entry_liste
