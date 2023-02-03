from    tkinter     import  ttk, font

class About(ttk.Frame) :
    """
    Frame Class, that shows the about page.
    @Inherits: ttk.Frame
    """
    def __init__(self, parent, root, *args, **kwargs) -> None:
        """
        Constructor Method of the About Frame Class.
        """
        super().__init__(parent, *args, **kwargs)
        
        self.root = root
        self.parent = parent

        self.style = self.root.style

        self.COLOR_PALETTES = self.root.COLOR_PALETTES

        self.style.configure("ABOUT_InnerContainer.TFrame", background=self.COLOR_PALETTES["INNER_BACKGROUND"])
        self.style.configure("ABOUT_Info.TLabel", font=("Robotic", 25, "bold"), foreground="#FFFFFF", background=self.COLOR_PALETTES["INNER_BACKGROUND"], border=1, borderwidth=5, anchor="center", justify="center")

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.container = ttk.Frame(self, style="ABOUT_InnerContainer.TFrame")
        self.container.grid(row=0, column=0, sticky="nsew")

        self.container.rowconfigure(0, weight=1)
        self.container.columnconfigure(0, weight=1)

        self.info_text = [
            "Merhaba Hosgeldiniz !",
            "Bu uygulamadaki motivasyonumuz asagidaki gibidir",
            "Durus Bozuklugunun: Yayginlasmasini onleyebilmek",
            "Durus Bozuklugunun: Farkindaligini Yaratabilmek",
            "Durus Bozuklugunun: Ogretimini Verimlendirmek",
            "MEF Dynamics - Saglikta Yapay Zeka - Ekibi Sunar"
        ]
        
        self.info_text = "\n\n".join(self.info_text)
        self.info_label = ttk.Label(self.container, text=self.info_text, style="ABOUT_Info.TLabel")
        self.info_label.grid(row=0, column=0, pady=60)

