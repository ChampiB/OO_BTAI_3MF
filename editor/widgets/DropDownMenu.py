import tkinter as tk


class DropDownMenu(tk.Frame):

    def __init__(self, parent, choice_labels, callbacks):
        """
        Create a drop-down menu.
        :param parent: the parent of the widget.
        :param choice_labels: the label of the various choices to display on the buttons.
        :param callbacks: the function to call when the buttons are clicked.
        """
        # Call parent constructor.
        super().__init__(parent, highlightbackground=parent.gui.gray, highlightthickness=2)

        # Create a button for each choice proposed to the user.
        self.buttons = []
        for i, (choice_label, callback) in enumerate(zip(choice_labels, callbacks)):
            button = tk.Button(self, text=choice_label, command=callback)
            button.grid(row=i, column=0, sticky="nsew")
            self.buttons.append(button)
