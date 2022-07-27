from env.enums.ObjectType import ObjectType
from env.enums.Action import Action
from env.weapons.MagicWand import MagicWand
from env.weapons.BearHand import BearHand


class Mage:
    """
    A class representing a mage.
    """

    def __init__(self, x, y):
        """
        Create a mage at position (x, y).
        :param x: the x position of the mage.
        :param y: the y position of the mage.
        """
        self.x = x
        self.y = y
        self.is_attacking = False
        self.weapon = BearHand()
        self.lp = 100

    def perform(self, action, env):
        """
        Perform an action in the environment.
        :param action: the action to perform.
        :param env: the environment in which to perform the action.
        :return: nothing.
        """
        actions_fn = {
            Action.UP: self.up,
            Action.DOWN: self.down,
            Action.RIGHT: self.right,
            Action.LEFT: self.left,
            Action.PICK_UP: self.pick_up,
            Action.ATTACK: self.attack,
        }
        actions_fn[action](self, env)

    def take_damage(self, damage):
        """
        Decrease the warrior's life points.
        :param damage: the number of life to remove.
        :return: nothing.
        """
        self.lp -= damage
        if self.lp < 0:
            self.lp = 0

    @staticmethod
    def up(self, env):
        """
        Move to upward.
        :param self: the agent performing the action.
        :param env: the environment in which the action is performed.
        :return: nothing.
        """
        self.is_attacking = False
        if not env.is_valid_pos(self.x, self.y - 1):
            return
        env.remove(ObjectType.MAGE, env.map, self.x, self.y)
        self.y -= 1
        env.add(ObjectType.MAGE, env.map, self.x, self.y)

    @staticmethod
    def down(self, env):
        """
        Move to downward.
        :param self: the agent performing the action.
        :param env: the environment in which the action is performed.
        :return: nothing.
        """
        self.is_attacking = False
        if not env.is_valid_pos(self.x, self.y + 1):
            return
        env.remove(ObjectType.MAGE, env.map, self.x, self.y)
        self.y += 1
        env.add(ObjectType.MAGE, env.map, self.x, self.y)

    @staticmethod
    def right(self, env):
        """
        Move to the right.
        :param self: the agent performing the action.
        :param env: the environment in which the action is performed.
        :return: nothing.
        """
        self.is_attacking = False
        if not env.is_valid_pos(self.x + 1, self.y):
            return
        env.remove(ObjectType.MAGE, env.map, self.x, self.y)
        self.x += 1
        env.add(ObjectType.MAGE, env.map, self.x, self.y)

    @staticmethod
    def left(self, env):
        """
        Move to the left.
        :param self: the agent performing the action.
        :param env: the environment in which the action is performed.
        :return: nothing.
        """
        self.is_attacking = False
        if not env.is_valid_pos(self.x - 1, self.y):
            return
        env.remove(ObjectType.MAGE, env.map, self.x, self.y)
        self.x -= 1
        env.add(ObjectType.MAGE, env.map, self.x, self.y)

    @staticmethod
    def pick_up(self, env):
        """
        Pick up the surronding weapon.
        :param self: the agent performing the action.
        :param env: the environment in which the action is performed.
        :return: nothing.
        """
        self.is_attacking = False
        if env.is_obj_at(ObjectType.MAGIC_WAND, env.map, self.x, self.y):
            env.remove(ObjectType.MAGIC_WAND, env.map, self.x, self.y)
            self.weapon = MagicWand()

    @staticmethod
    def attack(self, env):
        """
        Attack the surronding characters.
        :param self: the agent performing the action.
        :param env: the environment in which the action is performed.
        :return: nothing.
        """
        self.is_attacking = True
        characters = env.get_characters(self.x, self.y, self.weapon.range)
        for character in characters:
            if character != self:
                character.take_damage(self.weapon.damage)
