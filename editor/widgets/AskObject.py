import tkinter as tk
import tkinter.ttk as ttk
from editor.widgets.ObjectItem import ObjectItem
from tkinter import messagebox
from editor.widgets.PlaceholderEntry import PlaceholderEntry


class AskObject(tk.Toplevel):
    """
    A class representing a box dialog asking the user to provide the
    name and value of a fixed parameter.
    """

    def __init__(self, parent):
        """
        Create a box dialog asking the user to provide the name and value of a fixed parameter.
        :param parent: the parent of the tree view.
        """
        # Call the constructor.
        super().__init__()

        # Change the title.
        self.title('New object')

        # Store the widget's parent.
        self.parent = parent

        # Create the label and text box asking the user the parameter's name.
        self.name_text = PlaceholderEntry(self, "Object's name")
        self.name_text.grid(row=0, column=0, padx=10, pady=10)

        # Create the label and text box asking the user the parameter's value.
        self.is_on = tk.IntVar()
        self.is_on.set(0)
        self.switch_btn = ttk.Checkbutton(self, text='Temporal slice', variable=self.is_on, onvalue=1, offvalue=0)
        self.switch_btn.grid(row=1, column=0, padx=10, sticky="nsew")

        # Create the button allowing the user to add the parameter to the object.
        self.button = ttk.Button(self, text="Create", command=self.add)
        self.button.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)

    def add(self):
        """
        Add the parameter to the current object.
        :return: nothing.
        """
        # Check if the object name provided by the user is correct.
        obj_name = self.name_text.get()
        if obj_name.find("[") != -1 or obj_name.find("]") != -1:
            messagebox.showwarning("Warning", "The object can not contain a square bracket.")
            return
        if obj_name is None or obj_name == "":
            messagebox.showwarning("Warning", "The object name must be an non-empty string.")
            return

        # Update the object name if it is a temporal slice.
        if self.is_on.get() == 1:
            obj_name = "[TS] " + obj_name

        # Add a new object in the list.
        obj = ObjectItem(obj_name, {}, {})
        obj.save(self.parent.data_dir)
        self.parent.add_object(obj)

        # Close the pop-up.
        self.destroy()

    def reset(self):
        """
        Reset the dialog box.
        :return: nothing.
        """
        self.name_text.delete(0, 'end')
        if self.is_on.get() == 1:
            self.is_on.set(0)
