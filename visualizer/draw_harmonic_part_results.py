import music21 as m21
from input.midi_reader import put_sheet_in_output_folder
from metrics.distance_algorithms.distance_type import DistanceType
from metrics.rhythms.evaluate_rhythms import get_rhythmic_distance
from visualizer.harmonic_part_colors import HarmonicPartColors
from metrics.notes.note_relationship_type import NoteRelationshipType
from metrics.distance_algorithms.boyer_moore import *

NOTATION_CHORD_BEGINNING = "chord{"
NOTATION_CHORD_ENDING = "} "
NOTATION_REST = "r"

def add_matched_chunk_to_notation_string_bm_m21(notation_string, orig, bm_chunk_begin, bm_chunk_end, ins_empty_chunks):
  notation_string_length = len(notation_string)
  orig_chunk = orig[bm_chunk_begin - ins_empty_chunks : bm_chunk_end - ins_empty_chunks]
  m21_array = orig_chunk
  for elem in m21_array:
    if elem.isNote:
      notation_string += get_current_notation(elem, HarmonicPartColors.BLACK, DistanceType.SAME, False)
    elif elem.isChord:
      notation_string += NOTATION_CHORD_BEGINNING
      for note in elem:
        notation_string += get_current_notation(note, HarmonicPartColors.BLACK, DistanceType.SAME, False)
      notation_string += NOTATION_CHORD_ENDING
    elif elem.isRest:
      # notation_string += NOTATION_REST + HarmonicPartColors.BLACK.value + " "
      notation_string += get_current_notation(elem, HarmonicPartColors.BLACK, DistanceType.SAME, False)
  print("Generated notation string:")
  print(notation_string[notation_string_length:])
  return notation_string

# This is a drawing function for metrics.distance_algorithms.boyer_moore, which is not
# used, but kept for chance of future development
def draw_from_bm_chars(orig_exp, orig_giv, bm_exp, bm_giv, exp_copy, giv_copy, exp_chunks, giv_chunks):
  notation_string = ""
  current = 0
  current_exp = 0
  unmatched_chunk_count = 0
  exp_ins_empty_chunks = 0
  giv_ins_empty_chunks = 0
  while current < len(bm_giv):    
    if giv_copy[current] == BLANK_CHARACTER:
      print("\n------ Matched chunk ------")
      next_non_blank_letter_index = get_non_blank_letter_index(giv_copy[current:])
      if next_non_blank_letter_index != None:
        matched_chunk = bm_giv[current - giv_ins_empty_chunks : current + next_non_blank_letter_index - giv_ins_empty_chunks]
        print(f"Matched chunk at {current}-{current + next_non_blank_letter_index}")
        print(matched_chunk)
        notation_string = add_matched_chunk_to_notation_string_bm_chars(notation_string, orig_giv, bm_giv, current - giv_ins_empty_chunks, current + next_non_blank_letter_index - giv_ins_empty_chunks)
        current += next_non_blank_letter_index
        current_exp += next_non_blank_letter_index
      else:
        matched_chunk = bm_giv[current - giv_ins_empty_chunks :]
        print(f"Matched chunk at {current}-{len(giv_copy)}")
        print(matched_chunk)
        notation_string = add_matched_chunk_to_notation_string_bm_chars(notation_string, orig_giv, bm_giv, current - giv_ins_empty_chunks, len(giv_copy) - 1)
        current = len(giv_copy)
        current_exp = len(exp_copy)
      print("\nCurrent full notation string:")
      print(notation_string)
    else:
      print("\n------ Unmatched chunkpair ------")
      print("Expected chunk:")
      print(exp_chunks[unmatched_chunk_count], end="\n\n")
      print("Given chunk:")
      print(giv_chunks[unmatched_chunk_count])
      if exp_copy[current_exp] == EMPTY_CHUNK_CHARACTER:
        exp_ins_empty_chunks += 1
      if giv_copy[current] == EMPTY_CHUNK_CHARACTER:
        giv_ins_empty_chunks += 1
      next_blank_letter_index = get_next_blank_letter_index(giv_copy[current:])
      exp_chunk_length = len(exp_chunks[unmatched_chunk_count])
      orig_exp_chunk = get_m21_chunk(orig_exp, bm_exp, current_exp - exp_ins_empty_chunks, current_exp + exp_chunk_length - exp_ins_empty_chunks, True)
      if next_blank_letter_index != None:
        orig_giv_chunk = get_m21_chunk(orig_giv, bm_giv, current - giv_ins_empty_chunks, current + next_blank_letter_index - giv_ins_empty_chunks)
        current += next_blank_letter_index
      else:
        orig_giv_chunk = get_m21_chunk(orig_giv, bm_giv, current - giv_ins_empty_chunks, len(giv_copy) - 1)
        current = len(giv_copy)
      current_exp += exp_chunk_length
      dtw_expected = orig_exp_chunk
      dtw_given = orig_giv_chunk
      # This import is here to dodge circular import
      from evaluate import get_song_dtw_evaluation
      steps, note_eval, point = get_song_dtw_evaluation(dtw_expected, dtw_given)
      notation_string += get_notation_string_from_steps(dtw_expected, dtw_given, steps, note_eval)
      print("\nCurrent full notation string:")
      print(notation_string)
      unmatched_chunk_count += 1
      print()
    print("\nUnmatched expected chunk total:", len(exp_chunks))
    print("Unmatched given chunks total:", len(giv_chunks))
    print("Unmatched chunk pairs evaluated:", unmatched_chunk_count)
    print("Unmatched chunk pairs remaining:", len(exp_chunks) - unmatched_chunk_count)
  print("\n------ Final notation string ------")
  print(notation_string)
  draw_sheet_music(notation_string)

# This is a drawing function for metrics.distance_algorithms.boyer_moore, which is not
# used, but kept for chance of future development
def add_matched_chunk_to_notation_string_bm_chars(notation_string, orig, bm_array, bm_chunk_begin, bm_chunk_end):
  notation_string_length = len(notation_string)
  orig_chunk = get_m21_chunk(orig, bm_array, bm_chunk_begin, bm_chunk_end)
  m21_array = orig_chunk
  for elem in m21_array:
    if elem.isNote:
      notation_string += get_current_notation(elem, HarmonicPartColors.BLACK, DistanceType.SAME, False)
    elif elem.isChord:
      notation_string += NOTATION_CHORD_BEGINNING
      for note in elem:
        notation_string += get_current_notation(note, HarmonicPartColors.BLACK, DistanceType.SAME, False)
      notation_string += NOTATION_CHORD_ENDING
    elif elem.isRest:
      notation_string += get_current_notation(elem, HarmonicPartColors.BLACK, DistanceType.SAME, False)
  print("Generated notation string:")
  print(notation_string[notation_string_length:])
  return notation_string

def get_notation_string_from_steps(source, target, steps, note_evaluation):
  current_source_index = 0
  current_target_index = 0
  notation_string = ""

  for i in range(len(steps)):
    current_step = steps[i]
    if len(source) > 0: current_source = source[current_source_index]
    if len(target) > 0: current_target = target[current_target_index]

    if current_step == DistanceType.DELETION:

      if current_source.isNote:
        notation_string += get_current_notation(current_source, HarmonicPartColors.RED, DistanceType.DELETION, False)
      elif current_source.isChord:
        notation_string += NOTATION_CHORD_BEGINNING
        for note in current_source:
          notation_string += get_current_notation(note, HarmonicPartColors.RED, DistanceType.DELETION, False)
        notation_string += NOTATION_CHORD_ENDING
      elif current_source.isRest:
        notation_string += get_current_notation(current_source, HarmonicPartColors.RED, DistanceType.DELETION, True)
      
      if current_source_index < len(source) - 1:
        current_source_index += 1

    elif current_step == DistanceType.INSERTION:

      if current_target.isNote:
        notation_string += get_current_notation(current_target, HarmonicPartColors.BLUE, DistanceType.INSERTION, False)
      elif current_target.isChord:
        notation_string += NOTATION_CHORD_BEGINNING
        for note in current_target:
          notation_string += get_current_notation(note, HarmonicPartColors.BLUE, DistanceType.INSERTION, False)
        notation_string += NOTATION_CHORD_ENDING
      elif current_target.isRest:
        notation_string += get_current_notation(current_target, HarmonicPartColors.BLUE, DistanceType.INSERTION, True)

      if current_target_index < len(target) - 1:
        current_target_index += 1

    elif current_step == DistanceType.SAME:

      if current_source.isNote:
        notation_string += get_current_notation(current_source, HarmonicPartColors.BLACK, DistanceType.SAME, False)
      elif current_source.isChord:
        notation_string += NOTATION_CHORD_BEGINNING
        for note in current_source:
          notation_string += get_current_notation(note, HarmonicPartColors.BLACK, DistanceType.SAME, False)
        notation_string += NOTATION_CHORD_ENDING
      elif current_source.isRest:
        notation_string += get_current_notation(current_source, HarmonicPartColors.BLACK, DistanceType.SAME, True)

      if current_source_index < len(source) - 1:
        current_source_index += 1
      if current_target_index < len(target) - 1:
        current_target_index += 1

    elif current_step == DistanceType.SUBSTITUTION:
      note_eval = note_evaluation[current_source_index]
      rhythmic_distance = get_rhythmic_distance(current_source, current_target)
      is_rhythm_different = rhythmic_distance > 0

      if current_source.isChord or current_target.isChord:
        notation_string += NOTATION_CHORD_BEGINNING
      
      if note_eval != None and not (current_source.isRest or current_target.isRest):
        uncovered_notes = get_uncovered_notes(current_source, note_eval)
        for pitch in uncovered_notes:
          note = get_note_from_pitch(current_source, pitch)
          notation_string += get_current_notation(note, HarmonicPartColors.RED, DistanceType.DELETION, is_rhythm_different)
        for relationship in note_eval:
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
        notation_string += NOTATION_CHORD_ENDING

      if current_source_index < len(source) - 1:
        current_source_index += 1
      if current_target_index < len(target) - 1:
        current_target_index += 1
  
  print("Generated notation string:")
  print(notation_string)
  return notation_string

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
    return NOTATION_REST + length + color.value + title
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
  print("\n------ Drawing sheet music ------")
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
