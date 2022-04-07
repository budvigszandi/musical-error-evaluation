from enum import IntEnum

class NotePoints(IntEnum):
  PERFECT_MATCH_POINT = 20 # Harmonics would be worth more if this were less than 17!
  CENT_DIFFERENCE_POINT = 17
  HARMONIC_POINT = 1
  UNRELATED_POINT = 0
  COVERED_NOTE_POINT = 1
  DUPLICATE_COVER_POINT = -1 # Gets reducted for each added harmonic complexity

  RELATIONSHIP_POINT_WEIGHT = 1
  COVERED_NOTE_POINT_WEIGHT = 1
  DUPLICATE_POINT_WEIGHT = 1

  MAXIMUM_HARMONIC_NUMBER = 17