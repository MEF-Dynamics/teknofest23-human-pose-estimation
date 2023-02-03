from    PIL         import ImageTk, Image
from    time        import time
from    tkinter     import ttk
import  tkinter     as tk
import  mediapipe   as mp
import  pygame
import  math
import  cv2

class Camera(ttk.Frame) :
    """
    Frame Class, that contains the camera and the controls for the camera.
    @Inherits: ttk.Frame
    """
    def __init__(self, parent, root, *args, **kwargs) -> None:
        """
        Constructor Method of the Camera Frame Class.
        """
        super().__init__(parent, *args, **kwargs)
        
        self.root = root
        self.parent = parent

        self.style = self.root.style

        self.COLOR_PALETTES = self.root.COLOR_PALETTES

        self.style.configure("CAMERA_Handle.TButton", font=("Seoge UI", 20, "bold"), foreground="#FFFFFF", background=self.COLOR_PALETTES["INNER_BACKGROUND"], border=1, borderwidth=5)
        self.style.configure("CAMERA_InnerContainer.TFrame", background=self.COLOR_PALETTES["INNER_BACKGROUND"])

        self.style.map(
            "CAMERA_Handle.TButton",
            background=[("disabled", self.COLOR_PALETTES["MIDDLE_BACKGROUND"]), ("active", self.COLOR_PALETTES["MIDDLE_BACKGROUND"])],
            foreground=[("disabled", "#FFFFFF"), ("active", "#FFFFFF")]
        )

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.container = ttk.Frame(self, style="CAMERA_InnerContainer.TFrame")
        self.container.grid(row=0, column=0, sticky="nsew")

        self.container.rowconfigure((0,1), weight=1)
        self.container.columnconfigure((0,1), weight=1)

        # Load default shared settings at the beginning.
        self.device_index = self.root.shared_settings__settings["current_device_index"]
        self.device_name = self.root.shared_settings__settings["current_device_name"]

        # Setting mixer, for alerting user.
        pygame.mixer.init()
        pygame.mixer.music.load("Assets/Sound/alarm1.mp3")

        self._RGB_blue = (255, 0, 0)
        self._RGB_red = (0, 0, 255)
        self._RGB_green = (0, 255, 0)
        self._RGB_dark_blue = (255, 0, 0)
        self._RGB_light_green = (0, 255, 0)
        self._RGB_yellow = (0, 255, 255)
        self._RGB_pink = (255, 0, 255)

        self.model = self.root.model

        self.current_camera_frame = cv2.VideoCapture(self.device_index, cv2.CAP_DSHOW).read()[1]
        self.current_camera_frame = cv2.cvtColor(self.current_camera_frame, cv2.COLOR_BGR2RGB)
        self.current_camera_frame = cv2.flip(self.current_camera_frame, 1)
        self.captured_image = ImageTk.PhotoImage(Image.fromarray(self.current_camera_frame).resize((640, 495), Image.ANTIALIAS))
        self.camera_view_label = ttk.Label(self.container, image=self.captured_image)
        self.camera_view_label.grid(row=0, column=0, columnspan=2, sticky="nsew")

        self.start_camera_button = ttk.Button(self.container, text="Tespit Ediciyi Başlat", command=self._start_camera, style="CAMERA_Handle.TButton", cursor="hand2")
        self.start_camera_button.grid(row=1, column=0, sticky="wns", pady=30)

        self.stop_camera_button = ttk.Button(self.container, text="Tespit Ediciyi Durdur", command=self.stop_camera, state="disabled", style="CAMERA_Handle.TButton", cursor="hand2")
        self.stop_camera_button.grid(row=1, column=1, sticky="ens", pady=30)

        self.camera_frame = ttk.Frame(self.container)

    def _reset_variables(self) -> None:
        """
        Private Class Method, that resets the variables of the class.
        @Params:
            None
        @Returns:
            None
        """
        self.cap = cv2.VideoCapture(self.device_index, cv2.CAP_DSHOW)

        self.durus_bozuk = tk.DoubleVar(value=0)
        self.durus_duzgun = tk.DoubleVar(value=0)

        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose()

    def _start_camera(self) -> None:
        """
        Private Class Method, that starts the camera.
        @Params:
            None
        @Returns:
            None
        """
        # Set availability of buttons.
        self.start_camera_button.configure(state="disabled")
        self.stop_camera_button.configure(state="normal")
        # Initialize program.
        self._reset_variables()
        self._pose_estimation()

    def stop_camera(self) -> None:
        """
        Public Class Method, that stops the camera. It is also reached via root, at the @on_close method.
        @Params:
            None
        @Returns:
            None
        """
        # Set availability of buttons.
        self.start_camera_button.configure(state="normal")
        self.stop_camera_button.configure(state="disabled")
        last_captured_image = self.captured_image
        self.camera_view_label.configure(image=last_captured_image)
        # Release camera.
        self.cap.release()
        # Update daily report variables.
        self.root.shared_camera__durus_bozuk = self.durus_bozuk.get()
        self.root.shared_camera__durus_duzgun = self.durus_duzgun.get()
        # Write daily report.
        self.root.write_daily_report()
        # Update User reports.
        self.root.update_user_reports()

    def _findAngle(self, x1, y1, x2, y2) -> int:
        """
        Private Class Method, that finds the angle between two points.
        @Params:
            x1 : int : Required : The x coordinate of the first point.
            y1 : int : Required : The y coordinate of the first point.
            x2 : int : Required : The x coordinate of the second point.
            y2 : int : Required : The y coordinate of the second point.
        @Returns:
            int : The angle between the two points.
        """
        return int(180 / math.pi) * math.acos((y2 - y1) * (-y1) / (math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2) * y1))

    def _pose_estimation(self) -> None:
        """
        Private Class Method, that does the pose estimation. With openCV and mediapipe.
        @Params:
            None
        @Returns:   
            None
        """
        # Main loop.
        while self.cap.isOpened() :

            # Excption handled for missing landmark points.
            try :

                # Check if there is a change in shared settings. Apply it if there is.
                if self.root.shared_settings__settings["current_device_index"] != self.device_index :
                    self.device_index = self.root.shared_settings__settings["current_device_index"]
                    self.cap = cv2.VideoCapture(self.device_index, cv2.CAP_DSHOW)

                _, image = self.cap.read()

                h, w = image.shape[:2]
                # Check if there is a change in shared settings. Apply it if there is.
                if self.root.shared_settings__settings["is_sophisticate"] :
                    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                # Check if there is a change in shared settings. Apply it if there is.
                if self.root.shared_settings__settings["is_flip"] :
                    image = cv2.flip(image, 1)

                # Extract keypoints.
                keypoints = self.pose.process(image)

                # Extract landmark points and positions.
                lm = keypoints.pose_landmarks
                lmPose = self.mp_pose.PoseLandmark

                # Calculate, key points
                l_shldr_x = int(lm.landmark[lmPose.LEFT_SHOULDER].x * w)
                l_shldr_y = int(lm.landmark[lmPose.LEFT_SHOULDER].y * h)
                r_shldr_x = int(lm.landmark[lmPose.RIGHT_SHOULDER].x * w)
                r_shldr_y = int(lm.landmark[lmPose.RIGHT_SHOULDER].y * h)
                l_ear_x   = int(lm.landmark[lmPose.LEFT_EAR].x * w)
                l_ear_y   = int(lm.landmark[lmPose.LEFT_EAR].y * h)
                l_hip_x   = int(lm.landmark[lmPose.LEFT_HIP].x * w)
                l_hip_y   = int(lm.landmark[lmPose.LEFT_HIP].y * h)

                # Calculate, angles and show.
                neck_to_back = self._findAngle(l_shldr_x, l_shldr_y, l_ear_x, l_ear_y)
                body_to_back = self._findAngle(l_hip_x, l_hip_y, l_shldr_x, l_shldr_y)
                cv2.circle(image, (l_shldr_x, l_shldr_y), 7, self._RGB_yellow, -1)
                cv2.circle(image, (l_ear_x, l_ear_y), 7, self._RGB_yellow, -1)
                cv2.circle(image, (l_shldr_x, l_shldr_y - 100), 7, self._RGB_yellow, -1)
                cv2.circle(image, (r_shldr_x, r_shldr_y), 7, self._RGB_pink, -1)
                cv2.circle(image, (l_hip_x, l_hip_y), 7, self._RGB_yellow, -1)
                cv2.circle(image, (l_hip_x, l_hip_y - 100), 7, self._RGB_yellow, -1)

                # Run prediction, apply necessary changes.
                if self.model.predict([[neck_to_back, body_to_back]])[0] == 1:
                    color = self._RGB_green
                    start=time()
                    cv2.putText(image, 'Durus Bozuklugu Yok', (w - 340, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
                    end=time()
                    self.durus_duzgun.set(self.durus_duzgun.get() + (end-start))
                
                    # Apply warnings
                    if pygame.mixer.music.get_busy() :
                        pygame.mixer.music.stop()
                else:
                    color = self._RGB_red
                    start=time()
                    cv2.putText(image, 'Durusunuz Bozuk !!!', (w - 335, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
                    cv2.putText(image, 'Durusunuzu Duzeltin', (w - 335, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
                    end=time()  

                    # Apply warnings if sound is on by settings.
                    if pygame.mixer.music.get_busy() == False and self.root.shared_settings__settings["is_sound"] :
                        pygame.mixer.music.play()
                    
                    self.durus_bozuk.set(self.durus_bozuk.get() + (end-start))

                # Show the results.
                cv2.putText(image, str(int(neck_to_back)), (l_shldr_x + 10, l_shldr_y), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)
                cv2.putText(image, str(int(body_to_back)), (l_hip_x + 10, l_hip_y), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)
                cv2.line(image, (l_shldr_x, l_shldr_y), (l_ear_x, l_ear_y), color, 4)
                cv2.line(image, (l_shldr_x, l_shldr_y), (l_shldr_x, l_shldr_y - 100), color, 4)
                cv2.line(image, (l_hip_x, l_hip_y), (l_shldr_x, l_shldr_y), color, 4)
                cv2.line(image, (l_hip_x, l_hip_y), (l_hip_x, l_hip_y - 100), color, 4)

                # Colorize the image.
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

                # Check if there is a change in shared settings. Apply it if there is.
                if self.root.shared_settings__settings["is_grayscale"] :
                    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                if self.root.shared_settings__settings["is_highcontrast"] :
                    image = cv2.equalizeHist(image)
                if self.root.shared_settings__settings["is_blurr"] :
                    image = cv2.GaussianBlur(image, (5, 5), 0)
                if self.root.shared_settings__settings["is_canny"] :
                    image = cv2.Canny(image, 100, 200)
                if self.root.shared_settings__settings["is_bitwise"] :
                    image = cv2.bitwise_not(image)

                # Set the new frame to camera label.
                self.captured_image = ImageTk.PhotoImage(Image.fromarray(image).resize((640, 495), Image.ANTIALIAS))
                self.camera_view_label.configure(image=self.captured_image)

                # Update is must for root health.
                self.update()

            # Could not detect landmarks.
            except Exception as e :
                print(e)
                # Update is must for root health.
                self.update()