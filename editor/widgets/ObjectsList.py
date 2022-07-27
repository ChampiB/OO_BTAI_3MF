from editor.widgets.ObjectItem import ObjectItem
import tkinter.ttk as ttk
import tkinter as tk
from editor.widgets.AskObject import AskObject
import glob


class ObjectsList(ttk.Treeview):
    """
    A class representing a list of object.
    """

    def __init__(self, parent, gui, data_dir="./data/objects"):
        """
        Create an object list.
        :param parent: the parent of the tree view.
        :param gui: the graphical user interface.
        :param data_dir: the directory in which the objects are stored.
        """
        super().__init__(parent, columns=["objects"], show='headings')
        self.heading("objects", text="Objects")
        self.gui = gui
        self.parent = parent
        self.objs = []
        self.load_objects(data_dir)
        self.data_dir = data_dir
        self.bind("<Button-1>", self.display_object_info)

    def display_object_info(self, event):
        """
        Display information about existing object.
        :param event: an event describing the event that triggered the call to this function.
        :return: nothing.
        """
        # Check if an object has been clicked on.
        current_item = self.identify_row(event.y)
        if current_item == "":
            return

        # Get the object that have been clicked on.
        obj_name = self.item(current_item)["values"][0]
        p_object = self.get_object(obj_name)
        if p_object is None:
            return

        # Display the object that have been clicked on.
        self.parent.obj_canvas.display(p_object.obj, p_object.graph)

    def create_new_object(self):
        """
        Create a new object.
        :return: nothing.
        """
        pop_up = AskObject(self)
        self.gui.window.wait_window(pop_up)

    def add_object(self, obj):
        """
        Add an object to the tree view.
        :param obj: the object to add.
        :return: nothing.
        """
        self.insert('', tk.END, values=[obj.name])
        self.objs.append(obj)

    def load_objects(self, data_dir):
        """
        Load the objects from the data directory.
        :param data_dir: the data directory from which the object should be loaded.
        :return: nothing.
        """
        for file_name in glob.glob(data_dir + "/*.obj"):
            # Get the object name.
            i = file_name.rfind("/")
            obj_name = file_name[i + 1:-4] if i != -1 else file_name[:-4]

            # Load the object.
            obj = ObjectItem(obj_name, {}, {})
            obj.load(file_name, file_name[:-4] + ".graph")
            self.add_object(obj)

    def get_object(self, obj_name):
        """
        Getter.
        :param obj_name: the name of the object to select.
        :return: the object corresponding to the input name.
        """
        return next((obj for obj in self.objs if obj.name == obj_name), None)

    def current_item(self):
        """
        Getter.
        :return: the object currently seleted, or None if no item is currently selected.
        """
        # Check if an object is currently selected.
        current_item = self.focus()
        if current_item == "":
            return None

        # Get the currently selected object.
        obj_name = self.item(current_item)["values"][0]
        return self.get_object(obj_name)
