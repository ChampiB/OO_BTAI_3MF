import tkinter as tk
from editor.widgets.DropDownMenu import DropDownMenu
from editor.widgets.AskParameter import AskParameter


class ObjectCanvas(tk.Canvas):
    """
    A class representing a canvas displaying a probabilistic object.
    """

    def __init__(self, parent, gui, obj_list):
        """
        Contruct a canvas displaying a probabilistic object.
        :param parent: the parent of the tree view.
        :param gui: the graphical user interface.
        :param obj_list: the widget representing the list of probabilistic objects.
        """

        # Call parent constructor.
        super().__init__(
            parent, bg=gui.white, width=100, height=100,
            highlightbackground=gui.black, highlightthickness=2
        )

        # Store the object list and graphical user interface.
        self.obj_list = obj_list
        self.gui = gui

        # Create the tags corresponding to the object inside the canvas.
        self.tags = []

        # The label correponding to an empty object.
        empty_text = "The current object is empty, left click on the canvas to design the object content."
        self.empty_text_label = tk.Label(self, text=empty_text, bg=gui.white)

        # Create the drop-down menu.
        self.menu = DropDownMenu(self, [
            "Add fixed parameter",
            "Add categorical variable"
        ], [
            self.add_fixed_parameter,
            self.add_categorical_variable
        ])

        # Store the x, y position on click, and the object being drag and dropped.
        self.x = -1
        self.y = -1
        self.clicked_param_name = None

        # Handle the left click of the user.
        self.bind("<Button-1>", self.handle_left_click)
        self.bind("<B1-Motion>", self.move_parameter)
        self.bind("<ButtonRelease-1>", self.reset_clicked_param_name)
        self.bind("<Button-2>", self.display_drop_down_menu)
        self.bind("<Button-3>", self.display_drop_down_menu)

    def handle_left_click(self, event):
        """
        Handle the left click from the user.
        :param event: the event that triggered the call to this function.
        :return: nothing.
        """
        self.hide_all_pop_up()
        self.x = event.x
        self.y = event.y
        self.clicked_param_name = self.get_param_name(event.x, event.y)

    def get_param_name(self, x, y):
        """
        Getter.
        :param x: the position in x.
        :param y: the position in y.
        :return: the name of the parameter located in position (x, y).
        """
        obj_name = self.obj_list.current_item().name
        for param_name, graph in self.obj_list.get_object(obj_name).graph.items():
            if x - 10 < graph["x"] < x + 10 and y - 10 < graph["y"] < y + 10:
                return param_name
        return None

    def move_parameter(self, event):
        """
        Move the parameter that have been on.
        :param event: the event that triggered the event.
        :return: nothing.
        """
        # Check if an object can be moved.
        if self.clicked_param_name is None:
            return
        if self.x < 0 or self.y < 0:
            return

        # Move the object.
        x_shift = event.x - self.x
        y_shift = event.y - self.y
        item = self.obj_list.current_item()
        item.graph[self.clicked_param_name]["x"] += x_shift
        item.graph[self.clicked_param_name]["y"] += y_shift
        self.display(item.obj, item.graph)

        # Update the x and y position of the mouse.
        self.x = event.x
        self.y = event.y

    def reset_clicked_param_name(self, event):
        """
        Reset the name of the clicked parameter to None.
        :param event: the event that triggered the event.
        :return: nothing.
        """
        if self.clicked_param_name is not None:
            self.obj_list.current_item().save(self.obj_list.data_dir)
        self.clicked_param_name = None

    def hide(self, tag):
        """
        Hide the object corresponding to the input tag.
        :param tag: the tag that must be hide.
        :return: nothing.
        """
        if tag not in self.tags:
            return
        self.delete(tag)
        self.tags.remove(tag)

    def hide_drop_down_menu(self, event=None):
        """
        Hide the drop-down menu that allows the user to design the object.
        :param event: the event that triggered the call to this function.
        :return: nothing.
        """
        self.hide("drop_down_menu")

    def hide_ask_parameter(self):
        """
        Hide the ask parameter dialog.
        :return: nothing.
        """
        self.hide("ask_parameter")

    def hide_all_pop_up(self):
        """
        Hide the all dialog boxes.
        :return: nothing.
        """
        self.hide_drop_down_menu()
        self.hide_ask_parameter()

    def display_drop_down_menu(self, event):
        """
        Display the drop-down menu, allowing the user to design the object.
        :param event: the event that triggered the call to this function.
        :return: nothing.
        """
        if self.obj_list.current_item() is None:
            return
        self.hide_all_pop_up()
        self.x = event.x
        self.y = event.y
        self.create_window(event.x, event.y, window=self.menu, tags="drop_down_menu")
        self.tags.append("drop_down_menu")

    def add_fixed_parameter(self):
        """
        Add a fixed parameter to the object.
        :return: nothing.
        """
        self.hide_all_pop_up()
        pop_up = AskParameter(self)
        self.gui.window.wait_window(pop_up)

    def add_categorical_variable(self):
        self.hide_all_pop_up()
        print("add categorical variable")
        # TODO
        pass

    def draw_parameter(self, param_name, x=None, y=None):
        """
        Draw a parameter in the canvas.
        :param param_name: the name of the parameter to display.
        :param x: the x position where the parameter should be diaplayed (if None, x = self.x).
        :param y: the y position where the parameter should be diaplayed (if None, y = self.y).
        :return: nothing.
        """
        x = self.x if x is None else x
        y = self.y if y is None else y
        r = 5
        circle_tag = "circle_{}".format(param_name)
        text_tag = "text_{}".format(param_name)
        self.create_oval(x - r, y - r, x + r, y + r, fill=self.gui.black, tags=circle_tag)
        self.create_text(x, y - 15, text=param_name, tags=text_tag)
        self.tags.append(circle_tag)
        self.tags.append(text_tag)

    def display_current_object(self):
        """
        Display the object which is currently active in the object list.
        :return: nothing.
        """
        item = self.obj_list.current_item()
        self.display(item.obj, item.graph)

    def display(self, obj, graph):
        """
        Display the object in the canvas.
        :param obj: the object to be displayed.
        :param graph: the graphical representation of the object.
        :return: nothing.
        """
        # Delete all the object corresponding to the previous objects.
        for tag in self.tags:
            self.delete(tag)
        self.tags.clear()

        # If no object is provided as input, simply return.
        if obj is None:
            return

        # Display an empty object.
        if obj == {}:
            tag = "empty_obj"
            self.tags.append(tag)
            pos_x = int(self.winfo_width() / 2)
            pos_y = int(self.winfo_height() / 2)
            self.create_window(pos_x, pos_y, window=self.empty_text_label, tags=tag)
            return

        # Display a non-empty object.
        for param_name, _ in obj.items():
            x = graph[param_name]["x"]
            y = graph[param_name]["y"]
            self.draw_parameter(param_name, x, y)
