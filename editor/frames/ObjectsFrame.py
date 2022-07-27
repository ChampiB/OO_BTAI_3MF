import tkinter as tk
from editor.widgets.ObjectCanvas import ObjectCanvas
from editor.widgets.ObjectsList import ObjectsList


class ObjectsFrame(tk.Frame):
    """
    Class representing the frame used to create probabilistic objects.
    """

    def __init__(self, parent, gui):
        """
        Construct the objects-creation frame.
        :param parent: the parent widget.
        :param gui: the graphical user interface.
        """
        tk.Frame.__init__(self, parent)

        # Store graphical user interface.
        self.gui = gui

        # Set the weights of each row and column.
        self.grid_rowconfigure(0, weight=100)
        self.grid_rowconfigure(1, weight=2)
        self.grid_columnconfigure(0, weight=5)
        self.grid_columnconfigure(1, weight=100)

        # Create a list of objects.
        self.obj_list = ObjectsList(self, gui)
        self.obj_list.grid(column=0, row=0, sticky='nsew')

        # Create a button to add object to the list.
        self.new_obj_btn = tk.Button(self, text='Create new object', command=self.obj_list.create_new_object)
        self.new_obj_btn.grid(column=0, row=1, sticky='nsew')

        # Create an object canvas to display the object in the list.
        self.obj_canvas = ObjectCanvas(self, gui, self.obj_list)
        self.obj_canvas.grid(column=1, row=0, rowspan=2, sticky='nsew')

    def refresh(self):
        """
        Refresh the object-creation frame.
        :return: nothing.
        """
        pass
