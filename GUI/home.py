from    Utilities   import  get_gif_frame_count
from    PIL         import  ImageTk, Image
from    tkinter     import  ttk

class Home(ttk.Frame) :
    """
    Frame Class, that contains home page gif preview.
    @Inherits: ttk.Frame
    """
    def __init__(self, parent, root, *args, **kwargs) -> None:
        """
        Constructor Method of the Home Frame Class.
        """
        super().__init__(parent, *args, **kwargs)
        
        self.root = root
        self.parent = parent

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.container = ttk.Frame(self)
        self.container.grid(row=0, column=0, sticky="nsew")

        self.container.rowconfigure(0, weight=1)
        self.container.columnconfigure(0, weight=1)

        self.animation_length = get_gif_frame_count("Assets/Other/home animation.gif")

        self.animation_frames = [None] * self.animation_length

        # Set up animation frames
        for i in range(self.animation_length) :
            img = Image.open("Assets/Other/home animation.gif")
            img.seek(i)
            img = img.resize((800, 580), Image.ANTIALIAS)
            self.animation_frames[i] = ImageTk.PhotoImage(img)

        self.animation_index = 0

        self.current_animation_image = self.animation_frames[self.animation_index]

        self.animation_label = ttk.Label(self.container, image=self.current_animation_image)
        self.animation_label.grid(row=0, column=0)

        # Start animation loop | MUST assign to variable to delete later
        self.anim = self.after(0, self._animate)

    def _animate(self) -> None:
        """
        Recursive Private Class Method, that animates the gif.
        @Params:
            None
        @Returns:
            None
        """
        # Base condition
        self.animation_index += 1
        if self.animation_index == self.animation_length :
            self.animation_index = 0
        # Update image
        self.current_animation_image = self.animation_frames[self.animation_index]
        self.animation_label.configure(image=self.current_animation_image)
        # Recursive Call
        self.anim = self.after(60, self._animate)