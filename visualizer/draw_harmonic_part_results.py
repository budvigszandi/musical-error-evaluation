import music21 as m21
from input.midi_reader import put_sheet_in_output_folder
from metrics.distances.distance_type import DistanceType
from metrics.rhythms.evaluate_rhythms import get_rhythmic_distance
from visualizer.harmonic_part_colors import HarmonicPartColors
from metrics.notes.note_relationship_type import NoteRelationshipType

def draw_harmonic_part_differences_from_steps(source, target, steps, note_evaluation):
  current_source_index = 0
  current_target_index = 0
  notation_string = ""

  for i in range(len(steps)):
    current_step = steps[i]
    current_source = source[current_source_index]
    current_target = target[current_target_index]

    if current_step == DistanceType.DELETION:
      print("deleted", current_source)
      print()

      if current_source.isNote:
        notation_string += get_current_notation(current_source, HarmonicPartColors.RED, DistanceType.DELETION, False)
      elif current_source.isChord:
        notation_string += "chord{"
        for note in current_source:
          notation_string += get_current_notation(note, HarmonicPartColors.RED, DistanceType.DELETION, False)
        notation_string += "} "
      elif current_source.isRest:
        notation_string += "r" + HarmonicPartColors.RED.value + " "
      
      if current_source_index < len(source) - 1:
        current_source_index += 1

    elif current_step == DistanceType.INSERTION:
      print("inserted", current_target)
      print()

      if current_target.isNote:
        notation_string += get_current_notation(current_target, HarmonicPartColors.BLUE, DistanceType.INSERTION, False)
      elif current_target.isChord:
        notation_string += "chord{"
        for note in current_target:
          notation_string += get_current_notation(note, HarmonicPartColors.BLUE, DistanceType.INSERTION, False)
        notation_string += "} "
      elif current_target.isRest:
        notation_string += "r" + HarmonicPartColors.BLUE.value + " "

      if current_target_index < len(target) - 1:
        current_target_index += 1

    elif current_step == DistanceType.SAME:
      print("got match", current_source)
      print()

      if current_source.isNote:
        notation_string += get_current_notation(current_source, HarmonicPartColors.BLACK, DistanceType.SAME, False)
      elif current_source.isChord:
        notation_string += "chord{"
        for note in current_source:
          notation_string += get_current_notation(note, HarmonicPartColors.BLACK, DistanceType.SAME, False)
        notation_string += "} "
      elif current_source.isRest:
        notation_string += "r" + HarmonicPartColors.BLACK.value + " "

      if current_source_index < len(source) - 1:
        current_source_index += 1
      if current_target_index < len(target) - 1:
        current_target_index += 1

    elif current_step == DistanceType.SUBSTITUTION:
      print("wanted", current_source, "got", current_target)
      print("difference:")
      note_eval = note_evaluation[current_source_index]
      rhythmic_distance = get_rhythmic_distance(current_source, current_target)
      is_rhythm_different = rhythmic_distance > 0

      if current_source.isChord or current_target.isChord:
        notation_string += "chord{"
      
      if note_eval != None and not (current_source.isRest or current_target.isRest):
        uncovered_notes = get_uncovered_notes(current_source, note_eval)
        for pitch in uncovered_notes:
          note = get_note_from_pitch(current_source, pitch)
          notation_string += get_current_notation(note, HarmonicPartColors.RED, DistanceType.DELETION, is_rhythm_different)
        for relationship in note_eval:
          print(relationship)
          note = get_note_from_pitch(current_target, relationship.given_note)
          if relationship.type == NoteRelationshipType.PERFECT_MATCH:
            notation_string += get_current_notation(note, HarmonicPartColors.BLACK, DistanceType.SUBSTITUTION, is_rhythm_different)
          elif relationship.type == NoteRelationshipType.CENT_DIFFERENCE:
            notation_string += get_current_notation(note, HarmonicPartColors.YELLOW, DistanceType.SUBSTITUTION, is_rhythm_different)
          elif relationship.type == NoteRelationshipType.HARMONIC:
            notation_string += get_current_notation(note, HarmonicPartColors.PURPLE, DistanceType.SUBSTITUTION, is_rhythm_different)
          elif relationship.type == NoteRelationshipType.UNRELATED:
            notation_string += get_current_notation(note, HarmonicPartColors.GREY, DistanceType.SUBSTITUTION, is_rhythm_different)
      elif current_source.isRest and not current_target.isRest:
        if current_target.isNote:
          notation_string += get_current_notation(current_target, HarmonicPartColors.ORANGE, DistanceType.SUBSTITUTION, is_rhythm_different)
        elif current_target.isChord:
          for note in current_target:
            notation_string += get_current_notation(note, HarmonicPartColors.ORANGE, DistanceType.SUBSTITUTION, is_rhythm_different)
      elif current_target.isRest and not current_source.isRest:
        if current_source.isNote:
          notation_string += get_current_notation(current_source, HarmonicPartColors.ORANGE, DistanceType.SUBSTITUTION, is_rhythm_different)
        elif current_source.isChord:
          for note in current_source:
            notation_string += get_current_notation(note, HarmonicPartColors.ORANGE, DistanceType.SUBSTITUTION, is_rhythm_different)
      elif current_source.isRest and current_target.isRest:
        if is_rhythm_different:
          color = HarmonicPartColors.ORANGE
        else:
          color = HarmonicPartColors.BLACK
        notation_string += get_current_notation(current_target, color, DistanceType.SUBSTITUTION, is_rhythm_different)

      if current_source.isChord or current_target.isChord:
        notation_string += "} "

      if current_source_index < len(source) - 1:
        current_source_index += 1
      if current_target_index < len(target) - 1:
        current_target_index += 1
  
  print("notation string", notation_string)
  draw_sheet_music(notation_string)

def get_uncovered_notes(source, note_evaluation):
  expected_notes = []
  covered_notes = []
  if source.isNote:
    expected_notes.append(source.pitch)
  elif source.isChord:
    for note in source:
      expected_notes.append(note.pitch)
  for relationship in note_evaluation:
    covered_notes.append(relationship.expected_note)
  return set(expected_notes) - set(covered_notes)

def get_note_from_pitch(source, pitch):
  if source.isNote:
    return source
  else:
    for note in source:
      if note.pitch == pitch:
        return note

def get_current_notation(note, color, distance_type, is_rhythm_different):
  only_rhythm_difference = False
  if (color == HarmonicPartColors.BLACK and is_rhythm_different) or color == HarmonicPartColors.ORANGE:
    color = HarmonicPartColors.ORANGE
    only_rhythm_difference = True
  
  # title = get_lyric_title(distance_type, is_rhythm_different, only_rhythm_difference)
  title = " "
  length = get_notation_length(note)

  if note.isRest:
    return "r" + length + color.value + title
  else:
    octave = note.octave
    if octave == 3:
      return note.name.upper() + length + color.value + title
    elif octave == 4:
      return note.name.lower() + length + color.value + title
    elif octave < 3:
      difference = 3 - octave
      return note.name.upper() + note.name.upper() * difference + length + color.value + title
    elif octave > 3:
      difference = octave - 4
      return note.name.lower() + "'" * difference + length + color.value + title

def get_lyric_title(distance_type, is_rhythm_different, only_rhythm_difference):
  if only_rhythm_difference:
    return "_R "
  rhythm_change = ""
  if is_rhythm_different:
    rhythm_change = "R+"
  if distance_type == DistanceType.DELETION:
    return f"_{rhythm_change}del "
  elif distance_type == DistanceType.INSERTION:
    return f"_{rhythm_change}ins "
  elif distance_type == DistanceType.SAME:
    return " "
  elif distance_type == DistanceType.SUBSTITUTION:
    return f"_{rhythm_change}sub "

def get_notation_length(note):
  length = ""
  if note.duration.components[0].dots > 0:
    length += "."
  
  duration_type = note.duration.type
  if duration_type == "whole":
    length += "1"
  elif duration_type == "half":
    length += "2"
  elif duration_type == "quarter":
    length += "4"
  elif duration_type == "eighth":
    length += "8"
  elif duration_type == "16th":
    length += "16"
  elif duration_type == "32nd":
    length += "32"
  return length

def draw_sheet_music(notation_string):
  tnc = m21.tinyNotation.Converter('')
  tnc.modifierAngle = ColorModifier
  tnc.bracketStateMapping['chord'] = ChordState
  tnc.load(notation_string)
  tnc.parse()
  # tnc.stream.show("musicxml.png")
  put_sheet_in_output_folder(tnc.stream, True)

class ColorModifier(m21.tinyNotation.Modifier):
  def postParse(self, m21Obj):
    m21Obj.style.color = self.modifierData
    return m21Obj

class ChordState(m21.tinyNotation.State):
  def affectTokenAfterParse(self, n):
    super(ChordState, self).affectTokenAfterParse(n)
    return None # do not append Note object

  def end(self):
    ch = m21.chord.Chord(self.affectedTokens)
    ch.duration = self.affectedTokens[0].duration
    return ch

# tnc = m21.tinyNotation.Converter('')
# tnc.modifierAngle = ColorModifier
# tnc.bracketStateMapping['chord'] = ChordState
# tnc.load("3/4 c e g")
# tnc.parse()
# tnc.stream.show("musicxml.png")