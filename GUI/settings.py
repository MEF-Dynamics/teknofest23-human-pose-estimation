from    Utilities   import  get_available_cameras
from    tkinter     import  ttk
import  tkinter     as      tk

class Settings(ttk.Frame) :
    """
    Frame Class, that enables the user select settings.
    @Inherits: ttk.Frame
    """
    def __init__(self, parent, root, *args, **kwargs) -> None:
        """
        Constructor Method of the Settings Frame Class.
        """
        super().__init__(parent, *args, **kwargs)
        
        self.root = root
        self.parent = parent

        self.style = self.root.style

        self.COLOR_PALETTES = self.root.COLOR_PALETTES

        self.style.configure("SETTINGS_InnerContainer.TFrame", background=self.COLOR_PALETTES["INNER_BACKGROUND"])
        self.style.configure("SETTINGS_INInnerContainer.TFrame", background=self.COLOR_PALETTES["INNER_BACKGROUND"])
        self.style.configure("SETTINGS_Heading.TLabel", font=("Seoge UI", 25, "bold"), foreground="#FFFFFF", background=self.COLOR_PALETTES["INNER_BACKGROUND"], border=1, borderwidth=5, anchor="center")
        self.style.configure("SETTINGS_CheckBox.TCheckbutton", background=self.COLOR_PALETTES["INNER_BACKGROUND"], foreground=self.COLOR_PALETTES["FILLER3"], border=1, borderwidth=5, anchor="center", justify="center")
        self.style.configure("SETTINGS_CHBX_Label.TLabel", background=self.COLOR_PALETTES["INNER_BACKGROUND"], foreground=self.COLOR_PALETTES["FILLER3"], font=("Seoge UI", 20, "bold"), border=1, borderwidth=5, anchor="center", justify="center")

        self.style.configure("SETTINGS_SelectionCombobox.TCombobox", 
            fieldbackground=self.COLOR_PALETTES["MIDDLE_BACKGROUND"],
        )

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.container = ttk.Frame(self, style="SETTINGS_InnerContainer.TFrame")
        self.container.grid(row=0, column=0, sticky="nsew")

        self.container.rowconfigure(0, weight=1)
        self.container.columnconfigure((0,1,2), weight=1)

        # Load out containers
        self.opencv_settings_container = ttk.Frame(self.container, style="SETTINGS_INInnerContainer.TFrame", padding=15)
        self.opencv_settings_container.grid(row=0, column=0, sticky="nsew")

        self.camera_settings_container = ttk.Frame(self.container, style="SETTINGS_INInnerContainer.TFrame", padding=15)
        self.camera_settings_container.grid(row=0, column=1, sticky="nwe", padx=30)

        self.program_settings_container = ttk.Frame(self.container, style="SETTINGS_INInnerContainer.TFrame", padding=15)
        self.program_settings_container.grid(row=0, column=2, sticky="nwe")

        # Initialize the settings
        self._layout_opencv_settings()
        self._layout_camera_settings()
        self.layout_program_settings()

        # Start track changes, for data sharing
        self._update_root_share()

    def _layout_opencv_settings(self) -> None:
        """
        Private Class Method, that creates the OpenCV setting options.
        @Params:
            None
        @Returns:
            None
        """
        self.opencv_settings_container.rowconfigure((0,1,2,3,4,5,6,7), weight=1)
        self.opencv_settings_container.columnconfigure((0,1), weight=1)

        self.info_label = ttk.Label(self.opencv_settings_container, text="Görüntü Ayarları", style="SETTINGS_Heading.TLabel")
        self.info_label.grid(row=0, column=0, columnspan=2)
        
        size = 35

        self.is_flip_label = ttk.Label(self.opencv_settings_container, text="Yansıt", style="SETTINGS_CHBX_Label.TLabel")
        self.is_flip_label.grid(row=1, column=0)
        self.is_flip_var = tk.BooleanVar(value=True)
        self.is_flip_checkbutton = ttk.Checkbutton(self.opencv_settings_container, variable=self.is_flip_var, style="SETTINGS_CheckBox.TCheckbutton")
        self.is_flip_checkbutton.grid(row=1, column=1, pady=size)
        
        self.is_grayscale_label = ttk.Label(self.opencv_settings_container, text="Gri Tonlama", style="SETTINGS_CHBX_Label.TLabel")
        self.is_grayscale_label.grid(row=2, column=0)
        self.is_grayscale_var = tk.BooleanVar()
        self.is_grayscale_checkbutton = ttk.Checkbutton(self.opencv_settings_container, variable=self.is_grayscale_var, style="SETTINGS_CheckBox.TCheckbutton")
        self.is_grayscale_checkbutton.grid(row=2, column=1)

        self.is_highcontrast_label = ttk.Label(self.opencv_settings_container, text="Yüksek Kontrast", style="SETTINGS_CHBX_Label.TLabel")
        self.is_highcontrast_label.grid(row=3, column=0)
        self.is_highcontrast_var = tk.BooleanVar()
        self.is_highcontrast_checkbutton = ttk.Checkbutton(self.opencv_settings_container, variable=self.is_highcontrast_var, style="SETTINGS_CheckBox.TCheckbutton")
        self.is_highcontrast_checkbutton.grid(row=3, column=1, pady=size)

        self.is_blurr_label = ttk.Label(self.opencv_settings_container, text="Bulanıklaştır", style="SETTINGS_CHBX_Label.TLabel")
        self.is_blurr_label.grid(row=4, column=0)
        self.is_blurr_var = tk.BooleanVar()
        self.is_blurr_checkbutton = ttk.Checkbutton(self.opencv_settings_container, variable=self.is_blurr_var, style="SETTINGS_CheckBox.TCheckbutton")
        self.is_blurr_checkbutton.grid(row=4, column=1)

        self.is_canny_label = ttk.Label(self.opencv_settings_container, text="Çizgisel", style="SETTINGS_CHBX_Label.TLabel")
        self.is_canny_label.grid(row=5, column=0)
        self.is_canny_var = tk.BooleanVar()
        self.is_canny_checkbutton = ttk.Checkbutton(self.opencv_settings_container, variable=self.is_canny_var, style="SETTINGS_CheckBox.TCheckbutton")
        self.is_canny_checkbutton.grid(row=5, column=1, pady=size)

        self.is_sophisticate_label = ttk.Label(self.opencv_settings_container, text="Canlı", style="SETTINGS_CHBX_Label.TLabel")
        self.is_sophisticate_label.grid(row=6, column=0)
        self.is_sophisticate_var = tk.BooleanVar()
        self.is_sophisticate_checkbutton = ttk.Checkbutton(self.opencv_settings_container, variable=self.is_sophisticate_var, style="SETTINGS_CheckBox.TCheckbutton")
        self.is_sophisticate_checkbutton.grid(row=6, column=1)

        self.is_bitwise_label = ttk.Label(self.opencv_settings_container, text="Bitwise", style="SETTINGS_CHBX_Label.TLabel")
        self.is_bitwise_label.grid(row=7, column=0)
        self.is_bitwise_var = tk.BooleanVar()
        self.is_bitwise_checkbutton = ttk.Checkbutton(self.opencv_settings_container, variable=self.is_bitwise_var, style="SETTINGS_CheckBox.TCheckbutton")
        self.is_bitwise_checkbutton.grid(row=7, column=1, pady=size)

    def _layout_camera_settings(self) -> None:
        """
        Private Class Method, that creates the Camera setting options.
        @Params:
            None
        @Returns:
            None
        """
        self.available_cameras = get_available_cameras() 

        self.current_device_name = tk.StringVar(value=self.available_cameras[0])
        self.current_device_index = tk.IntVar(value=0)

        self.camera_settings_container.rowconfigure((0,1,2,3), weight=1)
        self.camera_settings_container.columnconfigure((0,1), weight=1)

        self.info_label = ttk.Label(self.camera_settings_container, text="Kamera Ayarları", style="SETTINGS_Heading.TLabel")
        self.info_label.grid(row=0, column=0, columnspan=2)

        self.camera_label = ttk.Label(self.camera_settings_container, text="Cihaz Seçimi", style="SETTINGS_CHBX_Label.TLabel")
        self.camera_label.grid(row=1, column=0, pady=35, columnspan=2)
        self.device_selection_combobox = ttk.Combobox(self.camera_settings_container, textvariable=self.current_device_name, values=list(self.available_cameras.values()), state="normal", justify="center", validate="none", background=self.COLOR_PALETTES["MIDDLE_BACKGROUND"], foreground="white", style="DATA_SelectionCombobox.TCombobox", font=("Seoge UI", 18, "bold"), cursor="hand2")
        self.device_selection_combobox.grid(row=2, column=0, columnspan=2)
        self.device_selection_combobox.bind("<<ComboboxSelected>>", self._handle_device_selection)

        self.high_performance_label = ttk.Label(self.camera_settings_container, text="Yüksek Performans", style="SETTINGS_CHBX_Label.TLabel")
        self.high_performance_label.grid(row=3, column=0, pady=35)
        self.high_performance_var = tk.BooleanVar()
        self.high_performance_checkbutton = ttk.Checkbutton(self.camera_settings_container, variable=self.high_performance_var, style="SETTINGS_CheckBox.TCheckbutton")
        self.high_performance_checkbutton.grid(row=3, column=1)

    def _handle_device_selection(self, *event) -> None:
        """
        Private Event Handler Class Metod, that handles the device selection.
        @Params:
            *event: tk.Event : Optional : The event that triggered the handler.
        @Returns:
            None
        """
        self.current_device_name.set(self.device_selection_combobox.get())
        self.current_device_index.set(list(self.available_cameras.values()).index(self.current_device_name.get()))

    def layout_program_settings(self) -> None:
        """
        Private Class Method, that creates the Program setting options.
        @Params:
            None
        @Returns:
            None
        """
        self.program_settings_container.rowconfigure((0,1,2,3,4,5), weight=1)
        self.program_settings_container.columnconfigure((0,1), weight=1)

        self.info_label = ttk.Label(self.program_settings_container, text="Program Ayarları", style="SETTINGS_Heading.TLabel")
        self.info_label.grid(row=0, column=0, columnspan=2)

        size = 35

        self.available_themes = ["Karanlık", "Aydınlık"]
        self.current_theme = tk.StringVar(value="Karanlık")
        self.theme_label = ttk.Label(self.program_settings_container, text="Tema Seçimi", style="SETTINGS_CHBX_Label.TLabel")
        self.theme_label.grid(row=1, column=0, columnspan=2, pady=size)
        self.theme_selection_combobox = ttk.Combobox(self.program_settings_container, textvariable=self.current_theme, values=self.available_themes, state="normal", justify="center", validate="none", background=self.COLOR_PALETTES["MIDDLE_BACKGROUND"], foreground="white", style="DATA_SelectionCombobox.TCombobox", font=("Seoge UI", 18, "bold"), cursor="hand2")
        self.theme_selection_combobox.grid(row=2, columnspan=2, column=0)
        self.theme_selection_combobox.bind("<<ComboboxSelected>>", self._handle_theme_selection)

        self.is_sound_label = ttk.Label(self.program_settings_container, text="Ses", style="SETTINGS_CHBX_Label.TLabel")
        self.is_sound_label.grid(row=3, column=0, columnspan=2, pady=size)
        self.is_sound_var = tk.BooleanVar(value=False)
        self.is_sound_checkbutton = ttk.Checkbutton(self.program_settings_container, variable=self.is_sound_var, style="SETTINGS_CheckBox.TCheckbutton")
        self.is_sound_checkbutton.grid(row=3, column=1)

        self.language_selection_label = ttk.Label(self.program_settings_container, text="Dil Seçimi", style="SETTINGS_CHBX_Label.TLabel")
        self.language_selection_label.grid(row=4, column=0, columnspan=2)
        self.available_languages = ["Türkçe", "English"]
        self.current_language = tk.StringVar(value="Türkçe")
        self.language_selection_combobox = ttk.Combobox(self.program_settings_container, textvariable=self.current_language, values=self.available_languages, state="normal", justify="center", validate="none", background=self.COLOR_PALETTES["MIDDLE_BACKGROUND"], foreground="white", style="DATA_SelectionCombobox.TCombobox", font=("Seoge UI", 18, "bold"), cursor="hand2")
        self.language_selection_combobox.grid(row=5, columnspan=2, column=0, pady=size)
        
    def _handle_theme_selection(self, *event) -> None:
        """
        Private Event Handler Class Metod, that handles the theme selection.
        @Params:
            *event: tk.Event : Optional : The event that triggered the handler.
        @Returns:
            None
        """
        selected = self.theme_selection_combobox.get()
        
        self.current_theme.set(selected)
        if selected == "Karanlık":
            self.root.style.theme_use("clam")
        elif selected == "Aydınlık":
            self.root.style.theme_use("vista")

    def _handle_language_selection(self, *event) -> None:
        """
        Private Event Handler Class Metod, that handles the language selection.
        @Params:
            *event: tk.Event : Optional : The event that triggered the handler.
        @Returns:
            None
        """
        self.current_language.set(self.language_selection_combobox.get())
        
    def _update_variables(self, *event) -> None:
        """
        Private Event Handler Class Metod, that updates the variables.
        @Params:
            *event: tk.Event : Optional : The event that triggered the handler.
        @Returns:
            None
        """
        # Load default settings
        self.root.shared_settings__settings = {
            "is_flip" : self.is_flip_var.get(),
            "is_grayscale" : self.is_grayscale_var.get(),
            "is_highcontrast" : self.is_highcontrast_var.get(),
            "is_blurr" : self.is_blurr_var.get(),
            "is_canny" : self.is_canny_var.get(),
            "is_sophisticate" : self.is_sophisticate_var.get(),
            "is_bitwise" : self.is_bitwise_var.get(),
            "current_device_name" : self.current_device_name.get(),
            "current_device_index" : self.current_device_index.get(),
            "current_theme" : self.current_theme.get(),
            "is_sound" : self.is_sound_var.get(),
        }

    def _update_root_share(self) -> None:
        """
        Private Class Method, that updates the root shared variables.
        @Params:
            None
        @Returns:
            None
        """
        self.all_tk_variables = [
            self.is_flip_var,
            self.is_grayscale_var,
            self.is_highcontrast_var,
            self.is_blurr_var,
            self.is_canny_var,
            self.is_sophisticate_var,
            self.is_bitwise_var,
            self.current_device_name,
            self.current_device_index,
            self.current_theme,
            self.is_sound_var
        ]

        # Start tracking the variables
        for tk_variable in self.all_tk_variables :
            tk_variable.trace_add("write", self._update_variables)