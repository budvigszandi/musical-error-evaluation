from enum import Enum, auto

class RhythmRelationshipType(Enum):
  SAME = auto()
  DELETION = auto()
  INSERTION = auto()
  SUBSTITUTION = auto()