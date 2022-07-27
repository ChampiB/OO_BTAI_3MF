import ast


class ObjectItem:
    """
    A class representing a probabilistic object.
    """

    def __init__(self, name, obj, graph):
        """
        Construct an object item.
        :param name: the object name.
        :param obj: the object content.
        :param graph: the object graphical representation.
        """
        self.name = name
        self.obj = obj
        self.graph = graph

    def save(self, data_dir):
        """
        Save the object on file system.
        :param data_dir: the directory in which to save the object.
        :return: nothing.
        """
        self.save_dictionary(data_dir, self.obj, extension=".obj")
        self.save_dictionary(data_dir, self.graph, extension=".graph")

    def save_dictionary(self, data_dir, obj, extension):
        """
        Save the dictionary sent as input on file system.
        :param data_dir: the directory in which to save the dictionary.
        :param obj: the object to save.
        :param extension: the file extension to use.
        :return: nothing.
        """
        file_name = data_dir + "/" + self.name + extension
        file = open(file_name, mode='w')
        file.write(str(obj))
        file.close()

    def load(self, obj_file_name, graph_file_name):
        """
        Load an object from the file system.
        :param obj_file_name: the file name from which to load the object's content.
        :param graph_file_name: the file name from which to load the object's graphical representation.
        :return: nothing.
        """
        self.obj = self.load_dictionary(obj_file_name)
        self.graph = self.load_dictionary(graph_file_name)

    @staticmethod
    def load_dictionary(file_name):
        """
        Load a dictionary from the file system.
        :param file_name: the file name from which to load the dictionary.
        :return: the loaded dictionary.
        """
        # Load the dictionary.
        file = open(file_name, mode='r')
        dictionary = ast.literal_eval(file.read())
        file.close()
        return dictionary
