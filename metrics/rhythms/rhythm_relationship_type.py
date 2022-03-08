from enum import Enum, auto

class DistanceType(Enum):
  SAME = auto()
  DELETION = auto()
  INSERTION = auto()
  SUBSTITUTION = auto()