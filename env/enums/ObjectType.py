from enum import IntEnum


class ObjectType(IntEnum):
    """
    An enum representing an object type.
    """
    WALL = 1
    WARRIOR = 2
    MAGE = 4
    SWORD = 8
    MAGIC_WAND = 16
