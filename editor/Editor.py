import tkinter as tk
import tkinter.ttk as ttk
from editor.frames.ObjectsFrame import ObjectsFrame


#
# A class representing the editor used to create probabilitic objects.
#
class Editor:

    def __init__(self):
        """
        Construct the graphical user interface used to create probabilitic objects.
        """

        # Create the main window.
        self.window = tk.Tk()
        self.window.title("OO_BTAI_3MF editor")
        self.window.geometry(self.get_screen_size())
        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_columnconfigure(0, weight=1)

        # Colors.
        self.white = "#ffffff"
        self.gray = "#818589"
        self.black = "#000000"

        # Set the windows style.
        style = ttk.Style(self.window)
        self.window.tk.call("source", "./data/theme/ttk-Breeze/breeze.tcl")
        style.theme_use("Breeze")
        style.configure("Placeholder.TEntry", foreground=self.gray)

        # Create the frame container.
        self.container = tk.Frame(self.window)
        self.container.grid(row=0, column=0, sticky="nsew")

        # The dictionary of frames' constructor.
        self.frames_classes = {
            "ObjectsFrame": ObjectsFrame,
        }

        # The list of currently loaded frames.
        self.frames = {}
        self.current_frame = None

        # Show the page used to load the model and dataset.
        self.show_frame("ObjectsFrame")

    def get_screen_size(self):
        """
        Getter.
        :return: the screen' size.
        """
        screen_size = str(self.window.winfo_screenwidth() - 85)
        screen_size += "x"
        screen_size += str(self.window.winfo_screenheight() - 75)
        screen_size += "+85+35"
        return screen_size

    def show_frame(self, frame_name):
        """
        Show a frame for the given frame name.
        :param frame_name: the name of the frame to show.
        :return: nothing.
        """
        # Construct the frame if it does not already exist.
        if frame_name not in self.frames.keys():
            frame = self.frames_classes[frame_name](parent=self.container, gui=self)
            self.frames[frame_name] = frame

        # Display the requested frame.
        if self.current_frame is not None:
            self.current_frame.grid_forget()
        self.current_frame = self.frames[frame_name]

        self.current_frame.grid(row=0, column=0, sticky="nsew")
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        self.current_frame.refresh()
        self.current_frame.tkraise()

    def loop(self):
        """
        Launch the main loop of the graphical user interface.
        :return: nothing.
        """
        self.window.mainloop()
