import music21 as m21

CHORD_NOTE_SWITCH_POINT = 0
REST_SOUND_SWITCH_POINT = 0

# TODO: Continue point system
def get_harmonic_part_distance(source, target):
  distance = 0
  is_chord_note_switch = (source.isNote and target.isChord) or (source.isChord and target.isNote)
  is_rest_sound_switch = (source.isRest and (not target.isRest)) or ((not source.isRest) and target.isRest)
  if is_chord_note_switch:
    distance += CHORD_NOTE_SWITCH_POINT
  if is_rest_sound_switch:
    distance += REST_SOUND_SWITCH_POINT
  # if source.quarterLength != target.quarterLength:
  #   if source.quarterLength > target.quarterLength:
  #     distance += (source.quarterLength - target.quarterLength) * LENGTH_DIFFERENCE_WEIGHT
  #   else:
  #     distance += (target.quarterLength - source.quarterLength) * LENGTH_DIFFERENCE_WEIGHT
  return distance
