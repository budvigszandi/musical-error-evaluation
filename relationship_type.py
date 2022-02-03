from enum import Enum, auto

class RelationshipType(Enum):
  PERFECT_MATCH = auto()
  HARMONIC = auto()
  CENT_DIFFERENCE = auto()
  UNRELATED = auto()