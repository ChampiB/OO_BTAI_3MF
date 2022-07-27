import tkinter as tk
from tkinter import messagebox
from editor.widgets.PlaceholderEntry import PlaceholderEntry


class AskParameter(tk.Toplevel):
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
        self.title('Add parameter')

        # Store the widget's parent.
        self.parent = parent

        # Create the label and text box asking the user the parameter's name.
        self.name_text = PlaceholderEntry(self, "Parameter's name")
        self.name_text.grid(row=0, column=0, padx=25, pady=10)

        # Create the label and text box asking the user the parameter's value.
        self.value_text = PlaceholderEntry(self, "Parameter's value")
        self.value_text.grid(row=1, column=0, padx=25)

        # Create the button allowing the user to add the parameter to the object.
        self.button = tk.Button(self, text="Add", command=self.add)
        self.button.grid(row=2, column=0, padx=25, pady=10, sticky="nsew")

    def add(self):
        """
        Add the parameter to the current object.
        :return: nothing.
        """
        try:
            # Add the new paramter to the current object.
            param_name = self.name_text.get()
            value = float(self.value_text.get())
            item = self.parent.obj_list.current_item()
            item.obj[param_name] = value
            item.graph[param_name] = {'x': self.parent.x, 'y': self.parent.y}
            item.save(self.parent.obj_list.data_dir)

            # Update the object canvas.
            self.parent.hide_ask_parameter()
            self.parent.display(item.obj, item.graph)

            # Close the pop-up.
            self.destroy()

        except ValueError:
            messagebox.showwarning("Warning", "The parameter value must be a valid number.")

    def reset(self):
        """
        Reset the dialog box.
        :return: nothing.
        """
        self.name_text.delete(0, 'end')
        self.value_text.delete(0, 'end')
