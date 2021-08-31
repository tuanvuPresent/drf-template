from enum import Enum


class UserGender(Enum):
    MALE = 0
    FEMALE = 1
    OTHER = 2


class UserType(Enum):
    STAFF = 0
    LEADER = 1
    ADMIN = 2
    CEO = 3
