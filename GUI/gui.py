import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("OGEMOS")
mainframe = ttk.Frame(root)
mainframe.grid(row=0, column=0)


def run_gui(frame):
    def show_entreprise_set_up(frame_entreprise):
        def get_information_entreprise():
            global nom_entreprise
            nom_entreprise = nom_entreprise_entry.get()
            global nombre_de_champs
            nombre_de_champs = int(nombre_de_champs_entry.get())

            for widget in frame_entreprise.winfo_children():
                widget.destroy()
            show_creation_champs(frame)

        nom_entreprise_label = ttk.Label(frame_entreprise, text="Nom de l'entreprise: ")
        nom_entreprise_entry = ttk.Entry(frame_entreprise)
        nombre_de_champs_label = ttk.Label(frame_entreprise, text="Nombre de champs: ")
        nombre_de_champs_entry = ttk.Entry(frame_entreprise)
        nombre_de_champs_entry.insert(0, "1")

        nom_entreprise_label.grid(row=0, column=0)
        nom_entreprise_entry.grid(row=0, column=1)
        nombre_de_champs_label.grid(row=1, column=0)
        nombre_de_champs_entry.grid(row=1, column=1)

        creer_bouton = ttk.Button(frame_entreprise, command=get_information_entreprise)
        creer_bouton.grid(columnspan=2, row=2, column=0)

    def show_creation_champs(frame_champs_list):
        def get_information_champs(scrollable_frame):
            global information_champs
            information_champs = []
            for scrollable_frame_widget in scrollable_frame.winfo_children():
                if isinstance(scrollable_frame_widget, ttk.LabelFrame):
                    grid_slave0_1 = scrollable_frame_widget.grid_slaves(row=0, column=1)
                    for entry in grid_slave0_1:
                        nom_du_champs = entry.get()
                    grid_slave1_1 = scrollable_frame_widget.grid_slaves(row=1, column=1)
                    for entry in grid_slave1_1:
                        nombre_de_zone_de_gestion = entry.get()
                    information_champs.append({"nom_du_champs": nom_du_champs,
                                               "nombre_de_zone_de_gestion": nombre_de_zone_de_gestion,
                                               "information_zone_de_gestion": []})

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

        creation_champs_bouton = ttk.Button(scrollable_frame, command=lambda: get_information_champs(scrollable_frame))
        creation_champs_bouton.pack()

    def show_creation_zone_de_gestion(zone_de_gestion_mainframe):
        def get_information_zone_de_gestion(scrollable_frame):
            index = 0
            for scrollable_frame_widget in scrollable_frame.winfo_children():
                if isinstance(scrollable_frame_widget, ttk.LabelFrame):
                    for champs_frame_widget in scrollable_frame_widget.winfo_children():
                        if isinstance(champs_frame_widget, ttk.LabelFrame):
                            grid_slave0_1 = champs_frame_widget.grid_slaves(row=0, column=1)
                            for entry in grid_slave0_1:
                                taux_matiere_organique = entry.get()
                            grid_slave1_1 = champs_frame_widget.grid_slaves(row=1, column=1)
                            for entry in grid_slave1_1:
                                municipalite = entry.get()
                            grid_slave2_1 = champs_frame_widget.grid_slaves(row=2, column=1)
                            for entry in grid_slave2_1:
                                serie_de_sol = entry.get()
                            grid_slave3_1 = champs_frame_widget.grid_slaves(row=3, column=1)
                            for entry in grid_slave3_1:
                                classe_de_drainage = entry.get()
                            grid_slave4_1 = champs_frame_widget.grid_slaves(row=4, column=1)
                            for entry in grid_slave4_1:
                                masse_volumique_apparente = entry.get()
                            grid_slave5_1 = champs_frame_widget.grid_slaves(row=5, column=1)
                            for entry in grid_slave5_1:
                                profondeur = entry.get()
                            grid_slave6_1 = champs_frame_widget.grid_slaves(row=6, column=1)
                            for entry in grid_slave6_1:
                                superficie_de_la_zone = entry.get()
                            global information_champs
                            information_champs[index]["information_zone_de_gestion"].append(
                                {"taux_matiere_organique": taux_matiere_organique,
                                 "municipalite": municipalite,
                                 "serie_de_sol": serie_de_sol,
                                 "classe_de_drainage": classe_de_drainage,
                                 "masse_volumique_apparente": masse_volumique_apparente,
                                 "profondeur": profondeur,
                                 "superficie_de_la_zone": superficie_de_la_zone})
                index += 1

            for widget in zone_de_gestion_mainframe.winfo_children():
                widget.destroy()

            show_creation_des_regies(zone_de_gestion_mainframe)

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

        creation_zone_de_gestion_bouton = ttk.Button(scrollable_frame,
                                                     command=lambda: get_information_zone_de_gestion(scrollable_frame))
        creation_zone_de_gestion_bouton.pack()

    def show_creation_des_regies(parent_frame_tabs):
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
                        tab = ttk.Frame(simulation_notebook)
                        simulation_notebook.add(tab, text="+")
                        global nombre_simulations
                        nombre_simulations -= 1
                        duree_simulation_window.destroy()

                    def get_duree_de_la_simulation():
                        annee_historique_initiale = annee_historique_initiale_entry.get()
                        annee_historique_finale = annee_historique_finale_entry.get()
                        annee_projection_initiale = annee_projection_initiale_entry.get()
                        annee_projection_finale = annee_projection_finale_entry.get()

                        global duree_simulation
                        duree_simulation.append({"annee_historique_initiale": annee_historique_initiale,
                                                 "annee_historique_finale": annee_historique_finale,
                                                 "annee_projection_initiale": annee_projection_initiale,
                                                 "annee_projection_finale": annee_projection_finale})

                        duree_simulation_window.destroy()
                        set_up_simulation(simulation_notebook)

                    duree_simulation_window = tk.Toplevel()
                    duree_simulation_window.protocol("WM_DELETE_WINDOW", readd_simulation)
                    duree_simulation_frame = ttk.Frame(duree_simulation_window)
                    annee_historique_initiale_label = ttk.Label(duree_simulation_frame,
                                                                text="Année historique initiale: ")
                    annee_historique_initiale_entry = ttk.Entry(duree_simulation_frame)
                    annee_historique_finale_label = ttk.Label(duree_simulation_frame, text="Année historique finale: ")
                    annee_historique_finale_entry = ttk.Entry(duree_simulation_frame)
                    annee_projection_initiale_label = ttk.Label(duree_simulation_frame,
                                                                text="Année de projection initiale: ")
                    annee_projection_initiale_entry = ttk.Entry(duree_simulation_frame)
                    annee_projection_finale_label = ttk.Label(duree_simulation_frame,
                                                              text="Année de projection finale: ")
                    annee_projection_finale_entry = ttk.Entry(duree_simulation_frame)

                    annee_historique_initiale_label.grid(row=0, column=0)
                    annee_historique_initiale_entry.grid(row=0, column=1)
                    annee_historique_finale_label.grid(row=1, column=0)
                    annee_historique_finale_entry.grid(row=1, column=1)
                    annee_projection_initiale_label.grid(row=2, column=0)
                    annee_projection_initiale_entry.grid(row=2, column=1)
                    annee_projection_finale_label.grid(row=3, column=0)
                    annee_projection_finale_entry.grid(row=3, column=1)

                    creer_simulation_bouton = ttk.Button(duree_simulation_frame,
                                                         command= get_duree_de_la_simulation)
                    creer_simulation_bouton.grid(row=4, column=0, columnspan=2)
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
                    nombre_de_champs += 1
                    set_up_new_champs()

            def delete_champs_tab(event):
                clicked_tab = champs_notebook.tk.call(champs_notebook._w, "identify", "tab", event.x, event.y)
                index_clicked_tab = champs_notebook.index(clicked_tab)
                if index_clicked_tab != champs_notebook.index("end") - 1:
                    global information_champs
                    information_champs.pop(index_clicked_tab)
                    global nombre_de_champs
                    nombre_de_champs -= 1
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
                simulation_index = len(duree_simulation)-1
                set_up_champs(zone_de_gestion_notebook, int(champs["nombre_de_zone_de_gestion"]), champs_notebook, simulation_index)

            tab = ttk.Frame(champs_notebook)
            champs_notebook.add(tab, text="+")

            champs_notebook.pack()

        def set_up_new_champs():
            new_champs_window = tk.Toplevel()

            def creation_des_zone_de_gestion_du_nouveau_champs():
                nom_du_champs = nom_du_champs_entry.get()
                nombre_de_zone_de_gestion = nombre_de_zone_de_gestion_entry.get()
                global information_champs
                information_champs.append({"nom_du_champs": nom_du_champs,
                                           "nombre_de_zone_de_gestion": nombre_de_zone_de_gestion,
                                           "information_zone_de_gestion": []})
                global nombre_de_champs
                nombre_de_champs += 1
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

                creation_zone_de_gestion_bouton = ttk.Button(scrollable_frame,
                                                             command=lambda: add_new_zone_tab())
                creation_zone_de_gestion_bouton.pack()
                canvas.pack(side="left", fill="x", expand=True)
                scrollbar.pack(side="right", fill="y")
                creation_zone_frame.pack()

                def add_new_zone_tab():
                    for scrollable_frame_widget in scrollable_frame.winfo_children():
                        if isinstance(scrollable_frame_widget, ttk.LabelFrame):
                            grid_slave0_1 = scrollable_frame_widget.grid_slaves(row=0, column=1)
                            for entry in grid_slave0_1:
                                taux_matiere_organique = entry.get()
                            grid_slave1_1 = scrollable_frame_widget.grid_slaves(row=1, column=1)
                            for entry in grid_slave1_1:
                                municipalite = entry.get()
                            grid_slave2_1 = scrollable_frame_widget.grid_slaves(row=2, column=1)
                            for entry in grid_slave2_1:
                                serie_de_sol = entry.get()
                            grid_slave3_1 = scrollable_frame_widget.grid_slaves(row=3, column=1)
                            for entry in grid_slave3_1:
                                classe_de_drainage = entry.get()
                            grid_slave4_1 = scrollable_frame_widget.grid_slaves(row=4, column=1)
                            for entry in grid_slave4_1:
                                masse_volumique_apparente = entry.get()
                            grid_slave5_1 = scrollable_frame_widget.grid_slaves(row=5, column=1)
                            for entry in grid_slave5_1:
                                profondeur = entry.get()
                            grid_slave6_1 = scrollable_frame_widget.grid_slaves(row=6, column=1)
                            for entry in grid_slave6_1:
                                superficie_de_la_zone = entry.get()
                            global information_champs
                            information_champs[len(information_champs) - 1]["information_zone_de_gestion"].append(
                                {"taux_matiere_organique": taux_matiere_organique,
                                 "municipalite": municipalite,
                                 "serie_de_sol": serie_de_sol,
                                 "classe_de_drainage": classe_de_drainage,
                                 "masse_volumique_apparente": masse_volumique_apparente,
                                 "profondeur": profondeur,
                                 "superficie_de_la_zone": superficie_de_la_zone})
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
                            set_up_champs(zone_notebook, nombre_de_zone_de_gestion, notebook, simulation_notebook.index(simulation_frame))
                            new_tab = ttk.Frame(notebook)
                            notebook.add(new_tab, text="+")

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
            creer_nouveau_champs_bouton = ttk.Button(nouveau_champs_frame,
                                                     command=creation_des_zone_de_gestion_du_nouveau_champs)
            creer_nouveau_champs_bouton.grid(row=3, column=0, columnspan=2)
            nouveau_champs_frame.pack()

        def set_up_champs(zone_notebook, nombre_de_zone, champs_notebook, simulation_index):

            def add_new_zone_de_gestion_tab(event):
                clicked_tab = zone_notebook.tk.call(zone_notebook._w, "identify", "tab", event.x, event.y)
                if clicked_tab == zone_notebook.index("end") - 1:
                    champs_index = champs_notebook.index("current")
                    global information_champs
                    information_champs[champs_index]["nombre_de_zone_de_gestion"] = str(
                        int(information_champs[champs_index]["nombre_de_zone_de_gestion"]) + 1)
                    set_up_new_zone_de_gestion(champs_index, simulation_index)

            def delete_zone_de_gestion_tab(event):
                clicked_tab = zone_notebook.tk.call(zone_notebook._w, "identify", "tab", event.x, event.y)
                index_clicked_tab = zone_notebook.index(clicked_tab)
                if index_clicked_tab != zone_notebook.index("end") - 1:
                    champs_index = champs_notebook.index("current")
                    global information_champs
                    information_champs[champs_index]["nombre_de_zone_de_gestion"] = str(
                        int(information_champs[champs_index]["nombre_de_zone_de_gestion"]) - 1)
                    information_champs[champs_index]["information_zone_de_gestion"].pop(index_clicked_tab)
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

            def set_up_new_zone_de_gestion(champs_index, simulation_index):
                new_zone_window = tk.Toplevel()
                creation_zone_frame = ttk.Frame(new_zone_window)
                canvas = tk.Canvas(creation_zone_frame)
                scrollbar = ttk.Scrollbar(creation_zone_frame, orient="vertical", command=canvas.yview)
                scrollable_frame = ttk.Frame(canvas)
                scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
                canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
                canvas.configure(yscrollcommand=scrollbar.set)
                global information_champs
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

                creation_zone_de_gestion_bouton = ttk.Button(scrollable_frame,
                                                             command=lambda: add_new_tab())
                creation_zone_de_gestion_bouton.pack()
                canvas.pack(side="left", fill="x", expand=True)
                scrollbar.pack(side="right", fill="y")
                creation_zone_frame.pack()

                def add_new_tab():
                    index = 0
                    for scrollable_frame_widget in scrollable_frame.winfo_children():
                        if isinstance(scrollable_frame_widget, ttk.LabelFrame):
                            grid_slave0_1 = scrollable_frame_widget.grid_slaves(row=0, column=1)
                            for entry in grid_slave0_1:
                                taux_matiere_organique = entry.get()
                            grid_slave1_1 = scrollable_frame_widget.grid_slaves(row=1, column=1)
                            for entry in grid_slave1_1:
                                municipalite = entry.get()
                            grid_slave2_1 = scrollable_frame_widget.grid_slaves(row=2, column=1)
                            for entry in grid_slave2_1:
                                serie_de_sol = entry.get()
                            grid_slave3_1 = scrollable_frame_widget.grid_slaves(row=3, column=1)
                            for entry in grid_slave3_1:
                                classe_de_drainage = entry.get()
                            grid_slave4_1 = scrollable_frame_widget.grid_slaves(row=4, column=1)
                            for entry in grid_slave4_1:
                                masse_volumique_apparente = entry.get()
                            grid_slave5_1 = scrollable_frame_widget.grid_slaves(row=5, column=1)
                            for entry in grid_slave5_1:
                                profondeur = entry.get()
                            grid_slave6_1 = scrollable_frame_widget.grid_slaves(row=6, column=1)
                            for entry in grid_slave6_1:
                                superficie_de_la_zone = entry.get()
                            global information_champs
                            information_champs[index]["information_zone_de_gestion"].append(
                                {"taux_matiere_organique": taux_matiere_organique,
                                 "municipalite": municipalite,
                                 "serie_de_sol": serie_de_sol,
                                 "classe_de_drainage": classe_de_drainage,
                                 "masse_volumique_apparente": masse_volumique_apparente,
                                 "profondeur": profondeur,
                                 "superficie_de_la_zone": superficie_de_la_zone})
                        index += 1

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
                            set_up_regies(tab, index)

                            new_zone_tab = ttk.Frame(champs_courant_zone_notebook)
                            champs_courant_zone_notebook.add(new_zone_tab, text="+")
                        index += 1

            zone_notebook.bind("<Button-1>", add_new_zone_de_gestion_tab)
            zone_notebook.bind("<Button-3>", delete_zone_de_gestion_tab)

            global duree_simulation
            for zone in range(int(nombre_de_zone)):
                zone_tab = ttk.Frame(zone_notebook)
                zone_notebook.add(zone_tab, text="Zone de gestion " + str(zone + 1))
                set_up_regies(zone_tab, simulation_index)

            new_tab = ttk.Frame(zone_notebook)
            zone_notebook.add(new_tab, text="+")
            zone_notebook.pack()

        def set_up_regies(zone_tab, index):
            historique_frame = ttk.LabelFrame(zone_tab, text="Régies historiques")
            canvas_historique = tk.Canvas(historique_frame)
            scrollbar_historique = ttk.Scrollbar(historique_frame, orient="vertical",
                                                 command=canvas_historique.yview)
            scrollable_frame_historique = ttk.Frame(canvas_historique)
            scrollable_frame_historique.bind("<Configure>", lambda e: canvas_historique.configure(
                scrollregion=canvas_historique.bbox("all")))
            add_regies_historiques(scrollable_frame_historique, index)
            canvas_historique.create_window((0, 0), window=scrollable_frame_historique, anchor="nw")
            canvas_historique.configure(yscrollcommand=scrollbar_historique.set)
            canvas_historique.pack(side="left", fill="both", expand=True)
            scrollbar_historique.pack(side="right", fill="y")
            historique_frame.grid(row=0, column=0)
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
            projection_frame.grid(row=1, column=0)

        def add_regies_historiques(scrollable_frame, index):
            global duree_simulation
            annee_historique_initiale = int(duree_simulation[index]["annee_historique_initiale"])
            annee_historique_finale = int(duree_simulation[index]["annee_historique_finale"])
            annee_courante = annee_historique_initiale
            while annee_courante <= annee_historique_finale:
                annee_courante_frame = ttk.LabelFrame(scrollable_frame, text=str(annee_courante))
                culture_principale_label = ttk.Label(annee_courante_frame, text="Culture principale: ")
                culture_principale_combobox = ttk.Combobox(annee_courante_frame)
                rendement_label = ttk.Label(annee_courante_frame, text="Rendement: ")
                rendement_entry = ttk.Entry(annee_courante_frame)
                proportion_tige_exporte_label = ttk.Label(annee_courante_frame, text="Proportion tige exporté: ")
                proportion_tige_exporte_entry = ttk.Entry(annee_courante_frame)
                production_non_recolte_label = ttk.Label(annee_courante_frame, text="Production non récoltée: ")
                production_non_recolte_combobox = ttk.Combobox(annee_courante_frame)
                taux_matiere_seche_label = ttk.Label(annee_courante_frame, text="Taux de matière sèche: ")
                taux_matiere_seche_entry = ttk.Entry(annee_courante_frame)
                travail_du_sol_label = ttk.Label(annee_courante_frame, text="Travail du sol: ")
                travail_du_sol_combobox = ttk.Combobox(annee_courante_frame)
                profondeur_maximale_label = ttk.Label(annee_courante_frame, text="Profondeur maxiamle: ")
                profondeur_maximale_entry = ttk.Entry(annee_courante_frame)
                culture_secondaire_label = ttk.Label(annee_courante_frame, text="Culture secondaire: ")
                culture_secondaire_combobox = ttk.Combobox(annee_courante_frame)
                rendement_culture_secondaire_label = ttk.Label(annee_courante_frame, text="Rendement culture secondaire: ")
                rendement_culture_secondaire_entry = ttk.Entry(annee_courante_frame)

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

                annee_courante += 1
                annee_courante_frame.pack()

        simulation_notebook.bind("<Button-1>", add_new_simulation_tab)
        simulation_notebook.bind("<Button-3>", delete_simulation_tab)

        simulation_notebook.add(tab1, text="+")

        simulation_notebook.pack(expand=1, fill="both")

    show_entreprise_set_up(frame)


run_gui(mainframe)

root.mainloop()
