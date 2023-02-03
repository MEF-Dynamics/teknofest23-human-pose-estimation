# -*- coding: utf-8 -*-

from    sqlalchemy                  import  Column, Integer, String, ForeignKey, DateTime, Float
from    Utilities                   import  read_config, get_available_cameras
from    sqlalchemy.ext.declarative  import  declarative_base
from    PIL                         import  Image, ImageTk
from    sqlalchemy                  import  create_engine
from    sqlalchemy.orm              import  sessionmaker
from    datetime                    import  datetime
from    tkinter                     import  ttk
import  tkinter                     as      tk
import  warnings
import  random
import  joblib
import  json

# Import all GUI Page Frames
from GUI import (
    About,
    Home,
    Data,
    Camera,
    Report,
    Settings
)

class Program(tk.Tk) :
    """
    Window Class, that ruins the application after login page. With frame classes.
    @Inherits:
        tk.Tk : tkinter.Tk : Window Class
    """
    def __init__(self, username, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        """
        Constructor Method, that ruins the application after login page. With frame classes.
        @Params:
            username : str : Required : Username of the user that logged in.
        @Returns:
            None
        """
        # Set DPI Awareness for Windows Users
        try:
            from ctypes import windll
            windll.shcore.SetProcessDpiAwareness(1)
        except:
            pass

        self.effect_size = (50, 50)

        # Ignore Warnings of OpenCV
        warnings.filterwarnings("ignore")

        # Set Window Title and Icon
        self.title("Duruş Bozukluğu Tespit Uygulaması - Uygulama")
        self.iconbitmap("Assets/GUI/icon.ico")
        
        # Set Default Variables - DB and Model
        self._initialize_program_variables()

        # STYLING
        self.style = ttk.Style()

        with open("Resources\Config\color_palette.json", "r") as f:
            self.COLOR_PALETTES = json.load(f)

        self.style.theme_use("clam")

        self.style.configure("Header.TLabel", font=("Seoge UI", 21, "bold"), foreground=self.COLOR_PALETTES["OUTER_BACKGROUND"], background=self.COLOR_PALETTES["INNER_BACKGROUND"])
        self.style.configure("Effect.TButton", foreground=self.COLOR_PALETTES["FILLER3"], background=self.COLOR_PALETTES["INNER_BACKGROUND"], border=1, borderwidth=5)
        self.style.configure("InnerContainer.TFrame", background=self.COLOR_PALETTES["INNER_BACKGROUND"])
        self.style.configure("User.TLabel", background=self.COLOR_PALETTES["INNER_BACKGROUND"])

        self.style.map(
            "Effect.TButton",
            background=[("disabled", self.COLOR_PALETTES["MIDDLE_BACKGROUND"]), ("active", self.COLOR_PALETTES["MIDDLE_BACKGROUND"])],
        )

        # make background of main frame
        self.configure(background=self.COLOR_PALETTES["OUTER_BACKGROUND"])

        self.username = username

        # Get user via database
        self._define_user()

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # Containers are set
        self.root_container = ttk.Frame(self, style="InnerContainer.TFrame")
        self.root_container.grid(row=0, column=0, padx=15, pady=15)

        self.top_bar_container = ttk.Frame(self.root_container, padding=15, style="InnerContainer.TFrame")
        self.top_bar_container.grid(row=0, column=0, columnspan=2, sticky="nsew")
        
        self.menu_selection_container = ttk.Frame(self.root_container, padding=15, style="InnerContainer.TFrame")

        self.page_container = ttk.Frame(self.root_container, style="InnerContainer.TFrame")
        self.page_container.grid(row=1, column=1, sticky="nsew", padx=30, pady=15)

        # Initialize Pages
        self.About_Page = About(parent=self.page_container, root=self)
        self.Camera_Page = Camera(parent=self.page_container, root=self)
        self.Data_Page = Data(parent=self.page_container, root=self)
        self.Home_Page = Home(parent=self.page_container, root=self)
        self.Report_Page = Report(parent=self.page_container, root=self)
        self.Settings_Page = Settings(parent=self.page_container, root=self)

        self.pages = {
            "ABOUT" : self.About_Page,
            "CAMERA" : self.Camera_Page,
            "DATA" : self.Data_Page,
            "HOME" : self.Home_Page,
            "REPORT" : self.Report_Page,
            "SETTINGS" : self.Settings_Page
        }

        self.current_page = self.Home_Page
        self.current_page.grid(row=0, column=0, sticky="nsew")

        # Layout All Widgets
        self._layout_top_bar_widgets()
        self._layout_menu_selection_widgets()

        # Set Window in the center of the screen, and set minimum size of the window
        self._set_window_geometry()

        # Catch Window Close Event - for anti-crash
        self.protocol("WM_DELETE_WINDOW", self._on_closing)

    def _on_closing(self) -> None:
        """
        Private Class Method, that runs when the window is closed.
        @Params:
            None
        @Returns:
            None
        """
        # Exception Cases for anti-crash, CAM Exception and Animation Exception for after program.
        try :
            self.Camera_Page.stop_camera()
        except :
            pass

        try :
            self.Home_Page.after_cancel(self.Home_Page.anim)
        except :
            pass

        self.destroy()
        self.quit()

    def _layout_top_bar_widgets(self) -> None:
        """
        Private Class Method, that layouts the widgets of the top bar.
        @Params:
            None
        @Returns:
            None
        """
        # Menu Bar Widgets
        self.top_bar_container.columnconfigure((0,1,2), weight=1)
        
        self.menu_button_image = ImageTk.PhotoImage(Image.open("Assets/GUI/menu.png").resize(self.effect_size, Image.ANTIALIAS))
        self.menu_button = ttk.Button(self.top_bar_container, image=self.menu_button_image, command=self._toggle_menu, style="Effect.TButton", cursor="hand2")
        self.is_menu_open = False
        self.menu_button.grid(row=0, column=0, sticky="w", padx=15, pady=15)
        self.current_menu_degree = 0
        self.addition_constant = 5
        self.addition_degree = self.addition_constant

        self.username_label = ttk.Label(self.top_bar_container, text=self.username, justify="center", anchor="center", style="Header.TLabel")
        self.username_label.grid(row=0, column=1, padx=15, pady=15)

        self.user_photo_image = ImageTk.PhotoImage(Image.open("Assets/GUI/user.png").resize((70, 70), Image.ANTIALIAS))
        self.user_photo = ttk.Label(self.top_bar_container, image=self.user_photo_image, style="User.TLabel")
        self.user_photo.grid(row=0, column=2, sticky="e", padx=15, pady=15)

    def _animate_menu_image(self) -> None:
        """
        Private Class Method, that animates the menu button.
        @Params:
            None
        @Returns:
            None
        """
        # Animation Loop
        while True :

            self.current_menu_degree += self.addition_degree

            self.menu_button_image = ImageTk.PhotoImage(Image.open("Assets/GUI/menu.png").resize(self.effect_size, Image.ANTIALIAS).rotate(self.current_menu_degree))
            self.menu_button.configure(image=self.menu_button_image)

            # Update is must for root health
            self.update()

            if self.current_menu_degree in (0, 90) :
                break

    def _toggle_menu(self) -> None:
        """
        Private Class Method, that toggles the menu. Runs neccessary methods with a menu toggle animation.
        @Params:
            None
        @Returns:
            None
        """

        if self.is_menu_open :
            self._animate_menu_image()
            self.addition_constant = 3
            self.current_menu_degree = 0
            self.addition_degree = self.addition_constant
            self.is_menu_open = False
            self.menu_selection_container.grid_remove()
        else :
            self._animate_menu_image()
            self.addition_constant = 2
            self.current_menu_degree = 90
            self.addition_degree = -self.addition_constant
            self.is_menu_open = True
            self.menu_selection_container.grid(row=1, column=0, sticky="nsew")

        self._set_min_size()
        
    def _layout_menu_selection_widgets(self) -> None:
        """
        Private Class Method, that layouts the widgets of the menu selection.
        @Params:
            None
        @Returns:
            None
        """
        self.menu_selection_container.columnconfigure(0, weight=1)
        self.menu_selection_container.rowconfigure((0,1,2,3,4,5), weight=1)

        self.home_button_image = ImageTk.PhotoImage(Image.open("Assets/GUI/home.png").resize(self.effect_size, Image.ANTIALIAS))
        self.home_button = ttk.Button(self.menu_selection_container, image=self.home_button_image, command=lambda : self._switch_page("HOME"), style="Effect.TButton", cursor="hand2")
        self.home_button.grid(row=0, column=0, sticky="nsew", padx=15)

        self.camera_button_image = ImageTk.PhotoImage(Image.open("Assets/GUI/camera.png").resize(self.effect_size, Image.ANTIALIAS))
        self.camera_button = ttk.Button(self.menu_selection_container, image=self.camera_button_image, command=lambda : self._switch_page("CAMERA"), style="Effect.TButton", cursor="hand2")
        self.camera_button.grid(row=1, column=0, sticky="nsew", padx=15, pady=30)

        self.data_button_image = ImageTk.PhotoImage(Image.open("Assets/GUI/data.png").resize(self.effect_size, Image.ANTIALIAS))
        self.data_button = ttk.Button(self.menu_selection_container, image=self.data_button_image, command=lambda : self._switch_page("DATA"), style="Effect.TButton", cursor="hand2")
        self.data_button.grid(row=2, column=0, sticky="nsew", padx=15)

        self.report_button_image = ImageTk.PhotoImage(Image.open("Assets/GUI/report.png").resize(self.effect_size, Image.ANTIALIAS))
        self.report_button = ttk.Button(self.menu_selection_container, image=self.report_button_image, command=lambda : self._switch_page("REPORT"), style="Effect.TButton", cursor="hand2")
        self.report_button.grid(row=3, column=0, sticky="nsew", padx=15, pady=30)

        self.about_button_image = ImageTk.PhotoImage(Image.open("Assets/GUI/about.png").resize(self.effect_size, Image.ANTIALIAS))
        self.about_button = ttk.Button(self.menu_selection_container, image=self.about_button_image, command=lambda : self._switch_page("ABOUT"), style="Effect.TButton", cursor="hand2")
        self.about_button.grid(row=4, column=0, sticky="nsew", padx=15)

        self.settings_button_image = ImageTk.PhotoImage(Image.open("Assets/GUI/settings.png").resize(self.effect_size, Image.ANTIALIAS))
        self.settings_button = ttk.Button(self.menu_selection_container, image=self.settings_button_image, command=lambda : self._switch_page("SETTINGS"), style="Effect.TButton", cursor="hand2")
        self.settings_button.grid(row=5, column=0, sticky="nsew", padx=15, pady=30)

        # Disable Database Access Buttons for employees
        if not isinstance(self.current_user, self.Hr) :
            self.data_button.configure(state="disabled")

    def write_daily_report(self) -> None:
        """
        Public Class Method, that writes the daily report to the database.
        @Params:
            None
        @Returns:
            None
        """

        # These variables are updated after @camera_close pull in Camera_Page
        durus_bozuk = self.shared_camera__durus_bozuk
        durus_duzgun = self.shared_camera__durus_duzgun

        self.db_session.add(
            self.DailyReport(
                date = datetime.now(),
                employee_id = self.current_user.id,
                bad_posture_time = durus_bozuk,
                good_posture_time = durus_duzgun
            )
        )

        self.db_session.commit()

    def _define_user(self) -> None:
        """
        Private Class Method, that defines the user from the database.
        @Params:
            None
        @Returns:
            None
        """
        name, *surname = self.username.split(" ")
        surname = " ".join(surname)

        hr_list = self.db_session.query(self.Hr).filter(self.Hr.name == name, self.Hr.surname == surname).all()
        employee_list = self.db_session.query(self.Employee).filter(self.Employee.name == name, self.Employee.surname == surname).all()

        # User is not in the database, create a new one
        if len(hr_list) == 0 and len(employee_list) == 0 :
            print("USER NOT FOUND IN DATABASE, CREATING ...")
            random_hr = random.choice(self.db_session.query(self.Hr).all())

            self.current_user = self.Employee(
                                    name=name,
                                    surname=surname,
                                    email=f"{surname.lower()}.{str(name).lower()}@mef.edu.tr",
                                    hr_id=random_hr.id
                                )

            self.db_session.add(
                self.current_user
            )

            self.db_session.commit()
        # User is in the database, define the user
        elif len(hr_list) > 0 :
            for hr in hr_list :
                if hr.name == name and hr.surname == surname :
                    self.current_user = hr
                    break
        elif len(employee_list) > 0 :
            for employee in employee_list :
                if employee.name == name and employee.surname == surname :
                    self.current_user = employee
                    break

    def _switch_page(self, page_id) -> None:
        """
        Private Class Method, that switches the page.
        @Params:
            page_id : str : Reqired : The page id to switch to.
        @Returns:
            None
        """
        # When grid is removed, the settings and info stays, it just not displays anymore.
        self.current_page.grid_remove()
        # CurrentPage concept is used to avoid write 6 if else lines. Thats why page_id is used.
        self.current_page = self.pages[page_id]
        self.current_page.grid(row=0, column=0, sticky="nsew")

        self._set_min_size()

    def _checkout_database(self) -> None:
        """
        Private Class Method, that checks out the database. Drops the tables if they exist, and creates new ones. If it is wanted, drop part can be removed, it will keep adding new data to the database.
        @Params:
            None
        @Returns:
            None
        """
        # Drop tables if they exist
        self.db_base.metadata.drop_all(self.db_engine)
        # Create tables
        self.db_base.metadata.create_all(self.db_engine)

    def _fill_database(self) -> None:
        """
        Private Class Method, that fills the database with dummy data.
        @Params:
            None
        @Returns:
            None
        """
        # Username Mappings
        employee_list = ["ECM", "Emir Cetin M", "Mehmet Su", "Ahmet Yıldız", "Ali Bal", "Pelinsu Yıldırım", "Ayşe Nur", "Fatma Öz", "Zeynep Sıla", "Selin Boğa", "Seda Yıldız", "Sude Eş", "Süleyman Soylu", "Mehmet Bozan", "Mustafa Mert Tunalı"]
        hr_list = ["ECS", "Emir Cetin Memis", "Sıla Borkmaz", "Cem Baysal", "Verda Alataş", "Emircan Yaprak", "Talha Bozan"]

        # Fill Hr Table
        for hr in hr_list :
            
            name, *surname = hr.split(" ")
            surname = " ".join(surname)

            self.db_session.add(
                self.Hr(
                    name=name,
                    surname=surname,
                    email=f"{surname.lower()}.{name.lower()}@mef.edu.tr"
                )
            )

        self.db_session.commit()

        # Fill Employee Table
        for employee in employee_list :
                
            name, *surname = employee.split(" ")
            surname = " ".join(surname)

            random_hr_name, *random_hr_surname = random.choice(hr_list).split(" ")
            random_hr_surname = " ".join(random_hr_surname)
            hr_id = self.db_session.query(self.Hr).filter(self.Hr.name == random_hr_name, self.Hr.surname == random_hr_surname).first().id

            self.db_session.add(
                self.Employee(
                    name=name,
                    surname=surname,
                    email=f"{surname.lower()}.{name.lower()}@mef.edu.tr",
                    hr_id=hr_id
                )
            )

        self.db_session.commit()

        # Fill DailyReport Table
        for employee in employee_list :

            employee_name, *employee_surname = employee.split(" ")
            employee_surname = " ".join(employee_surname)

            employee_id = self.db_session.query(self.Employee).filter(self.Employee.name == employee_name, self.Employee.surname == employee_surname).first().id
            
            data_count = 20

            for i in range(data_count) :

                random_interval1 = random.uniform(0.01, 8)
                random_interval2 = random.uniform(0.01, 8)

                self.db_session.add(
                    self.DailyReport(
                        employee_id=employee_id,
                        date=datetime.now(),
                        bad_posture_time=random_interval1,
                        good_posture_time=random_interval2
                    )
                )

        self.db_session.commit()

    def _initialize_hard_variables(self) -> None:
        """
        Private Class Method, that initializes the hard variables.
        @Params:
            None
        @Returns:
            None
        """
        # Load Model
        self.model = joblib.load("Resources/Model/gbc.sav")
        # Load Database
        postgre_password = read_config("Resources/Config/config.json")["POSTGRE_PASSWORD"]
        self.db_engine = create_engine(f"postgresql+psycopg2://postgres:{postgre_password}@localhost/pose_estimation")
        self.db_base = declarative_base()
        self.db_session = sessionmaker(bind=self.db_engine)()
        # Fix Database
        self._initialize_attribute_classes()
        self._checkout_database()
        self._fill_database()

    def _initialize_shared_variables(self) -> None:
        """
        Private Class Method, that initializes the shared variables.
        @Note:
            - This method is must, for data sharing between pages. There is no other way to share data between pages except file writing.
            - The way this method, works. It makes pages initialize with default variables written here. When they are changed by their page, the initialized other pages also updated.
        @Params:
            None
        @Returns:
            None
        """
        # Setting variables
        self.shared_settings__settings = {
            "is_flip" : True,
            "is_grayscale" : False,
            "is_highcontrast" : False,
            "is_blurr" : False,
            "is_canny" : False,
            "is_sophisticate" : False,
            "is_bitwise" : False,
            "current_device_name" : get_available_cameras()[0],
            "current_device_index" : 0,
            "current_theme" : "clam",
            "is_sound" : False
        }
        # Algorithm variables
        self.shared_camera__durus_bozuk = 0
        self.shared_camera__durus_duzgun = 0

    def _initialize_attribute_classes(self) -> None:
        """
        Private Class Method, that initializes the attribute classes.
        @Params:
            None
        @Returns:
            None
        """
        class Employee(self.db_base):
            __tablename__ = 'employee'
            id = Column(Integer, primary_key=True,  autoincrement=True)
            name = Column(String(80), nullable=False)
            surname = Column(String(80), nullable=False)
            email = Column(String(80), nullable=False)
            hr_id = Column(Integer, ForeignKey('hr.id'))


            def __init__(self, name, surname, email, hr_id):
                self.name = name
                self.surname = surname
                self.email = email
                self.hr_id = hr_id

            def __repr__(self):
                return '<Employee %r>' % self.name

        class Hr(self.db_base):
            __tablename__ = 'hr'
            id = Column(Integer, primary_key=True, autoincrement=True)
            name = Column(String(80), nullable=False)
            surname = Column(String(80), nullable=False)
            email = Column(String(80), nullable=False)


            def __init__(self, name, surname, email):
                self.name = name
                self.surname = surname
                self.email = email

            def __repr__(self):
                return '<Hr %r>' % (self.name)

        class DailyReport(self.db_base):
            __tablename__ = 'daily_report'
            id = Column(Integer, primary_key=True, autoincrement=True)
            date = Column(DateTime, default=datetime.now)
            employee_id = Column(Integer, ForeignKey('employee.id'))
            bad_posture_time = Column(Float)
            good_posture_time = Column(Float)

            def __init__(self, date, employee_id, bad_posture_time, good_posture_time):
                self.date = date
                self.employee_id = employee_id
                self.bad_posture_time = bad_posture_time
                self.good_posture_time = good_posture_time

            def __repr__(self):
                return '<DailyReport %r>' % (self.id)

        # Assigning classes to class variables
        self.Employee = Employee
        self.Hr = Hr
        self.DailyReport = DailyReport

    def _initialize_program_variables(self) -> None:
        """
        Private Class Method, that initializes the program variables by calling hard and shared variables.
        @Params:
            None
        @Returns:
            None
        """
        self._initialize_hard_variables()
        self._initialize_shared_variables()

    def _rotateApplicationWindow(self) -> None:
        """
        Private Class Method, that rotates the application window.
        @Params:
            None
        @Returns:
            None
        """
        self.update()
        self.geometry("+{}+{}".format(int(self.winfo_screenwidth()/2 - self.winfo_reqwidth()/2), int(self.winfo_screenheight()/2 - self.winfo_reqheight()/2)))
        self.update()

    def _set_min_size(self) -> None:
        """
        Private Class Method, that sets the minimum size of the window.
        @Params:
            None
        @Returns:
            None
        """
        # Set minumum size of the window
        self.update()
        tpl = (self.winfo_reqwidth(), self.winfo_reqheight())
        self.minsize(*tpl)
        # set size of the window
        self.update()
        tpl = (self.winfo_reqwidth(), self.winfo_reqheight())
        self.geometry("{}x{}".format(*tpl))
        self.update()
        
    def update_user_reports(self) -> None:
        """
        Public Class Method, that updates the user reports.
        @Params:
            None
        @Returns:
            None
        """
        self.Report_Page.load_user_reports()

    def _set_window_geometry(self) -> None:
        """
        Private Class Method, that sets the window.
        @Params:
            None
        @Returns:
            None
        """
        # Set minimum size
        self._set_min_size()
        # Set window position
        self._rotateApplicationWindow()

class Application(tk.Tk) :
    """
    Class, that represents the application.
    @Inherits:
        tk.Tk : Inherits from tkinter.Tk class.
    """
    def __init__(self, *args, **kwargs) -> None:
        """
        Constructor Method, that shows an login page and initializes the application with user's credentials.
        @Params:
            None
        @Returns:
            None
        """
        super().__init__(*args, **kwargs)

        # Setting DPI awareness for Windows users
        try:
            from ctypes import windll
            windll.shcore.SetProcessDpiAwareness(1)
        except:
            pass

        self.style = ttk.Style()

        with open("Resources\Config\color_palette.json", "r") as f:
            self.COLOR_PALETTES = json.load(f)

        self.style.theme_use("clam")

        self.style.configure("Header.TLabel", font=("Seoge UI", 40, "bold"), foreground=self.COLOR_PALETTES["OUTER_BACKGROUND"], background=self.COLOR_PALETTES["INNER_BACKGROUND"])
        self.style.configure("Handle.TButton", font=("Seoge UI", 20, "bold"), foreground=self.COLOR_PALETTES["FILLER3"], background=self.COLOR_PALETTES["INNER_BACKGROUND"], border=1, borderwidth=5)
        self.style.configure("Effect.TButton", foreground=self.COLOR_PALETTES["FILLER3"], background=self.COLOR_PALETTES["INNER_BACKGROUND"], border=1, borderwidth=5)
        self.style.configure("Container.TFrame", background=self.COLOR_PALETTES["INNER_BACKGROUND"])

        self.style.map(
            "Effect.TButton",
            background=[("disabled", self.COLOR_PALETTES["MIDDLE_BACKGROUND"]), ("active", self.COLOR_PALETTES["MIDDLE_BACKGROUND"])],

        )
        self.style.map(
            "Handle.TButton",
            background=[("disabled", self.COLOR_PALETTES["MIDDLE_BACKGROUND"]), ("active", self.COLOR_PALETTES["MIDDLE_BACKGROUND"])],
            foreground=[("disabled", self.COLOR_PALETTES["FILLER3"]), ("active", self.COLOR_PALETTES["FILLER3"])]
        )

        # make background of main frame
        self.configure(background=self.COLOR_PALETTES["OUTER_BACKGROUND"])

        # Setting window title and icon
        self.title("Duruş Bozukluğu Tespit Uygulaması - Giriş")
        self.iconbitmap("Assets/GUI/icon.ico")

        self.default_username = "Kullanıcı Adı"
        self.default_password = "Şifre"

        self.username_var = tk.StringVar(value=self.default_username) 
        self.password_var = tk.StringVar(value=self.default_password)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # Loading containers
        self.login_container = ttk.Frame(self, padding=15, style="Container.TFrame")
        self.login_container.grid(row=0, column=0, padx=15, pady=15)

        self.login_container.columnconfigure((0,1), weight=1)

        self.club_logo_image = ImageTk.PhotoImage(Image.open("Assets/GUI/club logo.png").resize((250, 170), Image.ANTIALIAS))
        self.teknofest_logo_image = ImageTk.PhotoImage(Image.open("Assets/GUI/teknofest logo.png").resize((250, 170), Image.ANTIALIAS))

        self.club_logo_label = ttk.Label(self.login_container, image=self.club_logo_image, border=1, borderwidth=5, background="white", cursor="heart")
        self.teknofest_logo_label = ttk.Label(self.login_container, image=self.teknofest_logo_image, border=1, borderwidth=5, background="white", cursor="heart")

        self.club_logo_label.grid(row=0, column=0, padx=15, pady=15)
        self.teknofest_logo_label.grid(row=0, column=1, padx=15, pady=15)

        self.info_label = ttk.Label(self.login_container, text="Giriş Ekranı", style="Header.TLabel")
        self.info_label.grid(row=1, column=0, columnspan=2, padx=15, pady=15)

        self.username_entry = ttk.Entry(self.login_container, textvariable=self.username_var, foreground=self.COLOR_PALETTES["OUTER_BACKGROUND"], font=("Seoge UI", 20), justify="center")
        self.username_entry.grid(row=2, column=0, columnspan=2, padx=15, pady=15)

        self.clear_image = ImageTk.PhotoImage(Image.open("Assets/GUI/clear.png").resize((31, 31), Image.ANTIALIAS))

        self.clear_entry_button = ttk.Button(self.login_container, image=self.clear_image, command=self._clear_entry, style="Effect.TButton", cursor="hand2")
        self.clear_entry_button.grid(row=2, column=1, padx=15, pady=15)

        self.password_entry = ttk.Entry(self.login_container, textvariable=self.password_var, foreground=self.COLOR_PALETTES["OUTER_BACKGROUND"], font=("Seoge UI", 20), justify="center")
        self.password_entry.grid(row=3, column=0, columnspan=2, padx=15, pady=15)

        self.open_eye_image = ImageTk.PhotoImage(Image.open("Assets/GUI/open eye.png").resize((31, 31), Image.ANTIALIAS))
        self.closed_eye_image = ImageTk.PhotoImage(Image.open("Assets/GUI/closed eye.png").resize((31, 31), Image.ANTIALIAS))

        self.password_show_button = ttk.Button(self.login_container, image=self.open_eye_image, command=self._toggle_password_show, style="Effect.TButton", cursor="hand2")
        self.password_show_button.grid(row=3, column=1, padx=15, pady=15)

        self.login_button = ttk.Button(self.login_container, text="Giriş Yap", command=self._login, style="Handle.TButton", cursor="hand2")
        self.login_button.grid(row=4, column=0, padx=15, pady=15, sticky="nsew")

        self.forgat_password_button = ttk.Button(self.login_container, text="Şifremi Unuttum", command=self._forgat_password, style="Handle.TButton", cursor="hand2")
        self.forgat_password_button.grid(row=4, column=1, padx=15, pady=15, sticky="nsew")

        # Binding events, that clears the entry widgets
        self.username_entry.bind("<Button-1>", lambda event : self.username_entry.delete(0, tk.END) if self.username_entry.get() == self.default_username else None)
        self.password_entry.bind("<Button-1>", lambda event : self.password_entry.delete(0, tk.END) if self.password_entry.get() == self.default_password else None)
        
        # Set Window in the center of the screen, and set minimum size of the window
        self._set_window_geometry()

        # Catch Window Close Event - for anti-crash
        self.protocol("WM_DELETE_WINDOW", self._on_closing)


    def _on_closing(self) -> None:
        """
        Private Class Method, that runs when the window is closed.
        @Params:
            None
        @Returns:
            None
        """
        self.destroy()
        self.quit()

    def _clear_entry(self) -> None:
        """
        Private Class Method, that clears the entry widgets.
        @Params:
            None
        @Returns:
            None
        """
        self.username_entry.delete(0, tk.END)
        self.username_entry.insert(0, self.default_username)
        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, self.default_password)

    def _toggle_password_show(self) -> None:
        """
        Private Class Method, that toggles the password show.
        @Params:
            None
        @Returns:
            None
        """
        if self.password_entry["show"] == "*" :
            self.password_entry["show"] = ""
            self.password_show_button["image"] = self.open_eye_image
        else :
            self.password_entry["show"] = "*"
            self.password_show_button["image"] = self.closed_eye_image

    def _login(self) -> None:
        """
        Private Class Method, that initializes main program.
        @Params:
            None
        @Returns:
            None
        """
        username = self.username_entry.get()
        # Close login window
        self.destroy()
        # Initialize main program
        Program(username).mainloop()

    def _forgat_password(self) -> None:
        """
        Unknow Class Method.
        @TO:DO
            Track passwords via database
            Track, register and delete users via database
        """
        pass

    def _set_min_size(self) -> None:
        """
        Private Class Method, that sets the minimum size of the window.
        @Params:
            None
        @Returns:
            None
        """
        # Set minumum size of the window
        self.update()
        tpl = (self.winfo_width(), self.winfo_height())
        self.minsize(*tpl)

    def _rotateApplicationWindow(self) -> None:
        """
        Private Class Method, that rotates the application window.
        @Params:
            None
        @Returns:
            None
        """
        self.update()
        self.geometry("+{}+{}".format(int(self.winfo_screenwidth()/2 - self.winfo_reqwidth()/2), int(self.winfo_screenheight()/2 - self.winfo_reqheight()/2)))
        self.update()

    def _set_window_geometry(self) -> None:
        """
        Private Class Method, that sets the window.
        @Params:
            None
        @Returns:
            None
        """
        # Set minimum size
        self._set_min_size()
        # Set window position
        self._rotateApplicationWindow()