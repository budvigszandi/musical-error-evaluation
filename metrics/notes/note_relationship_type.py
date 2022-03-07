from enum import Enum, auto

class NoteRelationshipType(Enum):
  PERFECT_MATCH = auto()
  HARMONIC = auto()
  CENT_DIFFERENCE = auto()
  UNRELATED = auto()