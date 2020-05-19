from enum import Enum

class ClientTypeEnum(Enum):
    Email = 100
    Github = 101
    Twitter = 102

class AuthTypeEnum(Enum):
    USER = 1
    ADMIN = 2


class ScopeTypeEnum(Enum):
    RestrictScope = 0
    UserScope = 1
    AdminScope = 2