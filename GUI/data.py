from    matplotlib.backends.backend_tkagg   import  FigureCanvasTkAgg
from    tkinter                             import  ttk
import  tkinter                             as      tk
import  matplotlib                          as      mpl

class Data(ttk.Frame) :
    """
    Frame Class, that contains database controll for hrs.
    @Inherits: ttk.Frame
    """
    def __init__(self, parent, root, *args, **kwargs) -> None:
        """
        Constructor Method of the Data Frame Class.
        """
        super().__init__(parent, *args, **kwargs)
        
        self.root = root
        self.parent = parent

        self.style = self.root.style

        self.COLOR_PALETTES = self.root.COLOR_PALETTES

        self.style.configure("DATA_InnerContainer.TFrame", background=self.COLOR_PALETTES["INNER_BACKGROUND"])
        self.style.configure("DATA_InInnerContainer.TFrame", background=self.COLOR_PALETTES["INNER_BACKGROUND"])
        self.style.configure("DATA_Headings.TLabel", font=("Seoge UI", 25, "bold"), foreground=self.COLOR_PALETTES["FILLER3"], background=self.COLOR_PALETTES["INNER_BACKGROUND"], border=1, borderwidth=5, anchor="center")

        self.style.configure("DATA.Treeview", background=self.COLOR_PALETTES["MIDDLE_BACKGROUND"], foreground="white", fieldbackground=self.COLOR_PALETTES["MIDDLE_BACKGROUND"], font=("Seoge UI", 16), rowheight=26)

        self.style.configure("DATA_SelectionCombobox.TCombobox", 
            fieldbackground=self.COLOR_PALETTES["MIDDLE_BACKGROUND"],
        )

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.container = ttk.Frame(self, style="DATA_InnerContainer.TFrame")
        self.container.grid(row=0, column=0, sticky="nsew")

        # Load containers
        self.container.rowconfigure((0,1), weight=1)
        self.container.columnconfigure((0,1), weight=1)

        self.employee_selection_frame = ttk.Frame(self.container, style="DATA_InnerContainer.TFrame")
        self.employee_selection_frame.grid(row=0, column=0, sticky="nsew", padx=15, pady=15)

        self.employee_stats_frame = ttk.Frame(self.container, style="DATA_InnerContainer.TFrame")
        self.employee_stats_frame.grid(row=1, column=0, sticky="nsew", padx=15, pady=15)

        self.employee_performance_graph_frame = ttk.Frame(self.container, style="DATA_InnerContainer.TFrame")
        self.employee_performance_graph_frame.grid(row=0, column=1, rowspan=2, columnspan=2, sticky="nsew", padx=15, pady=15)

        self.available_employees = self.root.db_session.query(self.root.Employee).filter_by(hr_id = self.root.current_user.id).all()
        self.current_employee = None
        self.current_employee_name = tk.StringVar()

        # Initialize By Employee Selection
        self._employee_selection()

    def _employee_selection(self) -> None:
        """
        Private Class Method, that creates the employee selection frame.
        @Params:
            None
        @Returns:
            None
        """
        self.employee_selection_frame.rowconfigure((0,1), weight=1)
        self.employee_selection_frame.columnconfigure(0, weight=1)

        self.employee_selection_label = ttk.Label(self.employee_selection_frame, text="Çalışan Seçimi", style="DATA_Headings.TLabel")
        self.employee_selection_label.grid(row=0, column=0, sticky="nsew", pady=15)

        self.employee_selection_combobox = ttk.Combobox(self.employee_selection_frame, values=[employee.name+" "+employee.surname for employee in self.available_employees], textvariable=self.current_employee_name, state="normal", justify="center", validate="none", background=self.COLOR_PALETTES["MIDDLE_BACKGROUND"], foreground="white", style="DATA_SelectionCombobox.TCombobox", font=("Seoge UI", 18, "bold"), cursor="hand2")
        self.employee_selection_combobox.grid(row=1, column=0, sticky="nsew")

        # Bind the combobox to the on_employee_select method
        self.employee_selection_combobox.bind("<<ComboboxSelected>>", self._on_employee_select)

    def _on_employee_select(self, *event) -> None:
        """
        Private Class Method, that is called when the employee is selected.
        @Params:
            *event: Event : Optional : Event that is triggered.
        @Returns:
            None
        """
        # Load current employee credentials
        self.current_employee = self.available_employees[self.employee_selection_combobox.current()]
        self.current_employe_reports = self.root.db_session.query(self.root.DailyReport).filter_by(employee_id=self.current_employee.id).all()
        self.current_employee_name.set(self.current_employee.name+" "+self.current_employee.surname)
        # Initialize Employee Stats
        self._employee_stats()
        # Initialize Employee Graph
        self._employe_graph()

        self.root._set_min_size()

    def _employee_stats(self) -> None:
        """
        Private Class Method, that creates the employee stats frame.
        @Params:
            None
        @Returns:
            None
        """
        self.employee_stats_label = ttk.Label(self.employee_stats_frame, text="Çalışan İstatistikleri", style="DATA_Headings.TLabel")
        self.employee_stats_label.grid(row=0, column=0, sticky="nsew", pady=15)

        self.employee_stats_treeview = ttk.Treeview(self.employee_stats_frame, columns=("Tarih", "Düzgün Duruş Süresi", "Bozuk Duruş Süresi"), height=12, style="DATA.Treeview")
        self.employee_stats_treeview.grid(row=1, column=0, sticky="nsew")

        self.vertical_scrollbar = ttk.Scrollbar(self.employee_stats_frame, orient="vertical", command=self.employee_stats_treeview.yview)
        self.vertical_scrollbar.grid(row=1, column=1, sticky="ns")

        self.employee_stats_treeview.configure(yscrollcommand=self.vertical_scrollbar.set)

        # Fill the treeview with the data
        for report in self.current_employe_reports :
            self.employee_stats_treeview.insert("", "end", text=report.id, values=(report.date, report.good_posture_time, report.bad_posture_time))

        # Set the headings
        self.employee_stats_treeview.heading("#0", text="ID")
        self.employee_stats_treeview.heading("Tarih", text="Tarih")
        self.employee_stats_treeview.heading("Düzgün Duruş Süresi", text="Düzgün Duruş Süresi")
        self.employee_stats_treeview.heading("Bozuk Duruş Süresi", text="Bozuk Duruş Süresi")

        # Set the column widths
        self.employee_stats_treeview.column("#0", width=100, anchor="center")
        self.employee_stats_treeview.column("Tarih", width=300, anchor="center")
        self.employee_stats_treeview.column("Düzgün Duruş Süresi", width=300, anchor="center")
        self.employee_stats_treeview.column("Bozuk Duruş Süresi", width=300, anchor="center")

    def _employe_graph(self) -> None:
        """
        Private Class Method, that creates the employee graph frame.
        @Params:
            None
        @Returns:
            None
        """
        self.employee_performance_graph_label = ttk.Label(self.employee_performance_graph_frame, text="Çalışan Performans Grafiği", style="DATA_Headings.TLabel")
        self.employee_performance_graph_label.grid(row=0, column=0, sticky="nsew", pady=15)

        # Create the canvas for matplotlib figure
        self._create_figure()

    def _create_figure(self) -> None:
        """
        Private Class Method, that creates the matplotlib figure.
        @Params:
            None
        @Returns:
            None
        """
        # Get the data
        self.dates = [report.date for report in self.current_employe_reports]
        self.good_postures = [report.good_posture_time for report in self.current_employe_reports]
        self.bad_postures = [report.bad_posture_time for report in self.current_employe_reports]

        self.figure = mpl.figure.Figure(figsize=(5, 4), dpi=100)
        self.subplot = self.figure.add_subplot(111)

        # Turn days into integers for better graph in case of timeXcost
        day_list = [day for day in range(1, len(self.dates)+1)]

        self.subplot.plot(day_list, self.good_postures, label="Düzgün Duruş")
        self.subplot.plot(day_list, self.bad_postures, label="Bozuk Duruş")
        self.subplot.legend()

        resize = (500, 490)
        self.figure.set_size_inches(resize[0]/100, resize[1]/100)
        
        # Initialize Canvas
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.employee_performance_graph_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=1, column=0, sticky="nsew")