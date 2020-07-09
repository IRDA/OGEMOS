import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import json
import copy
import GUI.fonction_utilitaire as util

root = tk.Tk()
root.title("OGEMOS")
mainframe = ttk.Frame(root)
mainframe.grid(row=0, column=0)


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

        nom_entreprise_label.grid(row=0, column=0)
        nom_entreprise_entry.grid(row=0, column=1)
        nombre_de_champs_label.grid(row=1, column=0)
        nombre_de_champs_entry.grid(row=1, column=1)

        creer_bouton = ttk.Button(frame_entreprise, text="Créer", command=get_information_entreprise)
        creer_bouton.grid(columnspan=2, row=2, column=0)

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
                        information_champs.append({"nom_du_champs": nom_du_champs,
                                                   "nombre_de_zone_de_gestion": nombre_de_zone_de_gestion,
                                                   "information_zone_de_gestion": []})
                    else:
                        champs_valides = False
                        information_champs = []
                        messagebox.showwarning("Warning",
                                               "Une entrée \"Nombre de zone de gestion\" est invalide.Veuillez entrer un nombre naturel plus grand que 0.")
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
            nom_du_champs_label = ttk.Label(champs_frame, text="Nom du champs: ")
            nom_du_champs_entry = ttk.Entry(champs_frame)
            nombre_de_zone_de_gestion_label = ttk.Label(champs_frame, text="Nombre de zone de gestion: ")
            nombre_de_zone_de_gestion_entry = ttk.Entry(champs_frame)
            nombre_de_zone_de_gestion_entry.insert(0, "1")
            nom_du_champs_label.grid(row=0, column=0)
            nom_du_champs_entry.grid(row=0, column=1)
            nombre_de_zone_de_gestion_label.grid(row=1, column=0)
            nombre_de_zone_de_gestion_entry.grid(row=1, column=1)

            champs_frame.pack(fill="both")

        canvas.pack(side="left", fill="x", expand=True)
        scrollbar.pack(side="right", fill="y")

        creation_champs_bouton = ttk.Button(scrollable_frame, text="Créer",
                                            command=lambda: get_information_champs(scrollable_frame))
        creation_champs_bouton.pack()

    def show_creation_zone_de_gestion(zone_de_gestion_mainframe):
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
                                        taux_matiere_organique) < 0:
                                    entree_invalide_liste.append((information_champs[index]["nom_du_champs"],
                                                                  "Zone de gestion " + str(index_zone),
                                                                  "\"Taux de matière organique\" doit être un réel positif"))
                            grid_slave1_1 = champs_frame_widget.grid_slaves(row=1, column=1)
                            for entry in grid_slave1_1:
                                # TODO: ajouter la validation après avoir call l'API pour les données
                                municipalite = entry.get()
                            grid_slave2_1 = champs_frame_widget.grid_slaves(row=2, column=1)
                            for entry in grid_slave2_1:
                                # TODO: ajouter la validation après avoir call l'API pour les données
                                serie_de_sol = entry.get()
                            grid_slave3_1 = champs_frame_widget.grid_slaves(row=3, column=1)
                            for entry in grid_slave3_1:
                                # TODO: ajouter la validation après avoir call l'API pour les données
                                classe_de_drainage = entry.get()
                            grid_slave4_1 = champs_frame_widget.grid_slaves(row=4, column=1)
                            for entry in grid_slave4_1:
                                masse_volumique_apparente = entry.get()
                                if (not util.is_decimal_number(masse_volumique_apparente) and masse_volumique_apparente != "") or (util.is_decimal_number(masse_volumique_apparente) and float(
                                        masse_volumique_apparente) < 0):
                                    entree_invalide_liste.append(
                                        (information_champs[index]["nom_du_champs"],
                                         "Zone de gestion " + str(
                                             information_champs[index]["nombre_de_zone_de_gestion"]),
                                         "\"Masse volumique apparente\" doit être un réel positif ou laissé vide pour aller chercher la valeur par défaut"))
                                if masse_volumique_apparente == "":
                                    masse_volumique_apparente = None
                            grid_slave5_1 = champs_frame_widget.grid_slaves(row=5, column=1)
                            for entry in grid_slave5_1:
                                profondeur = entry.get()
                                if not util.is_decimal_number(profondeur) or float(
                                        profondeur) < 0:
                                    entree_invalide_liste.append((information_champs[index]["nom_du_champs"],
                                                                  "Zone de gestion " + str(index_zone),
                                                                  "\"Profondeur\" doit être un réel positif"))
                            grid_slave6_1 = champs_frame_widget.grid_slaves(row=6, column=1)
                            for entry in grid_slave6_1:
                                superficie_de_la_zone = entry.get()
                                if not util.is_decimal_number(superficie_de_la_zone) or float(
                                        superficie_de_la_zone) < 0:
                                    entree_invalide_liste.append((information_champs[index]["nom_du_champs"],
                                                                  "Zone de gestion " + str(index_zone),
                                                                  "\"Superficie de la zone\" doit être un réel positif"))
                            information_champs[index]["information_zone_de_gestion"].append(
                                {"taux_matiere_organique": taux_matiere_organique,
                                 "municipalite": municipalite,
                                 "serie_de_sol": serie_de_sol,
                                 "classe_de_drainage": classe_de_drainage,
                                 "masse_volumique_apparente": masse_volumique_apparente,
                                 "profondeur": profondeur,
                                 "superficie_de_la_zone": superficie_de_la_zone})
                            index_zone += 1
                index += 1
            if len(entree_invalide_liste) == 0:
                sauvegarde_reussi = sauvergarder_attributs_entreprise_apres_creation()
                for widget in zone_de_gestion_mainframe.winfo_children():
                    widget.destroy()

                if sauvegarde_reussi:
                    question_ajout_regie_historique(zone_de_gestion_mainframe)
                else:
                    show_creation_zone_de_gestion(zone_de_gestion_mainframe)
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
                                                       text="Zone de gestion " + str(index_zone_de_gestion + 1))
                taux_matiere_organique_label = ttk.Label(zone_de_gestion_frame, text="Taux matière organique (en %): ")
                taux_matiere_organique_entry = ttk.Entry(zone_de_gestion_frame)
                municipalite_label = ttk.Label(zone_de_gestion_frame, text="Municipalité: ")
                municipalite_combobox = ttk.Combobox(zone_de_gestion_frame)
                serie_de_sol_label = ttk.Label(zone_de_gestion_frame, text="Série de sol: ")
                serie_de_sol_combobox = ttk.Combobox(zone_de_gestion_frame)
                classe_de_drainage_label = ttk.Label(zone_de_gestion_frame, text="Classe de drainage: ")
                classe_de_drainage_combobox = ttk.Combobox(zone_de_gestion_frame)
                masse_volumique_apparente_label = ttk.Label(zone_de_gestion_frame,
                                                            text="Masse volumique apparente (g/cm3): ")
                masse_volumique_apparente_entry = ttk.Entry(zone_de_gestion_frame)
                profondeur_label = ttk.Label(zone_de_gestion_frame, text="Profondeur (cm): ")
                profondeur_entry = ttk.Entry(zone_de_gestion_frame)
                superficie_de_la_zone_label = ttk.Label(zone_de_gestion_frame, text="Superficie de la zone (ha): ")
                superficie_de_la_zone_entry = ttk.Entry(zone_de_gestion_frame)
                taux_matiere_organique_label.grid(row=0, column=0)
                taux_matiere_organique_entry.grid(row=0, column=1)
                municipalite_label.grid(row=1, column=0)
                municipalite_combobox.grid(row=1, column=1)
                serie_de_sol_label.grid(row=2, column=0)
                serie_de_sol_combobox.grid(row=2, column=1)
                classe_de_drainage_label.grid(row=3, column=0)
                classe_de_drainage_combobox.grid(row=3, column=1)
                masse_volumique_apparente_label.grid(row=4, column=0)
                masse_volumique_apparente_entry.grid(row=4, column=1)
                profondeur_label.grid(row=5, column=0)
                profondeur_entry.grid(row=5, column=1)
                superficie_de_la_zone_label.grid(row=6, column=0)
                superficie_de_la_zone_entry.grid(row=6, column=1)

                zone_de_gestion_frame.pack()

            champs_frame.pack(fill="both")

        canvas.pack(side="left", fill="x", expand=True)
        scrollbar.pack(side="right", fill="y")

        creation_zone_de_gestion_bouton = ttk.Button(scrollable_frame, text="Créer",
                                                     command=lambda: get_information_zone_de_gestion(scrollable_frame))
        creation_zone_de_gestion_bouton.pack()

    def show_creation_des_regies(parent_frame_tabs, show_regie_historique):
        for widget in parent_frame_tabs.winfo_children():
            widget.destroy()

        donnees_de_rechauffement_label_frame = ttk.LabelFrame(parent_frame_tabs, text="Données de réchauffement")
        simulation_notebook = ttk.Notebook(parent_frame_tabs)
        global nombre_simulations
        nombre_simulations = 0

        global duree_simulation
        duree_simulation = []

        tab1 = ttk.Frame(simulation_notebook)

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
                        annee_projection_initiale = annee_projection_initiale_entry.get()
                        duree_projection = duree_projection_entry.get()
                        global annees_historiques
                        annee_projection_initiale_valide = True
                        try:
                            if int(annees_historiques["annee_historique_finale"]) + 1 != int(annee_projection_initiale):
                                annee_projection_initiale_valide = False
                        except NameError:
                            pass
                        if annee_projection_initiale.isdigit() and duree_projection.isdigit() and int(
                                duree_projection) > 0 and annee_projection_initiale_valide:
                            global duree_simulation
                            duree_simulation.append({"annee_projection_initiale": annee_projection_initiale,
                                                     "duree_projection": duree_projection})

                            duree_simulation_window.destroy()
                            set_up_simulation(simulation_notebook)
                        else:
                            entree_invalide_liste = []
                            message = ""
                            if not annee_projection_initiale.isdigit() or not annee_projection_initiale_valide:
                                entree_invalide_liste.append(
                                    "L'entrée \"Année de projection initiale\" est invalide. Si il y a une année historique finale, elle doit être supérieur d'une année à celle-ci et être un nombre naturel plus grand que 0.")
                            if not duree_projection.isdigit() or int(duree_projection) <= 0:
                                entree_invalide_liste.append(
                                    "L'entrée \"Durée de la projection\" est invalide. Elle doit être un nombre naturel plus grand que 0.")
                            for entree_invalide in entree_invalide_liste:
                                message = message + entree_invalide
                            messagebox.showwarning("Warning", message)
                            show_creation_des_regies(parent_frame_tabs, show_regie_historique)
                            duree_simulation_window.destroy()

                    root.withdraw()
                    duree_simulation_window = tk.Toplevel()
                    duree_simulation_window.protocol("WM_DELETE_WINDOW", readd_simulation)
                    duree_simulation_frame = ttk.Frame(duree_simulation_window)
                    annee_projection_initiale_label = ttk.Label(duree_simulation_frame,
                                                                text="Année de projection initiale: ")
                    annee_projection_initiale_entry = ttk.Entry(duree_simulation_frame)
                    duree_projection_label = ttk.Label(duree_simulation_frame,
                                                       text="Durée de la projection: ")
                    duree_projection_entry = ttk.Entry(duree_simulation_frame)
                    duree_projection_entry.insert(0, "30")

                    annee_projection_initiale_label.grid(row=0, column=0)
                    annee_projection_initiale_entry.grid(row=0, column=1)
                    duree_projection_label.grid(row=1, column=0)
                    duree_projection_entry.grid(row=1, column=1)

                    creer_simulation_bouton = ttk.Button(duree_simulation_frame,
                                                         command=get_duree_de_la_simulation)
                    creer_simulation_bouton.grid(row=5, column=0, columnspan=2)
                    duree_simulation_frame.pack()

                duree_de_la_simulation()

        def delete_simulation_tab(event):
            clicked_tab = simulation_notebook.tk.call(simulation_notebook._w, "identify", "tab", event.x, event.y)
            index_clicked_tab = simulation_notebook.index(clicked_tab)
            if index_clicked_tab != simulation_notebook.index("end") - 1:
                simulation_notebook.winfo_children()[index_clicked_tab].destroy()
                global nombre_simulations
                nombre_simulations -= 1
                current_index = index_clicked_tab
                global duree_simulation
                duree_simulation.pop(index_clicked_tab)
                while current_index < simulation_notebook.index("end"):
                    simulation_notebook.tab(current_index, text="Simulation " + str(current_index + 1))
                    if current_index == simulation_notebook.index("end") - 1:
                        simulation_notebook.tab(current_index, text="+")
                    current_index += 1

        def set_up_simulation(simulation_notebook):
            tab = ttk.Frame(simulation_notebook)
            global nombre_simulations
            simulation_notebook.add(tab, text="Simulation " + str(nombre_simulations))
            new_tab = ttk.Frame(simulation_notebook)
            simulation_notebook.add(new_tab, text="+")
            champs_notebook = ttk.Notebook(tab)

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
                            current_index = index_clicked_tab
                            while current_index < len(information_champs):
                                notebook.tab(current_index, text=information_champs[current_index]["nom_du_champs"])
                                current_index += 1

            champs_notebook.bind("<Button-1>", add_new_champs_tab)
            champs_notebook.bind("<Button-3>", delete_champs_tab)

            global information_champs
            for champs in information_champs:
                tab = ttk.Frame(champs_notebook)
                champs_notebook.add(tab, text=champs["nom_du_champs"])
                zone_de_gestion_notebook = ttk.Notebook(tab)
                global duree_simulation
                set_up_champs(zone_de_gestion_notebook, int(champs["nombre_de_zone_de_gestion"]), champs_notebook)

            tab = ttk.Frame(champs_notebook)
            champs_notebook.add(tab, text="+")

            champs_notebook.pack()

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
                    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
                    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
                    canvas.configure(yscrollcommand=scrollbar.set)
                    for index_zone_de_gestion_nouveau_champs in range(
                            int(nombre_de_zone_de_gestion)):
                        zone_de_gestion_frame = ttk.LabelFrame(scrollable_frame,
                                                               text="Zone de gestion " + str(
                                                                   index_zone_de_gestion_nouveau_champs + 1))
                        taux_matiere_organique_label = ttk.Label(zone_de_gestion_frame,
                                                                 text="Taux matière organique (en %): ")
                        taux_matiere_organique_entry = ttk.Entry(zone_de_gestion_frame)
                        municipalite_label = ttk.Label(zone_de_gestion_frame, text="Municipalité: ")
                        municipalite_combobox = ttk.Combobox(zone_de_gestion_frame)
                        serie_de_sol_label = ttk.Label(zone_de_gestion_frame, text="Série de sol: ")
                        serie_de_sol_combobox = ttk.Combobox(zone_de_gestion_frame)
                        classe_de_drainage_label = ttk.Label(zone_de_gestion_frame, text="Classe de drainage: ")
                        classe_de_drainage_combobox = ttk.Combobox(zone_de_gestion_frame)
                        masse_volumique_apparente_label = ttk.Label(zone_de_gestion_frame,
                                                                    text="Masse volumique apparente (g/cm3): ")
                        masse_volumique_apparente_entry = ttk.Entry(zone_de_gestion_frame)
                        profondeur_label = ttk.Label(zone_de_gestion_frame, text="Profondeur (cm): ")
                        profondeur_entry = ttk.Entry(zone_de_gestion_frame)
                        superficie_de_la_zone_label = ttk.Label(zone_de_gestion_frame,
                                                                text="Superficie de la zone (ha): ")
                        superficie_de_la_zone_entry = ttk.Entry(zone_de_gestion_frame)
                        taux_matiere_organique_label.grid(row=0, column=0)
                        taux_matiere_organique_entry.grid(row=0, column=1)
                        municipalite_label.grid(row=1, column=0)
                        municipalite_combobox.grid(row=1, column=1)
                        serie_de_sol_label.grid(row=2, column=0)
                        serie_de_sol_combobox.grid(row=2, column=1)
                        classe_de_drainage_label.grid(row=3, column=0)
                        classe_de_drainage_combobox.grid(row=3, column=1)
                        masse_volumique_apparente_label.grid(row=4, column=0)
                        masse_volumique_apparente_entry.grid(row=4, column=1)
                        profondeur_label.grid(row=5, column=0)
                        profondeur_entry.grid(row=5, column=1)
                        superficie_de_la_zone_label.grid(row=6, column=0)
                        superficie_de_la_zone_entry.grid(row=6, column=1)

                        zone_de_gestion_frame.pack()

                    creation_zone_de_gestion_bouton = ttk.Button(scrollable_frame, text="Créer",
                                                                 command=lambda: add_new_zone_tab())
                    creation_zone_de_gestion_bouton.pack()
                    canvas.pack(side="left", fill="x", expand=True)
                    scrollbar.pack(side="right", fill="y")
                    creation_zone_frame.pack()
                else:
                    message = "L'entrée \"Nombre de zone de gestion\" est invalide. Elle doit être un nombre naturel plus grand que 0."
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
                                        taux_matiere_organique) < 0:
                                    entree_invalide_liste.append(
                                        (information_champs[nombre_de_champs - 1]["nom_du_champs"],
                                         "Zone de gestion " + str(index_zone + 1),
                                         "\"Taux de matière organique\" doit être un réel positif"))
                            grid_slave1_1 = scrollable_frame_widget.grid_slaves(row=1, column=1)
                            for entry in grid_slave1_1:
                                # TODO: Ajouter la validation avec les valeurs de l'API
                                municipalite = entry.get()
                            grid_slave2_1 = scrollable_frame_widget.grid_slaves(row=2, column=1)
                            for entry in grid_slave2_1:
                                # TODO: Ajouter la validation avec les valeurs de l'API
                                serie_de_sol = entry.get()
                            grid_slave3_1 = scrollable_frame_widget.grid_slaves(row=3, column=1)
                            for entry in grid_slave3_1:
                                # TODO: Ajouter la validation avec les valeurs de l'API
                                classe_de_drainage = entry.get()
                            grid_slave4_1 = scrollable_frame_widget.grid_slaves(row=4, column=1)
                            for entry in grid_slave4_1:
                                masse_volumique_apparente = entry.get()
                                if (not util.is_decimal_number(masse_volumique_apparente) and masse_volumique_apparente != "") or (util.is_decimal_number(masse_volumique_apparente) and float(
                                        masse_volumique_apparente) < 0):
                                    entree_invalide_liste.append(
                                        (information_champs[nombre_de_champs - 1]["nom_du_champs"],
                                         "Zone de gestion " + str(
                                             information_champs[nombre_de_champs - 1]["nombre_de_zone_de_gestion"]),
                                         "\"Masse volumique apparente\" doit être un réel positif ou laissé vide pour aller chercher la valeur par défaut"))
                                if masse_volumique_apparente == "":
                                    masse_volumique_apparente = None
                            grid_slave5_1 = scrollable_frame_widget.grid_slaves(row=5, column=1)
                            for entry in grid_slave5_1:
                                profondeur = entry.get()
                                if not util.is_decimal_number(profondeur) or float(
                                        profondeur) < 0:
                                    entree_invalide_liste.append(
                                        (information_champs[nombre_de_champs - 1]["nom_du_champs"],
                                         "Zone de gestion " + str(index_zone + 1),
                                         "\"Profondeur\" doit être un réel positif"))
                            grid_slave6_1 = scrollable_frame_widget.grid_slaves(row=6, column=1)
                            for entry in grid_slave6_1:
                                superficie_de_la_zone = entry.get()
                                if not util.is_decimal_number(superficie_de_la_zone) or float(
                                        superficie_de_la_zone) < 0:
                                    entree_invalide_liste.append(
                                        (information_champs[nombre_de_champs - 1]["nom_du_champs"],
                                         "Zone de gestion " + str(index_zone + 1),
                                         "\"Superficie de la zone\" doit être un réel positif"))
                            information_champs[len(information_champs) - 1]["information_zone_de_gestion"].append(
                                {"taux_matiere_organique": taux_matiere_organique,
                                 "municipalite": municipalite,
                                 "serie_de_sol": serie_de_sol,
                                 "classe_de_drainage": classe_de_drainage,
                                 "masse_volumique_apparente": masse_volumique_apparente,
                                 "profondeur": profondeur,
                                 "superficie_de_la_zone": superficie_de_la_zone})
                        index_zone += 1
                    if len(entree_invalide_liste) == 0:
                        sauvegarder_attributs_entreprise_apres_modification()
                        new_champs_window.destroy()
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
                        rechauffement_champs_label_frame = ttk.LabelFrame(
                            donnees_de_rechauffement_label_frame.winfo_children()[0].winfo_children()[0],
                            text=nom_du_champs)
                        rechauffement_champs_label_frame.pack()
                        index_zone = 0
                        while index_zone < int(nombre_de_zone_de_gestion):
                            rechauffement_zone_label_frame = ttk.LabelFrame(rechauffement_champs_label_frame,
                                                                            text="Zone de gestion " + str(
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
            nom_du_champs_label = ttk.Label(nouveau_champs_frame, text="Nom du champs: ")
            nom_du_champs_entry = ttk.Entry(nouveau_champs_frame)
            nombre_de_zone_de_gestion_label = ttk.Label(nouveau_champs_frame,
                                                        text="Nombre de zone de gestion: ")
            nombre_de_zone_de_gestion_entry = ttk.Entry(nouveau_champs_frame)
            nom_du_champs_label.grid(row=0, column=0)
            nom_du_champs_entry.grid(row=0, column=1)
            nombre_de_zone_de_gestion_label.grid(row=1, column=0)
            nombre_de_zone_de_gestion_entry.grid(row=1, column=1)
            creer_nouveau_champs_bouton = ttk.Button(nouveau_champs_frame, text="Créer",
                                                     command=creation_des_zone_de_gestion_du_nouveau_champs)
            creer_nouveau_champs_bouton.grid(row=3, column=0, columnspan=2)
            nouveau_champs_frame.pack()

        def set_up_champs(zone_notebook, nombre_de_zone, champs_notebook):

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
                            text="Zone de gestion " + str(zone_index + 1))
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
                                                                 text="Zone de gestion " + str(current_index + 1))
                                if current_index == champs_courant_zone_notebook.index("end") - 1:
                                    champs_courant_zone_notebook.tab(current_index, text="+")
                                current_index += 1

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
                                                       text="Zone de gestion " + str(
                                                           information_champs[champs_index][
                                                               "nombre_de_zone_de_gestion"]))
                taux_matiere_organique_label = ttk.Label(zone_de_gestion_frame,
                                                         text="Taux matière organique (en %): ")
                taux_matiere_organique_entry = ttk.Entry(zone_de_gestion_frame)
                municipalite_label = ttk.Label(zone_de_gestion_frame, text="Municipalité: ")
                municipalite_combobox = ttk.Combobox(zone_de_gestion_frame)
                serie_de_sol_label = ttk.Label(zone_de_gestion_frame, text="Série de sol: ")
                serie_de_sol_combobox = ttk.Combobox(zone_de_gestion_frame)
                classe_de_drainage_label = ttk.Label(zone_de_gestion_frame, text="Classe de drainage: ")
                classe_de_drainage_combobox = ttk.Combobox(zone_de_gestion_frame)
                masse_volumique_apparente_label = ttk.Label(zone_de_gestion_frame,
                                                            text="Masse volumique apparente (g/cm3): ")
                masse_volumique_apparente_entry = ttk.Entry(zone_de_gestion_frame)
                profondeur_label = ttk.Label(zone_de_gestion_frame, text="Profondeur (cm): ")
                profondeur_entry = ttk.Entry(zone_de_gestion_frame)
                superficie_de_la_zone_label = ttk.Label(zone_de_gestion_frame,
                                                        text="Superficie de la zone (ha): ")
                superficie_de_la_zone_entry = ttk.Entry(zone_de_gestion_frame)
                taux_matiere_organique_label.grid(row=0, column=0)
                taux_matiere_organique_entry.grid(row=0, column=1)
                municipalite_label.grid(row=1, column=0)
                municipalite_combobox.grid(row=1, column=1)
                serie_de_sol_label.grid(row=2, column=0)
                serie_de_sol_combobox.grid(row=2, column=1)
                classe_de_drainage_label.grid(row=3, column=0)
                classe_de_drainage_combobox.grid(row=3, column=1)
                masse_volumique_apparente_label.grid(row=4, column=0)
                masse_volumique_apparente_entry.grid(row=4, column=1)
                profondeur_label.grid(row=5, column=0)
                profondeur_entry.grid(row=5, column=1)
                superficie_de_la_zone_label.grid(row=6, column=0)
                superficie_de_la_zone_entry.grid(row=6, column=1)

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
                                        taux_matiere_organique) < 0:
                                    entree_invalide_liste.append(
                                        (information_champs[champs_index]["nom_du_champs"],
                                         "Zone de gestion " + str(
                                             information_champs[champs_index]["nombre_de_zone_de_gestion"]),
                                         "\"Taux de matière organique\" doit être un réel positif"))
                            grid_slave1_1 = scrollable_frame_widget.grid_slaves(row=1, column=1)
                            for entry in grid_slave1_1:
                                # TODO: Ajouter la validation avec les valeurs de l'API
                                municipalite = entry.get()
                            grid_slave2_1 = scrollable_frame_widget.grid_slaves(row=2, column=1)
                            for entry in grid_slave2_1:
                                # TODO: Ajouter la validation avec les valeurs de l'API
                                serie_de_sol = entry.get()
                            grid_slave3_1 = scrollable_frame_widget.grid_slaves(row=3, column=1)
                            for entry in grid_slave3_1:
                                # TODO: Ajouter la validation avec les valeurs de l'API
                                classe_de_drainage = entry.get()
                            grid_slave4_1 = scrollable_frame_widget.grid_slaves(row=4, column=1)
                            for entry in grid_slave4_1:
                                masse_volumique_apparente = entry.get()
                                if (not util.is_decimal_number(masse_volumique_apparente) and masse_volumique_apparente != "") or (util.is_decimal_number(masse_volumique_apparente) and float(
                                        masse_volumique_apparente) < 0):
                                    entree_invalide_liste.append(
                                        (information_champs[champs_index]["nom_du_champs"],
                                         "Zone de gestion " + str(
                                             information_champs[champs_index]["nombre_de_zone_de_gestion"]),
                                         "\"Masse volumique apparente\" doit être un réel positif ou laissé vide pour aller chercher la valeur par défaut"))
                                if masse_volumique_apparente == "":
                                    masse_volumique_apparente = None
                            grid_slave5_1 = scrollable_frame_widget.grid_slaves(row=5, column=1)
                            for entry in grid_slave5_1:
                                profondeur = entry.get()
                                if not util.is_decimal_number(profondeur) or float(
                                        profondeur) < 0:
                                    entree_invalide_liste.append(
                                        (information_champs[champs_index]["nom_du_champs"],
                                         "Zone de gestion " + str(
                                             information_champs[champs_index]["nombre_de_zone_de_gestion"]),
                                         "\"Profondeur\" doit être un réel positif"))
                            grid_slave6_1 = scrollable_frame_widget.grid_slaves(row=6, column=1)
                            for entry in grid_slave6_1:
                                superficie_de_la_zone = entry.get()
                                if not util.is_decimal_number(superficie_de_la_zone) or float(
                                        superficie_de_la_zone) < 0:
                                    entree_invalide_liste.append(
                                        (information_champs[champs_index]["nom_du_champs"],
                                         "Zone de gestion " + str(
                                             information_champs[champs_index]["nombre_de_zone_de_gestion"]),
                                         "\"Superficie de la zone\" doit être un réel positif"))
                            information_champs[champs_index]["information_zone_de_gestion"].append(
                                {"taux_matiere_organique": taux_matiere_organique,
                                 "municipalite": municipalite,
                                 "serie_de_sol": serie_de_sol,
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
                                                                                   text="Zone de gestion " + str(len(
                                                                                       rechauffement_champs_label_frame.winfo_children()) + 1))
                        rechauffement_champs_new_zone_label_frame.pack()
                        if show_regie_historique:
                            add_regies_historiques(rechauffement_champs_new_zone_label_frame)
                        else:
                            ajouter_une_annee_a_la_rotation(rechauffement_champs_new_zone_label_frame)
                        new_zone_window.destroy()

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
                                tab = ttk.Frame(champs_courant_zone_notebook)
                                champs_courant_zone_notebook.add(tab, text="Zone de gestion " + str(
                                    len(champs_courant_zone_notebook.winfo_children())))
                                set_up_regies_projections(tab)

                                new_zone_tab = ttk.Frame(champs_courant_zone_notebook)
                                champs_courant_zone_notebook.add(new_zone_tab, text="+")
                            index += 1
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

            global duree_simulation
            for zone in range(int(nombre_de_zone)):
                zone_tab = ttk.Frame(zone_notebook)
                zone_notebook.add(zone_tab, text="Zone de gestion " + str(zone + 1))
                set_up_regies_projections(zone_tab)

            new_tab = ttk.Frame(zone_notebook)
            zone_notebook.add(new_tab, text="+")
            zone_notebook.pack()

        def set_up_regies_projections(zone_tab):
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
            ajouter_une_annee_a_la_rotation(scrollable_frame_projection)
            projection_frame.grid(row=1, column=0, columnspan=2)
            get_information_simulation_button = ttk.Button(zone_tab, text="Créer rapport",
                                                           command=get_information_toutes_les_simulations)
            get_information_simulation_button.grid(row=2, column=0)
            editer_information_entreprise_button = ttk.Button(zone_tab, text="Éditer attributs de l'entreprise",
                                                              command=editer_caracteristique_physique_entreprise)
            editer_information_entreprise_button.grid(row=2, column=1)

        def ajouter_une_annee_a_la_rotation(scrollable_frame_projection):
            if len(scrollable_frame_projection.winfo_children()) == 0:
                index = len(scrollable_frame_projection.winfo_children()) + 1
                add_regies_projection(scrollable_frame_projection, index)
                button_frame = ttk.Frame(scrollable_frame_projection)

                ajouter_une_annee_a_la_rotation_button = ttk.Button(button_frame, text="Ajouter une année de rotation",
                                                                    command=lambda: ajouter_une_annee_a_la_rotation(
                                                                        scrollable_frame_projection))
                ajouter_une_annee_a_la_rotation_button.grid(row=0, column=0)
                enlever_une_annee_a_la_rotation_button = ttk.Button(button_frame, text="Enlever une année de rotation",
                                                                    state="disabled")
                enlever_une_annee_a_la_rotation_button.grid(row=0, column=1)
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
                ajouter_une_annee_a_la_rotation_button.grid(row=0, column=0)
                enlever_une_annee_a_la_rotation_button = ttk.Button(button_frame, text="Enlever une année de rotation",
                                                                    command=lambda: enlever_une_annee_a_la_rotation(
                                                                        scrollable_frame_projection))
                enlever_une_annee_a_la_rotation_button.grid(row=0, column=1)
                button_frame.pack()

        def enlever_une_annee_a_la_rotation(scrollable_frame_projection):
            if len(scrollable_frame_projection.winfo_children()) > 1:
                scrollable_frame_projection.winfo_children()[
                    len(scrollable_frame_projection.winfo_children()) - 2].destroy()
            if len(scrollable_frame_projection.winfo_children()) - 1 == 1:
                scrollable_frame_projection.winfo_children()[
                    len(scrollable_frame_projection.winfo_children()) - 1].grid_slaves(row=0, column=1)[0].configure(
                    state="disabled")

        def set_up_regies_rechauffement(rechauffement_frame, show_regie_historique):
            global information_champs
            if show_regie_historique:
                canvas_historique = tk.Canvas(rechauffement_frame)
                scrollbar_historique = ttk.Scrollbar(rechauffement_frame, orient="vertical",
                                                     command=canvas_historique.yview)
                scrollable_frame_historique = ttk.Frame(canvas_historique)
                scrollable_frame_historique.bind("<Configure>", lambda e: canvas_historique.configure(
                    scrollregion=canvas_historique.bbox("all")))
                for champs in information_champs:
                    rechauffement_champs_label_frame = ttk.LabelFrame(scrollable_frame_historique,
                                                                      text=champs["nom_du_champs"])
                    rechauffement_champs_label_frame.pack()
                    index = 0
                    while index < int(champs["nombre_de_zone_de_gestion"]):
                        rechauffement_zone_label_frame = ttk.LabelFrame(rechauffement_champs_label_frame,
                                                                        text="Zone de gestion " + str(index + 1))
                        rechauffement_zone_label_frame.pack()
                        add_regies_historiques(rechauffement_zone_label_frame)
                        index += 1

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
                for champs in information_champs:
                    rechauffement_champs_label_frame = ttk.LabelFrame(scrollable_frame_rechauffement_via_rotation,
                                                                      text=champs["nom_du_champs"])
                    rechauffement_champs_label_frame.pack()
                    index = 0
                    while index < int(champs["nombre_de_zone_de_gestion"]):
                        rechauffement_zone_label_frame = ttk.LabelFrame(rechauffement_champs_label_frame,
                                                                        text="Zone de gestion " + str(index + 1))
                        rechauffement_zone_label_frame.pack()
                        ajouter_une_annee_a_la_rotation(rechauffement_zone_label_frame)
                        index += 1
                rechauffement_frame.grid(row=1, column=0, columnspan=2)

        def add_regies_historiques(scrollable_frame):
            global annees_historiques
            annee_historique_initiale = int(annees_historiques["annee_historique_initiale"])
            annee_historique_finale = int(annees_historiques["annee_historique_finale"])
            annee_courante = annee_historique_initiale
            while annee_courante <= annee_historique_finale:
                annee_courante_frame = ttk.LabelFrame(scrollable_frame, text=str(annee_courante))
                culture_principale_label = ttk.Label(annee_courante_frame, text="Culture principale: ")
                culture_principale_combobox = ttk.Combobox(annee_courante_frame)
                rendement_label = ttk.Label(annee_courante_frame, text="Rendement (t/ha): ")
                rendement_entry = ttk.Entry(annee_courante_frame)
                proportion_tige_exporte_label = ttk.Label(annee_courante_frame, text="Proportion tige exporté [0-1]: ")
                proportion_tige_exporte_entry = ttk.Entry(annee_courante_frame)
                production_non_recolte_label = ttk.Label(annee_courante_frame, text="Production non récoltée: ")
                production_non_recolte_combobox = ttk.Combobox(annee_courante_frame)
                taux_matiere_seche_label = ttk.Label(annee_courante_frame, text="Taux de matière sèche [0-1]: ")
                taux_matiere_seche_entry = ttk.Entry(annee_courante_frame)
                travail_du_sol_label = ttk.Label(annee_courante_frame, text="Travail du sol: ")
                travail_du_sol_combobox = ttk.Combobox(annee_courante_frame)
                profondeur_maximale_label = ttk.Label(annee_courante_frame, text="Profondeur maximale (cm): ")
                profondeur_maximale_entry = ttk.Entry(annee_courante_frame)
                culture_secondaire_label = ttk.Label(annee_courante_frame, text="Culture secondaire: ")
                culture_secondaire_combobox = ttk.Combobox(annee_courante_frame)
                rendement_culture_secondaire_label = ttk.Label(annee_courante_frame,
                                                               text="Rendement culture secondaire (t/ha): ")
                rendement_culture_secondaire_entry = ttk.Entry(annee_courante_frame)

                amendement_frame = ttk.LabelFrame(annee_courante_frame, text="Liste des amendements")
                ajouter_des_amendements(amendement_frame)

                culture_principale_label.grid(row=0, column=0)
                culture_principale_combobox.grid(row=0, column=1)
                rendement_label.grid(row=1, column=0)
                rendement_entry.grid(row=1, column=1)
                proportion_tige_exporte_label.grid(row=2, column=0)
                proportion_tige_exporte_entry.grid(row=2, column=1)
                production_non_recolte_label.grid(row=3, column=0)
                production_non_recolte_combobox.grid(row=3, column=1)
                taux_matiere_seche_label.grid(row=4, column=0)
                taux_matiere_seche_entry.grid(row=4, column=1)
                travail_du_sol_label.grid(row=5, column=0)
                travail_du_sol_combobox.grid(row=5, column=1)
                profondeur_maximale_label.grid(row=6, column=0)
                profondeur_maximale_entry.grid(row=6, column=1)
                culture_secondaire_label.grid(row=7, column=0)
                culture_secondaire_combobox.grid(row=7, column=1)
                rendement_culture_secondaire_label.grid(row=8, column=0)
                rendement_culture_secondaire_entry.grid(row=8, column=1)
                amendement_frame.grid(row=9, column=0, columnspan=2)

                annee_courante += 1
                annee_courante_frame.pack()

        def ajouter_des_amendements(amendement_frame):
            amendement_label = ttk.Label(amendement_frame, text="Amendement: ")
            amendement_combobox = ttk.Combobox(amendement_frame)
            apport_amendement_label = ttk.Label(amendement_frame, text="Apport (t):")
            apport_amendement_entry = ttk.Entry(amendement_frame)
            ajout_a_la_regie_button = ttk.Button(amendement_frame, text="Ajouter à la régie",
                                                 command=lambda: ajouter_amendement_regie(amendement_frame))
            ajout_a_la_liste_amendement = ttk.Button(amendement_frame, text="Ajouter un nouvel amendement",
                                                     command=ajouter_nouvel_amendement)
            amendement_label.grid(row=0, column=0)
            amendement_combobox.grid(row=0, column=1)
            apport_amendement_label.grid(row=1, column=0)
            apport_amendement_entry.grid(row=1, column=1)
            ajout_a_la_regie_button.grid(row=2, column=0)
            ajout_a_la_liste_amendement.grid(row=2, column=1)

        def ajouter_amendement_regie(amendement_frame):
            grid_size = amendement_frame.grid_size()
            amendement_frame.grid_slaves(grid_size[1] - 1, grid_size[0] - 1)[0].destroy()
            amendement_frame.grid_slaves(grid_size[1] - 1, grid_size[0] - 2)[0].destroy()
            amendement_label = ttk.Label(amendement_frame, text="Amendement: ")
            amendement_combobox = ttk.Combobox(amendement_frame)
            apport_amendement_label = ttk.Label(amendement_frame, text="Apport (t):")
            apport_amendement_entry = ttk.Entry(amendement_frame)
            ajout_a_la_regie_button = ttk.Button(amendement_frame, text="Ajouter à la régie",
                                                 command=lambda: ajouter_amendement_regie(amendement_frame))
            ajout_a_la_liste_amendement = ttk.Button(amendement_frame, text="Ajouter un nouvel amendement",
                                                     command=ajouter_nouvel_amendement)
            amendement_label.grid(row=grid_size[1] - 1, column=grid_size[0] - 2)
            amendement_combobox.grid(row=grid_size[1] - 1, column=grid_size[0] - 1)
            apport_amendement_label.grid(row=grid_size[1], column=grid_size[0] - 2)
            apport_amendement_entry.grid(row=grid_size[1], column=grid_size[0] - 1)
            ajout_a_la_regie_button.grid(row=grid_size[1] + 1, column=grid_size[0] - 2)
            ajout_a_la_liste_amendement.grid(row=grid_size[1] + 1, column=grid_size[0] - 1)

        def ajouter_nouvel_amendement():
            # TODO: Faire le UI et les calls nécessaire pour ajouter un amendement à la BD
            pass

        def add_regies_projection(scrollable_frame, index):
            annee_courante_frame = ttk.LabelFrame(scrollable_frame, text=str(index))
            culture_principale_label = ttk.Label(annee_courante_frame, text="Culture principale: ")
            culture_principale_combobox = ttk.Combobox(annee_courante_frame)
            rendement_label = ttk.Label(annee_courante_frame, text="Rendement (t/ha): ")
            rendement_entry = ttk.Entry(annee_courante_frame)
            proportion_tige_exporte_label = ttk.Label(annee_courante_frame, text="Proportion tige exporté [0-1]: ")
            proportion_tige_exporte_entry = ttk.Entry(annee_courante_frame)
            production_non_recolte_label = ttk.Label(annee_courante_frame, text="Production non récoltée: ")
            # TODO: Regarder pour autofill avec les combobox
            production_non_recolte_combobox = ttk.Combobox(annee_courante_frame, values=["Oui", "Non"])
            taux_matiere_seche_label = ttk.Label(annee_courante_frame, text="Taux de matière sèche [0-1]: ")
            taux_matiere_seche_entry = ttk.Entry(annee_courante_frame)
            travail_du_sol_label = ttk.Label(annee_courante_frame, text="Travail du sol: ")
            travail_du_sol_combobox = ttk.Combobox(annee_courante_frame)
            profondeur_maximale_label = ttk.Label(annee_courante_frame, text="Profondeur maxiamle (cm): ")
            profondeur_maximale_entry = ttk.Entry(annee_courante_frame)
            culture_secondaire_label = ttk.Label(annee_courante_frame, text="Culture secondaire: ")
            culture_secondaire_combobox = ttk.Combobox(annee_courante_frame)
            rendement_culture_secondaire_label = ttk.Label(annee_courante_frame,
                                                           text="Rendement culture secondaire (t/ha): ")
            rendement_culture_secondaire_entry = ttk.Entry(annee_courante_frame)

            amendement_frame = ttk.LabelFrame(annee_courante_frame, text="Liste des amendements")
            ajouter_des_amendements(amendement_frame)

            culture_principale_label.grid(row=0, column=0)
            culture_principale_combobox.grid(row=0, column=1)
            rendement_label.grid(row=1, column=0)
            rendement_entry.grid(row=1, column=1)
            proportion_tige_exporte_label.grid(row=2, column=0)
            proportion_tige_exporte_entry.grid(row=2, column=1)
            production_non_recolte_label.grid(row=3, column=0)
            production_non_recolte_combobox.grid(row=3, column=1)
            taux_matiere_seche_label.grid(row=4, column=0)
            taux_matiere_seche_entry.grid(row=4, column=1)
            travail_du_sol_label.grid(row=5, column=0)
            travail_du_sol_combobox.grid(row=5, column=1)
            profondeur_maximale_label.grid(row=6, column=0)
            profondeur_maximale_entry.grid(row=6, column=1)
            culture_secondaire_label.grid(row=7, column=0)
            culture_secondaire_combobox.grid(row=7, column=1)
            rendement_culture_secondaire_label.grid(row=8, column=0)
            rendement_culture_secondaire_entry.grid(row=8, column=1)
            amendement_frame.grid(row=9, column=0, columnspan=2)
            annee_courante_frame.pack()

        def get_information_toutes_les_simulations():
            simulations = []
            index_simualtion = 0
            for simulation in simulation_notebook.winfo_children():
                global nombre_simulations
                if index_simualtion < nombre_simulations:
                    simulation = get_information_simulation(simulation, index_simualtion)
                    simulations.append(simulation)
                index_simualtion += 1

        def get_information_simulation(simulation_frame, index_simulation):
            global information_champs
            global nombre_de_champs
            entree_invalide_simulation_liste = []
            regies_rechauffement, entree_invalide_liste = get_regies_rechauffement()
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
                            # TODO: Modifier cette section pour qu'elle prenne en considération la nouvelle façon de gérer les régies historiques
                            regies_projection_frame = zone_frames.winfo_children()[0]
                            regies_projection, entree_invalide_liste = get_regies(regies_projection_frame, index_champs,
                                                                                  index_zone, index_simulation)
                            zone_list.append({"regies_projection": regies_projection,
                                              "regies_rechauffement": regies_rechauffement[index_champs][index_zone]})
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
                                                 "serie_de_sol": zone["serie_de_sol"],
                                                 "classe_de_drainage": zone["classe_de_drainage"],
                                                 "masse_volumique_apparente": zone["masse_volumique_apparente"],
                                                 "profondeur": zone["profondeur"],
                                                 "superficie_de_la_zone": zone["superficie_de_la_zone"],
                                                 "regies_sol_et_culture_projection": champs_list[index_champs][index_zone]["regies_projection"],
                                                 "regies_sol_et_culture_historique": champs_list[index_champs][index_zone]["regies_rechauffement"]})
                        index_zone += 1
                    champs_attributs.append({"nom": champs["nom_du_champs"],
                                             "zones_de_gestion": zones_de_gestion})
                    index_champs += 1

                global nom_entreprise
                entreprise_agricole = {"nom": nom_entreprise,
                                       "champs": champs_attributs}
                global duree_simulation
                simulation = {
                    "annee_initiale_projection": int(duree_simulation[index_simulation]["annee_projection_initiale"]),
                    "annee_finale_projection": int(duree_simulation[index_simulation]["annee_projection_initiale"]) + int(
                        duree_simulation[index_simulation]["duree_projection"]),
                    "entreprise_agricole": entreprise_agricole}
                return simulation
            else:
                message = ""
                entree_invalide_liste = []
                for sous_liste in entree_invalide_simulation_liste:
                    for entree in sous_liste:
                        entree_invalide_liste.append(entree)
                for entree_invalide in entree_invalide_liste:
                    message = message + "Dans la " + entree_invalide[3] + ", le " + entree_invalide[0] + " et la " + entree_invalide[
                        1] + " l'entrée " + entree_invalide[2] + "\n"
                messagebox.showwarning("Warning", message)
                parent_frame_tabs.focus()

        def get_regies(regies_frame, champs_index, zone_index, simulation_index):
            entree_invalide_liste = []
            regies = []
            regies_canvas = regies_frame.winfo_children()[0]
            regies_scrollable_frame = regies_canvas.winfo_children()[0]
            compteur_regie = 0
            for regie in regies_scrollable_frame.winfo_children():
                if compteur_regie < len(regies_scrollable_frame.winfo_children()) - 1:
                    # TODO: Faire la validation une fois le call API fait pour avoir les valeurs
                    culture_principale = regie.grid_slaves(row=0, column=1)[0].get()
                    rendement = regie.grid_slaves(row=1, column=1)[0].get()
                    if not util.is_decimal_number(rendement) and rendement != "":
                        entree_invalide_liste.append(
                            (information_champs[champs_index]["nom_du_champs"],
                             "Zone de gestion " + str(zone_index + 1),
                             "\"Rendement\" doit être un réel positif ou la case peut être vide pour aller chercher un rendement par défaut",
                             "Régie projection Simulation "+str(simulation_index+1)))
                    if rendement == "":
                        rendement = None
                    if rendement is not None and util.is_decimal_number(rendement):
                        rendement = float(rendement)
                    proportion_tige_exporte = regie.grid_slaves(row=2, column=1)[0].get()
                    if (not util.is_decimal_number(
                            proportion_tige_exporte) and proportion_tige_exporte != "") or (util.is_decimal_number(proportion_tige_exporte) and (float(proportion_tige_exporte) < 0 or float(proportion_tige_exporte) > 1)):
                        entree_invalide_liste.append(
                            (information_champs[champs_index]["nom_du_champs"],
                             "Zone de gestion " + str(zone_index + 1),
                             "\"Proportion tige exportée\" doit être un réel positif dans l'intervalle [0,1] ou le champs peut être vide pour aller chercher une proportion par défaut",
                             "Régie projection Simulation "+str(simulation_index+1)))
                    if proportion_tige_exporte == "":
                        proportion_tige_exporte = None
                    if proportion_tige_exporte is not None and util.is_decimal_number(proportion_tige_exporte):
                        proportion_tige_exporte = float(proportion_tige_exporte)
                    production_non_recolte = regie.grid_slaves(row=3, column=1)[0].get()
                    if production_non_recolte not in ["Oui", "Non"]:
                        entree_invalide_liste.append(
                            (information_champs[champs_index]["nom_du_champs"],
                             "Zone de gestion " + str(zone_index + 1),
                             "\"Production non récolté\" doit être l'une des options de la combobox",
                             "Régie projection"))
                    taux_matiere_seche = regie.grid_slaves(row=4, column=1)[0].get()
                    if (not util.is_decimal_number(
                            taux_matiere_seche) and taux_matiere_seche != "") or (util.is_decimal_number(taux_matiere_seche) and (float(taux_matiere_seche) < 0 or float(taux_matiere_seche) > 1)):
                        entree_invalide_liste.append(
                            (information_champs[champs_index]["nom_du_champs"],
                             "Zone de gestion " + str(zone_index + 1),
                             "\"Taux matière sèche\" doit être un réel positif dans l'intervalle [0,1] ou le champs peut être vide pour aller chercher une proportion par défaut",
                             "Régie projection Simulation "+str(simulation_index+1)))
                    if taux_matiere_seche == "":
                        taux_matiere_seche = None
                    if taux_matiere_seche is not None and util.is_decimal_number(taux_matiere_seche):
                        taux_matiere_seche = float(taux_matiere_seche)
                    culture_principale_dict = {"culture_principale": culture_principale,
                                               "rendement": rendement,
                                               "proportion_tige_exporte": proportion_tige_exporte,
                                               "produit_non_recolte": production_non_recolte,
                                               "taux_matiere_seche": taux_matiere_seche}
                    # TODO: Faire la validation une fois le call API fait pour avoir les valeurs
                    travail_du_sol = regie.grid_slaves(row=5, column=1)[0].get()
                    profondeur = regie.grid_slaves(row=6, column=1)[0].get()
                    if (not util.is_decimal_number(
                            profondeur) and profondeur != "") or (util.is_decimal_number(profondeur) and (float(profondeur) < 0 or float(profondeur) > 1)):
                        entree_invalide_liste.append(
                            (information_champs[champs_index]["nom_du_champs"],
                             "Zone de gestion " + str(zone_index + 1),
                             "\"Profondeur\" doit être un réel positif",
                             "Régie projection Simulation "+str(simulation_index+1)))
                    if profondeur == "":
                        profondeur = None
                    if profondeur is not None and util.is_decimal_number(profondeur):
                        profondeur = float(taux_matiere_seche)
                    travail_du_sol_dict = {"travail_du_sol": travail_du_sol,
                                           "profondeur_du_travail": profondeur}
                    # TODO: Faire la validation une fois le call API fait pour avoir les valeurs
                    culture_secondaire = regie.grid_slaves(row=7, column=1)[0].get()
                    rendement_culture_secondaire = regie.grid_slaves(row=8, column=1)[0].get()
                    if not util.is_decimal_number(rendement_culture_secondaire):
                        entree_invalide_liste.append(
                            (information_champs[champs_index]["nom_du_champs"],
                             "Zone de gestion " + str(zone_index + 1),
                             "\"Rendement culture secondaire\" doit être un réel positif",
                             "Régie projection Simulation "+str(simulation_index+1)))
                    else:
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
                        apport = composante_amendement_liste.grid_slaves([index_composante_amendement + 1], column=1)[
                                0].get()
                        if not util.is_decimal_number(apport):
                            entree_invalide_liste.append(
                                (information_champs[champs_index]["nom_du_champs"],
                                 "Zone de gestion " + str(zone_index + 1),
                                 amendement + "\"Apport\" doit être un réel positif",
                                 "Régie projection Simulation "+str(simulation_index+1)))
                        else:
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

        simulation_notebook.bind("<Button-1>", add_new_simulation_tab)
        simulation_notebook.bind("<Button-3>", delete_simulation_tab)

        simulation_notebook.add(tab1, text="+")

        simulation_notebook.grid(row=0, column=0)
        set_up_regies_rechauffement(donnees_de_rechauffement_label_frame, show_regie_historique)
        donnees_de_rechauffement_label_frame.grid(row=0, column=1)

        def get_regies_rechauffement():
            entree_invalide_liste = []
            regies_rechauffement_simulation = []
            champs_label_frames = donnees_de_rechauffement_label_frame.winfo_children()[0].winfo_children()[0].winfo_children()
            champs_index = 0
            for champs_label_frame in champs_label_frames:
                champs_regies_liste = []
                zone_label_frames = champs_label_frame.winfo_children()
                zone_index = 0
                for zone_label_frame in zone_label_frames:
                    regies_de_rechauffement = zone_label_frame.winfo_children()
                    index_regie = 0
                    zone_regies = []
                    while index_regie < len(regies_de_rechauffement)-1:
                        regie = regies_de_rechauffement[index_regie]
                        culture_principale = regie.grid_slaves(row=0, column=1)[0].get()
                        rendement = regie.grid_slaves(row=1, column=1)[0].get()
                        if not util.is_decimal_number(rendement) and rendement != "":
                            entree_invalide_liste.append(
                                (information_champs[champs_index]["nom_du_champs"],
                                 "Zone de gestion " + str(zone_index + 1),
                                 "\"Rendement\" doit être un réel positif ou la case peut être vide pour aller chercher un rendement par défaut",
                                 " section Données réchauffement"))
                        if rendement == "":
                            rendement = None
                        if rendement is not None and util.is_decimal_number(rendement):
                            rendement = float(rendement)
                        proportion_tige_exporte = regie.grid_slaves(row=2, column=1)[0].get()
                        if (not util.is_decimal_number(
                                proportion_tige_exporte) and proportion_tige_exporte != "") or (util.is_decimal_number(proportion_tige_exporte) and (float(proportion_tige_exporte) < 0 or float(proportion_tige_exporte) > 1)):
                            entree_invalide_liste.append(
                                (information_champs[champs_index]["nom_du_champs"],
                                 "Zone de gestion " + str(zone_index + 1),
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
                                 "Zone de gestion " + str(zone_index + 1),
                                 "\"Production non récolté\" doit être l'une des options de la combobox",
                                 "sectionDonnées réchauffement"))
                        taux_matiere_seche = regie.grid_slaves(row=4, column=1)[0].get()
                        if (not util.is_decimal_number(
                                taux_matiere_seche) and taux_matiere_seche != "") or (
                                util.is_decimal_number(taux_matiere_seche) and (
                                float(taux_matiere_seche) < 0 or float(taux_matiere_seche) > 1)):
                            entree_invalide_liste.append(
                                (information_champs[champs_index]["nom_du_champs"],
                                 "Zone de gestion " + str(zone_index + 1),
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
                        # TODO: Faire la validation une fois le call API fait pour avoir les valeurs
                        travail_du_sol = regie.grid_slaves(row=5, column=1)[0].get()
                        profondeur = regie.grid_slaves(row=6, column=1)[0].get()
                        if (not util.is_decimal_number(
                                profondeur) and profondeur != "") or (util.is_decimal_number(profondeur) and (
                                float(profondeur) < 0 or float(profondeur) > 1)):
                            entree_invalide_liste.append(
                                (information_champs[champs_index]["nom_du_champs"],
                                 "Zone de gestion " + str(zone_index + 1),
                                 "\"Profondeur\" doit être un réel positif",
                                 "section Données réchauffement"))
                        if profondeur == "":
                            profondeur = None
                        if profondeur is not None and util.is_decimal_number(profondeur):
                            profondeur = float(taux_matiere_seche)
                        travail_du_sol_dict = {"travail_du_sol": travail_du_sol,
                                               "profondeur_du_travail": profondeur}
                        # TODO: Faire la validation une fois le call API fait pour avoir les valeurs
                        culture_secondaire = regie.grid_slaves(row=7, column=1)[0].get()
                        rendement_culture_secondaire = regie.grid_slaves(row=8, column=1)[0].get()
                        if not util.is_decimal_number(rendement_culture_secondaire):
                            entree_invalide_liste.append(
                                (information_champs[champs_index]["nom_du_champs"],
                                 "Zone de gestion " + str(zone_index + 1),
                                 "\"Rendement culture secondaire\" doit être un réel positif",
                                 "section Données réchauffement"))
                        else:
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
                            apport = composante_amendement_liste.grid_slaves([index_composante_amendement + 1], column=1)[
                                    0].get()
                            if not util.is_decimal_number(apport):
                                entree_invalide_liste.append(
                                    (information_champs[champs_index]["nom_du_champs"],
                                     "Zone de gestion " + str(zone_index + 1),
                                     amendement + "\"Apport\" doit être un réel positif",
                                     "section Données réchauffement"))
                            else:
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
            root.withdraw()
            edition_window = tk.Toplevel()
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
            nom_entreprise_label.grid(row=0, column=0)
            nom_entreprise_entry.grid(row=0, column=1)
            champs_row_index = 1
            global nombre_de_champs
            for champs_index in range(nombre_de_champs):
                champs_label_frame = ttk.LabelFrame(entreprise_label_frame, text="Champs " + str(champs_index + 1))
                global information_champs
                nom_champs_label = ttk.Label(champs_label_frame, text="Nom du champs: ")
                nom_champs_entry = ttk.Entry(champs_label_frame)
                nom_champs_entry.insert(0, information_champs[champs_index]["nom_du_champs"])
                nom_champs_label.grid(row=0, column=0)
                nom_champs_entry.grid(row=0, column=1)
                zone_row_index = 1
                information_zones_de_gestion = information_champs[champs_index]["information_zone_de_gestion"]
                for zone_index in range(int(information_champs[champs_index]["nombre_de_zone_de_gestion"])):
                    information_zone_de_gestion = information_zones_de_gestion[zone_index]
                    zone_label_frame = ttk.LabelFrame(champs_label_frame, text="Zone de gestion " + str(zone_index + 1))
                    taux_matiere_organique_label = ttk.Label(zone_label_frame,
                                                             text="Taux matière organique (en %): ")
                    taux_matiere_organique_entry = ttk.Entry(zone_label_frame)
                    taux_matiere_organique_entry.insert(0, information_zone_de_gestion["taux_matiere_organique"])
                    municipalite_label = ttk.Label(zone_label_frame, text="Municipalité: ")
                    municipalite_combobox = ttk.Combobox(zone_label_frame)
                    municipalite_combobox.set(information_zone_de_gestion["municipalite"])
                    serie_de_sol_label = ttk.Label(zone_label_frame, text="Série de sol: ")
                    serie_de_sol_combobox = ttk.Combobox(zone_label_frame)
                    serie_de_sol_combobox.set(information_zone_de_gestion["serie_de_sol"])
                    classe_de_drainage_label = ttk.Label(zone_label_frame, text="Classe de drainage: ")
                    classe_de_drainage_combobox = ttk.Combobox(zone_label_frame)
                    classe_de_drainage_combobox.set(information_zone_de_gestion["classe_de_drainage"])
                    masse_volumique_apparente_label = ttk.Label(zone_label_frame,
                                                                text="Masse volumique apparente (g/cm3): ")
                    masse_volumique_apparente_entry = ttk.Entry(zone_label_frame)
                    if information_zone_de_gestion["masse_volumique_apparente"] is not None:
                        masse_volumique_apparente_entry.insert(0, information_zone_de_gestion["masse_volumique_apparente"])
                    profondeur_label = ttk.Label(zone_label_frame, text="Profondeur (cm): ")
                    profondeur_entry = ttk.Entry(zone_label_frame)
                    profondeur_entry.insert(0, information_zone_de_gestion["profondeur"])
                    superficie_de_la_zone_label = ttk.Label(zone_label_frame,
                                                            text="Superficie de la zone (ha): ")
                    superficie_de_la_zone_entry = ttk.Entry(zone_label_frame)
                    superficie_de_la_zone_entry.insert(0, information_zone_de_gestion["superficie_de_la_zone"])
                    taux_matiere_organique_label.grid(row=0, column=0)
                    taux_matiere_organique_entry.grid(row=0, column=1)
                    municipalite_label.grid(row=1, column=0)
                    municipalite_combobox.grid(row=1, column=1)
                    serie_de_sol_label.grid(row=2, column=0)
                    serie_de_sol_combobox.grid(row=2, column=1)
                    classe_de_drainage_label.grid(row=3, column=0)
                    classe_de_drainage_combobox.grid(row=3, column=1)
                    masse_volumique_apparente_label.grid(row=4, column=0)
                    masse_volumique_apparente_entry.grid(row=4, column=1)
                    profondeur_label.grid(row=5, column=0)
                    profondeur_entry.grid(row=5, column=1)
                    superficie_de_la_zone_label.grid(row=6, column=0)
                    superficie_de_la_zone_entry.grid(row=6, column=1)
                    zone_label_frame.grid(row=zone_row_index, column=0, columnspan=2)
                    zone_row_index += 1
                champs_label_frame.grid(row=champs_row_index, column=0, columnspan=2)
                champs_row_index += 1
            entreprise_label_frame.pack()
            canvas.pack(side="left", fill="x", expand=True)
            scrollbar.pack(side="right", fill="y")

            def effectuer_la_sauvegarde():
                root.deiconify()
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
                        info_zones_de_gestion.append(
                            {"taux_matiere_organique": zone_frame.grid_slaves(row=0, column=1)[0].get(),
                             "municipalite": zone_frame.grid_slaves(row=1, column=1)[0].get(),
                             "serie_de_sol": zone_frame.grid_slaves(row=2, column=1)[0].get(),
                             "classe_de_drainage": zone_frame.grid_slaves(row=3, column=1)[0].get(),
                             "masse_volumique_apparente": zone_frame.grid_slaves(row=4, column=1)[0].get(),
                             "profondeur": zone_frame.grid_slaves(row=5, column=1)[0].get(),
                             "superficie_de_la_zone": zone_frame.grid_slaves(row=6, column=1)[0].get()})
                        zone_label_frame_index += 1
                    information_champs.append({"nom_du_champs": nom_du_champs,
                                               "nombre_de_zone_de_gestion": str(len(champs_widgets) - 2),
                                               "information_zone_de_gestion": info_zones_de_gestion})
                    champs_label_frame_index += 1

                effectuer_les_modifications_a_la_fenetre_principale()
                sauvegarder_attributs_entreprise_apres_modification()
                edition_window.destroy()

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

    def question_ajout_regie_historique(question_mainframe):
        question_frame = ttk.Frame(question_mainframe)
        question_label = ttk.Label(question_frame,
                                   text="Voulez-vous utiliser une régie historique pour réchauffer le modèle?")
        oui_button = ttk.Button(question_frame, text="Oui",
                                command=lambda: set_up_annees_historiques(question_mainframe))
        non_button = ttk.Button(question_frame, text="Non",
                                command=lambda: show_creation_des_regies(question_mainframe,
                                                                         show_regie_historique=False))
        question_label.grid(row=0, column=0, columnspan=2)
        oui_button.grid(row=1, column=0)
        non_button.grid(row=1, column=1)
        question_frame.pack()

    def set_up_annees_historiques(annee_historique_mainframe):
        def get_annees_historiques():
            global annees_historiques
            annee_historique_initiale = annee_historique_initiale_entry.get()
            annee_historique_finale = annee_historique_finale_entry.get()
            annees_historiques = {"annee_historique_initiale": annee_historique_initiale,
                                  "annee_historique_finale": annee_historique_finale}
            show_creation_des_regies(annee_historique_mainframe, show_regie_historique=True)

        for widget in annee_historique_mainframe.winfo_children():
            widget.destroy()
        annee_historique_frame = ttk.Frame(annee_historique_mainframe)
        annee_historique_initiale_label = ttk.Label(annee_historique_frame,
                                                    text="Année historique initiale: ")
        annee_historique_initiale_entry = ttk.Entry(annee_historique_frame)
        annee_historique_finale_label = ttk.Label(annee_historique_frame, text="Année historique finale: ")
        annee_historique_finale_entry = ttk.Entry(annee_historique_frame)

        annee_historique_initiale_label.grid(row=0, column=0)
        annee_historique_initiale_entry.grid(row=0, column=1)
        annee_historique_finale_label.grid(row=1, column=0)
        annee_historique_finale_entry.grid(row=1, column=1)

        get_annees_historiques_button = ttk.Button(annee_historique_frame, text="Confirmer",
                                                   command=get_annees_historiques)
        get_annees_historiques_button.grid(row=2, column=0, columnspan=2)

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

            with open(filename) as file:
                data = json.load(file)
            global nom_entreprise
            global nombre_de_champs
            global information_champs
            nom_entreprise = data["nom_entreprise"]
            nombre_de_champs = data["nombre_de_champs"]
            information_champs = data["information_champs"]

            question_ajout_regie_historique(menu_frame)

        bienvenue_label = ttk.Label(menu_frame, text="Bienvenue dans OGEMOS!")
        nouvelle_entreprise_button = ttk.Button(menu_frame, text="Créer une nouvelle entreprise",
                                                command=creation_nouvelle_entreprise)
        charger_entreprise_button = ttk.Button(menu_frame, text="Charger une entreprise", command=charger_entreprise)

        bienvenue_label.pack()
        nouvelle_entreprise_button.pack()
        charger_entreprise_button.pack()

    def sauvergarder_attributs_entreprise_apres_creation():
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
        with open(filename, 'w') as json_file:
            json.dump(save_dict, json_file)

    menu_initial_ogemos(frame)


run_gui(mainframe)

root.mainloop()
