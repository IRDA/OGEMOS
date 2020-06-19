import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("OGEMOS")

mainframe = ttk.Frame(root)

nom_entreprise_label = ttk.Label(mainframe, text="Nom de l'entreprise: ")
nom_entreprise_entry = ttk.Entry(mainframe)
nombre_de_champs_label = ttk.Label(mainframe, text="Nombre de champs: ")
default_value = tk.IntVar()
nombre_de_champs_entry = ttk.Entry(mainframe, text=default_value)
default_value.set(1)

nom_entreprise_label.grid(row=0, column=0)
nom_entreprise_entry.grid(row=0, column=1)
nombre_de_champs_label.grid(row=1, column=0)
nombre_de_champs_entry.grid(row=1, column=1)

mainframe.grid(row=0, column=0)


def set_up_simulation_ui(tab):
    container_frame = ttk.Frame(tab)
    champs_tab_parent = ttk.Notebook(container_frame)
    global nombre_de_champs
    for index_champs in range(int(nombre_de_champs) + 1):
        tab_champs = ttk.Frame(champs_tab_parent)
        if index_champs == int(nombre_de_champs):
            champs_tab_parent.add(tab_champs, text="+")

            def add_new_champs_tab_click(event):
                clicked_tab = champs_tab_parent.tk.call(champs_tab_parent._w, "identify", "tab", event.x,
                                                        event.y)

                def creation_zone_de_gestion_new_champs_tab():
                    nom_du_champs = nom_du_champs_entry.get()
                    nombre_de_zone_de_gestion = nombre_de_zone_de_gestion_entry.get()
                    global information_champs
                    information_champs.append({"nom_du_champs": nom_du_champs,
                                               "nombre_de_zone_de_gestion": nombre_de_zone_de_gestion})
                    global nombre_de_champs
                    nombre_de_champs += 1
                    for widget in fenetre_nouveau_champs.winfo_children():
                        widget.destroy()
                    creation_zone_frame = ttk.Frame(fenetre_nouveau_champs)
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
                                                                 command=lambda: add_new_tab())
                    creation_zone_de_gestion_bouton.pack()
                    canvas.pack(side="left", fill="x", expand=True)
                    scrollbar.pack(side="right", fill="y")
                    creation_zone_frame.pack()

                    def add_new_tab():
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
                                        global information_zone_de_gestion
                                        information_zone_de_gestion.append(
                                            {"taux_matiere_organique": taux_matiere_organique,
                                             "municipalite": municipalite,
                                             "serie_de_sol": serie_de_sol,
                                             "classe_de_drainage": classe_de_drainage,
                                             "masse_volumique_apparente": masse_volumique_apparente,
                                             "profondeur": profondeur,
                                             "superficie_de_la_zone": superficie_de_la_zone})
                        fenetre_nouveau_champs.destroy()
                        tab = ttk.Frame(champs_tab_parent)
                        champs_tab_parent.add(tab, text=nom_du_champs)
                        zone_de_gestion_parent = ttk.Notebook(tab)
                        for index_zone in range(int(nombre_de_zone_de_gestion) + 1):
                            tab_zone_de_gestion = ttk.Frame(zone_de_gestion_parent)
                            if index_zone == int(nombre_de_zone_de_gestion):
                                zone_de_gestion_parent.add(tab_zone_de_gestion, text="+")

                                def add_new_zone_de_gestion_tab(event):
                                    clicked_tab = zone_de_gestion_parent.tk.call(zone_de_gestion_parent._w, "identify",
                                                                                 "tab",
                                                                                 event.x, event.y)
                                    if clicked_tab == zone_de_gestion_parent.index("end") - 1:
                                        zone_de_gestion_parent.forget(clicked_tab)
                                        tab = ttk.Frame(zone_de_gestion_parent)
                                        zone_de_gestion_parent.add(tab,
                                                                   text="Zone de gestion " + str(
                                                                       zone_de_gestion_parent.index("end") + 1))
                                        new_tab = ttk.Frame(zone_de_gestion_parent)
                                        zone_de_gestion_parent.add(new_tab, text="+")

                                def delete_zone_de_gestion_tab(event):
                                    clicked_tab = zone_de_gestion_parent.tk.call(zone_de_gestion_parent._w, "identify", "tab",
                                                                          event.x, event.y)
                                    index_clicked_tab = zone_de_gestion_parent.index(clicked_tab)
                                    if index_clicked_tab != zone_de_gestion_parent.index("end") - 1:
                                        zone_de_gestion_parent.forget(index_clicked_tab)
                                        current_index = index_clicked_tab
                                        while current_index < zone_de_gestion_parent.index("end"):
                                            zone_de_gestion_parent.tab(current_index,
                                                                text="Simulation " + str(current_index + 1))
                                            if current_index == zone_de_gestion_parent.index("end") - 1:
                                                zone_de_gestion_parent.tab(current_index, text="+")
                                            current_index += 1

                                zone_de_gestion_parent.bind("<Button-1>", add_new_zone_de_gestion_tab)
                                zone_de_gestion_parent.bind("<Button-3>", delete_zone_de_gestion_tab)
                            else:
                                zone_de_gestion_parent.add(tab_zone_de_gestion,
                                                           text="Zone de gestion " + str(index_zone + 1))
                                historique_frame = ttk.LabelFrame(tab_zone_de_gestion, text="Régies historiques")
                                canvas_historique = tk.Canvas(historique_frame)
                                scrollbar_historique = ttk.Scrollbar(historique_frame, orient="vertical",
                                                                     command=canvas_historique.yview)
                                scrollable_frame_historique = ttk.Frame(canvas_historique)
                                scrollable_frame_historique.bind("<Configure>", lambda e: canvas_historique.configure(
                                    scrollregion=canvas_historique.bbox("all")))
                                canvas_historique.create_window((0, 0), window=scrollable_frame_historique, anchor="nw")
                                canvas_historique.configure(yscrollcommand=scrollbar_historique.set)
                                canvas_historique.pack(side="left", fill="both", expand=True)
                                scrollbar_historique.pack(side="right", fill="y")
                                historique_frame.grid(row=0, column=0)
                                projection_frame = ttk.LabelFrame(tab_zone_de_gestion, text="Régies de la projection")
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
                        zone_de_gestion_parent.grid(row=0, column=0)
                        new_tab = ttk.Frame(champs_tab_parent)
                        champs_tab_parent.add(new_tab, text="+")

                def add_tab_readd():
                    new_tab = ttk.Frame(champs_tab_parent)
                    champs_tab_parent.add(new_tab, text="+")
                    fenetre_nouveau_champs.destroy()

                if clicked_tab == champs_tab_parent.index("end") - 1:
                    champs_tab_parent.forget(clicked_tab)
                    fenetre_nouveau_champs = tk.Toplevel()
                    fenetre_nouveau_champs.protocol('WM_DELETE_WINDOW', add_tab_readd)
                    nouveau_champs_frame = ttk.Frame(fenetre_nouveau_champs)
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
                                                             command=creation_zone_de_gestion_new_champs_tab)
                    creer_nouveau_champs_bouton.grid(row=3, column=0, columnspan=2)
                    nouveau_champs_frame.pack()

            def delete_champs_tab(event):
                clicked_tab = champs_tab_parent.tk.call(champs_tab_parent._w, "identify", "tab", event.x,
                                                        event.y)
                index_clicked_tab = champs_tab_parent.index(clicked_tab)
                if index_clicked_tab != champs_tab_parent.index("end") - 1:
                    champs_tab_parent.forget(index_clicked_tab)
                    current_index = index_clicked_tab
                    while current_index < champs_tab_parent.index("end"):
                        champs_tab_parent.tab(current_index, text=information_champs[nombre_de_champs-1]["nom_du_champs"])
                        if current_index == champs_tab_parent.index("end") - 1:
                            champs_tab_parent.tab(current_index, text="+")
                        current_index += 1

            champs_tab_parent.bind("<Button-1>", add_new_champs_tab_click)
            champs_tab_parent.bind("<Button-3>", delete_champs_tab)
        else:
            zone_tab_parent = ttk.Notebook(tab_champs)
            for index_zone_de_gestion in range(int(information_champs[index_champs]["nombre_de_zone_de_gestion"]) + 1):
                tab_zone = ttk.Frame(zone_tab_parent)
                if index_zone_de_gestion == int(information_champs[index_champs]["nombre_de_zone_de_gestion"]):
                    zone_tab_parent.add(tab_zone, text="+")

                    def add_new_zone_tab(event):
                        clicked_tab = zone_tab_parent.tk.call(zone_tab_parent._w, "identify", "tab",
                                                              event.x, event.y)
                        if clicked_tab == zone_tab_parent.index("end") - 1:
                            zone_tab_parent.forget(clicked_tab)
                            tab = ttk.Frame(zone_tab_parent)
                            zone_tab_parent.add(tab,
                                                text="Zone de gestion " + str(zone_tab_parent.index("end") + 1))
                            new_tab = ttk.Frame(zone_tab_parent)
                            zone_tab_parent.add(new_tab, text="+")

                    def delete_zone_tab(event):
                        clicked_tab = zone_tab_parent.tk.call(zone_tab_parent._w, "identify", "tab",
                                                              event.x, event.y)
                        index_clicked_tab = zone_tab_parent.index(clicked_tab)
                        if index_clicked_tab != zone_tab_parent.index("end") - 1:
                            zone_tab_parent.forget(index_clicked_tab)
                            current_index = index_clicked_tab
                            while current_index < zone_tab_parent.index("end"):
                                zone_tab_parent.tab(current_index, text="Simulation " + str(current_index + 1))
                                if current_index == zone_tab_parent.index("end") - 1:
                                    zone_tab_parent.tab(current_index, text="+")
                                current_index += 1

                    zone_tab_parent.bind("<Button-1>", add_new_zone_tab)
                    zone_tab_parent.bind("<Button-3>", delete_zone_tab)
                else:
                    zone_tab_parent.add(tab_zone, text="Zone de gestion " + str(index_zone_de_gestion + 1))
                    historique_frame = ttk.LabelFrame(tab_zone, text="Régies historiques")
                    canvas_historique = tk.Canvas(historique_frame)
                    scrollbar_historique = ttk.Scrollbar(historique_frame, orient="vertical",
                                                         command=canvas_historique.yview)
                    scrollable_frame_historique = ttk.Frame(canvas_historique)
                    scrollable_frame_historique.bind("<Configure>", lambda e: canvas_historique.configure(
                        scrollregion=canvas_historique.bbox("all")))
                    canvas_historique.create_window((0, 0), window=scrollable_frame_historique, anchor="nw")
                    canvas_historique.configure(yscrollcommand=scrollbar_historique.set)
                    canvas_historique.pack(side="left", fill="both", expand=True)
                    scrollbar_historique.pack(side="right", fill="y")
                    historique_frame.grid(row=0, column=0)
                    projection_frame = ttk.LabelFrame(tab_zone, text="Régies de la projection")
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
            champs_tab_parent.add(tab_champs, text=information_champs[index_champs]["nom_du_champs"])

            zone_tab_parent.pack()

    champs_tab_parent.pack()

    container_frame.grid(row=0, column=0)


def get_information_entreprise():
    global nom_entreprise
    nom_entreprise = nom_entreprise_entry.get()
    global nombre_de_champs
    nombre_de_champs = int(nombre_de_champs_entry.get())

    for widget in mainframe.winfo_children():
        widget.destroy()

    show_creation_champs()


def show_creation_des_regies():
    simulation_tab_parent = ttk.Notebook(mainframe)

    tab1 = ttk.Frame(simulation_tab_parent)

    def add_new_simulation_tab(event):
        clicked_tab = simulation_tab_parent.tk.call(simulation_tab_parent._w, "identify", "tab", event.x, event.y)
        if clicked_tab == simulation_tab_parent.index("end") - 1:
            simulation_tab_parent.forget(clicked_tab)
            tab = ttk.Frame(simulation_tab_parent)
            simulation_tab_parent.add(tab, text="Simulation " + str(simulation_tab_parent.index("end") + 1))
            set_up_simulation_ui(tab)
            new_tab = ttk.Frame(simulation_tab_parent)
            simulation_tab_parent.add(new_tab, text="+")

    def delete_simulation_tab(event):
        clicked_tab = simulation_tab_parent.tk.call(simulation_tab_parent._w, "identify", "tab", event.x, event.y)
        index_clicked_tab = simulation_tab_parent.index(clicked_tab)
        if index_clicked_tab != simulation_tab_parent.index("end") - 1:
            simulation_tab_parent.forget(index_clicked_tab)
            current_index = index_clicked_tab
            while current_index < simulation_tab_parent.index("end"):
                simulation_tab_parent.tab(current_index, text="Simulation " + str(current_index + 1))
                if current_index == simulation_tab_parent.index("end") - 1:
                    simulation_tab_parent.tab(current_index, text="+")
                current_index += 1

    simulation_tab_parent.bind("<Button-1>", add_new_simulation_tab)
    simulation_tab_parent.bind("<Button-3>", delete_simulation_tab)

    simulation_tab_parent.add(tab1, text="+")

    simulation_tab_parent.pack(expand=1, fill="both")


def get_information_zone_de_gestion(scrollable_frame):
    global information_zone_de_gestion
    information_zone_de_gestion = []
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
                    information_zone_de_gestion.append({"taux_matiere_organique": taux_matiere_organique,
                                                        "municipalite": municipalite,
                                                        "serie_de_sol": serie_de_sol,
                                                        "classe_de_drainage": classe_de_drainage,
                                                        "masse_volumique_apparente": masse_volumique_apparente,
                                                        "profondeur": profondeur,
                                                        "superficie_de_la_zone": superficie_de_la_zone})

    for widget in mainframe.winfo_children():
        widget.destroy()

    show_creation_des_regies()


def show_creation_zone_de_gestion():
    canvas = tk.Canvas(mainframe)
    scrollbar = ttk.Scrollbar(mainframe, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)
    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    for index_champs in range(int(nombre_de_champs)):
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
                                       "nombre_de_zone_de_gestion": nombre_de_zone_de_gestion})

    for widget in mainframe.winfo_children():
        widget.destroy()

    show_creation_zone_de_gestion()


def show_creation_champs():
    canvas = tk.Canvas(mainframe)
    scrollbar = ttk.Scrollbar(mainframe, orient="vertical", command=canvas.yview)
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
        nom_du_champs_label.grid(row=0, column=0)
        nom_du_champs_entry.grid(row=0, column=1)
        nombre_de_zone_de_gestion_label.grid(row=1, column=0)
        nombre_de_zone_de_gestion_entry.grid(row=1, column=1)

        champs_frame.pack(fill="both")

    canvas.pack(side="left", fill="x", expand=True)
    scrollbar.pack(side="right", fill="y")

    creation_champs_bouton = ttk.Button(scrollable_frame, command=lambda: get_information_champs(scrollable_frame))
    creation_champs_bouton.pack()


creer_bouton = ttk.Button(mainframe, command=get_information_entreprise)
creer_bouton.grid(columnspan=2, row=2, column=0)

root.mainloop()
