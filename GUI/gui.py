import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from openpyxl import Workbook
import json
import copy
import GUI.fonction_utilitaire as util
import subprocess
import psutil
import requests

global furthest_left_tab_index_simulation
furthest_left_tab_index_simulation = 0
global furthest_right_tab_index_simulation
furthest_right_tab_index_simulation = 0

global min_index_simulation
min_index_simulation = 0
global max_index_simulation
max_index_simulation = 0

global furthest_left_tab_index_champs
furthest_left_tab_index_champs = 0
global furthest_right_tab_index_champs
furthest_right_tab_index_champs = 0

global min_index_champs
min_index_champs = 0
global max_index_champs
max_index_champs = 0

global furthest_left_tab_index_zone
furthest_left_tab_index_zone = 0
global furthest_right_tab_index_zone
furthest_right_tab_index_zone = 0

global min_index_zone
min_index_zone = 0
global max_index_zone
max_index_zone = 0

global current_champs_tab
current_champs_tab = None

global nombre_simulations
nombre_simulations = 0

global duree_simulation
duree_simulation = []

global annees_historiques
annees_historiques = None

global simulations_chargees
simulations_chargees = False

global filename
filename = None

global plan_gestion_filename
plan_gestion_filename = None


def kill(proc_pid):
    process = psutil.Process(proc_pid)
    for proc in process.children(recursive=True):
        proc.kill()
    process.kill()


sp = subprocess.Popen(
    "cd ../ICBM/VirtualEnvironmentSetUp & py \"app.py\"",
    shell=True)

global municipalites_supportees
municipalites_supportees_temporaire = requests.get("http://localhost:5000/api/get-municipalite")
municipalites_supportees = municipalites_supportees_temporaire.json()["municipalites_supportees"]
municipalites_supportees.sort()

global classes_texturales_supportees
classes_texturales_supportees_temporaire = requests.get("http://localhost:5000/api/get-classe_texturale")
classes_texturales_supportees = classes_texturales_supportees_temporaire.json()["classes_texturales_supportees"]
classes_texturales_supportees.sort()

global classes_de_drainage_supportees
classe_de_drainage_supportees_temporaire = requests.get("http://localhost:5000/api/get-classe_de_drainage")
classes_de_drainage_supportees = classe_de_drainage_supportees_temporaire.json()["classes_de_drainage_supportees"]
classes_de_drainage_supportees.sort()

global cultures_principales_supportees
culture_principale_supportees_temporaire = requests.get("http://localhost:5000/api/get-culture_principale")
cultures_principales_supportees = culture_principale_supportees_temporaire.json()["cultures_principales_supportees"]
cultures_principales_supportees.sort()

global types_travail_du_sol_supportes
travail_du_sol_supportees_temporaire = requests.get("http://localhost:5000/api/get-travail_du_sol")
types_travail_du_sol_supportes = travail_du_sol_supportees_temporaire.json()["types_travail_du_sol_supportes"]
types_travail_du_sol_supportes.sort()

global cultures_secondaires_supportees
culture_secondaire_supportees_temporaire = requests.get("http://localhost:5000/api/get-culture_secondaire")
cultures_secondaires_supportees = culture_secondaire_supportees_temporaire.json()["cultures_secondaires_supportees"]
cultures_secondaires_supportees.sort()

global amendements_supportees
amendements_supportees_temporaire = requests.get("http://localhost:5000/api/get-amendement")
amendements_supportees = amendements_supportees_temporaire.json()["amendements_supportees"]
amendements_supportees.sort()

root = tk.Tk()
root.title("OGEMOS")
mainframe = ttk.Frame(root)
mainframe.grid(row=0, column=0, ipadx=5, ipady=5)


def on_mousewheel(event):
    event_coordinates = root.winfo_pointerxy()
    try:
        canvas_path = str(root.winfo_containing(event_coordinates[0], event_coordinates[1]))
        if "canvas" in canvas_path:
            canvas_found = False
            widget_list = canvas_path.split(".")
            real_canvas_path = ""
            for widget in reversed(widget_list):
                if canvas_found:
                    if widget != "":
                        real_canvas_path = "." + widget + real_canvas_path
                else:
                    if "canvas" in widget:
                        real_canvas_path = "." + widget
                        canvas_found = True
            canvas = root.nametowidget(real_canvas_path)
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
    except KeyError:
        pass


root.bind_all("<MouseWheel>", on_mousewheel)
root.bind_all("<Button-4>", on_mousewheel)
root.bind_all("<Button-5>", on_mousewheel)

root.unbind_class("TCombobox", "<MouseWheel>")
root.unbind_class("TCombobox", "<ButtonPress-4>")
root.unbind_class("TCombobox", "<ButtonPress-5>")


def filter_combobox_values(combobox, values):
    current_string_in_combobox = combobox.get()
    if current_string_in_combobox == "":
        combobox.configure(values=values)
    else:
        new_values = []
        for item in values:
            if current_string_in_combobox.lower() in item.lower():
                new_values.append(item)
        combobox.configure(values=new_values)


def closing_root_protocol():
    kill(sp.pid)
    root.destroy()


root.protocol("WM_DELETE_WINDOW", closing_root_protocol)


def run_gui(frame):
    def show_entreprise_set_up(frame_entreprise):
        def get_information_entreprise():
            global nom_entreprise
            nom_entreprise = nom_entreprise_entry.get()
            nombre_de_champs_string = nombre_de_champs_entry.get()
            if nombre_de_champs_string.isdigit() and int(nombre_de_champs_string) > 0:
                global nombre_de_champs
                nombre_de_champs = int(nombre_de_champs_string)
                for widget in frame_entreprise.winfo_children():
                    widget.destroy()
                show_creation_champs(frame)
            else:
                messagebox.showwarning("Warning",
                                       "L'entrée \"Nombre de champs\" est invalide.Veuillez entrer un nombre naturel plus grand que 0.")

        nom_entreprise_label = ttk.Label(frame_entreprise, text="Nom de l'entreprise: ")
        nom_entreprise_entry = ttk.Entry(frame_entreprise)
        nombre_de_champs_label = ttk.Label(frame_entreprise, text="Nombre de champs: ")
        nombre_de_champs_entry = ttk.Entry(frame_entreprise)
        nombre_de_champs_entry.insert(0, "1")

        nom_entreprise_label.grid(row=0, column=0, sticky="E")
        nom_entreprise_entry.grid(row=0, column=1, sticky="W")
        nombre_de_champs_label.grid(row=1, column=0, sticky="E")
        nombre_de_champs_entry.grid(row=1, column=1, sticky="W")
        frame_entreprise.grid_columnconfigure(0, pad=10)
        frame_entreprise.grid_columnconfigure(1, pad=10)
        frame_entreprise.grid_rowconfigure(0, minsize=30)
        frame_entreprise.grid_rowconfigure(1, minsize=30)
        frame_entreprise.grid_rowconfigure(2, minsize=30)

        creer_bouton = ttk.Button(frame_entreprise, text="Créer", command=get_information_entreprise)
        creer_bouton.grid(columnspan=2, row=2, column=0, pady=3)

    def show_creation_champs(frame_champs_list):
        def get_information_champs(scrollable_frame):
            global information_champs
            information_champs = []
            champs_valides = True
            for scrollable_frame_widget in scrollable_frame.winfo_children():
                if isinstance(scrollable_frame_widget, ttk.LabelFrame):
                    grid_slave0_1 = scrollable_frame_widget.grid_slaves(row=0, column=1)
                    for entry in grid_slave0_1:
                        nom_du_champs = entry.get()
                    grid_slave1_1 = scrollable_frame_widget.grid_slaves(row=1, column=1)
                    for entry in grid_slave1_1:
                        nombre_de_zone_de_gestion = entry.get()
                    if nombre_de_zone_de_gestion.isdigit() and int(nombre_de_zone_de_gestion) > 0:
                        if len(nom_du_champs) < 13:
                            information_champs.append({"nom_du_champs": nom_du_champs,
                                                       "nombre_de_zone_de_gestion": nombre_de_zone_de_gestion,
                                                       "information_zone_de_gestion": []})
                        else:
                            champs_valides = False
                            information_champs = []
                            messagebox.showwarning("Warning",
                                                   "Le nom du champ devrait être composé de 12 caractères ou moins.")
                            break

                    else:
                        champs_valides = False
                        information_champs = []
                        messagebox.showwarning("Warning",
                                               "Une entrée \"Nombre de zones gestion\" est invalide.Veuillez entrer un nombre naturel plus grand que 0.")
                        break

            if champs_valides:
                for widget in frame_champs_list.winfo_children():
                    widget.destroy()

                show_creation_zone_de_gestion(frame_champs_list)

        canvas = tk.Canvas(frame_champs_list)
        scrollbar = ttk.Scrollbar(frame_champs_list, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        for index_champ in range(int(nombre_de_champs)):
            champs_frame = ttk.LabelFrame(scrollable_frame, text="Champs " + str(index_champ + 1))
            nom_du_champs_label = ttk.Label(champs_frame, text="Nom du champ: ")
            nom_du_champs_entry = ttk.Entry(champs_frame)
            nombre_de_zone_de_gestion_label = ttk.Label(champs_frame, text="Nombre de zones gestion: ")
            nombre_de_zone_de_gestion_entry = ttk.Entry(champs_frame)
            nombre_de_zone_de_gestion_entry.insert(0, "1")
            nom_du_champs_label.grid(row=0, column=0, sticky="w", pady=3, padx=5)
            nom_du_champs_entry.grid(row=0, column=1, sticky="w", pady=3, padx=5)
            nombre_de_zone_de_gestion_label.grid(row=1, column=0, sticky="w", pady=3, padx=5)
            nombre_de_zone_de_gestion_entry.grid(row=1, column=1, sticky="w", pady=3, padx=5)

            champs_frame.pack(fill="both", padx=55, pady=5)

        canvas.pack(side="left", ipadx=10)
        scrollbar.pack(side="right", fill="y")

        creation_champs_bouton = ttk.Button(scrollable_frame, text="Créer",
                                            command=lambda: get_information_champs(scrollable_frame))
        creation_champs_bouton.pack()

    def show_creation_zone_de_gestion(zone_de_gestion_mainframe, fill_fields=False):
        def get_information_zone_de_gestion(scrollable_frame):
            entree_invalide_liste = []
            global information_champs
            info_champs_temporaire = copy.deepcopy(information_champs)
            index = 0
            for scrollable_frame_widget in scrollable_frame.winfo_children():
                if isinstance(scrollable_frame_widget, ttk.LabelFrame):
                    index_zone = 1
                    for champs_frame_widget in scrollable_frame_widget.winfo_children():
                        if isinstance(champs_frame_widget, ttk.LabelFrame):
                            grid_slave0_1 = champs_frame_widget.grid_slaves(row=0, column=1)
                            for entry in grid_slave0_1:
                                taux_matiere_organique = entry.get()
                                if not util.is_decimal_number(taux_matiere_organique) or float(
                                        taux_matiere_organique) < 0 or float(taux_matiere_organique) > 100:
                                    entree_invalide_liste.append((information_champs[index]["nom_du_champs"],
                                                                  "Zone gestion " + str(index_zone),
                                                                  "\"Taux de matière organique\" doit être un réel positif dans l'intervalle [0,100]"))
                                else:
                                    taux_matiere_organique = float(taux_matiere_organique)
                            grid_slave1_1 = champs_frame_widget.grid_slaves(row=1, column=1)
                            for entry in grid_slave1_1:
                                municipalite = entry.get()
                                global municipalites_supportees
                                if municipalite not in municipalites_supportees:
                                    entree_invalide_liste.append(
                                        (information_champs[index]["nom_du_champs"],
                                         "Zone gestion " + str(index_zone),
                                         "\"Municipalité\" doit être parmis les choix disponibles"))
                            grid_slave2_1 = champs_frame_widget.grid_slaves(row=2, column=1)
                            for entry in grid_slave2_1:
                                classe_texturale = entry.get()
                                global classes_texturales_supportees
                                if classe_texturale not in classes_texturales_supportees:
                                    entree_invalide_liste.append(
                                        (information_champs[index]["nom_du_champs"],
                                         "Zone gestion " + str(index_zone),
                                         "\"Classe texturale\" doit être parmis les choix disponibles"))
                            grid_slave3_1 = champs_frame_widget.grid_slaves(row=3, column=1)
                            for entry in grid_slave3_1:
                                classe_de_drainage = entry.get()
                                global classes_de_drainage_supportees
                                if classe_de_drainage not in classes_de_drainage_supportees:
                                    entree_invalide_liste.append(
                                        (information_champs[index]["nom_du_champs"],
                                         "Zone gestion " + str(index_zone),
                                         "\"Classe de drainage\" doit être parmis les choix disponibles"))
                            grid_slave4_1 = champs_frame_widget.grid_slaves(row=4, column=1)
                            for entry in grid_slave4_1:
                                masse_volumique_apparente = entry.get()
                                if (not util.is_decimal_number(
                                        masse_volumique_apparente) and masse_volumique_apparente != "") or (
                                        util.is_decimal_number(masse_volumique_apparente) and float(
                                    masse_volumique_apparente) < 0):
                                    entree_invalide_liste.append(
                                        (information_champs[index]["nom_du_champs"],
                                         "Zone gestion " + str(
                                             index_zone),
                                         "\"Masse volumique apparente\" doit être un réel positif ou laissé vide pour aller chercher la valeur par défaut"))
                                else:
                                    if masse_volumique_apparente == "":
                                        masse_volumique_apparente = None
                                    else:
                                        masse_volumique_apparente = float(masse_volumique_apparente)
                            grid_slave5_1 = champs_frame_widget.grid_slaves(row=5, column=1)
                            for entry in grid_slave5_1:
                                profondeur = entry.get()
                                if not util.is_decimal_number(profondeur) or float(
                                        profondeur) < 0:
                                    entree_invalide_liste.append((information_champs[index]["nom_du_champs"],
                                                                  "Zone gestion " + str(index_zone),
                                                                  "\"Profondeur\" doit être un réel positif"))
                                else:
                                    profondeur = float(profondeur)
                            grid_slave6_1 = champs_frame_widget.grid_slaves(row=6, column=1)
                            for entry in grid_slave6_1:
                                superficie_de_la_zone = entry.get()
                                if not util.is_decimal_number(superficie_de_la_zone) or float(
                                        superficie_de_la_zone) < 0:
                                    entree_invalide_liste.append((information_champs[index]["nom_du_champs"],
                                                                  "Zone gestion " + str(index_zone),
                                                                  "\"Superficie de la zone\" doit être un réel positif"))
                                else:
                                    superficie_de_la_zone = float(superficie_de_la_zone)
                            information_champs[index]["information_zone_de_gestion"].append(
                                {"taux_matiere_organique": taux_matiere_organique,
                                 "municipalite": municipalite,
                                 "classe_texturale": classe_texturale,
                                 "classe_de_drainage": classe_de_drainage,
                                 "masse_volumique_apparente": masse_volumique_apparente,
                                 "profondeur": profondeur,
                                 "superficie_de_la_zone": superficie_de_la_zone})
                            index_zone += 1
                index += 1
            if len(entree_invalide_liste) == 0:
                sauvegarde_reussi = sauvegarder_attributs_entreprise_apres_creation()
                for widget in zone_de_gestion_mainframe.winfo_children():
                    widget.destroy()

                if sauvegarde_reussi:
                    question_ajout_regie_historique(zone_de_gestion_mainframe)
                else:
                    show_creation_zone_de_gestion(zone_de_gestion_mainframe, fill_fields=True)
            else:
                information_champs = info_champs_temporaire
                message = ""
                for entree_invalide in entree_invalide_liste:
                    message = message + "Dans le " + entree_invalide[0] + " et la " + entree_invalide[
                        1] + " l'entrée " + entree_invalide[2] + "\n"
                messagebox.showwarning("Warning", message)

        canvas = tk.Canvas(zone_de_gestion_mainframe)
        scrollbar = ttk.Scrollbar(zone_de_gestion_mainframe, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        for index_champs in range(int(nombre_de_champs)):
            global information_champs
            champs_frame = ttk.LabelFrame(scrollable_frame, text=information_champs[index_champs]["nom_du_champs"])
            for index_zone_de_gestion in range(int(information_champs[index_champs]["nombre_de_zone_de_gestion"])):
                zone_de_gestion_frame = ttk.LabelFrame(champs_frame,
                                                       text="Zone  gestion " + str(index_zone_de_gestion + 1))
                taux_matiere_organique_label = ttk.Label(zone_de_gestion_frame, text="Taux matière organique (en %): ")
                taux_matiere_organique_entry = ttk.Entry(zone_de_gestion_frame)
                municipalite_label = ttk.Label(zone_de_gestion_frame, text="Municipalité: ")
                global municipalites_supportees
                municipalite_combobox = ttk.Combobox(zone_de_gestion_frame, values=municipalites_supportees,
                                                     postcommand=lambda: filter_combobox_values(municipalite_combobox,
                                                                                                municipalites_supportees))
                classe_texturale_label = ttk.Label(zone_de_gestion_frame, text="Classe texturale: ")
                global classes_texturales_supportees
                classe_texturale_combobox = ttk.Combobox(zone_de_gestion_frame, values=classes_texturales_supportees,
                                                         postcommand=lambda: filter_combobox_values(
                                                             classe_texturale_combobox,
                                                             classes_texturales_supportees))
                classe_de_drainage_label = ttk.Label(zone_de_gestion_frame, text="Classe de drainage: ")
                global classes_de_drainage_supportees
                classe_de_drainage_combobox = ttk.Combobox(zone_de_gestion_frame, values=classes_de_drainage_supportees,
                                                           postcommand=lambda: filter_combobox_values(
                                                               classe_de_drainage_combobox,
                                                               classes_de_drainage_supportees))
                masse_volumique_apparente_label = ttk.Label(zone_de_gestion_frame,
                                                            text="Masse volumique apparente (g/cm3): ")
                masse_volumique_apparente_entry = ttk.Entry(zone_de_gestion_frame)
                profondeur_label = ttk.Label(zone_de_gestion_frame, text="Profondeur (cm): ")
                profondeur_entry = ttk.Entry(zone_de_gestion_frame)
                superficie_de_la_zone_label = ttk.Label(zone_de_gestion_frame, text="Superficie de la zone (ha): ")
                superficie_de_la_zone_entry = ttk.Entry(zone_de_gestion_frame)

                if fill_fields:
                    taux_matiere_organique_entry.insert(0, information_champs[index_champs]["information_zone_de_gestion"][index_zone_de_gestion]["taux_matiere_organique"])
                    municipalite_combobox.insert(0, information_champs[index_champs]["information_zone_de_gestion"][index_zone_de_gestion]["municipalite"])
                    classe_texturale_combobox.insert(0, information_champs[index_champs]["information_zone_de_gestion"][index_zone_de_gestion]["classe_texturale"])
                    classe_de_drainage_combobox.insert(0, information_champs[index_champs]["information_zone_de_gestion"][index_zone_de_gestion]["classe_de_drainage"])
                    masse_volumique_apparente_entry.insert(0, information_champs[index_champs]["information_zone_de_gestion"][index_zone_de_gestion]["masse_volumique_apparente"])
                    profondeur_entry.insert(0, information_champs[index_champs]["information_zone_de_gestion"][index_zone_de_gestion]["profondeur"])
                    superficie_de_la_zone_entry.insert(0, information_champs[index_champs]["information_zone_de_gestion"][index_zone_de_gestion]["superficie_de_la_zone"])

                taux_matiere_organique_label.grid(row=0, column=0, sticky="w", pady=3, padx=5)
                taux_matiere_organique_entry.grid(row=0, column=1, sticky="w", pady=3, padx=5)
                municipalite_label.grid(row=1, column=0, sticky="w", pady=3, padx=5)
                municipalite_combobox.grid(row=1, column=1, sticky="w", pady=3, padx=5)
                classe_texturale_label.grid(row=2, column=0, sticky="w", pady=3, padx=5)
                classe_texturale_combobox.grid(row=2, column=1, sticky="w", pady=3, padx=5)
                classe_de_drainage_label.grid(row=3, column=0, sticky="w", pady=3, padx=5)
                classe_de_drainage_combobox.grid(row=3, column=1, sticky="w", pady=3, padx=5)
                masse_volumique_apparente_label.grid(row=4, column=0, sticky="w", pady=3, padx=5)
                masse_volumique_apparente_entry.grid(row=4, column=1, sticky="w", pady=3, padx=5)
                profondeur_label.grid(row=5, column=0, sticky="w", pady=3, padx=5)
                profondeur_entry.grid(row=5, column=1, sticky="w", pady=3, padx=5)
                superficie_de_la_zone_label.grid(row=6, column=0, sticky="w", pady=3, padx=5)
                superficie_de_la_zone_entry.grid(row=6, column=1, sticky="w", pady=3, padx=5)

                zone_de_gestion_frame.pack()

            champs_frame.pack(fill="both", padx=10, pady=5, ipadx=10, ipady=5)

        canvas.pack(side="left", ipadx=10)
        scrollbar.pack(side="right", fill="y")

        creation_zone_de_gestion_bouton = ttk.Button(scrollable_frame, text="Créer",
                                                     command=lambda: get_information_zone_de_gestion(scrollable_frame))
        creation_zone_de_gestion_bouton.pack()

    def show_creation_des_regies(parent_frame_tabs, show_regie_historique, simulations=None):
        def add_new_simulation_tab(event):
            clicked_tab = simulation_notebook.tk.call(simulation_notebook._w, "identify", "tab", event.x, event.y)
            if clicked_tab == simulation_notebook.index("end") - 1:
                index_clicked_tab = simulation_notebook.index(clicked_tab)
                simulation_notebook.winfo_children()[index_clicked_tab].destroy()
                global nombre_simulations
                nombre_simulations += 1

                def duree_de_la_simulation():
                    def readd_simulation():
                        root.deiconify()
                        tab = ttk.Frame(simulation_notebook)
                        simulation_notebook.add(tab, text="+")
                        global nombre_simulations
                        nombre_simulations -= 1
                        duree_simulation_window.destroy()

                    def get_duree_de_la_simulation():
                        root.deiconify()
                        nom_simulation = nom_simulation_entry.get()
                        annee_projection_initiale = annee_projection_initiale_entry.get()
                        duree_projection = duree_projection_entry.get()
                        numero_simulation_copie = numero_simulation_copie_entry.get()
                        if numero_simulation_copie == "":
                            numero_simulation_copie = None
                        global annees_historiques
                        global nombre_simulations
                        annee_projection_initiale_valide = True
                        if annees_historiques is not None:
                            if int(annees_historiques["annee_historique_finale"]) + 1 != int(annee_projection_initiale):
                                annee_projection_initiale_valide = False
                        if annee_projection_initiale.isdigit() and duree_projection.isdigit() \
                                and int(duree_projection) > 0 \
                                and annee_projection_initiale_valide and \
                                (numero_simulation_copie is None or (numero_simulation_copie.isdigit() and
                                                                     (nombre_simulations > int(
                                                                         numero_simulation_copie) > 0))) and \
                                len(nom_simulation) < 13:
                            global duree_simulation
                            duree_simulation.append({"annee_projection_initiale": annee_projection_initiale,
                                                     "duree_projection": duree_projection,
                                                     "nom_simulation": nom_simulation})
                            if numero_simulation_copie is not None:
                                simulation = simulation_notebook.winfo_children()[int(numero_simulation_copie) - 1]
                                simulation_copie = get_information_simulation(simulation,
                                                                              int(numero_simulation_copie) - 1,
                                                                              simulation_unique=True)
                                if simulation_copie[0] is not None:
                                    simulation_copie = simulation_copie[0]
                                    duree_simulation_window.destroy()
                                    set_up_simulation(simulation_notebook, simulation_copie, False)
                                else:
                                    message = ""
                                    for entree_invalide in simulation_copie[1]:
                                        message = message + "Dans la " + entree_invalide[3] + ", le " + entree_invalide[
                                            0] + " et la " + \
                                                  entree_invalide[
                                                      1] + " l'entrée " + entree_invalide[2] + "\n"
                                    messagebox.showwarning("Warning", message)
                                    readd_simulation()
                            else:
                                simulation_copie = None
                                duree_simulation_window.destroy()
                                set_up_simulation(simulation_notebook, simulation_copie, True)
                        else:
                            entree_invalide_liste = []
                            message = ""
                            if not annee_projection_initiale.isdigit() or not annee_projection_initiale_valide:
                                entree_invalide_liste.append(
                                    "L'entrée \"Année de projection initiale\" est invalide. Si il y a une année historique finale, elle doit être supérieur d'une année à celle-ci et être un nombre naturel plus grand que 0.")
                            if not duree_projection.isdigit() or int(duree_projection) <= 0:
                                entree_invalide_liste.append(
                                    "L'entrée \"Durée de la projection\" est invalide. Elle doit être un nombre naturel plus grand que 0.")
                            if (numero_simulation_copie is not None and not numero_simulation_copie.isdigit()) or (
                                    numero_simulation_copie is not None and (int(
                                numero_simulation_copie) >= nombre_simulations or int(
                                numero_simulation_copie) < 1)):
                                entree_invalide_liste.append(
                                    "L'entrée \"Numéro de la simulation à copier\" est invalide. Elle doit être un nombre naturel plus grand que 0 et parmis les numéros de simulations existantes.")
                            if len(nom_simulation) > 12:
                                entree_invalide_liste.append(
                                    "Le nom de la simulation doit être composé de 12 caractères ou moins.")

                            for entree_invalide in entree_invalide_liste:
                                message = message + entree_invalide
                            messagebox.showwarning("Warning", message)
                            readd_simulation()

                    root.withdraw()
                    duree_simulation_window = tk.Toplevel()
                    duree_simulation_window.focus()
                    duree_simulation_window.protocol("WM_DELETE_WINDOW", readd_simulation)
                    duree_simulation_frame = ttk.Frame(duree_simulation_window)
                    nom_simulation_label = ttk.Label(duree_simulation_frame, text="Nom simulation: ")
                    nom_simulation_entry = ttk.Entry(duree_simulation_frame)
                    annee_projection_initiale_label = ttk.Label(duree_simulation_frame,
                                                                text="Année de projection initiale: ")
                    annee_projection_initiale_entry = ttk.Entry(duree_simulation_frame)
                    duree_projection_label = ttk.Label(duree_simulation_frame,
                                                       text="Durée de la projection: ")
                    duree_projection_entry = ttk.Entry(duree_simulation_frame)
                    duree_projection_entry.insert(0, "30")

                    numero_simulation_copie_label = ttk.Label(duree_simulation_frame,
                                                              text="Numéro de la simulation à copier: ")
                    numero_simulation_copie_entry = ttk.Entry(duree_simulation_frame)

                    global nombre_simulations
                    if nombre_simulations < 2:
                        numero_simulation_copie_entry.configure(state="disabled")

                    nom_simulation_label.grid(row=0, column=0, sticky="w", pady=3, padx=5)
                    nom_simulation_entry.grid(row=0, column=1, sticky="w", pady=3, padx=5)
                    annee_projection_initiale_label.grid(row=1, column=0, sticky="w", pady=3, padx=5)
                    annee_projection_initiale_entry.grid(row=1, column=1, sticky="w", pady=3, padx=5)
                    duree_projection_label.grid(row=2, column=0, sticky="w", pady=3, padx=5)
                    duree_projection_entry.grid(row=2, column=1, sticky="w", pady=3, padx=5)
                    numero_simulation_copie_label.grid(row=3, column=0, sticky="w", pady=3, padx=5)
                    numero_simulation_copie_entry.grid(row=3, column=1, sticky="w", pady=3, padx=5)

                    creer_simulation_bouton = ttk.Button(duree_simulation_frame, text="Créer",
                                                         command=get_duree_de_la_simulation)
                    creer_simulation_bouton.grid(row=5, column=0, columnspan=2, pady=3)
                    duree_simulation_frame.pack()

                duree_de_la_simulation()

        def delete_simulation_tab(event):
            clicked_tab = simulation_notebook.tk.call(simulation_notebook._w, "identify", "tab", event.x, event.y)
            index_clicked_tab = simulation_notebook.index(clicked_tab)
            if index_clicked_tab != simulation_notebook.index("end") - 1:
                simulation_notebook.winfo_children()[index_clicked_tab].destroy()
                global max_index_simulation
                global furthest_left_tab_index_simulation
                global furthest_right_tab_index_simulation
                if furthest_left_tab_index_simulation == min_index_simulation and len(
                        simulation_notebook.winfo_children()) > 5:
                    simulation_notebook.tab(furthest_right_tab_index_simulation, state="normal")
                elif furthest_left_tab_index_simulation == min_index_simulation and len(
                        simulation_notebook.winfo_children()) == 5:
                    for tab_index in range(len(simulation_notebook.winfo_children())):
                        simulation_notebook.tab(tab_index, state="normal")
                    scroll_right_button_simulation.configure(state="disabled")
                elif furthest_right_tab_index_simulation == max_index_simulation and len(
                        simulation_notebook.winfo_children()) == 5:
                    furthest_right_tab_index_simulation -= 1
                    furthest_left_tab_index_simulation -= 1
                    simulation_notebook.tab(furthest_left_tab_index_simulation, state="normal")
                    scroll_left_button_simulation.configure(state="disabled")
                elif furthest_left_tab_index_simulation == min_index_simulation and len(
                        simulation_notebook.winfo_children()) <= 4:
                    furthest_right_tab_index_simulation -= 1
                elif furthest_right_tab_index_simulation == max_index_simulation and len(
                        simulation_notebook.winfo_children()) > 5:
                    furthest_left_tab_index_simulation -= 1
                    furthest_right_tab_index_simulation -= 1
                    simulation_notebook.tab(furthest_left_tab_index_simulation, state="normal")
                else:
                    simulation_notebook.tab(furthest_right_tab_index_simulation, state="normal")
                    if max_index_simulation - 1 == furthest_right_tab_index_simulation:
                        scroll_right_button_simulation.configure(state="disabled")
                global nombre_simulations
                nombre_simulations -= 1
                global duree_simulation
                duree_simulation.pop(index_clicked_tab)
                max_index_simulation -= 1

        def set_up_simulation(simulation_notebook, simulation_copie, simulation_en_tete_de_liste):
            global nombre_simulations
            global furthest_left_tab_index_simulation
            global furthest_right_tab_index_simulation
            global max_index_simulation
            global duree_simulation
            global information_champs
            global nombre_de_champs
            global simulations_chargees
            global min_index_champs
            if (4 < nombre_simulations and not simulations_chargees) or (
                    simulations_chargees and len(simulation_notebook.winfo_children()) > 3):
                simulation_notebook.tab(furthest_left_tab_index_simulation, state="hidden")
                scroll_left_button_simulation.configure(state="normal")
                furthest_left_tab_index_simulation += 1
            furthest_right_tab_index_simulation += 1
            max_index_simulation += 1
            tab = ttk.Frame(simulation_notebook)

            if simulations_chargees:
                simulation_notebook.add(tab, text=simulation_copie["nom_simulation"])
            else:
                simulation_notebook.add(tab, text=duree_simulation[nombre_simulations - 1]["nom_simulation"])
            new_tab = ttk.Frame(simulation_notebook)
            simulation_notebook.add(new_tab, text="+")
            champs_notebook = ttk.Notebook(tab)
            champs_notebook.bind("<<NotebookTabChanged>>", zone_tab_management)

            def add_new_champs_tab(event):
                clicked_tab = champs_notebook.tk.call(champs_notebook._w, "identify", "tab", event.x, event.y)
                if clicked_tab == champs_notebook.index("end") - 1:
                    global nombre_de_champs
                    set_up_new_champs()

            def delete_champs_tab(event):
                clicked_tab = champs_notebook.tk.call(champs_notebook._w, "identify", "tab", event.x, event.y)
                index_clicked_tab = champs_notebook.index(clicked_tab)
                if index_clicked_tab != champs_notebook.index("end") - 1:
                    global information_champs
                    information_champs.pop(index_clicked_tab)
                    global nombre_de_champs
                    nombre_de_champs -= 1
                    sauvegarder_attributs_entreprise_apres_modification()
                    donnees_de_rechauffement_label_frame.winfo_children()[0].winfo_children()[0].winfo_children()[
                        index_clicked_tab].destroy()
                    champs_index = index_clicked_tab
                    while champs_index < len(donnees_de_rechauffement_label_frame.winfo_children()[0].winfo_children()[
                                                 0].winfo_children()):
                        donnees_de_rechauffement_label_frame.winfo_children()[0].winfo_children()[0].winfo_children()[
                            champs_index].configure(text=information_champs[champs_index]["nom_du_champs"])
                        champs_index += 1
                    for simulation_frame in simulation_notebook.winfo_children():
                        if len(simulation_frame.winfo_children()) == 0:
                            pass
                        else:
                            notebook = simulation_frame.winfo_children()[0]
                            notebook.winfo_children()[index_clicked_tab].destroy()
                            global furthest_left_tab_index_champs
                            global furthest_right_tab_index_champs
                            global max_index_champs
                            if furthest_left_tab_index_champs == min_index_champs and len(
                                    notebook.winfo_children()) > 5:
                                notebook.tab(furthest_right_tab_index_champs, state="normal")
                            elif furthest_left_tab_index_champs == min_index_champs and len(
                                    notebook.winfo_children()) == 5:
                                for tab_index in range(len(notebook.winfo_children())):
                                    notebook.tab(tab_index, state="normal")
                            elif furthest_right_tab_index_champs == max_index_champs and len(
                                    notebook.winfo_children()) == 5:
                                notebook.tab(furthest_left_tab_index_champs - 1, state="normal")
                            elif furthest_left_tab_index_champs == min_index_champs and len(
                                    notebook.winfo_children()) <= 4:
                                pass
                            elif furthest_right_tab_index_champs == max_index_champs and len(
                                    notebook.winfo_children()) > 5:
                                notebook.tab(furthest_left_tab_index_champs, state="normal")
                            else:
                                notebook.tab(furthest_right_tab_index_champs, state="normal")

                    notebook = simulation_notebook.winfo_children()[0].winfo_children()[0]
                    if furthest_left_tab_index_champs == min_index_champs and len(
                            notebook.winfo_children()) > 5:
                        pass
                    elif furthest_left_tab_index_champs == min_index_champs and len(
                            notebook.winfo_children()) == 5:
                        scroll_right_button_champs.configure(state="disabled")
                    elif furthest_right_tab_index_champs == max_index_champs and len(
                            notebook.winfo_children()) == 5:
                        furthest_left_tab_index_champs -= 1
                        furthest_right_tab_index_champs -= 1
                        scroll_left_button_champs.configure(state="disabled")
                    elif furthest_left_tab_index_champs == min_index_champs and len(
                            notebook.winfo_children()) <= 4:
                        furthest_right_tab_index_champs -= 1
                    elif furthest_right_tab_index_champs == max_index_champs and len(
                            notebook.winfo_children()) > 5:
                        furthest_left_tab_index_champs -= 1
                        furthest_right_tab_index_champs -= 1
                    else:
                        if max_index_champs - 1 == furthest_right_tab_index_champs:
                            scroll_right_button_champs.configure(state="disabled")
                    max_index_champs -= 1

            champs_notebook.bind("<Button-1>", add_new_champs_tab)
            champs_notebook.bind("<Button-3>", delete_champs_tab)

            global max_index_champs
            global furthest_right_tab_index_champs
            global furthest_left_tab_index_champs
            index_champs = 0
            for champs in information_champs:
                tab = ttk.Frame(champs_notebook)

                if simulation_en_tete_de_liste:
                    max_index_champs += 1
                    furthest_right_tab_index_champs += 1
                    if index_champs > 3:
                        champs_notebook.tab(furthest_left_tab_index_champs, state="hidden")
                        furthest_left_tab_index_champs += 1
                champs_notebook.add(tab, text=champs["nom_du_champs"])
                if not simulation_en_tete_de_liste and (
                        index_champs < furthest_left_tab_index_champs or index_champs > furthest_right_tab_index_champs):
                    champs_notebook.tab(index_champs, state="hidden")
                zone_de_gestion_notebook = ttk.Notebook(tab)
                set_up_champs(zone_de_gestion_notebook, int(champs["nombre_de_zone_de_gestion"]), champs_notebook,
                              simulation_copie, index_champs)
                index_champs += 1

            global nombre_de_champs
            if nombre_de_champs > 4:
                scroll_left_button_champs.configure(state="normal")

            tab = ttk.Frame(champs_notebook)
            champs_notebook.add(tab, text="+")

            champs_notebook.pack(anchor="nw")

        def set_up_new_champs():
            new_champs_window = tk.Toplevel()
            global nombre_de_champs_modifie
            nombre_de_champs_modifie = False
            global information_champs_modifie
            information_champs_modifie = False

            def revenir_a_etat_initial():
                global nombre_de_champs_modifie
                if nombre_de_champs_modifie:
                    global nombre_de_champs
                    nombre_de_champs -= 1
                global information_champs_modifie
                if information_champs_modifie:
                    global information_champs
                    information_champs.pop(len(information_champs) - 1)
                new_champs_window.destroy()

            new_champs_window.protocol("WM_DELETE_WINDOW", revenir_a_etat_initial)

            def creation_des_zone_de_gestion_du_nouveau_champs():
                nom_du_champs = nom_du_champs_entry.get()
                nombre_de_zone_de_gestion = nombre_de_zone_de_gestion_entry.get()
                if nombre_de_zone_de_gestion.isdigit() and int(nombre_de_zone_de_gestion) > 0:
                    if len(nom_du_champs) < 13:
                        global information_champs
                        information_champs.append({"nom_du_champs": nom_du_champs,
                                                   "nombre_de_zone_de_gestion": nombre_de_zone_de_gestion,
                                                   "information_zone_de_gestion": []})
                        global nombre_de_champs
                        nombre_de_champs += 1
                        global nombre_de_champs_modifie
                        nombre_de_champs_modifie = True
                        global information_champs_modifie
                        information_champs_modifie = True

                        for widget in new_champs_window.winfo_children():
                            widget.destroy()
                        creation_zone_frame = ttk.Frame(new_champs_window)
                        canvas = tk.Canvas(creation_zone_frame)
                        scrollbar = ttk.Scrollbar(creation_zone_frame, orient="vertical", command=canvas.yview)
                        scrollable_frame = ttk.Frame(canvas)
                        scrollable_frame.bind("<Configure>",
                                              lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
                        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
                        canvas.configure(yscrollcommand=scrollbar.set)
                        for index_zone_de_gestion_nouveau_champs in range(
                                int(nombre_de_zone_de_gestion)):
                            zone_de_gestion_frame = ttk.LabelFrame(scrollable_frame,
                                                                   text="Zone gestion " + str(
                                                                       index_zone_de_gestion_nouveau_champs + 1))
                            taux_matiere_organique_label = ttk.Label(zone_de_gestion_frame,
                                                                     text="Taux matière organique (en %): ")
                            taux_matiere_organique_entry = ttk.Entry(zone_de_gestion_frame)
                            municipalite_label = ttk.Label(zone_de_gestion_frame, text="Municipalité: ")
                            global municipalites_supportees
                            municipalite_combobox = ttk.Combobox(zone_de_gestion_frame, values=municipalites_supportees,
                                                                 postcommand=lambda: filter_combobox_values(
                                                                     municipalite_combobox, municipalites_supportees))
                            classe_texturale_label = ttk.Label(zone_de_gestion_frame, text="Classe texturale: ")
                            global classes_texturales_supportees
                            classe_texturale_combobox = ttk.Combobox(zone_de_gestion_frame,
                                                                     values=classes_texturales_supportees,
                                                                     postcommand=lambda: filter_combobox_values(
                                                                         classe_texturale_combobox,
                                                                         classes_texturales_supportees))
                            classe_de_drainage_label = ttk.Label(zone_de_gestion_frame, text="Classe de drainage: ")
                            global classes_de_drainage_supportees
                            classe_de_drainage_combobox = ttk.Combobox(zone_de_gestion_frame,
                                                                       values=classes_de_drainage_supportees,
                                                                       postcommand=lambda: filter_combobox_values(
                                                                           classe_de_drainage_combobox,
                                                                           classes_de_drainage_supportees))
                            masse_volumique_apparente_label = ttk.Label(zone_de_gestion_frame,
                                                                        text="Masse volumique apparente (g/cm3): ")
                            masse_volumique_apparente_entry = ttk.Entry(zone_de_gestion_frame)
                            profondeur_label = ttk.Label(zone_de_gestion_frame, text="Profondeur (cm): ")
                            profondeur_entry = ttk.Entry(zone_de_gestion_frame)
                            superficie_de_la_zone_label = ttk.Label(zone_de_gestion_frame,
                                                                    text="Superficie de la zone (ha): ")
                            superficie_de_la_zone_entry = ttk.Entry(zone_de_gestion_frame)
                            taux_matiere_organique_label.grid(row=0, column=0, sticky="w", pady=3, padx=5)
                            taux_matiere_organique_entry.grid(row=0, column=1, sticky="w", pady=3, padx=5)
                            municipalite_label.grid(row=1, column=0, sticky="w", pady=3, padx=5)
                            municipalite_combobox.grid(row=1, column=1, sticky="w", pady=3, padx=5)
                            classe_texturale_label.grid(row=2, column=0, sticky="w", pady=3, padx=5)
                            classe_texturale_combobox.grid(row=2, column=1, sticky="w", pady=3, padx=5)
                            classe_de_drainage_label.grid(row=3, column=0, sticky="w", pady=3, padx=5)
                            classe_de_drainage_combobox.grid(row=3, column=1, sticky="w", pady=3, padx=5)
                            masse_volumique_apparente_label.grid(row=4, column=0, sticky="w", pady=3, padx=5)
                            masse_volumique_apparente_entry.grid(row=4, column=1, sticky="w", pady=3, padx=5)
                            profondeur_label.grid(row=5, column=0, sticky="w", pady=3, padx=5)
                            profondeur_entry.grid(row=5, column=1, sticky="w", pady=3, padx=5)
                            superficie_de_la_zone_label.grid(row=6, column=0, sticky="w", pady=3, padx=5)
                            superficie_de_la_zone_entry.grid(row=6, column=1, sticky="w", pady=3, padx=5)

                            zone_de_gestion_frame.pack()

                        creation_zone_de_gestion_bouton = ttk.Button(scrollable_frame, text="Créer",
                                                                     command=lambda: add_new_zone_tab())
                        creation_zone_de_gestion_bouton.pack()
                        canvas.pack(side="left", fill="x", expand=True)
                        scrollbar.pack(side="right", fill="y")
                        creation_zone_frame.pack(fill=None, expand=False)
                    else:
                        messagebox.showwarning("Warning",
                                               "Le nom du champ devrait être composé de 12 caractères ou moins.")
                        new_champs_window.focus()
                else:
                    message = "L'entrée \"Nombre de zones gestion\" est invalide. Elle doit être un nombre naturel plus grand que 0."
                    messagebox.showwarning("Warning", message)
                    new_champs_window.focus()

                def add_new_zone_tab():
                    entree_invalide_liste = []
                    global nomde_de_champs
                    global information_champs
                    index_zone = 0
                    for scrollable_frame_widget in scrollable_frame.winfo_children():
                        if isinstance(scrollable_frame_widget, ttk.LabelFrame):
                            grid_slave0_1 = scrollable_frame_widget.grid_slaves(row=0, column=1)
                            for entry in grid_slave0_1:
                                taux_matiere_organique = entry.get()
                                if not util.is_decimal_number(taux_matiere_organique) or float(
                                        taux_matiere_organique) < 0 or float(taux_matiere_organique) > 100:
                                    entree_invalide_liste.append(
                                        (information_champs[nombre_de_champs - 1]["nom_du_champs"],
                                         "Zone gestion " + str(index_zone + 1),
                                         "\"Taux de matière organique\" doit être un réel positif dans l'intervalle [0,100]"))
                                else:
                                    taux_matiere_organique = float(taux_matiere_organique)
                            grid_slave1_1 = scrollable_frame_widget.grid_slaves(row=1, column=1)
                            for entry in grid_slave1_1:
                                municipalite = entry.get()
                                global municipalites_supportees
                                if municipalite not in municipalites_supportees:
                                    entree_invalide_liste.append(
                                        (information_champs[nombre_de_champs - 1]["nom_du_champs"],
                                         "Zone gestion " + str(index_zone + 1),
                                         "\"Municipalité\" doit être parmis les choix disponibles"))
                            grid_slave2_1 = scrollable_frame_widget.grid_slaves(row=2, column=1)
                            for entry in grid_slave2_1:
                                classe_texturale = entry.get()
                                global classes_texturales_supportees
                                if classe_texturale not in classes_texturales_supportees:
                                    entree_invalide_liste.append(
                                        (information_champs[nombre_de_champs - 1]["nom_du_champs"],
                                         "Zone gestion " + str(index_zone + 1),
                                         "\"Classe texturale\" doit être parmis les choix disponibles"))
                            grid_slave3_1 = scrollable_frame_widget.grid_slaves(row=3, column=1)
                            for entry in grid_slave3_1:
                                classe_de_drainage = entry.get()
                                global classes_de_drainage_supportees
                                if classe_de_drainage not in classes_de_drainage_supportees:
                                    entree_invalide_liste.append(
                                        (information_champs[nombre_de_champs - 1]["nom_du_champs"],
                                         "Zone gestion " + str(index_zone + 1),
                                         "\"Classe de drainage\" doit être parmis les choix disponibles"))
                            grid_slave4_1 = scrollable_frame_widget.grid_slaves(row=4, column=1)
                            for entry in grid_slave4_1:
                                masse_volumique_apparente = entry.get()
                                if (not util.is_decimal_number(
                                        masse_volumique_apparente) and masse_volumique_apparente != "") or (
                                        util.is_decimal_number(masse_volumique_apparente) and float(
                                    masse_volumique_apparente) < 0):
                                    entree_invalide_liste.append(
                                        (information_champs[nombre_de_champs - 1]["nom_du_champs"],
                                         "Zone gestion " + str(
                                             index_zone + 1),
                                         "\"Masse volumique apparente\" doit être un réel positif ou laissé vide pour aller chercher la valeur par défaut"))
                                else:
                                    if masse_volumique_apparente == "":
                                        masse_volumique_apparente = None
                                    else:
                                        masse_volumique_apparente = float(masse_volumique_apparente)
                            grid_slave5_1 = scrollable_frame_widget.grid_slaves(row=5, column=1)
                            for entry in grid_slave5_1:
                                profondeur = entry.get()
                                if not util.is_decimal_number(profondeur) or float(
                                        profondeur) < 0:
                                    entree_invalide_liste.append(
                                        (information_champs[nombre_de_champs - 1]["nom_du_champs"],
                                         "Zone gestion " + str(index_zone + 1),
                                         "\"Profondeur\" doit être un réel positif"))
                                else:
                                    profondeur = float(profondeur)
                            grid_slave6_1 = scrollable_frame_widget.grid_slaves(row=6, column=1)
                            for entry in grid_slave6_1:
                                superficie_de_la_zone = entry.get()
                                if not util.is_decimal_number(superficie_de_la_zone) or float(
                                        superficie_de_la_zone) < 0:
                                    entree_invalide_liste.append(
                                        (information_champs[nombre_de_champs - 1]["nom_du_champs"],
                                         "Zone gestion " + str(index_zone + 1),
                                         "\"Superficie de la zone\" doit être un réel positif"))
                                else:
                                    superficie_de_la_zone = float(superficie_de_la_zone)
                            information_champs[len(information_champs) - 1]["information_zone_de_gestion"].append(
                                {"taux_matiere_organique": taux_matiere_organique,
                                 "municipalite": municipalite,
                                 "classe_texturale": classe_texturale,
                                 "classe_de_drainage": classe_de_drainage,
                                 "masse_volumique_apparente": masse_volumique_apparente,
                                 "profondeur": profondeur,
                                 "superficie_de_la_zone": superficie_de_la_zone})
                        index_zone += 1
                    if len(entree_invalide_liste) == 0:
                        sauvegarder_attributs_entreprise_apres_modification()
                        new_champs_window.destroy()
                        global furthest_left_tab_index_champs
                        global max_index_champs
                        global furthest_right_tab_index_champs
                        for simulation_frame in simulation_notebook.winfo_children():
                            if len(simulation_frame.winfo_children()) == 0:
                                pass
                            else:
                                notebook = simulation_frame.winfo_children()[0]
                                for champs_frame in notebook.winfo_children():
                                    if len(champs_frame.winfo_children()) == 0:
                                        champs_frame.destroy()
                                    else:
                                        pass
                                tab = ttk.Frame(notebook)
                                notebook.add(tab, text=nom_du_champs)
                                zone_notebook = ttk.Notebook(tab)
                                set_up_champs(zone_notebook, nombre_de_zone_de_gestion, notebook)
                                new_tab = ttk.Frame(notebook)
                                notebook.add(new_tab, text="+")
                                if len(notebook.winfo_children()) > 5:
                                    notebook.tab(furthest_left_tab_index_champs, state="hidden")

                        max_index_champs += 1
                        furthest_right_tab_index_champs += 1
                        if len(simulation_notebook.winfo_children()[0].winfo_children()[0].winfo_children()) > 5:
                            furthest_left_tab_index_champs += 1
                            scroll_left_button_champs.configure(state="normal")
                        rechauffement_champs_label_frame = ttk.LabelFrame(
                            donnees_de_rechauffement_label_frame.winfo_children()[0].winfo_children()[0],
                            text=nom_du_champs)
                        rechauffement_champs_label_frame.pack()
                        index_zone = 0
                        while index_zone < int(nombre_de_zone_de_gestion):
                            rechauffement_zone_label_frame = ttk.LabelFrame(rechauffement_champs_label_frame,
                                                                            text="Zone gestion " + str(
                                                                                index_zone + 1))
                            rechauffement_zone_label_frame.pack()
                            if show_regie_historique:
                                add_regies_historiques(rechauffement_zone_label_frame)
                            else:
                                ajouter_une_annee_a_la_rotation(rechauffement_zone_label_frame)
                            index_zone += 1
                    else:
                        information_champs[nombre_de_champs - 1]["information_zone_de_gestion"] = []
                        message = ""
                        for entree_invalide in entree_invalide_liste:
                            message = message + "Dans le " + entree_invalide[0] + " et la " + entree_invalide[
                                1] + " l'entrée " + entree_invalide[2] + "\n"
                        messagebox.showwarning("Warning", message)
                        new_champs_window.focus()

            nouveau_champs_frame = ttk.Frame(new_champs_window)
            nom_du_champs_label = ttk.Label(nouveau_champs_frame, text="Nom du champ: ")
            nom_du_champs_entry = ttk.Entry(nouveau_champs_frame)
            nombre_de_zone_de_gestion_label = ttk.Label(nouveau_champs_frame,
                                                        text="Nombre de zones gestion: ")
            nombre_de_zone_de_gestion_entry = ttk.Entry(nouveau_champs_frame)
            nom_du_champs_label.grid(row=0, column=0, sticky="w", pady=3, padx=5)
            nom_du_champs_entry.grid(row=0, column=1, sticky="w", pady=3, padx=5)
            nombre_de_zone_de_gestion_label.grid(row=1, sticky="w", column=0, pady=3, padx=5)
            nombre_de_zone_de_gestion_entry.grid(row=1, sticky="w", column=1, pady=3, padx=5)
            creer_nouveau_champs_bouton = ttk.Button(nouveau_champs_frame, text="Créer",
                                                     command=creation_des_zone_de_gestion_du_nouveau_champs)
            creer_nouveau_champs_bouton.grid(row=3, column=0, columnspan=2, pady=3, padx=5)
            nouveau_champs_frame.pack()

        def set_up_champs(zone_notebook, nombre_de_zone, champs_notebook, simulation_copie=None, index_champs=None):

            def add_new_zone_de_gestion_tab(event):
                clicked_tab = zone_notebook.tk.call(zone_notebook._w, "identify", "tab", event.x, event.y)
                if clicked_tab == zone_notebook.index("end") - 1:
                    champs_index = champs_notebook.index("current")
                    global information_champs
                    information_champs[champs_index]["nombre_de_zone_de_gestion"] = str(
                        int(information_champs[champs_index]["nombre_de_zone_de_gestion"]) + 1)
                    set_up_new_zone_de_gestion(champs_index)

            def delete_zone_de_gestion_tab(event):
                clicked_tab = zone_notebook.tk.call(zone_notebook._w, "identify", "tab", event.x, event.y)
                index_clicked_tab = zone_notebook.index(clicked_tab)
                if index_clicked_tab != zone_notebook.index("end") - 1:
                    champs_index = champs_notebook.index("current")
                    global information_champs
                    information_champs[champs_index]["nombre_de_zone_de_gestion"] = str(
                        int(information_champs[champs_index]["nombre_de_zone_de_gestion"]) - 1)
                    information_champs[champs_index]["information_zone_de_gestion"].pop(index_clicked_tab)
                    sauvegarder_attributs_entreprise_apres_modification()
                    donnees_de_rechauffement_label_frame.winfo_children()[0].winfo_children()[0].winfo_children()[
                        champs_index].winfo_children()[index_clicked_tab].destroy()
                    zone_index = index_clicked_tab
                    while zone_index < len(donnees_de_rechauffement_label_frame.winfo_children()[0].winfo_children()[
                                               0].winfo_children()[
                                               champs_index].winfo_children()):
                        donnees_de_rechauffement_label_frame.winfo_children()[0].winfo_children()[0].winfo_children()[
                            champs_index].winfo_children()[zone_index].configure(
                            text="Zone gestion " + str(zone_index + 1))
                        zone_index += 1
                    for simulation_frame in simulation_notebook.winfo_children():
                        if len(simulation_frame.winfo_children()) == 0:
                            pass
                        else:
                            notebook = simulation_frame.winfo_children()[0]
                            champs_courant_zone_notebook = \
                                notebook.winfo_children()[champs_index].winfo_children()[0]
                            champs_courant_zone_notebook.winfo_children()[index_clicked_tab].destroy()
                            current_index = index_clicked_tab
                            while current_index < champs_courant_zone_notebook.index("end"):
                                champs_courant_zone_notebook.tab(current_index,
                                                                 text="Zone gestion " + str(current_index + 1))
                                if current_index == champs_courant_zone_notebook.index("end") - 1:
                                    champs_courant_zone_notebook.tab(current_index, text="+")
                                current_index += 1
                    global max_index_zone
                    global furthest_left_tab_index_zone
                    global furthest_right_tab_index_zone
                    champs_courant_notebook = \
                        simulation_notebook.winfo_children()[simulation_notebook.index("current")].winfo_children()[0]
                    champs_courant_zone_notebook = \
                        champs_courant_notebook.winfo_children()[
                            champs_courant_notebook.index("current")].winfo_children()[
                            0]
                    if furthest_left_tab_index_zone == min_index_zone and len(
                            champs_courant_zone_notebook.winfo_children()) > 4:
                        champs_courant_zone_notebook.tab(furthest_right_tab_index_zone, state="normal")
                    elif furthest_left_tab_index_zone == min_index_zone and len(
                            champs_courant_zone_notebook.winfo_children()) == 4:
                        for tab_index in range(len(champs_courant_zone_notebook.winfo_children())):
                            champs_courant_zone_notebook.tab(tab_index, state="normal")
                        scroll_right_button_zone.configure(state="disabled")
                    elif furthest_right_tab_index_zone == max_index_zone and len(
                            champs_courant_zone_notebook.winfo_children()) == 4:
                        furthest_right_tab_index_zone -= 1
                        furthest_left_tab_index_zone -= 1
                        champs_courant_zone_notebook.tab(furthest_left_tab_index_zone, state="normal")
                        scroll_left_button_zone.configure(state="disabled")
                    elif furthest_left_tab_index_zone == min_index_zone and len(
                            champs_courant_zone_notebook.winfo_children()) <= 3:
                        furthest_right_tab_index_zone -= 1
                    elif furthest_right_tab_index_zone == max_index_zone and len(
                            champs_courant_zone_notebook.winfo_children()) > 4:
                        furthest_left_tab_index_zone -= 1
                        furthest_right_tab_index_zone -= 1
                        champs_courant_zone_notebook.tab(furthest_left_tab_index_zone, state="normal")
                    else:
                        champs_courant_zone_notebook.tab(furthest_right_tab_index_zone, state="normal")
                        if max_index_zone - 1 == furthest_right_tab_index_zone:
                            scroll_right_button_zone.configure(state="disabled")
                    max_index_zone -= 1

            def set_up_new_zone_de_gestion(champs_index):
                global information_champs

                def remise_a_etat_initial():
                    information_champs[champs_index]["nombre_de_zone_de_gestion"] = str(
                        int(information_champs[champs_index]["nombre_de_zone_de_gestion"]) - 1)
                    new_zone_window.destroy()

                new_zone_window = tk.Toplevel()
                new_zone_window.protocol("WM_DELETE_WINDOW", remise_a_etat_initial)
                creation_zone_frame = ttk.Frame(new_zone_window)
                canvas = tk.Canvas(creation_zone_frame)
                scrollbar = ttk.Scrollbar(creation_zone_frame, orient="vertical", command=canvas.yview)
                scrollable_frame = ttk.Frame(canvas)
                scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
                canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
                canvas.configure(yscrollcommand=scrollbar.set)
                zone_de_gestion_frame = ttk.LabelFrame(scrollable_frame,
                                                       text="Zone gestion " + str(
                                                           information_champs[champs_index][
                                                               "nombre_de_zone_de_gestion"]))
                taux_matiere_organique_label = ttk.Label(zone_de_gestion_frame,
                                                         text="Taux matière organique (en %): ")
                taux_matiere_organique_entry = ttk.Entry(zone_de_gestion_frame)
                municipalite_label = ttk.Label(zone_de_gestion_frame, text="Municipalité: ")
                global municipalites_supportees
                municipalite_combobox = ttk.Combobox(zone_de_gestion_frame, values=municipalites_supportees,
                                                     postcommand=lambda: filter_combobox_values(municipalite_combobox,
                                                                                                municipalites_supportees))
                classe_texturale_label = ttk.Label(zone_de_gestion_frame, text="Classe texturale: ")
                global classes_texturales_supportees
                classe_texturale_combobox = ttk.Combobox(zone_de_gestion_frame, values=classes_texturales_supportees,
                                                         postcommand=lambda: filter_combobox_values(
                                                             classe_texturale_combobox, classes_texturales_supportees))
                classe_de_drainage_label = ttk.Label(zone_de_gestion_frame, text="Classe de drainage: ")
                global classes_de_drainage_supportees
                classe_de_drainage_combobox = ttk.Combobox(zone_de_gestion_frame, values=classes_de_drainage_supportees,
                                                           postcommand=lambda: filter_combobox_values(
                                                               classe_de_drainage_combobox,
                                                               classes_de_drainage_supportees))
                masse_volumique_apparente_label = ttk.Label(zone_de_gestion_frame,
                                                            text="Masse volumique apparente (g/cm3): ")
                masse_volumique_apparente_entry = ttk.Entry(zone_de_gestion_frame)
                profondeur_label = ttk.Label(zone_de_gestion_frame, text="Profondeur (cm): ")
                profondeur_entry = ttk.Entry(zone_de_gestion_frame)
                superficie_de_la_zone_label = ttk.Label(zone_de_gestion_frame,
                                                        text="Superficie de la zone (ha): ")
                superficie_de_la_zone_entry = ttk.Entry(zone_de_gestion_frame)
                taux_matiere_organique_label.grid(row=0, column=0, sticky="w", pady=3, padx=5)
                taux_matiere_organique_entry.grid(row=0, column=1, sticky="w", pady=3, padx=5)
                municipalite_label.grid(row=1, column=0, sticky="w", pady=3, padx=5)
                municipalite_combobox.grid(row=1, column=1, sticky="w", pady=3, padx=5)
                classe_texturale_label.grid(row=2, column=0, sticky="w", pady=3, padx=5)
                classe_texturale_combobox.grid(row=2, column=1, sticky="w", pady=3, padx=5)
                classe_de_drainage_label.grid(row=3, column=0, sticky="w", pady=3, padx=5)
                classe_de_drainage_combobox.grid(row=3, column=1, sticky="w", pady=3, padx=5)
                masse_volumique_apparente_label.grid(row=4, column=0, sticky="w", pady=3, padx=5)
                masse_volumique_apparente_entry.grid(row=4, column=1, sticky="w", pady=3, padx=5)
                profondeur_label.grid(row=5, column=0, sticky="w", pady=3, padx=5)
                profondeur_entry.grid(row=5, column=1, sticky="w", pady=3, padx=5)
                superficie_de_la_zone_label.grid(row=6, column=0, sticky="w", pady=3, padx=5)
                superficie_de_la_zone_entry.grid(row=6, column=1, sticky="w", pady=3, padx=5)

                zone_de_gestion_frame.pack()

                creation_zone_de_gestion_bouton = ttk.Button(scrollable_frame, text="Créer",
                                                             command=lambda: add_new_tab())
                creation_zone_de_gestion_bouton.pack()
                canvas.pack(side="left", fill="x", expand=True)
                scrollbar.pack(side="right", fill="y")
                creation_zone_frame.pack()

                def add_new_tab():
                    entree_invalide_liste = []
                    global information_champs
                    index_zone = 0
                    for scrollable_frame_widget in scrollable_frame.winfo_children():
                        if isinstance(scrollable_frame_widget, ttk.LabelFrame):
                            grid_slave0_1 = scrollable_frame_widget.grid_slaves(row=0, column=1)
                            for entry in grid_slave0_1:
                                taux_matiere_organique = entry.get()
                                if not util.is_decimal_number(taux_matiere_organique) or float(
                                        taux_matiere_organique) < 0 or float(taux_matiere_organique) > 100:
                                    entree_invalide_liste.append(
                                        (information_champs[champs_index]["nom_du_champs"],
                                         "Zone gestion " + str(
                                             information_champs[champs_index]["nombre_de_zone_de_gestion"]),
                                         "\"Taux de matière organique\" doit être un réel positif dans l'intervalle [0-100]"))
                                else:
                                    taux_matiere_organique = float(taux_matiere_organique)
                            grid_slave1_1 = scrollable_frame_widget.grid_slaves(row=1, column=1)
                            for entry in grid_slave1_1:
                                municipalite = entry.get()
                                global municipalites_supportees
                                if municipalite not in municipalites_supportees:
                                    entree_invalide_liste.append(
                                        (information_champs[champs_index]["nom_du_champs"],
                                         "Zone gestion " + str(
                                             information_champs[champs_index]["nombre_de_zone_de_gestion"]),
                                         "\"Municipalité\" doit être parmis les choix disponibles"))
                            grid_slave2_1 = scrollable_frame_widget.grid_slaves(row=2, column=1)
                            for entry in grid_slave2_1:
                                classe_texturale = entry.get()
                                global classes_texturales_supportees
                                if classe_texturale not in classes_texturales_supportees:
                                    entree_invalide_liste.append(
                                        (information_champs[champs_index]["nom_du_champs"],
                                         "Zone gestion " + str(
                                             information_champs[champs_index]["nombre_de_zone_de_gestion"]),
                                         "\"Classe texturale\" doit être parmis les choix disponibles"))
                            grid_slave3_1 = scrollable_frame_widget.grid_slaves(row=3, column=1)
                            for entry in grid_slave3_1:
                                classe_de_drainage = entry.get()
                                global classes_de_drainage_supportees
                                if classe_de_drainage not in classes_de_drainage_supportees:
                                    entree_invalide_liste.append(
                                        (information_champs[champs_index]["nom_du_champs"],
                                         "Zone gestion " + str(
                                             information_champs[champs_index]["nombre_de_zone_de_gestion"]),
                                         "\"Classe de drainage\" doit être parmis les choix disponibles"))
                            grid_slave4_1 = scrollable_frame_widget.grid_slaves(row=4, column=1)
                            for entry in grid_slave4_1:
                                masse_volumique_apparente = entry.get()
                                if (not util.is_decimal_number(
                                        masse_volumique_apparente) and masse_volumique_apparente != "") or (
                                        util.is_decimal_number(masse_volumique_apparente) and float(
                                    masse_volumique_apparente) < 0):
                                    entree_invalide_liste.append(
                                        (information_champs[champs_index]["nom_du_champs"],
                                         "Zone gestion " + str(
                                             information_champs[champs_index]["nombre_de_zone_de_gestion"]),
                                         "\"Masse volumique apparente\" doit être un réel positif ou laissé vide pour aller chercher la valeur par défaut"))
                                else:
                                    if masse_volumique_apparente == "":
                                        masse_volumique_apparente = None
                                    else:
                                        masse_volumique_apparente = float(masse_volumique_apparente)
                            grid_slave5_1 = scrollable_frame_widget.grid_slaves(row=5, column=1)
                            for entry in grid_slave5_1:
                                profondeur = entry.get()
                                if not util.is_decimal_number(profondeur) or float(
                                        profondeur) < 0:
                                    entree_invalide_liste.append(
                                        (information_champs[champs_index]["nom_du_champs"],
                                         "Zone gestion " + str(
                                             information_champs[champs_index]["nombre_de_zone_de_gestion"]),
                                         "\"Profondeur\" doit être un réel positif"))
                                else:
                                    profondeur = float(profondeur)
                            grid_slave6_1 = scrollable_frame_widget.grid_slaves(row=6, column=1)
                            for entry in grid_slave6_1:
                                superficie_de_la_zone = entry.get()
                                if not util.is_decimal_number(superficie_de_la_zone) or float(
                                        superficie_de_la_zone) < 0:
                                    entree_invalide_liste.append(
                                        (information_champs[champs_index]["nom_du_champs"],
                                         "Zone gestion " + str(
                                             information_champs[champs_index]["nombre_de_zone_de_gestion"]),
                                         "\"Superficie de la zone\" doit être un réel positif"))
                                else:
                                    superficie_de_la_zone = float(superficie_de_la_zone)
                            information_champs[champs_index]["information_zone_de_gestion"].append(
                                {"taux_matiere_organique": taux_matiere_organique,
                                 "municipalite": municipalite,
                                 "classe_texturale": classe_texturale,
                                 "classe_de_drainage": classe_de_drainage,
                                 "masse_volumique_apparente": masse_volumique_apparente,
                                 "profondeur": profondeur,
                                 "superficie_de_la_zone": superficie_de_la_zone})
                        index_zone += 1
                    if len(entree_invalide_liste) == 0:
                        sauvegarder_attributs_entreprise_apres_modification()
                        rechauffement_champs_label_frame = \
                            donnees_de_rechauffement_label_frame.winfo_children()[0].winfo_children()[
                                0].winfo_children()[
                                champs_index]
                        rechauffement_champs_new_zone_label_frame = ttk.LabelFrame(rechauffement_champs_label_frame,
                                                                                   text="Zone gestion " + str(len(
                                                                                       rechauffement_champs_label_frame.winfo_children()) + 1))
                        rechauffement_champs_new_zone_label_frame.pack()
                        if show_regie_historique:
                            add_regies_historiques(rechauffement_champs_new_zone_label_frame)
                        else:
                            ajouter_une_annee_a_la_rotation(rechauffement_champs_new_zone_label_frame)
                        new_zone_window.destroy()

                        global furthest_left_tab_index_zone
                        global furthest_right_tab_index_zone
                        global max_index_zone
                        index = 0
                        for simulation_frame in simulation_notebook.winfo_children():
                            if len(simulation_frame.winfo_children()) == 0:
                                pass
                            else:
                                notebook = simulation_frame.winfo_children()[0]
                                champs_courant_zone_notebook = \
                                    notebook.winfo_children()[champs_index].winfo_children()[0]
                                champs_courant_zone_notebook.winfo_children()[
                                    len(champs_courant_zone_notebook.winfo_children()) - 1].destroy()
                                if furthest_right_tab_index_zone >= 3:
                                    champs_courant_zone_notebook.tab(furthest_left_tab_index_zone, state="hidden")
                                tab = ttk.Frame(champs_courant_zone_notebook)
                                champs_courant_zone_notebook.add(tab, text="Zone gestion " + str(
                                    len(champs_courant_zone_notebook.winfo_children())))
                                set_up_regies_projections(tab)

                                new_zone_tab = ttk.Frame(champs_courant_zone_notebook)
                                champs_courant_zone_notebook.add(new_zone_tab, text="+")
                            index += 1
                        furthest_right_tab_index_zone += 1
                        if furthest_right_tab_index_zone > 3:
                            furthest_left_tab_index_zone += 1
                        max_index_zone += 1
                        if furthest_left_tab_index_zone != min_index_zone:
                            scroll_left_button_zone.configure(state="normal")
                    else:
                        information_champs[champs_index]["information_zone_de_gestion"].pop(
                            len(information_champs[champs_index]["information_zone_de_gestion"]) - 1)
                        message = ""
                        for entree_invalide in entree_invalide_liste:
                            message = message + "Dans le " + entree_invalide[0] + " et la " + entree_invalide[
                                1] + " l'entrée " + entree_invalide[2] + "\n"
                        messagebox.showwarning("Warning", message)
                        new_zone_window.focus()

            zone_notebook.bind("<Button-1>", add_new_zone_de_gestion_tab)
            zone_notebook.bind("<Button-3>", delete_zone_de_gestion_tab)

            if simulation_copie is not None and index_champs is not None:
                champs = simulation_copie["entreprise_agricole"]["champs"][index_champs]
            else:
                champs = None

            global duree_simulation
            for zone in range(int(nombre_de_zone)):
                zone_tab = ttk.Frame(zone_notebook)
                zone_notebook.add(zone_tab, text="Zone gestion " + str(zone + 1))
                set_up_regies_projections(zone_tab, champs, zone)

            new_tab = ttk.Frame(zone_notebook)
            zone_notebook.add(new_tab, text="+")
            zone_notebook.pack(anchor="nw")

        def set_up_regies_projections(zone_tab, champs=None, zone_index=None):
            if champs is not None:
                zone = champs["zones_de_gestion"][zone_index]
            else:
                zone = None
            projection_frame = ttk.LabelFrame(zone_tab, text="Régies de la projection")
            canvas_projection = tk.Canvas(projection_frame)
            scrollbar_projection = ttk.Scrollbar(projection_frame, orient="vertical",
                                                 command=canvas_projection.yview)
            scrollable_frame_projection = ttk.Frame(canvas_projection)
            scrollable_frame_projection.bind("<Configure>", lambda e: canvas_projection.configure(
                scrollregion=canvas_projection.bbox("all")))
            canvas_projection.create_window((0, 0), window=scrollable_frame_projection, anchor="nw")
            canvas_projection.configure(yscrollcommand=scrollbar_projection.set)
            canvas_projection.pack(side="left", fill="both", expand=True)
            scrollbar_projection.pack(side="right", fill="y")
            ajouter_une_annee_a_la_rotation(scrollable_frame_projection, zone)
            projection_frame.grid(row=1, column=0, columnspan=2, pady=3)
            get_information_simulation_button = ttk.Button(zone_tab, text="Créer rapport",
                                                           command=get_information_toutes_les_simulations)
            get_information_simulation_button.grid(row=2, column=0, pady=3)
            editer_information_entreprise_button = ttk.Button(zone_tab, text="Éditer attributs de l'entreprise",
                                                              command=editer_caracteristique_physique_entreprise)
            editer_information_entreprise_button.grid(row=2, column=1, pady=3)

        def ajouter_une_annee_a_la_rotation(scrollable_frame_projection, zone=None, zone_rechauffement=None):
            if len(scrollable_frame_projection.winfo_children()) == 0:
                if zone is not None:
                    for regie in zone["regies_sol_et_culture_projection"]:
                        index = len(scrollable_frame_projection.winfo_children()) + 1
                        add_regies_projection(scrollable_frame_projection, index, regie)
                elif zone_rechauffement is not None:
                    for regie in zone_rechauffement["regies_sol_et_culture_historique"]:
                        index = len(scrollable_frame_projection.winfo_children()) + 1
                        add_regies_projection(scrollable_frame_projection, index, regie)
                else:
                    index = len(scrollable_frame_projection.winfo_children()) + 1
                    add_regies_projection(scrollable_frame_projection, index)

                button_frame = ttk.Frame(scrollable_frame_projection)
                ajouter_une_annee_a_la_rotation_button = ttk.Button(button_frame, text="Ajouter une année de rotation",
                                                                    command=lambda: ajouter_une_annee_a_la_rotation(
                                                                        scrollable_frame_projection))
                ajouter_une_annee_a_la_rotation_button.grid(row=0, column=0, pady=3)
                if zone is not None and len(zone) > 1:
                    enlever_une_annee_a_la_rotation_button = ttk.Button(button_frame,
                                                                        text="Enlever une année de rotation",
                                                                        command=lambda: enlever_une_annee_a_la_rotation(
                                                                            scrollable_frame_projection))
                else:
                    enlever_une_annee_a_la_rotation_button = ttk.Button(button_frame,
                                                                        text="Enlever une année de rotation",
                                                                        state="disabled")
                enlever_une_annee_a_la_rotation_button.grid(row=0, column=1, pady=3)
                button_frame.pack()
            else:
                scrollable_frame_projection.winfo_children()[
                    len(scrollable_frame_projection.winfo_children()) - 1].destroy()
                index = len(scrollable_frame_projection.winfo_children()) + 1
                add_regies_projection(scrollable_frame_projection, index)
                button_frame = ttk.Frame(scrollable_frame_projection)

                ajouter_une_annee_a_la_rotation_button = ttk.Button(button_frame, text="Ajouter une année de rotation",
                                                                    command=lambda: ajouter_une_annee_a_la_rotation(
                                                                        scrollable_frame_projection))
                ajouter_une_annee_a_la_rotation_button.grid(row=0, column=0, pady=3)
                enlever_une_annee_a_la_rotation_button = ttk.Button(button_frame, text="Enlever une année de rotation",
                                                                    command=lambda: enlever_une_annee_a_la_rotation(
                                                                        scrollable_frame_projection))
                enlever_une_annee_a_la_rotation_button.grid(row=0, column=1, pady=3)
                button_frame.pack()

        def enlever_une_annee_a_la_rotation(scrollable_frame_projection):
            if len(scrollable_frame_projection.winfo_children()) > 1:
                scrollable_frame_projection.winfo_children()[
                    len(scrollable_frame_projection.winfo_children()) - 2].destroy()
            if len(scrollable_frame_projection.winfo_children()) - 1 == 1:
                scrollable_frame_projection.winfo_children()[
                    len(scrollable_frame_projection.winfo_children()) - 1].grid_slaves(row=0, column=1)[0].configure(
                    state="disabled")

        def set_up_regies_rechauffement(rechauffement_frame, show_regie_historique, simulations):
            global information_champs
            if show_regie_historique:
                canvas_historique = tk.Canvas(rechauffement_frame)
                scrollbar_historique = ttk.Scrollbar(rechauffement_frame, orient="vertical",
                                                     command=canvas_historique.yview)
                scrollable_frame_historique = ttk.Frame(canvas_historique)
                scrollable_frame_historique.bind("<Configure>", lambda e: canvas_historique.configure(
                    scrollregion=canvas_historique.bbox("all")))
                if simulations is not None:
                    entreprise = simulations[0]["entreprise_agricole"]
                    champs_liste = entreprise["champs"]
                index_champs = 0
                for champs in information_champs:
                    rechauffement_champs_label_frame = ttk.LabelFrame(scrollable_frame_historique,
                                                                      text=champs["nom_du_champs"])
                    rechauffement_champs_label_frame.pack()
                    if simulations is not None:
                        champs_courant = champs_liste[index_champs]
                        zone_liste = champs_courant["zones_de_gestion"]
                    index = 0
                    while index < int(champs["nombre_de_zone_de_gestion"]):
                        rechauffement_zone_label_frame = ttk.LabelFrame(rechauffement_champs_label_frame,
                                                                        text="Zone gestion " + str(index + 1))
                        if simulations is not None:
                            regies_historiques = zone_liste[index]["regies_sol_et_culture_historique"]
                        rechauffement_zone_label_frame.pack()
                        if simulations is not None:
                            add_regies_historiques(rechauffement_zone_label_frame,
                                                   regies_historiques=regies_historiques)
                        else:
                            add_regies_historiques(rechauffement_zone_label_frame)
                        index += 1
                    index_champs += 1

                canvas_historique.create_window((0, 0), window=scrollable_frame_historique, anchor="nw")
                canvas_historique.configure(yscrollcommand=scrollbar_historique.set)
                canvas_historique.pack(side="left", fill="both", expand=True)
                scrollbar_historique.pack(side="right", fill="y")
            else:
                canvas_rechauffement_via_rotation = tk.Canvas(rechauffement_frame)
                scrollbar_rechauffement_via_rotation = ttk.Scrollbar(rechauffement_frame, orient="vertical",
                                                                     command=canvas_rechauffement_via_rotation.yview)
                scrollable_frame_rechauffement_via_rotation = ttk.Frame(canvas_rechauffement_via_rotation)
                scrollable_frame_rechauffement_via_rotation.bind("<Configure>",
                                                                 lambda e: canvas_rechauffement_via_rotation.configure(
                                                                     scrollregion=canvas_rechauffement_via_rotation.bbox(
                                                                         "all")))
                canvas_rechauffement_via_rotation.create_window((0, 0),
                                                                window=scrollable_frame_rechauffement_via_rotation,
                                                                anchor="nw")
                canvas_rechauffement_via_rotation.configure(yscrollcommand=scrollbar_rechauffement_via_rotation.set)
                canvas_rechauffement_via_rotation.pack(side="left", fill="both", expand=True)
                scrollbar_rechauffement_via_rotation.pack(side="right", fill="y")
                if simulations is not None:
                    entreprise = simulations[0]["entreprise_agricole"]
                    champs_liste = entreprise["champs"]
                index_champs = 0
                for champs in information_champs:
                    rechauffement_champs_label_frame = ttk.LabelFrame(scrollable_frame_rechauffement_via_rotation,
                                                                      text=champs["nom_du_champs"])
                    rechauffement_champs_label_frame.pack()
                    if simulations is not None:
                        champs_courant = champs_liste[index_champs]
                        zone_liste = champs_courant["zones_de_gestion"]
                    index = 0
                    while index < int(champs["nombre_de_zone_de_gestion"]):
                        rechauffement_zone_label_frame = ttk.LabelFrame(rechauffement_champs_label_frame,
                                                                        text="Zone gestion " + str(index + 1))
                        if simulations is not None:
                            zone_rechauffement = zone_liste[index]
                        rechauffement_zone_label_frame.pack()
                        if simulations is not None:
                            ajouter_une_annee_a_la_rotation(rechauffement_zone_label_frame,
                                                            zone_rechauffement=zone_rechauffement)
                        else:
                            ajouter_une_annee_a_la_rotation(rechauffement_zone_label_frame)
                        index += 1
                    index_champs += 1
                rechauffement_frame.grid(row=1, column=0, columnspan=2, pady=3)

        def add_regies_historiques(scrollable_frame, regies_historiques=None):
            global annees_historiques
            annee_historique_initiale = int(annees_historiques["annee_historique_initiale"])
            annee_historique_finale = int(annees_historiques["annee_historique_finale"])
            annee_courante = annee_historique_initiale
            index = 0
            while annee_courante <= annee_historique_finale:
                if regies_historiques is not None:
                    regie_historique = regies_historiques[index]
                annee_courante_frame = ttk.LabelFrame(scrollable_frame, text=str(annee_courante))
                culture_principale_label = ttk.Label(annee_courante_frame, text="Culture principale: ")
                global cultures_principales_supportees
                culture_principale_combobox = ttk.Combobox(annee_courante_frame, values=cultures_principales_supportees,
                                                           postcommand=lambda: filter_combobox_values(
                                                               culture_principale_combobox,
                                                               cultures_principales_supportees))
                rendement_label = ttk.Label(annee_courante_frame, text="Rendement (t/ha): ")
                rendement_entry = ttk.Entry(annee_courante_frame)
                proportion_tige_exporte_label = ttk.Label(annee_courante_frame, text="Proportion tige exporté [0-1]: ")
                proportion_tige_exporte_entry = ttk.Entry(annee_courante_frame)
                production_non_recolte_label = ttk.Label(annee_courante_frame, text="Production non récoltée: ")
                production_non_recolte_combobox = ttk.Combobox(annee_courante_frame, values=["Oui", "Non"],
                                                               postcommand=lambda: filter_combobox_values(
                                                                   production_non_recolte_combobox, ["Oui", "Non"]))
                taux_matiere_seche_label = ttk.Label(annee_courante_frame, text="Taux de matière sèche [0-1]: ")
                taux_matiere_seche_entry = ttk.Entry(annee_courante_frame)
                travail_du_sol_label = ttk.Label(annee_courante_frame, text="Travail du sol: ")
                global types_travail_du_sol_supportes
                travail_du_sol_combobox = ttk.Combobox(annee_courante_frame, values=types_travail_du_sol_supportes,
                                                       postcommand=lambda: filter_combobox_values(
                                                           travail_du_sol_combobox, types_travail_du_sol_supportes))
                profondeur_maximale_label = ttk.Label(annee_courante_frame, text="Profondeur maximale (cm): ")
                profondeur_maximale_entry = ttk.Entry(annee_courante_frame)
                culture_secondaire_label = ttk.Label(annee_courante_frame, text="Culture secondaire: ")
                global cultures_secondaires_supportees
                culture_secondaire_combobox = ttk.Combobox(annee_courante_frame, values=cultures_secondaires_supportees,
                                                           postcommand=lambda: filter_combobox_values(
                                                               culture_secondaire_combobox,
                                                               cultures_secondaires_supportees))
                rendement_culture_secondaire_label = ttk.Label(annee_courante_frame,
                                                               text="Rendement culture secondaire (t/ha): ")
                rendement_culture_secondaire_entry = ttk.Entry(annee_courante_frame)
                amendement_frame = ttk.LabelFrame(annee_courante_frame, text="Liste des amendements")
                if regies_historiques is not None:
                    culture_principale_combobox.set(regie_historique["culture_principale"]["culture_principale"])
                    if regie_historique["culture_principale"]["rendement"] is not None:
                        rendement_entry.insert(0, regie_historique["culture_principale"]["rendement"])
                    if regie_historique["culture_principale"]["proportion_tige_exporte"] is not None:
                        proportion_tige_exporte_entry.insert(0, regie_historique["culture_principale"][
                            "proportion_tige_exporte"])
                    if regie_historique["culture_principale"]["produit_non_recolte"]:
                        production_non_recolte_combobox.set("Oui")
                    else:
                        production_non_recolte_combobox.set("Non")
                    if taux_matiere_seche_entry is not None:
                        taux_matiere_seche_entry.insert(0, regie_historique["culture_principale"]["taux_matiere_seche"])
                    travail_du_sol_combobox.set(regie_historique["travail_du_sol"]["travail_du_sol"])
                    if profondeur_maximale_entry is not None:
                        profondeur_maximale_entry.insert(0, regie_historique["travail_du_sol"]["profondeur_du_travail"])
                    culture_secondaire_combobox.set(regie_historique["culture_secondaire"]["culture_secondaire"])
                    if rendement_culture_secondaire_entry is not None:
                        rendement_culture_secondaire_entry.insert(0,
                                                                  regie_historique["culture_secondaire"]["rendement"])
                    ajouter_des_amendements(amendement_frame, regie_historique["amendements"])
                else:
                    ajouter_des_amendements(amendement_frame)

                culture_principale_label.grid(row=0, column=0, sticky="w", pady=3)
                culture_principale_combobox.grid(row=0, column=1, sticky="w", pady=3)
                rendement_label.grid(row=1, column=0, sticky="w", pady=3)
                rendement_entry.grid(row=1, column=1, sticky="w", pady=3)
                proportion_tige_exporte_label.grid(row=2, column=0, sticky="w", pady=3)
                proportion_tige_exporte_entry.grid(row=2, column=1, sticky="w", pady=3)
                production_non_recolte_label.grid(row=3, column=0, sticky="w", pady=3)
                production_non_recolte_combobox.grid(row=3, column=1, sticky="w", pady=3)
                taux_matiere_seche_label.grid(row=4, column=0, sticky="w", pady=3)
                taux_matiere_seche_entry.grid(row=4, column=1, sticky="w", pady=3)
                travail_du_sol_label.grid(row=5, column=0, sticky="w", pady=3)
                travail_du_sol_combobox.grid(row=5, column=1, sticky="w", pady=3)
                profondeur_maximale_label.grid(row=6, column=0, sticky="w", pady=3)
                profondeur_maximale_entry.grid(row=6, column=1, sticky="w", pady=3)
                culture_secondaire_label.grid(row=7, column=0, sticky="w", pady=3)
                culture_secondaire_combobox.grid(row=7, column=1, sticky="w", pady=3)
                rendement_culture_secondaire_label.grid(row=8, column=0, sticky="w", pady=3)
                rendement_culture_secondaire_entry.grid(row=8, column=1, sticky="w", pady=3)
                amendement_frame.grid(row=9, column=0, columnspan=2, pady=3)

                annee_courante += 1
                index += 1
                annee_courante_frame.pack()

        def ajouter_des_amendements(amendement_frame, amendements=None):
            global amendements_supportees
            if amendements is not None:
                index = 0
                for amendement in amendements:
                    amendement_label = ttk.Label(amendement_frame, text="Amendement: ")
                    amendement_combobox = ttk.Combobox(amendement_frame, values=amendements_supportees,
                                                       postcommand=lambda: filter_combobox_values(amendement_combobox,
                                                                                                  amendements_supportees))
                    if amendement["amendement"] is not None:
                        amendement_combobox.set(amendement["amendement"])
                    apport_amendement_label = ttk.Label(amendement_frame, text="Apport (t/ha):")
                    apport_amendement_entry = ttk.Entry(amendement_frame)
                    if amendement["apport"] is not None:
                        apport_amendement_entry.insert(0, str(amendement["apport"]))
                    amendement_label.grid(row=index, column=0, sticky="w", pady=3)
                    amendement_combobox.grid(row=index, column=1, sticky="w", pady=3)
                    apport_amendement_label.grid(row=index + 1, column=0, sticky="w", pady=3)
                    apport_amendement_entry.grid(row=index + 1, column=1, sticky="w", pady=3)
                    index += 2
            else:
                index = 0
                amendement_label = ttk.Label(amendement_frame, text="Amendement: ")
                amendement_combobox = ttk.Combobox(amendement_frame, values=amendements_supportees,
                                                   postcommand=lambda: filter_combobox_values(amendement_combobox,
                                                                                              amendements_supportees))
                apport_amendement_label = ttk.Label(amendement_frame, text="Apport (t/ha):")
                apport_amendement_entry = ttk.Entry(amendement_frame)
                amendement_label.grid(row=0, column=0, sticky="w", pady=3)
                amendement_combobox.grid(row=0, column=1, sticky="w", pady=3)
                apport_amendement_label.grid(row=1, column=0, sticky="w", pady=3)
                apport_amendement_entry.grid(row=1, column=1, sticky="w", pady=3)
                index += 2

            ajout_a_la_regie_button = ttk.Button(amendement_frame, text="Ajouter à la régie",
                                                 command=lambda: ajouter_amendement_regie(amendement_frame))
            ajout_a_la_liste_amendement = ttk.Button(amendement_frame, text="Ajouter un nouvel amendement",
                                                     command=ajouter_nouvel_amendement)

            ajout_a_la_regie_button.grid(row=index, column=0, pady=3)
            ajout_a_la_liste_amendement.grid(row=index, column=1, pady=3)

        def ajouter_amendement_regie(amendement_frame):
            grid_size = amendement_frame.grid_size()
            amendement_frame.grid_slaves(grid_size[1] - 1, grid_size[0] - 1)[0].destroy()
            amendement_frame.grid_slaves(grid_size[1] - 1, grid_size[0] - 2)[0].destroy()
            amendement_label = ttk.Label(amendement_frame, text="Amendement: ")
            global amendements_supportees
            amendement_combobox = ttk.Combobox(amendement_frame, values=amendements_supportees,
                                               postcommand=lambda: filter_combobox_values(amendement_combobox,
                                                                                          amendements_supportees))
            apport_amendement_label = ttk.Label(amendement_frame, text="Apport (t/ha):")
            apport_amendement_entry = ttk.Entry(amendement_frame)
            ajout_a_la_regie_button = ttk.Button(amendement_frame, text="Ajouter à la régie",
                                                 command=lambda: ajouter_amendement_regie(amendement_frame))
            ajout_a_la_liste_amendement = ttk.Button(amendement_frame, text="Ajouter un nouvel amendement",
                                                     command=ajouter_nouvel_amendement)
            amendement_label.grid(row=grid_size[1] - 1, column=grid_size[0] - 2, sticky="w", pady=3)
            amendement_combobox.grid(row=grid_size[1] - 1, column=grid_size[0] - 1, sticky="w", pady=3)
            apport_amendement_label.grid(row=grid_size[1], column=grid_size[0] - 2, sticky="w", pady=3)
            apport_amendement_entry.grid(row=grid_size[1], column=grid_size[0] - 1, sticky="w", pady=3)
            ajout_a_la_regie_button.grid(row=grid_size[1] + 1, column=grid_size[0] - 2, pady=3)
            ajout_a_la_liste_amendement.grid(row=grid_size[1] + 1, column=grid_size[0] - 1, pady=3)

        def ajouter_nouvel_amendement():
            # TODO: Faire le UI et les calls nécessaire pour ajouter un amendement à la BD
            pass

        def add_regies_projection(scrollable_frame, index, regie=None):
            annee_courante_frame = ttk.LabelFrame(scrollable_frame, text=str(index))
            culture_principale_label = ttk.Label(annee_courante_frame, text="Culture principale: ")
            global cultures_principales_supportees
            culture_principale_combobox = ttk.Combobox(annee_courante_frame, values=cultures_principales_supportees,
                                                       postcommand=lambda: filter_combobox_values(
                                                           culture_principale_combobox,
                                                           cultures_principales_supportees))
            rendement_label = ttk.Label(annee_courante_frame, text="Rendement (t/ha): ")
            rendement_entry = ttk.Entry(annee_courante_frame)
            proportion_tige_exporte_label = ttk.Label(annee_courante_frame, text="Proportion tige exporté [0-1]: ")
            proportion_tige_exporte_entry = ttk.Entry(annee_courante_frame)
            production_non_recolte_label = ttk.Label(annee_courante_frame, text="Production non récoltée: ")
            production_non_recolte_combobox = ttk.Combobox(annee_courante_frame, values=["Oui", "Non"],
                                                           postcommand=lambda: filter_combobox_values(
                                                               production_non_recolte_combobox, ["Oui", "Non"]))
            taux_matiere_seche_label = ttk.Label(annee_courante_frame, text="Taux de matière sèche [0-1]: ")
            taux_matiere_seche_entry = ttk.Entry(annee_courante_frame)
            travail_du_sol_label = ttk.Label(annee_courante_frame, text="Travail du sol: ")
            global types_travail_du_sol_supportes
            travail_du_sol_combobox = ttk.Combobox(annee_courante_frame, values=types_travail_du_sol_supportes,
                                                   postcommand=lambda: filter_combobox_values(travail_du_sol_combobox,
                                                                                              types_travail_du_sol_supportes))
            profondeur_maximale_label = ttk.Label(annee_courante_frame, text="Profondeur maxiamle (cm): ")
            profondeur_maximale_entry = ttk.Entry(annee_courante_frame)
            culture_secondaire_label = ttk.Label(annee_courante_frame, text="Culture secondaire: ")
            global cultures_secondaires_supportees
            culture_secondaire_combobox = ttk.Combobox(annee_courante_frame, values=cultures_secondaires_supportees,
                                                       postcommand=lambda: filter_combobox_values(
                                                           culture_secondaire_combobox,
                                                           cultures_secondaires_supportees))
            rendement_culture_secondaire_label = ttk.Label(annee_courante_frame,
                                                           text="Rendement culture secondaire (t/ha): ")
            rendement_culture_secondaire_entry = ttk.Entry(annee_courante_frame)

            if regie is not None:
                culture_principale_combobox.set(regie["culture_principale"]["culture_principale"])
                if regie["culture_principale"]["rendement"] is not None:
                    rendement_entry.insert(0, str(regie["culture_principale"]["rendement"]))

                if regie["culture_principale"]["proportion_tige_exporte"] is not None:
                    proportion_tige_exporte_entry.insert(0, str(regie["culture_principale"]["proportion_tige_exporte"]))
                if regie["culture_principale"]["produit_non_recolte"]:
                    production_non_recolte_combobox.set("Oui")
                else:
                    production_non_recolte_combobox.set("Non")
                if regie["culture_principale"]["taux_matiere_seche"] is not None:
                    taux_matiere_seche_entry.insert(0, str(regie["culture_principale"]["taux_matiere_seche"]))
                travail_du_sol_combobox.set(regie["travail_du_sol"]["travail_du_sol"])
                if regie["travail_du_sol"]["profondeur_du_travail"] is not None:
                    profondeur_maximale_entry.insert(0, str(regie["travail_du_sol"]["profondeur_du_travail"]))
                if regie["culture_secondaire"]["culture_secondaire"] is not None:
                    culture_secondaire_combobox.set(regie["culture_secondaire"]["culture_secondaire"])
                if regie["culture_secondaire"]["rendement"]:
                    rendement_culture_secondaire_entry.insert(0, str(regie["culture_secondaire"]["rendement"]))

            amendement_frame = ttk.LabelFrame(annee_courante_frame, text="Liste des amendements")
            if regie is not None:
                ajouter_des_amendements(amendement_frame, regie["amendements"])
            else:
                ajouter_des_amendements(amendement_frame)

            culture_principale_label.grid(row=0, column=0, sticky="w", pady=3)
            culture_principale_combobox.grid(row=0, column=1, sticky="w", pady=3)
            rendement_label.grid(row=1, column=0, sticky="w", pady=3)
            rendement_entry.grid(row=1, column=1, sticky="w", pady=3)
            proportion_tige_exporte_label.grid(row=2, column=0, sticky="w", pady=3)
            proportion_tige_exporte_entry.grid(row=2, column=1, sticky="w", pady=3)
            production_non_recolte_label.grid(row=3, column=0, sticky="w", pady=3)
            production_non_recolte_combobox.grid(row=3, column=1, sticky="w", pady=3)
            taux_matiere_seche_label.grid(row=4, column=0, sticky="w", pady=3)
            taux_matiere_seche_entry.grid(row=4, column=1, sticky="w", pady=3)
            travail_du_sol_label.grid(row=5, column=0, sticky="w", pady=3)
            travail_du_sol_combobox.grid(row=5, column=1, sticky="w", pady=3)
            profondeur_maximale_label.grid(row=6, column=0, sticky="w", pady=3)
            profondeur_maximale_entry.grid(row=6, column=1, sticky="w", pady=3)
            culture_secondaire_label.grid(row=7, column=0, sticky="w", pady=3)
            culture_secondaire_combobox.grid(row=7, column=1, sticky="w", pady=3)
            rendement_culture_secondaire_label.grid(row=8, column=0, sticky="w", pady=3)
            rendement_culture_secondaire_entry.grid(row=8, column=1, sticky="w", pady=3)
            amendement_frame.grid(row=9, column=0, columnspan=2, pady=3)
            annee_courante_frame.pack()

        def get_information_toutes_les_simulations():
            simulations = []
            entree_invalide_liste = []
            index_simualtion = 0
            for simulation in simulation_notebook.winfo_children():
                global nombre_simulations
                if index_simualtion < nombre_simulations:
                    simulation, entree_invalide_liste_simulation = get_information_simulation(simulation,
                                                                                              index_simualtion,
                                                                                              simulation_unique=False)
                    for entree in entree_invalide_liste_simulation:
                        entree_invalide_liste.append(entree)
                    simulations.append(simulation)
                index_simualtion += 1

            if len(entree_invalide_liste) == 0:
                response = requests.post('http://localhost:5000/api/icbm-bilan', json={"simulations": simulations})
                print(response.text)
                # TODO: Ajouter la suite avec la generation du rapport
                creation_du_rapport(response)
            else:
                message = ""
                for entree_invalide in entree_invalide_liste:
                    message = message + "Dans la " + entree_invalide[3] + ", le " + entree_invalide[0] + " et la " + \
                              entree_invalide[
                                  1] + " l'entrée " + entree_invalide[2] + "\n"
                messagebox.showwarning("Warning", message)
                parent_frame_tabs.focus()

        def sauvegarder_toutes_les_simulations():
            simulations = []
            entree_invalide_liste = []
            index_simulation = 0
            for simulation in simulation_notebook.winfo_children():
                global duree_simulation
                global nombre_simulations
                if index_simulation < nombre_simulations:
                    simulation, entree_invalide_liste_simulation = get_information_simulation(simulation,
                                                                                              index_simulation,
                                                                                              simulation_unique=False)
                    for entree in entree_invalide_liste_simulation:
                        entree_invalide_liste.append(entree)
                    simulations.append(simulation)
                index_simulation += 1

            if len(entree_invalide_liste) == 0:
                global annees_historiques
                return {"simulations": simulations,
                        "presence_regie_historique": show_regie_historique,
                        "annees_historiques": annees_historiques}
            else:
                return entree_invalide_liste

        def get_information_simulation(simulation_frame, index_simulation, simulation_unique):
            global information_champs
            global nombre_de_champs
            entree_invalide_simulation_liste = []
            if simulation_unique:
                regies_rechauffement, entree_invalide_liste = None, []
            else:
                regies_rechauffement, entree_invalide_liste = get_regies_rechauffement()
            entree_invalide_simulation_liste.append(entree_invalide_liste)
            champs_notebook = simulation_frame.winfo_children()[0]
            index_champs = 0
            champs_list = []
            for champs_frame in champs_notebook.winfo_children():
                zone_list = []
                index_zone = 0
                if index_champs < nombre_de_champs:
                    zone_notebook = champs_frame.winfo_children()[0]
                    for zone_frames in zone_notebook.winfo_children():
                        if index_zone < int(information_champs[index_champs]["nombre_de_zone_de_gestion"]):
                            regies_projection_frame = zone_frames.winfo_children()[0]
                            regies_projection, entree_invalide_liste = get_regies(regies_projection_frame, index_champs,
                                                                                  index_zone, index_simulation)
                            if regies_rechauffement is not None:
                                regie_rechauffement = regies_rechauffement[index_champs][index_zone]
                            else:
                                regie_rechauffement = None
                            zone_list.append({"regies_projection": regies_projection,
                                              "regies_rechauffement": regie_rechauffement})
                            entree_invalide_simulation_liste.append(entree_invalide_liste)
                        index_zone += 1
                    champs_list.append(zone_list)
                index_champs += 1
            if len(entree_invalide_simulation_liste[0]) == 0 and len(entree_invalide_simulation_liste[1]) == 0:
                champs_attributs = []
                index_champs = 0
                for champs in information_champs:
                    index_zone = 0
                    zones_de_gestion = []
                    for zone in champs["information_zone_de_gestion"]:
                        zones_de_gestion.append({"taux_matiere_organique": zone["taux_matiere_organique"],
                                                 "municipalite": zone["municipalite"],
                                                 "classe_texturale": zone["classe_texturale"],
                                                 "classe_de_drainage": zone["classe_de_drainage"],
                                                 "masse_volumique_apparente": zone["masse_volumique_apparente"],
                                                 "profondeur": zone["profondeur"],
                                                 "superficie_de_la_zone": zone["superficie_de_la_zone"],
                                                 "regies_sol_et_culture_projection":
                                                     champs_list[index_champs][index_zone]["regies_projection"],
                                                 "regies_sol_et_culture_historique":
                                                     champs_list[index_champs][index_zone]["regies_rechauffement"]})
                        index_zone += 1
                    champs_attributs.append({"nom": champs["nom_du_champs"],
                                             "zones_de_gestion": zones_de_gestion})
                    index_champs += 1

                global nom_entreprise
                entreprise_agricole = {"nom": nom_entreprise,
                                       "champs": champs_attributs}
                global duree_simulation
                simulation = {
                    "nom_simulation": duree_simulation[index_simulation]["nom_simulation"],
                    "duree_projection": duree_simulation[index_simulation]["duree_projection"],
                    "annee_initiale_projection": int(duree_simulation[index_simulation]["annee_projection_initiale"]),
                    "annee_finale_projection": int(
                        duree_simulation[index_simulation]["annee_projection_initiale"]) + int(
                        duree_simulation[index_simulation]["duree_projection"]),
                    "entreprise_agricole": entreprise_agricole}
                return simulation, []
            else:
                entree_invalide_liste = []
                for sous_liste in entree_invalide_simulation_liste:
                    for entree in sous_liste:
                        entree_invalide_liste.append(entree)
                return None, entree_invalide_liste

        def get_regies(regies_frame, champs_index, zone_index, simulation_index):
            entree_invalide_liste = []
            regies = []
            regies_canvas = regies_frame.winfo_children()[0]
            regies_scrollable_frame = regies_canvas.winfo_children()[0]
            compteur_regie = 0
            for regie in regies_scrollable_frame.winfo_children():
                if compteur_regie < len(regies_scrollable_frame.winfo_children()) - 1:
                    culture_principale = regie.grid_slaves(row=0, column=1)[0].get()
                    global cultures_principales_supportees
                    if culture_principale not in cultures_principales_supportees:
                        entree_invalide_liste.append(
                            (information_champs[champs_index]["nom_du_champs"],
                             "Zone gestion " + str(zone_index + 1),
                             "\"Culture principale\" doit être parmis les choix disponibles",
                             "Régie projection Simulation " + str(simulation_index + 1)))
                    rendement = regie.grid_slaves(row=1, column=1)[0].get()
                    if not util.is_decimal_number(rendement) and rendement != "" and float(rendement) < 0:
                        entree_invalide_liste.append(
                            (information_champs[champs_index]["nom_du_champs"],
                             "Zone gestion " + str(zone_index + 1),
                             "\"Rendement\" doit être un réel positif ou la case peut être vide pour aller chercher un rendement par défaut",
                             "Régie projection Simulation " + str(simulation_index + 1)))
                    if rendement == "":
                        rendement = None
                    if rendement is not None and util.is_decimal_number(rendement) and float(rendement) >= 0:
                        rendement = float(rendement)
                    proportion_tige_exporte = regie.grid_slaves(row=2, column=1)[0].get()
                    if (not util.is_decimal_number(
                            proportion_tige_exporte) and proportion_tige_exporte != "") or (
                            util.is_decimal_number(proportion_tige_exporte) and (
                            float(proportion_tige_exporte) < 0 or float(proportion_tige_exporte) > 1)):
                        entree_invalide_liste.append(
                            (information_champs[champs_index]["nom_du_champs"],
                             "Zone gestion " + str(zone_index + 1),
                             "\"Proportion tige exportée\" doit être un réel positif dans l'intervalle [0,1] ou le champs peut être vide pour aller chercher une proportion par défaut",
                             "Régie projection Simulation " + str(simulation_index + 1)))
                    if proportion_tige_exporte == "":
                        proportion_tige_exporte = None
                    if proportion_tige_exporte is not None and util.is_decimal_number(proportion_tige_exporte):
                        proportion_tige_exporte = float(proportion_tige_exporte)
                    production_non_recolte = regie.grid_slaves(row=3, column=1)[0].get()
                    if production_non_recolte not in ["Oui", "Non"]:
                        entree_invalide_liste.append(
                            (information_champs[champs_index]["nom_du_champs"],
                             "Zone gestion " + str(zone_index + 1),
                             "\"Production non récolté\" doit être l'une des options de la combobox",
                             "Régie projection"))
                    else:
                        if production_non_recolte == "Oui":
                            production_non_recolte = True
                        else:
                            production_non_recolte = False
                    taux_matiere_seche = regie.grid_slaves(row=4, column=1)[0].get()
                    if (not util.is_decimal_number(
                            taux_matiere_seche) and taux_matiere_seche != "") or (
                            util.is_decimal_number(taux_matiere_seche) and (
                            float(taux_matiere_seche) < 0 or float(taux_matiere_seche) > 1)):
                        entree_invalide_liste.append(
                            (information_champs[champs_index]["nom_du_champs"],
                             "Zone gestion " + str(zone_index + 1),
                             "\"Taux matière sèche\" doit être un réel positif dans l'intervalle [0,1] ou le champs peut être vide pour aller chercher une proportion par défaut",
                             "Régie projection Simulation " + str(simulation_index + 1)))
                    if taux_matiere_seche == "":
                        taux_matiere_seche = None
                    if taux_matiere_seche is not None and util.is_decimal_number(taux_matiere_seche):
                        taux_matiere_seche = float(taux_matiere_seche)
                    culture_principale_dict = {"culture_principale": culture_principale,
                                               "rendement": rendement,
                                               "proportion_tige_exporte": proportion_tige_exporte,
                                               "produit_non_recolte": production_non_recolte,
                                               "taux_matiere_seche": taux_matiere_seche}
                    travail_du_sol = regie.grid_slaves(row=5, column=1)[0].get()
                    global types_travail_du_sol_supportes
                    if travail_du_sol not in types_travail_du_sol_supportes:
                        entree_invalide_liste.append(
                            (information_champs[champs_index]["nom_du_champs"],
                             "Zone gestion " + str(zone_index + 1),
                             "\"Travail du sol\" doit être parmis les choix disponibles",
                             "Régie projection Simulation " + str(simulation_index + 1)))
                    profondeur = regie.grid_slaves(row=6, column=1)[0].get()
                    if not util.is_decimal_number(profondeur) or float(
                            profondeur) < 0:
                        entree_invalide_liste.append(
                            (information_champs[champs_index]["nom_du_champs"],
                             "Zone gestion " + str(zone_index + 1),
                             "\"Profondeur\" doit être un réel positif",
                             "Régie projection Simulation " + str(simulation_index + 1)))
                    if profondeur == "":
                        profondeur = None
                    if profondeur is not None and util.is_decimal_number(profondeur):
                        profondeur = float(profondeur)
                    travail_du_sol_dict = {"travail_du_sol": travail_du_sol,
                                           "profondeur_du_travail": profondeur}
                    culture_secondaire = regie.grid_slaves(row=7, column=1)[0].get()
                    global cultures_secondaires_supportees
                    if culture_secondaire == "":
                        culture_secondaire = None
                    if culture_secondaire is not None and culture_secondaire not in cultures_secondaires_supportees:
                        entree_invalide_liste.append(
                            (information_champs[champs_index]["nom_du_champs"],
                             "Zone gestion " + str(zone_index + 1),
                             "\"Culture secondaire\" doit être parmis les choix disponibles ou laissé vide s'il n'y a pas de culture secondaire",
                             "Régie projection Simulation " + str(simulation_index + 1)))
                    rendement_culture_secondaire = regie.grid_slaves(row=8, column=1)[0].get()
                    if rendement_culture_secondaire == "":
                        rendement_culture_secondaire = None
                    if rendement_culture_secondaire is not None and not util.is_decimal_number(
                            rendement_culture_secondaire):
                        entree_invalide_liste.append(
                            (information_champs[champs_index]["nom_du_champs"],
                             "Zone gestion " + str(zone_index + 1),
                             "\"Rendement culture secondaire\" doit être un réel positif ou laissé vide s'il n'y a pas de culture secondaire",
                             "Régie projection Simulation " + str(simulation_index + 1)))
                    elif (culture_secondaire is None and rendement_culture_secondaire is not None) or (
                            culture_secondaire is not None and rendement_culture_secondaire is None):
                        entree_invalide_liste.append(
                            (information_champs[champs_index]["nom_du_champs"],
                             "Zone gestion " + str(zone_index + 1),
                             "\"Rendement culture secondaire\" et \"Culture secondaire\" doivent être tout deux laissé vide s'il n'y a pas de culture secondaire",
                             "Régie projection Simulation " + str(simulation_index + 1)))
                    else:
                        if rendement_culture_secondaire is not None:
                            rendement_culture_secondaire = float(rendement_culture_secondaire)
                    culture_secondaire_dict = {"culture_secondaire": culture_secondaire,
                                               "rendement": rendement_culture_secondaire}
                    index_composante_amendement = 0
                    composante_amendement_liste = regie.grid_slaves(row=9, column=0)[0]
                    grid_size = composante_amendement_liste.grid_size()
                    amendements = []
                    while index_composante_amendement < grid_size[1] - 1:
                        amendement = composante_amendement_liste.grid_slaves([index_composante_amendement], column=1)[
                            0].get()
                        global amendements_supportees
                        if amendement == "":
                            amendement = None
                        if amendement is not None and amendement not in amendements_supportees:
                            entree_invalide_liste.append(
                                (information_champs[champs_index]["nom_du_champs"],
                                 "Zone gestion " + str(zone_index + 1),
                                 "\"Amendement\" " + str(
                                     index_composante_amendement + 1) + " doit être parmis les choix disponibles",
                                 "Régie projection Simulation " + str(simulation_index + 1)))
                        apport = composante_amendement_liste.grid_slaves([index_composante_amendement + 1], column=1)[
                            0].get()
                        if apport == "":
                            apport = None
                        if apport is not None and not util.is_decimal_number(apport):
                            entree_invalide_liste.append(
                                (information_champs[champs_index]["nom_du_champs"],
                                 "Zone gestion " + str(zone_index + 1),
                                 "\"Apport\" " + str(index_composante_amendement + 1) +
                                 " est invalide, il doit être un réel positif ou laissé vide s'il n'y a pas d'amendements",
                                 "Régie projection Simulation " + str(simulation_index + 1)))
                        elif (amendement is None and apport is not None) or (amendement is not None and apport is None):
                            entree_invalide_liste.append(
                                (information_champs[champs_index]["nom_du_champs"],
                                 "Zone gestion " + str(zone_index + 1),
                                 "\"Apport\" " + str(
                                     index_composante_amendement + 1) + " et \"Amendement\" " + str(
                                     index_composante_amendement + 1) +
                                 " doivent être tout deux laissé vide s'il n'y a pas d'amendements",
                                 "Régie projection Simulation " + str(simulation_index + 1)))
                        else:
                            if apport is not None:
                                apport = float(apport)
                        amendements.append({"amendement": amendement,
                                            "apport": apport})
                        index_composante_amendement += 2
                    regie_dict = {"culture_principale": culture_principale_dict,
                                  "culture_secondaire": culture_secondaire_dict,
                                  "amendements": amendements,
                                  "travail_du_sol": travail_du_sol_dict}
                    regies.append(regie_dict)
                compteur_regie += 1
            return regies, entree_invalide_liste

        def scroll_right_simulation():
            global duree_simulation
            global furthest_left_tab_index_simulation
            global furthest_right_tab_index_simulation
            simulation_notebook.tab(furthest_left_tab_index_simulation, state="hidden")
            furthest_left_tab_index_simulation += 1
            furthest_right_tab_index_simulation += 1
            if furthest_right_tab_index_simulation == max_index_simulation:
                tab_text = "+"
            else:
                tab_text = duree_simulation[furthest_right_tab_index_simulation]["nom_simulation"]
            simulation_notebook.add(simulation_notebook.winfo_children()[furthest_right_tab_index_simulation],
                                    text=tab_text)
            if furthest_right_tab_index_simulation == max_index_simulation:
                scroll_right_button_simulation.configure(state="disabled")
            else:
                scroll_right_button_simulation.configure(state="normal")
            if furthest_left_tab_index_simulation == min_index_simulation:
                scroll_left_button_simulation.configure(state="disabled")
            else:
                scroll_left_button_simulation.configure(state="normal")

        def scroll_left_simulation():
            global duree_simulation
            global furthest_left_tab_index_simulation
            global furthest_right_tab_index_simulation
            simulation_notebook.tab(furthest_right_tab_index_simulation, state="hidden")
            furthest_left_tab_index_simulation -= 1
            furthest_right_tab_index_simulation -= 1
            simulation_notebook.add(simulation_notebook.winfo_children()[furthest_left_tab_index_simulation],
                                    text=duree_simulation[furthest_left_tab_index_simulation]["nom_simulation"])
            if furthest_right_tab_index_simulation == max_index_simulation:
                scroll_right_button_simulation.configure(state="disabled")
            else:
                scroll_right_button_simulation.configure(state="normal")
            if furthest_left_tab_index_simulation == min_index_simulation:
                scroll_left_button_simulation.configure(state="disabled")
            else:
                scroll_left_button_simulation.configure(state="normal")

        def scroll_right_champs():
            global information_champs
            global furthest_left_tab_index_champs
            global furthest_right_tab_index_champs
            index_champs_frame = 0
            for simulation_frame in simulation_notebook.winfo_children():
                if index_champs_frame < len(simulation_notebook.winfo_children()) - 1:
                    champs_notebook = simulation_frame.winfo_children()[0]
                    champs_notebook.tab(furthest_left_tab_index_champs, state="hidden")
                index_champs_frame += 1
            furthest_left_tab_index_champs += 1
            furthest_right_tab_index_champs += 1
            if furthest_right_tab_index_champs == max_index_champs:
                tab_text = "+"
            else:
                tab_text = information_champs[furthest_right_tab_index_champs]["nom_du_champs"]
            index_champs_frame = 0
            for simulation_frame in simulation_notebook.winfo_children():
                if index_champs_frame < len(simulation_notebook.winfo_children()) - 1:
                    champs_notebook = simulation_frame.winfo_children()[0]
                    champs_notebook.add(champs_notebook.winfo_children()[furthest_right_tab_index_champs],
                                        text=tab_text)
                index_champs_frame += 1
            if furthest_right_tab_index_champs == max_index_champs:
                scroll_right_button_champs.configure(state="disabled")
            else:
                scroll_right_button_champs.configure(state="normal")
            if furthest_left_tab_index_champs == min_index_champs:
                scroll_left_button_champs.configure(state="disabled")
            else:
                scroll_left_button_champs.configure(state="normal")

        def scroll_left_champs():
            global information_champs
            global furthest_left_tab_index_champs
            global furthest_right_tab_index_champs
            index_champs_frame = 0
            for simulation_frame in simulation_notebook.winfo_children():
                if index_champs_frame < len(simulation_notebook.winfo_children()) - 1:
                    champs_notebook = simulation_frame.winfo_children()[0]
                    champs_notebook.tab(furthest_right_tab_index_champs, state="hidden")
                index_champs_frame += 1
            furthest_left_tab_index_champs -= 1
            furthest_right_tab_index_champs -= 1
            index_champs_frame = 0
            for simulation_frame in simulation_notebook.winfo_children():
                if index_champs_frame < len(simulation_notebook.winfo_children()) - 1:
                    champs_notebook = simulation_frame.winfo_children()[0]
                    champs_notebook.add(champs_notebook.winfo_children()[furthest_left_tab_index_champs],
                                        text=information_champs[furthest_left_tab_index_champs]["nom_du_champs"])
                index_champs_frame += 1
            if furthest_right_tab_index_champs == max_index_champs:
                scroll_right_button_champs.configure(state="disabled")
            else:
                scroll_right_button_champs.configure(state="normal")
            if furthest_left_tab_index_champs == min_index_champs:
                scroll_left_button_champs.configure(state="disabled")
            else:
                scroll_left_button_champs.configure(state="normal")

        def scroll_right_zone():
            global furthest_left_tab_index_zone
            global furthest_right_tab_index_zone
            champs_notebook = \
                simulation_notebook.winfo_children()[simulation_notebook.index("current")].winfo_children()[0]
            zone_notebook = champs_notebook.winfo_children()[champs_notebook.index("current")].winfo_children()[0]
            zone_notebook.tab(furthest_left_tab_index_zone, state="hidden")
            furthest_left_tab_index_zone += 1
            furthest_right_tab_index_zone += 1
            if furthest_right_tab_index_zone == max_index_zone:
                tab_text = "+"
            else:
                tab_text = "Zone gestion " + str(furthest_right_tab_index_zone + 1)
            zone_notebook.add(zone_notebook.winfo_children()[furthest_right_tab_index_zone], text=tab_text)
            if furthest_right_tab_index_zone == max_index_zone:
                scroll_right_button_zone.configure(state="disabled")
            else:
                scroll_right_button_zone.configure(state="normal")
            if furthest_left_tab_index_zone == min_index_zone:
                scroll_left_button_zone.configure(state="disabled")
            else:
                scroll_left_button_zone.configure(state="normal")

        def scroll_left_zone():
            global furthest_left_tab_index_zone
            global furthest_right_tab_index_zone
            champs_notebook = \
                simulation_notebook.winfo_children()[simulation_notebook.index("current")].winfo_children()[0]
            zone_notebook = champs_notebook.winfo_children()[champs_notebook.index("current")].winfo_children()[0]
            zone_notebook.tab(furthest_right_tab_index_zone, state="hidden")
            furthest_left_tab_index_zone -= 1
            furthest_right_tab_index_zone -= 1
            zone_notebook.add(zone_notebook.winfo_children()[furthest_left_tab_index_zone],
                              text="Zone gestion " + str(furthest_left_tab_index_zone + 1))
            if furthest_right_tab_index_zone == max_index_zone:
                scroll_right_button_zone.configure(state="disabled")
            else:
                scroll_right_button_zone.configure(state="normal")
            if furthest_left_tab_index_zone == min_index_zone:
                scroll_left_button_zone.configure(state="disabled")
            else:
                scroll_left_button_zone.configure(state="normal")

        def zone_tab_management(event):
            global max_index_zone
            global furthest_left_tab_index_zone
            global furthest_right_tab_index_zone
            furthest_left_tab_index_zone = 0
            furthest_right_tab_index_zone = 0
            current_simulation_index = simulation_notebook.index("current")
            champs_notebook = simulation_notebook.winfo_children()[current_simulation_index].winfo_children()[0]
            if champs_notebook.index("end") - 1 != champs_notebook.index("current"):
                current_zone_notebook = \
                    champs_notebook.winfo_children()[champs_notebook.index("current")].winfo_children()[0]
            else:
                current_zone_notebook = ttk.Notebook()
            for index in range(len(current_zone_notebook.winfo_children())):
                current_zone_notebook.tab(index, state="hidden")
            max_index_zone = len(current_zone_notebook.winfo_children()) - 1
            if max_index_zone <= 3:
                furthest_right_tab_index_zone = max_index_zone
                scroll_left_button_zone.configure(state="disabled")
                scroll_right_button_zone.configure(state="disabled")
            else:
                furthest_right_tab_index_zone = 3
                scroll_left_button_zone.configure(state="disabled")
                scroll_right_button_zone.configure(state="normal")
            for index in range(len(current_zone_notebook.winfo_children())):
                if index <= furthest_right_tab_index_zone:
                    current_zone_notebook.tab(index, state="normal")
                else:
                    current_zone_notebook.tab(index, state="hidden")
            if len(current_zone_notebook.winfo_children()) > 0:
                current_zone_notebook.select(furthest_left_tab_index_zone)

        def get_regies_rechauffement():
            entree_invalide_liste = []
            regies_rechauffement_simulation = []
            champs_label_frames = donnees_de_rechauffement_label_frame.winfo_children()[0].winfo_children()[
                0].winfo_children()
            champs_index = 0
            for champs_label_frame in champs_label_frames:
                champs_regies_liste = []
                zone_label_frames = champs_label_frame.winfo_children()
                zone_index = 0
                for zone_label_frame in zone_label_frames:
                    regies_de_rechauffement = zone_label_frame.winfo_children()
                    index_regie = 0
                    zone_regies = []
                    if show_regie_historique:
                        number_of_label_frames = len(regies_de_rechauffement)
                    else:
                        number_of_label_frames = len(regies_de_rechauffement) - 1
                    while index_regie < number_of_label_frames:
                        regie = regies_de_rechauffement[index_regie]
                        culture_principale = regie.grid_slaves(row=0, column=1)[0].get()
                        global cultures_principales_supportees
                        if culture_principale not in cultures_principales_supportees:
                            entree_invalide_liste.append(
                                (information_champs[champs_index]["nom_du_champs"],
                                 "Zone gestion " + str(zone_index + 1),
                                 "\"Culture principale\" doit être parmis les choix disponibles",
                                 " section Données réchauffement"))
                        rendement = regie.grid_slaves(row=1, column=1)[0].get()
                        if not util.is_decimal_number(rendement) and rendement != "":
                            entree_invalide_liste.append(
                                (information_champs[champs_index]["nom_du_champs"],
                                 "Zone gestion " + str(zone_index + 1),
                                 "\"Rendement\" doit être un réel positif ou la case peut être vide pour aller chercher un rendement par défaut",
                                 " section Données réchauffement"))
                        if rendement == "":
                            rendement = None
                        if rendement is not None and util.is_decimal_number(rendement):
                            rendement = float(rendement)
                        proportion_tige_exporte = regie.grid_slaves(row=2, column=1)[0].get()
                        if (not util.is_decimal_number(
                                proportion_tige_exporte) and proportion_tige_exporte != "") or (
                                util.is_decimal_number(proportion_tige_exporte) and (
                                float(proportion_tige_exporte) < 0 or float(proportion_tige_exporte) > 1)):
                            entree_invalide_liste.append(
                                (information_champs[champs_index]["nom_du_champs"],
                                 "Zone gestion " + str(zone_index + 1),
                                 "\"Proportion tige exportée\" doit être un réel positif dans l'intervalle [0,1] ou le champs peut être vide pour aller chercher une proportion par défaut",
                                 "section Données réchauffement"))
                        if proportion_tige_exporte == "":
                            proportion_tige_exporte = None
                        if proportion_tige_exporte is not None and util.is_decimal_number(proportion_tige_exporte):
                            proportion_tige_exporte = float(proportion_tige_exporte)
                        production_non_recolte = regie.grid_slaves(row=3, column=1)[0].get()
                        if production_non_recolte not in ["Oui", "Non"]:
                            entree_invalide_liste.append(
                                (information_champs[champs_index]["nom_du_champs"],
                                 "Zone gestion " + str(zone_index + 1),
                                 "\"Production non récolté\" doit être parmis les choix disponibles",
                                 "sectionDonnées réchauffement"))
                        else:
                            if production_non_recolte == "Oui":
                                production_non_recolte = True
                            else:
                                production_non_recolte = False
                        taux_matiere_seche = regie.grid_slaves(row=4, column=1)[0].get()
                        if (not util.is_decimal_number(
                                taux_matiere_seche) and taux_matiere_seche != "") or (
                                util.is_decimal_number(taux_matiere_seche) and (
                                float(taux_matiere_seche) < 0 or float(taux_matiere_seche) > 1)):
                            entree_invalide_liste.append(
                                (information_champs[champs_index]["nom_du_champs"],
                                 "Zone gestion " + str(zone_index + 1),
                                 "\"Taux matière sèche\" doit être un réel positif dans l'intervalle [0,1] ou le champs peut être vide pour aller chercher une proportion par défaut",
                                 "section Données réchauffement"))
                        if taux_matiere_seche == "":
                            taux_matiere_seche = None
                        if taux_matiere_seche is not None and util.is_decimal_number(taux_matiere_seche):
                            taux_matiere_seche = float(taux_matiere_seche)
                        culture_principale_dict = {"culture_principale": culture_principale,
                                                   "rendement": rendement,
                                                   "proportion_tige_exporte": proportion_tige_exporte,
                                                   "produit_non_recolte": production_non_recolte,
                                                   "taux_matiere_seche": taux_matiere_seche}
                        travail_du_sol = regie.grid_slaves(row=5, column=1)[0].get()
                        global types_travail_du_sol_supportes
                        if travail_du_sol not in types_travail_du_sol_supportes:
                            entree_invalide_liste.append(
                                (information_champs[champs_index]["nom_du_champs"],
                                 "Zone gestion " + str(zone_index + 1),
                                 "\"Travail du sol\" doit être parmis les choix disponibles",
                                 " section Données réchauffement"))
                        profondeur = regie.grid_slaves(row=6, column=1)[0].get()
                        if not util.is_decimal_number(profondeur) or float(
                                profondeur) < 0:
                            entree_invalide_liste.append(
                                (information_champs[champs_index]["nom_du_champs"],
                                 "Zone gestion " + str(zone_index + 1),
                                 "\"Profondeur\" doit être un réel positif",
                                 "section Données réchauffement"))
                        if profondeur == "":
                            profondeur = None
                        if profondeur is not None and util.is_decimal_number(profondeur):
                            profondeur = float(profondeur)
                        travail_du_sol_dict = {"travail_du_sol": travail_du_sol,
                                               "profondeur_du_travail": profondeur}
                        culture_secondaire = regie.grid_slaves(row=7, column=1)[0].get()
                        global cultures_secondaires_supportees
                        if culture_secondaire == "":
                            culture_secondaire = None
                        if culture_secondaire is not None and culture_secondaire not in cultures_secondaires_supportees:
                            entree_invalide_liste.append(
                                (information_champs[champs_index]["nom_du_champs"],
                                 "Zone gestion " + str(zone_index + 1),
                                 "\"Culture secondaire\" doit être parmis les choix disponibles ou laissé vide s'il n'y a pas de culture secondaire",
                                 " section Données réchauffement"))
                        rendement_culture_secondaire = regie.grid_slaves(row=8, column=1)[0].get()
                        if rendement_culture_secondaire == "":
                            rendement_culture_secondaire = None
                        if rendement_culture_secondaire is not None and not util.is_decimal_number(
                                rendement_culture_secondaire):
                            entree_invalide_liste.append(
                                (information_champs[champs_index]["nom_du_champs"],
                                 "Zone gestion " + str(zone_index + 1),
                                 "\"Rendement culture secondaire\" doit être un réel positif ou laissé vide s'il n'y a pas de culture secondaire",
                                 "section Données réchauffement"))
                        elif (culture_secondaire is None and rendement_culture_secondaire is not None) or (
                                culture_secondaire is not None and rendement_culture_secondaire is None):
                            entree_invalide_liste.append(
                                (information_champs[champs_index]["nom_du_champs"],
                                 "Zone gestion " + str(zone_index + 1),
                                 "\"Rendement culture secondaire\" et \"Culture secondaire\" doivent être tout deux laissé vide s'il n'y a pas de culture secondaire",
                                 "section Données réchauffement"))
                        else:
                            if rendement_culture_secondaire is not None:
                                rendement_culture_secondaire = float(rendement_culture_secondaire)
                        culture_secondaire_dict = {"culture_secondaire": culture_secondaire,
                                                   "rendement": rendement_culture_secondaire}
                        index_composante_amendement = 0
                        composante_amendement_liste = regie.grid_slaves(row=9, column=0)[0]
                        grid_size = composante_amendement_liste.grid_size()
                        amendements = []
                        while index_composante_amendement < grid_size[1] - 1:
                            amendement = \
                                composante_amendement_liste.grid_slaves([index_composante_amendement], column=1)[
                                    0].get()
                            global amendements_supportees
                            if amendement == "":
                                amendement = None
                            if amendement is not None and amendement not in amendements_supportees:
                                entree_invalide_liste.append(
                                    (information_champs[champs_index]["nom_du_champs"],
                                     "Zone gestion " + str(zone_index + 1),
                                     "\"Amendement\" " + str(
                                         index_composante_amendement + 1) + " doit être parmis les choix disponibles",
                                     "section Données réchauffement"))
                            apport = \
                                composante_amendement_liste.grid_slaves([index_composante_amendement + 1], column=1)[
                                    0].get()
                            if apport == "":
                                apport = None
                            if apport is not None and not util.is_decimal_number(apport):
                                entree_invalide_liste.append(
                                    (information_champs[champs_index]["nom_du_champs"],
                                     "Zone gestion " + str(zone_index + 1),
                                     "\"Apport\" " + str(index_composante_amendement + 1) +
                                     " est invalide, il doit être un réel positif ou laissé vide s'il n'y a pas d'amendements",
                                     "section Données réchauffement"))
                            elif (amendement is None and apport is not None) or (
                                    amendement is not None and apport is None):
                                entree_invalide_liste.append(
                                    (information_champs[champs_index]["nom_du_champs"],
                                     "Zone gestion " + str(zone_index + 1),
                                     "\"Apport\" " + str(
                                         index_composante_amendement + 1) + " et \"Amendement\" " + str(
                                         index_composante_amendement + 1) +
                                     " doivent être tout deux laissé vide s'il n'y a pas d'amendements",
                                     "section Données réchauffement"))
                            else:
                                if apport is not None:
                                    apport = float(apport)
                            amendements.append({"amendement": amendement,
                                                "apport": apport})
                            index_composante_amendement += 2
                        regie_dict = {"culture_principale": culture_principale_dict,
                                      "culture_secondaire": culture_secondaire_dict,
                                      "amendements": amendements,
                                      "travail_du_sol": travail_du_sol_dict}
                        zone_regies.append(regie_dict)
                        index_regie += 1
                    champs_regies_liste.append(zone_regies)
                    zone_index += 1
                regies_rechauffement_simulation.append(champs_regies_liste)
                champs_index += 1
            return regies_rechauffement_simulation, entree_invalide_liste

        def editer_caracteristique_physique_entreprise():
            def fenetre_edition_ferme():
                root.deiconify()
                edition_window.destroy()

            root.withdraw()
            edition_window = tk.Toplevel()
            edition_window.protocol("WM_DELETE_WINDOW", fenetre_edition_ferme)
            edition_frame = ttk.Frame(edition_window)
            canvas = tk.Canvas(edition_frame)
            scrollbar = ttk.Scrollbar(edition_frame, orient="vertical", command=canvas.yview)
            scrollable_frame = ttk.Frame(canvas)
            scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            entreprise_label_frame = ttk.LabelFrame(scrollable_frame, text="Entreprise")
            nom_entreprise_label = ttk.Label(entreprise_label_frame, text="Nom de l'entreprise: ")
            nom_entreprise_entry = ttk.Entry(entreprise_label_frame)
            global nom_entreprise
            nom_entreprise_entry.insert(0, nom_entreprise)
            nom_entreprise_label.grid(row=0, column=0, sticky="w", pady=3)
            nom_entreprise_entry.grid(row=0, column=1, sticky="w", pady=3)
            champs_row_index = 1
            global nombre_de_champs
            for champs_index in range(nombre_de_champs):
                champs_label_frame = ttk.LabelFrame(entreprise_label_frame, text="Champs " + str(champs_index + 1))
                global information_champs
                nom_champs_label = ttk.Label(champs_label_frame, text="Nom du champ: ")
                nom_champs_entry = ttk.Entry(champs_label_frame)
                if information_champs[champs_index]["nom_du_champs"]:
                    nom_champs_entry.insert(0, information_champs[champs_index]["nom_du_champs"])
                nom_champs_label.grid(row=0, column=0, sticky="w", pady=3)
                nom_champs_entry.grid(row=0, column=1, sticky="w", pady=3)
                zone_row_index = 1
                information_zones_de_gestion = information_champs[champs_index]["information_zone_de_gestion"]
                for zone_index in range(int(information_champs[champs_index]["nombre_de_zone_de_gestion"])):
                    information_zone_de_gestion = information_zones_de_gestion[zone_index]
                    zone_label_frame = ttk.LabelFrame(champs_label_frame, text="Zone gestion " + str(zone_index + 1))
                    taux_matiere_organique_label = ttk.Label(zone_label_frame,
                                                             text="Taux matière organique (en %): ")
                    taux_matiere_organique_entry = ttk.Entry(zone_label_frame)
                    if information_zone_de_gestion["taux_matiere_organique"] is not None:
                        taux_matiere_organique_entry.insert(0, information_zone_de_gestion["taux_matiere_organique"])
                    municipalite_label = ttk.Label(zone_label_frame, text="Municipalité: ")
                    global municipalites_supportees
                    municipalite_combobox = ttk.Combobox(zone_label_frame, values=municipalites_supportees,
                                                         postcommand=lambda: filter_combobox_values(
                                                             municipalite_combobox, municipalites_supportees))
                    municipalite_combobox.set(information_zone_de_gestion["municipalite"])
                    classe_texturale_label = ttk.Label(zone_label_frame, text="Classe texturale: ")
                    global classes_texturales_supportees
                    classe_texturale_combobox = ttk.Combobox(zone_label_frame, values=classes_texturales_supportees,
                                                             postcommand=lambda: filter_combobox_values(
                                                                 classe_texturale_combobox,
                                                                 classes_texturales_supportees))
                    classe_texturale_combobox.set(information_zone_de_gestion["classe_texturale"])
                    classe_de_drainage_label = ttk.Label(zone_label_frame, text="Classe de drainage: ")
                    global classes_de_drainage_supportees
                    classe_de_drainage_combobox = ttk.Combobox(zone_label_frame, values=classes_de_drainage_supportees,
                                                               postcommand=lambda: filter_combobox_values(
                                                                   classe_de_drainage_combobox,
                                                                   classes_de_drainage_supportees))
                    classe_de_drainage_combobox.set(information_zone_de_gestion["classe_de_drainage"])
                    masse_volumique_apparente_label = ttk.Label(zone_label_frame,
                                                                text="Masse volumique apparente (g/cm3): ")
                    masse_volumique_apparente_entry = ttk.Entry(zone_label_frame)
                    if information_zone_de_gestion["masse_volumique_apparente"] is not None:
                        masse_volumique_apparente_entry.insert(0,
                                                               information_zone_de_gestion["masse_volumique_apparente"])
                    profondeur_label = ttk.Label(zone_label_frame, text="Profondeur (cm): ")
                    profondeur_entry = ttk.Entry(zone_label_frame)
                    if information_zone_de_gestion["profondeur"] is not None:
                        profondeur_entry.insert(0, information_zone_de_gestion["profondeur"])
                    superficie_de_la_zone_label = ttk.Label(zone_label_frame,
                                                            text="Superficie de la zone (ha): ")
                    superficie_de_la_zone_entry = ttk.Entry(zone_label_frame)
                    if information_zone_de_gestion["superficie_de_la_zone"] is not None:
                        superficie_de_la_zone_entry.insert(0, information_zone_de_gestion["superficie_de_la_zone"])
                    taux_matiere_organique_label.grid(row=0, column=0, sticky="w", pady=3)
                    taux_matiere_organique_entry.grid(row=0, column=1, sticky="w", pady=3)
                    municipalite_label.grid(row=1, column=0, sticky="w", pady=3)
                    municipalite_combobox.grid(row=1, column=1, sticky="w", pady=3)
                    classe_texturale_label.grid(row=2, column=0, sticky="w", pady=3)
                    classe_texturale_combobox.grid(row=2, column=1, sticky="w", pady=3)
                    classe_de_drainage_label.grid(row=3, column=0, sticky="w", pady=3)
                    classe_de_drainage_combobox.grid(row=3, column=1, sticky="w", pady=3)
                    masse_volumique_apparente_label.grid(row=4, column=0, sticky="w", pady=3)
                    masse_volumique_apparente_entry.grid(row=4, column=1, sticky="w", pady=3)
                    profondeur_label.grid(row=5, column=0, sticky="w", pady=3)
                    profondeur_entry.grid(row=5, column=1, sticky="w", pady=3)
                    superficie_de_la_zone_label.grid(row=6, column=0, sticky="w", pady=3)
                    superficie_de_la_zone_entry.grid(row=6, column=1, sticky="w", pady=3)
                    zone_label_frame.grid(row=zone_row_index, column=0, columnspan=2, padx=10)
                    zone_row_index += 1
                champs_label_frame.grid(row=champs_row_index, column=0, columnspan=2, padx=10)
                champs_row_index += 1
            entreprise_label_frame.pack(padx=10, pady=10)
            canvas.pack(side="left", ipadx=5)
            scrollbar.pack(side="right", fill="y")

            def effectuer_la_sauvegarde():
                entree_invalide_liste = []
                global nom_entreprise
                nom_entreprise = nom_entreprise_entry.get()
                global information_champs
                information_champs = []
                champs_label_frame_index = 2
                entreprise_widgets = entreprise_label_frame.winfo_children()
                while champs_label_frame_index < len(entreprise_widgets):
                    champs_frame = entreprise_widgets[champs_label_frame_index]
                    nom_du_champs = champs_frame.winfo_children()[1].get()
                    champs_widgets = champs_frame.winfo_children()
                    zone_label_frame_index = 2
                    info_zones_de_gestion = []
                    while zone_label_frame_index < len(champs_widgets):
                        zone_frame = champs_widgets[zone_label_frame_index]
                        taux_matiere_organique = zone_frame.grid_slaves(row=0, column=1)[0].get()
                        if not util.is_decimal_number(taux_matiere_organique) or float(
                                taux_matiere_organique) < 0 or float(taux_matiere_organique) > 100:
                            entree_invalide_liste.append(
                                ("Champs " + str(champs_label_frame_index - 1),
                                 "Zone gestion " + str(zone_label_frame_index - 1),
                                 "\"Taux de matière organique\" doit être un réel positif dans l'intervalle [0-100]"))
                        else:
                            taux_matiere_organique = float(taux_matiere_organique)
                        municipalite = zone_frame.grid_slaves(row=1, column=1)[0].get()
                        global municipalites_supportees
                        if municipalite not in municipalites_supportees:
                            entree_invalide_liste.append(
                                ("Champs " + str(champs_label_frame_index - 1),
                                 "Zone gestion " + str(zone_label_frame_index - 1),
                                 "\"Municipalité\" doit être parmis les choix disponibles"))
                        classe_texturale = zone_frame.grid_slaves(row=2, column=1)[0].get()
                        global classes_texturales_supportees
                        if classe_texturale not in classes_texturales_supportees:
                            entree_invalide_liste.append(
                                ("Champs " + str(champs_label_frame_index - 1),
                                 "Zone gestion " + str(zone_label_frame_index - 1),
                                 "\"Classe texturale\" doit être parmis les choix disponibles"))
                        classe_de_drainage = zone_frame.grid_slaves(row=3, column=1)[0].get()
                        global classes_de_drainage_supportees
                        if classe_de_drainage not in classes_de_drainage_supportees:
                            entree_invalide_liste.append(
                                ("Champs " + str(champs_label_frame_index - 1),
                                 "Zone gestion " + str(zone_label_frame_index - 1),
                                 "\"Classe de drainage\" doit être parmis les choix disponibles"))
                        masse_volumique_apparente = zone_frame.grid_slaves(row=4, column=1)[0].get()
                        if (not util.is_decimal_number(
                                masse_volumique_apparente) and masse_volumique_apparente != "") or (
                                util.is_decimal_number(masse_volumique_apparente) and float(
                            masse_volumique_apparente) < 0):
                            entree_invalide_liste.append(
                                ("Champs " + str(champs_label_frame_index - 1),
                                 "Zone gestion " + str(zone_label_frame_index - 1),
                                 "\"Masse volumique apparente\" doit être un réel positif ou laissé vide pour aller chercher la valeur par défaut"))
                        else:
                            if masse_volumique_apparente == "":
                                masse_volumique_apparente = None
                            else:
                                masse_volumique_apparente = float(masse_volumique_apparente)
                        profondeur = zone_frame.grid_slaves(row=5, column=1)[0].get()
                        if not util.is_decimal_number(profondeur) or float(
                                profondeur) < 0:
                            entree_invalide_liste.append(
                                ("Champs " + str(champs_label_frame_index - 1),
                                 "Zone gestion " + str(zone_label_frame_index - 1),
                                 "\"Profondeur\" doit être un réel positif"))
                        else:
                            profondeur = float(profondeur)
                        superficie_de_la_zone = zone_frame.grid_slaves(row=6, column=1)[0].get()
                        if not util.is_decimal_number(superficie_de_la_zone) or float(
                                superficie_de_la_zone) < 0:
                            entree_invalide_liste.append(
                                ("Champs " + str(champs_label_frame_index - 1),
                                 "Zone gestion " + str(zone_label_frame_index - 1),
                                 "\"Superficie de la zone\" doit être un réel positif"))
                        else:
                            superficie_de_la_zone = float(superficie_de_la_zone)
                        info_zones_de_gestion.append(
                            {"taux_matiere_organique": taux_matiere_organique,
                             "municipalite": municipalite,
                             "classe_texturale": classe_texturale,
                             "classe_de_drainage": classe_de_drainage,
                             "masse_volumique_apparente": masse_volumique_apparente,
                             "profondeur": profondeur,
                             "superficie_de_la_zone": superficie_de_la_zone})
                        zone_label_frame_index += 1
                    information_champs.append({"nom_du_champs": nom_du_champs,
                                               "nombre_de_zone_de_gestion": str(len(champs_widgets) - 2),
                                               "information_zone_de_gestion": info_zones_de_gestion})
                    champs_label_frame_index += 1

                if len(entree_invalide_liste) == 0:
                    root.deiconify()
                    effectuer_les_modifications_a_la_fenetre_principale()
                    sauvegarder_attributs_entreprise_apres_modification()
                    edition_window.destroy()
                else:
                    message = ""
                    for entree_invalide in entree_invalide_liste:
                        message = message + "Dans le " + entree_invalide[0] + " et la " + entree_invalide[
                            1] + " l'entrée " + entree_invalide[2] + "\n"
                    messagebox.showwarning("Warning", message)
                    edition_window.focus()

            def effectuer_les_modifications_a_la_fenetre_principale():
                index_simulation_frame = 0
                simulation_frames = simulation_notebook.winfo_children()
                global information_champs
                for simulation_frame in simulation_frames:
                    if index_simulation_frame < len(simulation_frames) - 1:
                        champs_notebook = simulation_frame.winfo_children()[0]
                        index_champs_frame = 0
                        while index_champs_frame < len(champs_notebook.winfo_children()) - 1:
                            champs_notebook.tab(index_champs_frame,
                                                text=information_champs[index_champs_frame]["nom_du_champs"])
                            index_champs_frame += 1

                    index_simulation_frame += 1
                rechauffement_frame = donnees_de_rechauffement_label_frame.winfo_children()[0].winfo_children()[0]
                index = 0
                for champs in rechauffement_frame.winfo_children():
                    champs.configure(text=information_champs[index]["nom_du_champs"])
                    index += 1

            sauvegarde_des_modifications_button = ttk.Button(scrollable_frame, text="Sauvegarder",
                                                             command=effectuer_la_sauvegarde)
            sauvegarde_des_modifications_button.pack()

            edition_frame.pack()

        for widget in parent_frame_tabs.winfo_children():
            widget.destroy()

        rechauffement_frame = ttk.Frame(parent_frame_tabs)
        projection_frame = ttk.Frame(parent_frame_tabs, width=575, height=400)

        rechauffement_frame.grid(row=0, column=1)
        projection_frame.grid(row=0, column=0)
        projection_frame.grid_propagate(False)

        donnees_de_rechauffement_label_frame = ttk.LabelFrame(rechauffement_frame, text="Données de réchauffement")
        simulation_notebook = ttk.Notebook(projection_frame)

        global nombre_simulations
        if nombre_simulations != 0:
            pass
        else:
            nombre_simulations = 0

        global duree_simulation
        if len(duree_simulation) != 0:
            pass
        else:
            duree_simulation = []

        tab1 = ttk.Frame(simulation_notebook)

        simulation_notebook.bind("<Button-1>", add_new_simulation_tab)
        simulation_notebook.bind("<Button-3>", delete_simulation_tab)

        simulation_notebook.add(tab1, text="+")

        scroll_right_frame = ttk.Frame(projection_frame)
        scroll_left_frame = ttk.Frame(projection_frame)

        scroll_right_button_simulation = ttk.Button(scroll_right_frame, text="\u25b6")
        scroll_left_button_simulation = ttk.Button(scroll_left_frame, text="\u25c0")

        scroll_right_button_simulation.configure(command=scroll_right_simulation, state="disabled")
        scroll_left_button_simulation.configure(command=scroll_left_simulation, state="disabled")

        scroll_right_button_simulation.grid(row=0, column=0, sticky="n")
        scroll_left_button_simulation.grid(row=0, column=0, sticky="n")

        scroll_right_button_champs = ttk.Button(scroll_right_frame, text="\u25b6")
        scroll_left_button_champs = ttk.Button(scroll_left_frame, text="\u25c0")

        scroll_right_button_champs.configure(command=scroll_right_champs, state="disabled")
        scroll_left_button_champs.configure(command=scroll_left_champs, state="disabled")

        scroll_right_button_champs.grid(row=1, column=0, sticky="n")
        scroll_left_button_champs.grid(row=1, column=0, sticky="n")

        scroll_right_button_zone = ttk.Button(scroll_right_frame, text="\u25b6")
        scroll_left_button_zone = ttk.Button(scroll_left_frame, text="\u25c0")

        scroll_right_button_zone.configure(command=scroll_right_zone, state="disabled")
        scroll_left_button_zone.configure(command=scroll_left_zone, state="disabled")

        scroll_right_button_zone.grid(row=2, column=0, sticky="n")
        scroll_left_button_zone.grid(row=2, column=0, sticky="n")

        scroll_right_frame.grid(row=0, column=2, sticky="n")
        scroll_left_frame.grid(row=0, column=0, sticky="n")

        simulation_notebook.grid(row=0, column=1, sticky="nw")

        set_up_regies_rechauffement(donnees_de_rechauffement_label_frame, show_regie_historique, simulations)
        donnees_de_rechauffement_label_frame.grid(row=0, column=0, pady=3)
        sauvegarder_plan_de_gestion_button = ttk.Button(rechauffement_frame, text="Sauvegarder le plan de gestion",
                                                        command=lambda: sauvegarder_plan_de_gestion_de_carbone(
                                                            sauvegarder_toutes_les_simulations()))
        sauvegarder_plan_de_gestion_button.grid(row=1, column=0, pady=3)

        if simulations is not None:
            simulation_notebook.winfo_children()[simulation_notebook.index("end") - 1].destroy()
            index_simulation = 0
            for simulation in simulations:
                if index_simulation == 0:
                    set_up_simulation(simulation_notebook, simulation, True)
                else:
                    set_up_simulation(simulation_notebook, simulation, False)
                if index_simulation != len(simulations) - 1:
                    simulation_notebook.winfo_children()[simulation_notebook.index("end") - 1].destroy()
                index_simulation += 1
            global simulations_chargees
            simulations_chargees = False

    def question_ajout_regie_historique(question_mainframe, simulations=None):
        question_frame = ttk.Frame(question_mainframe)
        question_label = ttk.Label(question_frame,
                                   text="Voulez-vous utiliser une régie historique pour réchauffer le modèle?")
        oui_button = ttk.Button(question_frame, text="Oui",
                                command=lambda: set_up_annees_historiques(question_mainframe, simulations=simulations))
        non_button = ttk.Button(question_frame, text="Non",
                                command=lambda: show_creation_des_regies(question_mainframe,
                                                                         show_regie_historique=False,
                                                                         simulations=simulations))
        question_label.grid(row=0, column=0, columnspan=2, padx=5, pady=3)
        oui_button.grid(row=1, column=0, padx=5, pady=3)
        non_button.grid(row=1, column=1, padx=5, pady=3)
        question_frame.pack()

    def set_up_annees_historiques(annee_historique_mainframe, simulations=None):
        def get_annees_historiques():
            global annees_historiques
            annee_historique_initiale = annee_historique_initiale_entry.get()
            annee_historique_finale = annee_historique_finale_entry.get()
            annees_historiques = {"annee_historique_initiale": annee_historique_initiale,
                                  "annee_historique_finale": annee_historique_finale}
            show_creation_des_regies(annee_historique_mainframe, show_regie_historique=True, simulations=simulations)

        for widget in annee_historique_mainframe.winfo_children():
            widget.destroy()
        annee_historique_frame = ttk.Frame(annee_historique_mainframe)
        annee_historique_initiale_label = ttk.Label(annee_historique_frame,
                                                    text="Année historique initiale: ")
        annee_historique_initiale_entry = ttk.Entry(annee_historique_frame)
        annee_historique_finale_label = ttk.Label(annee_historique_frame, text="Année historique finale: ")
        annee_historique_finale_entry = ttk.Entry(annee_historique_frame)

        annee_historique_initiale_label.grid(row=0, column=0, sticky="w", pady=3)
        annee_historique_initiale_entry.grid(row=0, column=1, sticky="w", pady=3)
        annee_historique_finale_label.grid(row=1, column=0, sticky="w", pady=3)
        annee_historique_finale_entry.grid(row=1, column=1, sticky="w", pady=3)

        get_annees_historiques_button = ttk.Button(annee_historique_frame, text="Confirmer",
                                                   command=get_annees_historiques)
        get_annees_historiques_button.grid(row=2, column=0, columnspan=2, pady=3)

        annee_historique_frame.pack()

    def menu_initial_ogemos(menu_frame):
        def creation_nouvelle_entreprise():
            for widget in menu_frame.winfo_children():
                widget.destroy()
            show_entreprise_set_up(menu_frame)

        def charger_entreprise():
            for widget in menu_frame.winfo_children():
                widget.destroy()
            root.withdraw()
            global filename
            filename = filedialog.askopenfilename(initialdir="/", title="Select file",
                                                  filetypes=(("json files", "*.json"), ("all files", "*.*")))
            if filename == "":
                menu_initial_ogemos(menu_frame)
                root.deiconify()
                return
            root.deiconify()

            no_error = True
            try:
                with open(filename) as file:
                    data = json.load(file)
                global nom_entreprise
                global nombre_de_champs
                global information_champs
                nom_entreprise = data["nom_entreprise"]
                nombre_de_champs = data["nombre_de_champs"]
                information_champs = data["information_champs"]
            except KeyError:
                root.withdraw()
                no_error = False
                messagebox.showwarning("Fichier Invalide", "Le fichier ne correspondant pas au format désiré.")
                root.deiconify()
                menu_initial_ogemos(menu_frame)

            if no_error:
                question_ajout_regie_historique(menu_frame)

        def charger_plan_de_gestion_de_carbone():
            global simulations_chargees
            simulations_chargees = True
            for widget in menu_frame.winfo_children():
                widget.destroy()
            root.withdraw()
            global plan_gestion_filename
            plan_gestion_filename = filedialog.askopenfilename(initialdir="/", title="Select file",
                                                               filetypes=(
                                                                   ("json files", "*.json"), ("all files", "*.*")))
            if plan_gestion_filename == "":
                menu_initial_ogemos(menu_frame)
                root.deiconify()
                return
            root.deiconify()

            no_error = True
            try:
                with open(plan_gestion_filename) as file:
                    data = json.load(file)
                global nom_entreprise
                global nombre_de_champs
                global information_champs
                global duree_simulation
                global nombre_simulations
                global annees_historiques
                annees_historiques = data["annees_historiques"]
                information_champs = []
                duree_simulation = []
                simulations = data["simulations"]
                nombre_simulations = len(simulations)
                for simulation in simulations:
                    duree_simulation.append({"annee_projection_initiale": simulation["annee_initiale_projection"],
                                             "duree_projection": simulation["duree_projection"],
                                             "nom_simulation": simulation["nom_simulation"]})
                if len(simulations) > 0:
                    entreprise = simulations[0]["entreprise_agricole"]
                    nom_entreprise = entreprise["nom"]
                    nombre_de_champs = len(entreprise["champs"])
                    if nombre_de_champs > 0:
                        champs_liste = entreprise["champs"]
                        for champs in champs_liste:
                            if len(champs["zones_de_gestion"]) > 0:
                                information_zone_de_gestion = []
                                zone_de_gestion_liste = champs["zones_de_gestion"]
                                for zone_de_gestion in zone_de_gestion_liste:
                                    information_zone_de_gestion.append(
                                        {"taux_matiere_organique": zone_de_gestion["taux_matiere_organique"],
                                         "municipalite": zone_de_gestion["municipalite"],
                                         "classe_texturale": zone_de_gestion["classe_texturale"],
                                         "classe_de_drainage": zone_de_gestion["classe_de_drainage"],
                                         "masse_volumique_apparente": zone_de_gestion["masse_volumique_apparente"],
                                         "profondeur": zone_de_gestion["profondeur"],
                                         "superficie_de_la_zone": zone_de_gestion["superficie_de_la_zone"]})
                                information_champs.append({"nom_du_champs": champs["nom"],
                                                           "nombre_de_zone_de_gestion": len(champs["zones_de_gestion"]),
                                                           "information_zone_de_gestion": information_zone_de_gestion})
            except KeyError:
                root.withdraw()
                no_error = False
                messagebox.showwarning("Fichier Invalide", "Le fichier ne correspondant pas au format désiré.")
                root.deiconify()
                menu_initial_ogemos(menu_frame)

            if no_error:
                show_creation_des_regies(menu_frame, show_regie_historique=data["presence_regie_historique"],
                                         simulations=simulations)

        bienvenue_label = ttk.Label(menu_frame, text="Bienvenue dans OGEMOS!")
        nouvelle_entreprise_button = ttk.Button(menu_frame, text="Créer une nouvelle entreprise",
                                                command=creation_nouvelle_entreprise)
        charger_entreprise_button = ttk.Button(menu_frame, text="Charger une entreprise", command=charger_entreprise)
        charger_plan_de_gestion_de_carbone_button = ttk.Button(menu_frame, text="Charger un plan de gestion de carbone",
                                                               command=charger_plan_de_gestion_de_carbone)

        bienvenue_label.pack(pady=5, padx=10)
        nouvelle_entreprise_button.pack(pady=5, padx=10)
        charger_entreprise_button.pack(pady=5, padx=10)
        charger_plan_de_gestion_de_carbone_button.pack(pady=5, padx=10)

    def sauvegarder_attributs_entreprise_apres_creation():
        root.withdraw()
        global filename
        filename = filedialog.asksaveasfilename(initialdir="/", title="File Explorer",
                                                filetypes=(("json files", "*.json"), ("all files", "*.*")))
        if filename == "":
            root.deiconify()
            return False
        if ".json" not in filename:
            filename = filename + ".json"
        global nom_entreprise
        global nombre_de_champs
        global information_champs
        save_dict = {"nom_entreprise": nom_entreprise,
                     "nombre_de_champs": nombre_de_champs,
                     "information_champs": information_champs}

        with open(filename, 'w') as json_file:
            json.dump(save_dict, json_file)
        root.deiconify()
        return True

    def sauvegarder_attributs_entreprise_apres_modification():
        global nom_entreprise
        global nombre_de_champs
        global information_champs
        save_dict = {"nom_entreprise": nom_entreprise,
                     "nombre_de_champs": nombre_de_champs,
                     "information_champs": information_champs}
        global filename
        if filename is None:
            response = messagebox.askyesno("Sauvegarde entreprise",
                                           "Souhaitez-vous sauvegarder les modifications apportées à l'entreprise?")
            if response:
                filename_valide = sauvegarder_attributs_entreprise_apres_creation()
                if filename_valide:
                    with open(filename, 'w') as json_file:
                        json.dump(save_dict, json_file)
        else:
            with open(filename, 'w') as json_file:
                json.dump(save_dict, json_file)

    def sauvegarder_plan_de_gestion_de_carbone(simulations):
        if isinstance(simulations, list):
            entree_invalide_liste = simulations
            message = ""
            for entree_invalide in entree_invalide_liste:
                message = message + "Dans la " + entree_invalide[3] + ", le " + entree_invalide[0] + " et la " + \
                          entree_invalide[
                              1] + " l'entrée " + entree_invalide[2] + "\n"
            messagebox.showwarning("Warning", message)
            root.deiconify()
            return
        root.withdraw()
        global plan_gestion_filename
        plan_gestion_filename = filedialog.asksaveasfilename(initialdir="/", title="File Explorer",
                                                             filetypes=(("json files", "*.json"), ("all files", "*.*")))
        if plan_gestion_filename == "":
            root.deiconify()
            return False
        if ".json" not in plan_gestion_filename:
            plan_gestion_filename = plan_gestion_filename + ".json"

        save_dict = simulations

        with open(plan_gestion_filename, 'w') as json_file:
            json.dump(save_dict, json_file)
        root.deiconify()

    def creation_du_rapport(bilan_response):
        bilan_workbook = Workbook()
        description_champs_worksheet = bilan_workbook.active
        index_column_cell = 1
        index_row_cell = 1
        global information_champs
        for champs in information_champs:
            description_champs_worksheet.cell(row=index_row_cell, column=index_column_cell,
                                              value=champs["nom_du_champs"])
            index_row_cell += 1
            description_champs_worksheet.cell(row=index_row_cell, column=index_column_cell,
                                              value="Taux de matière organique")
            index_row_cell += 1
            description_champs_worksheet.cell(row=index_row_cell, column=index_column_cell,
                                              value="Municipalité")
            index_row_cell += 1
            description_champs_worksheet.cell(row=index_row_cell, column=index_column_cell,
                                              value="Classe de drainage")
            index_row_cell += 1
            description_champs_worksheet.cell(row=index_row_cell, column=index_column_cell,
                                              value="Masse volumique apparente")
            index_row_cell += 1
            description_champs_worksheet.cell(row=index_row_cell, column=index_column_cell,
                                              value="Profondeur")
            index_row_cell += 1
            description_champs_worksheet.cell(row=index_row_cell, column=index_column_cell,
                                              value="Superficie de la zone")
            index_column_cell += 1
            index_zone = 1
            for zones in champs["information_zone_de_gestion"]:
                index_row_cell = 1
                description_champs_worksheet.cell(row=index_row_cell, column=index_column_cell,
                                                  value="Zone de gestion " + str(index_zone))
                index_row_cell += 1
                description_champs_worksheet.cell(row=index_row_cell, column=index_column_cell,
                                                  value=zones["taux_matiere_organique"])
                index_row_cell += 1
                description_champs_worksheet.cell(row=index_row_cell, column=index_column_cell,
                                                  value=zones["municipalite"])
                index_row_cell += 1
                description_champs_worksheet.cell(row=index_row_cell, column=index_column_cell,
                                                  value=zones["classe_de_drainage"])
                index_row_cell += 1
                description_champs_worksheet.cell(row=index_row_cell, column=index_column_cell,
                                                  value=zones["masse_volumique_apparente"])
                index_row_cell += 1
                description_champs_worksheet.cell(row=index_row_cell, column=index_column_cell,
                                                  value=zones["profondeur"])
                index_row_cell += 1
                description_champs_worksheet.cell(row=index_row_cell, column=index_column_cell,
                                                  value=zones["superficie_de_la_zone"])
                index_column_cell += 1
                index_zone += 1
            index_row_cell = 1

        global duree_simulation
        index_row_cell = 1
        index_column_cell = 1
        index_simulation = 0
        for simulation in bilan_response.json()["bilans_des_simulations"]:
            description_simulation_worksheet = bilan_workbook.create_sheet(
                duree_simulation[index_simulation]["nom_simulation"])
            for champs in simulation["bilans_des_champs"]:
                row_shift = 0
                count_row_shift = True
                description_simulation_worksheet.cell(row=index_row_cell, column=index_column_cell,
                                                      value=champs["nom_du_champs"])
                index_row_cell += 1
                index = 1
                for zone in champs["bilans_des_zones"]:
                    description_simulation_worksheet.cell(row=index_row_cell, column=index_column_cell,
                                                          value="Zone de gestion " + str(index))
                    index_row_cell += 1
                    description_simulation_worksheet.cell(row=index_row_cell, column=index_column_cell,
                                                          value="Année de projection")
                    index_row_cell += 1

                    for annee in range(int(duree_simulation[index_simulation]["annee_projection_initiale"]),
                                       int(duree_simulation[index_simulation]["annee_projection_initiale"]) + int(
                                           duree_simulation[index_simulation]["duree_projection"])):
                        description_simulation_worksheet.cell(row=index_row_cell, column=index_column_cell,
                                                              value=annee)
                        index_row_cell += 1
                    description_simulation_worksheet.cell(row=index_row_cell, column=index_column_cell,
                                                          value="Total")
                    index_row_cell += 1
                    description_simulation_worksheet.cell(row=index_row_cell, column=index_column_cell,
                                                          value="Moyenne")
                    index_row_cell = 3
                    index_column_cell += 1
                    description_simulation_worksheet.cell(row=index_row_cell, column=index_column_cell,
                                                          value="Apport culture principale")
                    index_row_cell += 1
                    for apport_culture_principale in zone["bilan_apports_cultures_principales"]:
                        description_simulation_worksheet.cell(row=index_row_cell, column=index_column_cell,
                                                              value=apport_culture_principale)
                        if count_row_shift:
                            row_shift += 1
                        index_row_cell += 1

                    count_row_shift = False

                    row_shift += 1

                    description_simulation_worksheet.cell(row=index_row_cell, column=index_column_cell,
                                                          value="=SUM(" + str(index_row_cell) + "," + str(
                                                              index_column_cell) + ")")
                    index_row_cell += 1

                    row_shift += 1

                    description_simulation_worksheet.cell(row=index_row_cell, column=index_column_cell,
                                                          value="=AVERAGE(" + str(index_row_cell) + "," + str(
                                                              index_column_cell) + ")")
                    index_row_cell = 3
                    index_column_cell += 1

                    description_simulation_worksheet.cell(row=index_row_cell, column=index_column_cell,
                                                          value="Apport culture secondaire")
                    index_row_cell += 1

                    for apport_culture_secondaire in zone["bilan_apports_cultures_secondaires"]:
                        description_simulation_worksheet.cell(row=index_row_cell, column=index_column_cell,
                                                              value=apport_culture_secondaire)
                        index_row_cell += 1

                    description_simulation_worksheet.cell(row=index_row_cell, column=index_column_cell,
                                                          value="=SUM(" + str(index_row_cell) + "," + str(
                                                              index_column_cell) + ")")
                    index_row_cell += 1

                    description_simulation_worksheet.cell(row=index_row_cell, column=index_column_cell,
                                                          value="=AVERAGE(" + str(index_row_cell) + "," + str(
                                                              index_column_cell) + ")")
                    index_row_cell = 3
                    index_column_cell += 1

                    description_simulation_worksheet.cell(row=index_row_cell, column=index_column_cell,
                                                          value="Apport amendements")
                    index_row_cell += 1

                    for apport_amendement in zone["bilan_apports_amendements"]:
                        description_simulation_worksheet.cell(row=index_row_cell, column=index_column_cell,
                                                              value=apport_amendement)
                        index_row_cell += 1

                    description_simulation_worksheet.cell(row=index_row_cell, column=index_column_cell,
                                                          value="=SUM(" + str(index_row_cell) + "," + str(
                                                              index_column_cell) + ")")
                    index_row_cell += 1

                    description_simulation_worksheet.cell(row=index_row_cell, column=index_column_cell,
                                                          value="=AVERAGE(" + str(index_row_cell) + "," + str(
                                                              index_column_cell) + ")")

                    index_row_cell += 1
                    index_column_cell -= 3

                    description_simulation_worksheet.cell(row=index_row_cell, column=index_column_cell,
                                                          value="Teneur initiale en MOS de la zone")
                    index_row_cell += 1

                    description_simulation_worksheet.cell(row=index_row_cell, column=index_column_cell,
                                                          value="Teneur finale en MOS de la zone")
                    index_row_cell += 1

                    description_simulation_worksheet.cell(row=index_row_cell, column=index_column_cell,
                                                          value="Évolution du taux de MOS de la zone")
                    index_row_cell += 1

                    description_simulation_worksheet.cell(row=index_row_cell, column=index_column_cell,
                                                          value="Comparaison 50ème percentile de la zone")
                    index_row_cell += 1

                    description_simulation_worksheet.cell(row=index_row_cell, column=index_column_cell,
                                                          value="Comparaison 90ème percentile de la zone")

                    index_row_cell -= 4
                    index_column_cell += 1

                    # TODO: Modifier les 5 valeurs plus bas pour les valeurs calcuclés dans le bilan

                    description_simulation_worksheet.cell(row=index_row_cell, column=index_column_cell,
                                                          value="Teneur initiale en MOS")
                    index_row_cell += 1

                    description_simulation_worksheet.cell(row=index_row_cell, column=index_column_cell,
                                                          value="Teneur finale en MOS")
                    index_row_cell += 1

                    description_simulation_worksheet.cell(row=index_row_cell, column=index_column_cell,
                                                          value="Évolution du taux de MOS")
                    index_row_cell += 1

                    description_simulation_worksheet.cell(row=index_row_cell, column=index_column_cell,
                                                          value="Comparaison 50ème percentile")
                    index_row_cell += 1

                    description_simulation_worksheet.cell(row=index_row_cell, column=index_column_cell,
                                                          value="Comparaison 90ème percentile")

                    index_row_cell = 2
                    index_column_cell += 3

                    index += 1

                index_column_cell -= champs["nombre_de_zone_de_gestion"] * 4
                index_row_cell += row_shift

                description_simulation_worksheet.cell(row=index_row_cell, column=index_column_cell,
                                                      value="Teneur initiale en MOS du champs")
                index_row_cell += 1

                description_simulation_worksheet.cell(row=index_row_cell, column=index_column_cell,
                                                      value="Teneur finale en MOS du champs")
                index_row_cell += 1

                description_simulation_worksheet.cell(row=index_row_cell, column=index_column_cell,
                                                      value="Évolution du taux de MOS du champs")
                index_row_cell += 1

                description_simulation_worksheet.cell(row=index_row_cell, column=index_column_cell,
                                                      value="Comparaison 50ème percentile du champs")
                index_row_cell += 1

                description_simulation_worksheet.cell(row=index_row_cell, column=index_column_cell,
                                                      value="Comparaison 90ème percentile du champs")

                index_row_cell -= 4
                index_column_cell += 1

                # TODO: Modifier les 5 valeurs plus bas pour les valeurs calcuclés dans le bilan

                description_simulation_worksheet.cell(row=index_row_cell, column=index_column_cell,
                                                      value="Teneur initiale en MOS")
                index_row_cell += 1

                description_simulation_worksheet.cell(row=index_row_cell, column=index_column_cell,
                                                      value="Teneur finale en MOS")
                index_row_cell += 1

                description_simulation_worksheet.cell(row=index_row_cell, column=index_column_cell,
                                                      value="Évolution du taux de MOS")
                index_row_cell += 1

                description_simulation_worksheet.cell(row=index_row_cell, column=index_column_cell,
                                                      value="Comparaison 50ème percentile")
                index_row_cell += 1

                description_simulation_worksheet.cell(row=index_row_cell, column=index_column_cell,
                                                      value="Comparaison 90ème percentile")

                index_row_cell = 1
                index_column_cell = 1 + champs["nombre_de_zone_de_gestion"] * 4

            index_row_cell = row_shift + 7
            index_column_cell = 1

            description_simulation_worksheet.cell(row=index_row_cell, column=index_column_cell,
                                                  value="Teneur initiale en MOS du champs")
            index_row_cell += 1

            description_simulation_worksheet.cell(row=index_row_cell, column=index_column_cell,
                                                  value="Teneur finale en MOS du champs")
            index_row_cell += 1

            description_simulation_worksheet.cell(row=index_row_cell, column=index_column_cell,
                                                  value="Évolution du taux de MOS du champs")
            index_row_cell += 1

            description_simulation_worksheet.cell(row=index_row_cell, column=index_column_cell,
                                                  value="Comparaison 50ème percentile du champs")
            index_row_cell += 1

            description_simulation_worksheet.cell(row=index_row_cell, column=index_column_cell,
                                                  value="Comparaison 90ème percentile du champs")

            index_row_cell -= 4
            index_column_cell += 1

            # TODO: Modifier les 5 valeurs plus bas pour les valeurs calcuclés dans le bilan

            description_simulation_worksheet.cell(row=index_row_cell, column=index_column_cell,
                                                  value="Teneur initiale en MOS")
            index_row_cell += 1

            description_simulation_worksheet.cell(row=index_row_cell, column=index_column_cell,
                                                  value="Teneur finale en MOS")
            index_row_cell += 1

            description_simulation_worksheet.cell(row=index_row_cell, column=index_column_cell,
                                                  value="Évolution du taux de MOS")
            index_row_cell += 1

            description_simulation_worksheet.cell(row=index_row_cell, column=index_column_cell,
                                                  value="Comparaison 50ème percentile")
            index_row_cell += 1

            description_simulation_worksheet.cell(row=index_row_cell, column=index_column_cell,
                                                  value="Comparaison 90ème percentile")

            index_simulation += 1

            index_row_cell = 1
            index_column_cell = 1

        bilan_workbook.save("C:\\Users\\Samuel\\Documents\\Stage IRDA\\Test sauvegarde\\test.xlsx")

    menu_initial_ogemos(frame)


run_gui(mainframe)

root.mainloop()
