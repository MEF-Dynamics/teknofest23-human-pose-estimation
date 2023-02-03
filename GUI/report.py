from    tkinter     import  ttk
import  tkinter     as      tk

class Report(ttk.Frame) :
    """
    Frame Class, that enables the user to see his/her reports.
    @Inherits: ttk.Frame
    """
    def __init__(self, parent, root, *args, **kwargs) -> None:
        """
        Constructor Method of the Report Frame Class.
        """
        super().__init__(parent, *args, **kwargs)
        
        self.root = root
        self.parent = parent

        self.style = self.root.style

        self.COLOR_PALETTES = self.root.COLOR_PALETTES

        self.style.configure("REPORT_InnerContainer.TFrame", background=self.COLOR_PALETTES["INNER_BACKGROUND"])
        self.style.configure("Report_Headings.TLabel", font=("Seoge UI", 13, "bold"), foreground=self.COLOR_PALETTES["FILLER3"], background=self.COLOR_PALETTES["INNER_BACKGROUND"], border=1, borderwidth=5, anchor="center")
        self.style.configure("REPORT_Info.TLabel", font=("Seoge UI", 25, "bold"), foreground=self.COLOR_PALETTES["FILLER3"], background=self.COLOR_PALETTES["INNER_BACKGROUND"], border=1, borderwidth=5, anchor="center")
        self.style.configure("REPORT.Treeview", background=self.COLOR_PALETTES["MIDDLE_BACKGROUND"], foreground="white", fieldbackground=self.COLOR_PALETTES["MIDDLE_BACKGROUND"], font=("Seoge UI", 16), rowheight=35)

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.container = ttk.Frame(self, style="REPORT_InnerContainer.TFrame")
        self.container.grid(row=0, column=0, sticky="nsew")

        # Load all the reports of the current user.
        self.current_users_reports = self.root.db_session.query(self.root.DailyReport).filter_by(employee_id=self.root.current_user.id).all()

        self.current_users_name = self.root.current_user.name
        self.current_users_id = self.root.current_user.name

        self.response_var = tk.StringVar(value="")

        self.info_label = ttk.Label(self.container, text=f"Rapor Analizi", style="REPORT_Info.TLabel")
        self.info_label.grid(row=0, column=0, sticky="nsew", pady=17)

        self.report_list = ttk.Treeview(self.container, columns=("Tarih", "Düzgün Duruş Süresi", "Bozuk Duruş Süresi"), style="REPORT.Treeview", height=12)
        self.report_list.grid(row=1, column=0, sticky="nsew")

        self.vertical_scrollbar = ttk.Scrollbar(self.container, orient="vertical", command=self.report_list.yview)
        self.vertical_scrollbar.grid(row=1, column=1, sticky="ns")

        self.report_list.configure(yscrollcommand=self.vertical_scrollbar.set)

        # Set the headings and column widths.
        self.report_list.heading("#0", text="ID")
        self.report_list.heading("Tarih", text="Tarih")
        self.report_list.heading("Düzgün Duruş Süresi", text="Düzgün Duruş Süresi")
        self.report_list.heading("Bozuk Duruş Süresi", text="Bozuk Duruş Süresi")

        self.report_list.column("#0", width=100, anchor="center")
        self.report_list.column("Tarih", width=300, anchor="center")
        self.report_list.column("Düzgün Duruş Süresi", width=300, anchor="center")
        self.report_list.column("Bozuk Duruş Süresi", width=300, anchor="center")

        # Insert the reports into the treeview.
        self._insert_reports()

        # Set a later - gridded - label to show the selected report's information.
        self.response_label = ttk.Label(self.container, textvariable=self.response_var, style="Report_Headings.TLabel")

        # Bind the treeview to a function that will be called when a report is selected.
        self.report_list.bind("<<TreeviewSelect>>", self._on_report_select)

    def _on_report_select(self, *event) -> None:
        """
        Private Class Method, that is called when a report is selected.
        @Params:
            event : Event : Optional : The event that triggered the function.
        @Returns:
            None
        """
        # Get the selected report's information.
        report_id = self.report_list.item(self.report_list.selection())["text"]
        report_date = self.report_list.item(self.report_list.selection())["values"][0]
        report_good_posture = self.report_list.item(self.report_list.selection())["values"][1]
        report_bad_posture = self.report_list.item(self.report_list.selection())["values"][2]
        # Set the color of the label according to the good posture time.
        color_good_posture = "#00FF00" if report_good_posture > report_bad_posture else "#FF0000"
        # Set the label's text and color.
        self.response_var.set(f"ID: {report_id} Tarih: {report_date} Düzgün Duruş: {report_good_posture} Bozuk Duruş: {report_bad_posture}")
        self.response_label.grid(row=2, column=0, sticky="nsew", pady=15)
        self.response_label.configure(foreground=color_good_posture)

    def load_user_reports(self) -> None:
        """
        Public Class Method, that loads the reports of the current user.
        @Params:
            None
        @Returns:
            None
        """
        self.current_users_reports = self.root.db_session.query(self.root.DailyReport).filter_by(employee_id=self.root.current_user.id).all()
        self._insert_reports()

    def _insert_reports(self) -> None:
        """
        Private Class Method, that inserts the reports into the treeview.
        @Params:
            None
        @Returns:
            None
        """
        # Clear the treeview.
        self.report_list.delete(*self.report_list.get_children())
        # Insert the reports into the treeview.
        for report in self.current_users_reports :
            self.report_list.insert("", "end", text=report.id, values=(report.date, report.good_posture_time, report.bad_posture_time))