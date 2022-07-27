import random
import torch
from PIL import Image
from env.viewer.ArenaViewer import ArenaViewer
from env.weapons.BearHand import BearHand
from env.characters.Mage import Mage
from env.characters.Warrior import Warrior
from env.enums.ObjectType import ObjectType


class ArenaEnv:
    """
    A class representing an area in which some agents can fight.
    """

    def __init__(self, config, data_dir="./data/"):
        """
        Create an arena environment.
        :param config: the configuration of the environment.
        :param data_dir: the directory containing the sprites of the environment.
        :return: nothing.
        """

        # Store the arena configuration.
        self.width = config["width"] if "width" in config.keys() else 5
        self.height = config["height"] if "height" in config.keys() else 5
        self.n_warriors = config["n_warriors"] if "n_warriors" in config.keys() else 1
        self.n_mages = config["n_mages"] if "n_mages" in config.keys() else 1
        self.n_swords = config["n_swords"] if "n_swords" in config.keys() else 1
        self.n_wands = config["n_magic_wands"] if "n_magic_wands" in config.keys() else 1
        self.n_walls = config["n_walls"] if "n_walls" in config.keys() else 5

        # Create a list of warriors and a list of mages.
        self.warriors = []
        self.mages = []

        # Create the arena.
        self.initial_map = torch.zeros([self.height, self.width], dtype=torch.int)
        self.change_map()
        self.map = self.initial_map.clone()

        # Load the sprites.
        w_size = int(500 / self.width)
        h_size = int(500 / self.height)
        self.size = (w_size, h_size)
        self.sprites = self.load_sprites(data_dir, self.size)

        # Graphical interface
        self.viewer = None

    def change_map(self):
        """
        Change the topology of the arena.
        :return: nothing.
        """
        # Create an empty arena.
        self.initial_map = torch.zeros([self.height, self.width], dtype=torch.int)

        # Add the walls in the arena.
        for _ in range(0, self.n_walls):
            self.add_object_to_initial_map(ObjectType.WALL, self.can_add_wall)

        # Add the warriors in the arena.
        for _ in range(0, self.n_warriors):
            self.add_object_to_initial_map(ObjectType.WARRIOR, self.can_add_object)

        # Add the mages in the arena.
        for _ in range(0, self.n_mages):
            self.add_object_to_initial_map(ObjectType.MAGE, self.can_add_object)

        # Add the magic wands in the arena.
        for _ in range(0, self.n_wands):
            self.add_object_to_initial_map(ObjectType.MAGIC_WAND, self.can_add_object)

        # Add the sword in the arena.
        for _ in range(0, self.n_swords):
            self.add_object_to_initial_map(ObjectType.SWORD, self.can_add_object)

    def add_object_to_initial_map(self, obj_type, can_add_obj):
        """
        Add an object in the arena.
        :param obj_type: the type of object to add.
        :param can_add_obj: the function used to check if an object can be added at position (x, y).
        :return: nothing.
        """
        x = -1
        y = -1
        while not can_add_obj(obj_type, x, y, self.initial_map):
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
        self.add(obj_type, self.initial_map, x, y)

    def can_add_object(self, obj_type, x, y, arena):
        """
        Check if an object can be added in an arena.
        :param obj_type: the type of object to add.
        :param x: the x position where the object should be added.
        :param y: the y position where the object should be added.
        :param arena: the arena where the object should be added.
        :return: True, if the object can be added in an arena, False otherwise.
        """
        # If the (x, y) position is not valid, return False
        if x < 0 or y < 0 or x >= self.width or y >= self.height:
            return False

        # Return False if there is already an object of this type at position (x, y)
        # or if there is a wall at position (x, y).
        return not self.is_obj_at(ObjectType.WALL, arena, x, y) and \
            not self.is_obj_at(obj_type, arena, x, y)

    def can_add_wall(self, obj_type, x, y, arena):
        """
        Check if a wall can be added in an arena without disconnecting two parts of the arena.
        :param x: the x position where the wall should be added.
        :param y: the y position where the wall should be added.
        :param arena: the arena where the wall should be added.
        :param obj_type: unused.
        :return: True, if the wall can be added in an arena, False otherwise.
        """
        # If the (x, y) position is not valid, return False
        if x < 0 or y < 0 or x >= self.width or y >= self.height:
            return False

        # If there is already an object at position (x, y), return False
        if arena[y][x]:
            return False

        # If the addition of the wall split the arena in two, return False
        copy_arena = arena.clone()
        self.add(ObjectType.WALL, copy_arena, x, y)
        no_wall_pos = []
        for xi in range(0, self.width):
            for yi in range(0, self.height):
                if not self.is_obj_at(ObjectType.WALL, copy_arena, xi, yi):
                    no_wall_pos.append((xi, yi))
        return self.are_connected(no_wall_pos)

    def are_connected(self, positions):
        """
        Check if all the positions sent as input as connected.
        :param positions: the positions for which need to check connectivity.
        :return: True, if all input positions are connected, False otherwise.
        """
        # If there are zero or one cell without a wall, return True.
        if len(positions) <= 1:
            return True

        # Return True if all the position are connected.
        actions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        connected_pos = [positions[0]]
        while len(connected_pos):
            pos = connected_pos.pop(0)
            if pos not in positions:
                continue
            positions.pop(positions.index(pos))
            for action in actions:
                x = pos[0] + action[0]
                y = pos[1] + action[1]
                if 0 <= x < self.width and 0 <= y < self.height and (x, y) in positions:
                    connected_pos.append((x, y))
        return len(positions) == 0

    def is_obj_at(self, obj_type, arena, x, y):
        """
        Check if an object is in the arena at position (x, y).
        :param obj_type: the object type.
        :param arena: the arena in which the object may be.
        :param x: the position in x where the object may be.
        :param y: the position in y where the object may be.
        :return: True, if the object is in the arena at position (x, y), False otherwise.
        """
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return False
        return arena[y][x] & obj_type

    def is_valid_pos(self, x, y):
        """
        Check if the input position is valid.
        :param x: the x position.
        :param y: the y position.
        :return: True, if a character cam move to position (x, y), False otherwise.
        """
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return False
        if self.is_obj_at(ObjectType.WALL, self.map, x, y):
            return False
        return True

    @staticmethod
    def add(obj_type, arena, x, y):
        """
        Add an object into the arena provided as input.
        :param obj_type: the type of object to add.
        :param arena: the arena in which to add the object.
        :param x: the position in x where the object should be added.
        :param y: the position in y where the object should be added.
        :return: nothing.
        """
        arena[y][x] |= obj_type

    @staticmethod
    def remove(obj_type, arena, x, y):
        """
        Remove an object from the arena provided as input.
        :param obj_type: the type of object to remove.
        :param arena: the arena in which to remove the object.
        :param x: the position in x where the object should be removed.
        :param y: the position in y where the object should be removed.
        :return: nothing.
        """
        arena[y][x] &= ~obj_type

    def reset(self, new_map=False):
        """
        Reset the environment to its initial state.
        :param new_map: True, if a new arena should be created, False otherwise.
        :return: nothing.
        """
        # Reset the arena.
        if new_map:
            self.change_map()
        self.map = self.initial_map.clone()

        # Reset the characters.
        self.warriors.clear()
        self.mages.clear()
        for x in range(0, self.width):
            for y in range(0, self.height):
                if self.is_obj_at(ObjectType.WARRIOR, self.map, x, y):
                    self.warriors.append(Warrior(x, y))
                if self.is_obj_at(ObjectType.MAGE, self.map, x, y):
                    self.mages.append(Mage(x, y))

    @staticmethod
    def load_sprites(data_dir, size=(64, 64)):
        """
        Load the sprites of the environment.
        :data_dir: the directory from which to load the sprites.
        :size: the size of the sprites to load.
        :return: the sprites.
        """
        return {
            "dead_warrior": Image.open(data_dir + "dead_warrior.png").resize(size),
            "warrior": Image.open(data_dir + "warrior.png").resize(size),
            "warrior_sword": Image.open(data_dir + "warrior_sword.png").resize(size),
            "warrior_sword_attack": Image.open(data_dir + "warrior_sword_attack.png").resize(size),
            "sword": Image.open(data_dir + "sword.png").resize(size),
            "dead_mage": Image.open(data_dir + "dead_mage.png").resize(size),
            "mage": Image.open(data_dir + "mage.png").resize(size),
            "mage_wand": Image.open(data_dir + "mage_wand.png").resize(size),
            "mage_wand_attack": Image.open(data_dir + "mage_wand_attack.png").resize(size),
            "wand": Image.open(data_dir + "wand.png").resize(size),
            "empty": Image.open(data_dir + "empty.png").resize(size),
            "wall": Image.open(data_dir + "wall.png").resize(size)
        }

    def render(self):
        """
        Display the current state of the environment as an image.
        :return: nothing.
        """

        # Gather the images to display.
        imgs = []
        for y in range(0, self.height):
            imgs.append([])
            for x in range(0, self.width):
                imgs[y].append(self.get_sprite(x, y))

        # Gather the life point to display.
        warriors_lps = []
        for warrior in self.warriors:
            warriors_lps.append(warrior.lp)
        mages_lps = []
        for mage in self.mages:
            mages_lps.append(mage.lp)

        # Update the viewer.
        if self.viewer is None:
            self.viewer = ArenaViewer('Arena', imgs, warriors_lps, mages_lps)
        else:
            self.viewer.update(imgs, warriors_lps, mages_lps)

    def get_sprite(self, x, y):
        """
        Getter.
        :param x: the x position.
        :param y: the y position.
        :return: the sprite that must be displayed at position (x, y).
        """

        # Get the cell that must be displayed.
        cell = self.map[y][x]

        # Get the sprites that must be displayed.
        if cell == 0:
            return self.sprites["empty"]
        if cell == ObjectType.WALL:
            return self.sprites["wall"]
        if cell & ObjectType.WARRIOR:
            warrior = self.get_warrior(x, y)
            if warrior.lp <= 0:
                return self.sprites["dead_warrior"]
            elif isinstance(warrior.weapon, BearHand):
                return self.sprites["warrior"]
            elif not isinstance(warrior.weapon, BearHand) and not warrior.is_attacking:
                return self.sprites["warrior_sword"]
            else:
                return self.sprites["warrior_sword_attack"]
        if cell & ObjectType.MAGE:
            mage = self.get_mage(x, y)
            if mage.lp <= 0:
                return self.sprites["dead_mage"]
            elif isinstance(mage.weapon, BearHand):
                return self.sprites["mage"]
            elif not isinstance(mage.weapon, BearHand) and not mage.is_attacking:
                return self.sprites["mage_wand"]
            else:
                return self.sprites["mage_wand_attack"]
        if cell & ObjectType.SWORD:
            return self.sprites["sword"]
        if cell & ObjectType.MAGIC_WAND:
            return self.sprites["wand"]
        raise Exception("Error: Unknown sprite.")

    def get_characters(self, x, y, distance):
        """
        Getter.
        :param x: the x position around to select character.
        :param y: the y position around to select character.
        :param distance: the distance below which character are selected.
        :return: the character within a certain distance of position (x, y).
        """
        characters = []
        for warrior in self.warriors:
            if self.manhattan_distance(x, y, warrior.x, warrior.y) <= distance:
                characters.append(warrior)
        for mage in self.mages:
            if self.manhattan_distance(x, y, mage.x, mage.y) <= distance:
                characters.append(mage)
        return characters

    def manhattan_distance(self, x1, y1, x2, y2):
        """
        Compute the Manhattan distance between (x1, y1) and (x2, y2).
        :param x1: the first x position.
        :param y1: the first y position.
        :param x2: the second x position.
        :param y2: the second y position.
        :return: The Manhattan distance between (x1, y1) and (x2, y2).
        """
        return abs(x1 - x2) + abs(y1 - y2)

    def get_warrior(self, x, y):
        """
        Getter.
        :param x: the x position of the warrior.
        :param y: the y position of the warrior.
        :return: a warrior at position (x, y).
        """
        for warrior in self.warriors:
            if warrior.x == x and warrior.y == y:
                return warrior
        raise Exception("Error: could not find warrior at position ({}, {}).".format(x, y))

    def get_mage(self, x, y):
        """
        Getter.
        :param x: the x position of the mage.
        :param y: the y position of the mage.
        :return: a mage at position (x, y).
        """
        for mage in self.mages:
            if mage.x == x and mage.y == y:
                return mage
        raise Exception("Error: could not find mage at position ({}, {}).".format(x, y))

    def done(self):
        """
        Getter.
        :return: True if the environment is over, False otherwise.
        """
        # TODO
        return False

    def execute(self, action):
        """
        Execute an action in the environment.
        :param action: the action to perform.
        :return: the new observation.
        """
        for (ctype, cid), action in action.items():
            if ctype == "warrior":
                if self.warriors[cid].lp > 0:
                    self.warriors[cid].perform(action, self)
            elif ctype == "mage":
                if self.mages[cid].lp > 0:
                    self.mages[cid].perform(action, self)
            else:
                raise Exception("Error: Unknown character type.")

        return None  # TODO
