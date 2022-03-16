import music21 as m21
from metrics.distances.distance_type import DistanceType
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
        notation_string += get_current_notation(current_source, HarmonicPartColors.RED)
      elif current_source.isChord:
        notation_string += "chord{"
        for note in current_source:
          notation_string += get_current_notation(note, HarmonicPartColors.RED)
        notation_string += "} "
      elif current_source.isRest:
        notation_string += "r" + HarmonicPartColors.RED.value
      
      if current_source_index < len(source) - 1:
        current_source_index += 1

    elif current_step == DistanceType.INSERTION:
      print("inserted", current_target)
      print()

      if current_target.isNote:
        notation_string += get_current_notation(current_target, HarmonicPartColors.BLUE)
      elif current_target.isChord:
        notation_string += "chord{"
        for note in current_target:
          notation_string += get_current_notation(note, HarmonicPartColors.BLUE)
        notation_string += "} "
      elif current_target.isRest:
        notation_string += "r" + HarmonicPartColors.BLUE.value

      if current_target_index < len(target) - 1:
        current_target_index += 1

    elif current_step == DistanceType.SAME:
      print("got match", current_source)
      print()

      if current_source.isNote:
        notation_string += get_current_notation(current_source, HarmonicPartColors.BLACK)
      elif current_source.isChord:
        notation_string += "chord{"
        for note in current_source:
          notation_string += get_current_notation(note, HarmonicPartColors.BLACK)
        notation_string += "} "
      elif current_source.isRest:
        notation_string += "r" + HarmonicPartColors.BLACK.value

      if current_source_index < len(source) - 1:
        current_source_index += 1
      if current_target_index < len(target) - 1:
        current_target_index += 1

    elif current_step == DistanceType.SUBSTITUTION:
      print("wanted", current_source, "got", current_target)
      print("difference:")
      note_eval = note_evaluation[current_source_index]
      if current_target.isChord:
        notation_string += "chord{"
      if note_eval != None:
        for relationship in note_eval:
          print(relationship)
          if relationship.type == NoteRelationshipType.PERFECT_MATCH:
            notation_string += get_current_notation(relationship.expected_note, HarmonicPartColors.BLACK)
          elif relationship.type == NoteRelationshipType.CENT_DIFFERENCE:
            notation_string += get_current_notation(relationship.given_note, HarmonicPartColors.YELLOW)
          elif relationship.type == NoteRelationshipType.HARMONIC:
            notation_string += get_current_notation(relationship.given_note, HarmonicPartColors.PURPLE)
          elif relationship.type == NoteRelationshipType.UNRELATED:
            notation_string += get_current_notation(relationship.given_note, HarmonicPartColors.GREY)
      else:
        print("rhythmic difference")
      print()
      if current_target.isChord:
        notation_string += "} "

      if current_source_index < len(source) - 1:
        current_source_index += 1
      if current_target_index < len(target) - 1:
        current_target_index += 1
  
  print("notation string", notation_string)
  draw_sheet_music(notation_string)

def get_current_notation(note, color):
  # TODO: Add length as well
  octave = note.octave
  if octave == 3:
    return note.name.upper() + color.value
  elif octave == 4:
    return note.name.lower() + color.value
  elif octave < 3:
    difference = 3 - octave
    return note.name.upper() + note.name.upper() * difference + color.value
  elif octave > 3:
    difference = octave - 4
    return note.name.lower() + "'" * difference + color.value

def draw_sheet_music(notation_string):
  tnc = m21.tinyNotation.Converter('')
  tnc.modifierAngle = ColorModifier
  tnc.bracketStateMapping['chord'] = ChordState
  tnc.load(notation_string)
  tnc.parse()
  tnc.stream.show("musicxml.png")

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