from metrics.notes.evaluate_notes import *
from metrics.harmonic_parts.harmonic_part_points import HarmonicPartPoints
from metrics.notes.note_points import NotePoints
from metrics.rhythms.evaluate_rhythms import get_rhythmic_distance
from metrics.distances.distance_type import DistanceType
from metrics.rhythms.rhythm_points import RhythmPoints
from metrics.notes.note_points import NotePoints

def get_harmonic_part_point(step_permutation, source, target):
  # Starting from the maximum possible amount of points
  point = len(source) * HarmonicPartPoints.CORRECT_HARMONIC_ELEMENT_POINT
  current_source_index = 0
  current_target_index = 0
  for i in range(len(step_permutation)):
    current_step = step_permutation[i]
    current_source = source[current_source_index]
    current_target = target[current_target_index]
    print("source", current_source_index, "target", current_target_index, "step", current_step)
    if current_step == DistanceType.DELETION:
      point += HarmonicPartPoints.DELETED_HARMONIC_ELEMENT_POINT
      point -= current_source.quarterLength * RhythmPoints.LENGTH_DIFFERENCE_WEIGHT
      if current_source.isNote:
        point -= NotePoints.COVERED_NOTE_POINT
      elif current_source.isChord:
        point -= len(current_source) * NotePoints.COVERED_NOTE_POINT
      if current_source_index < len(source) - 1: current_source_index += 1
    elif current_step == DistanceType.INSERTION:
      point += RhythmPoints.INSERTED_RHYTHM_POINT
      point -= current_target.quarterLength * RhythmPoints.LENGTH_DIFFERENCE_WEIGHT
      if current_source.isNote:
        point += HarmonicPartPoints.INSERTED_NOTE_POINT
      elif current_source.isChord:
        point += len(current_target) * HarmonicPartPoints.INSERTED_NOTE_POINT
      if current_target_index < len(target) - 1: current_target_index += 1
    elif current_step == DistanceType.SAME:
      if current_source_index < len(source) - 1: current_source_index += 1
      if current_target_index < len(target) - 1: current_target_index += 1
      continue
    elif current_step == DistanceType.SUBSTITUTION:
      point += HarmonicPartPoints.SUBSTITUTED_HARMONIC_ELEMENT_POINT
      point -= abs(get_harmonic_part_distance(current_source, current_target))
      if current_source_index < len(source) - 1: current_source_index += 1
      if current_target_index < len(target) - 1: current_target_index += 1
  return point

# TODO: Continue point system
# TODO: Consider music21.Voice object as well
def get_harmonic_part_distance(source, target):
  distance = 0
  if source != target:
    neither_is_rest = (not source.isRest) and (not target.isRest)
    is_chord_note_switch = (source.isNote and target.isChord) or (source.isChord and target.isNote)
    is_rest_sound_switch = (source.isRest and (not target.isRest)) or ((not source.isRest) and target.isRest)
    both_are_rests = source.isRest and target.isRest
    if neither_is_rest:
      if is_chord_note_switch:
        distance += HarmonicPartPoints.CHORD_NOTE_SWITCH_POINT
        if source.isNote and target.isChord:
          maximum_point = NotePoints.PERFECT_MATCH_POINT
          points = get_best_note_evaluation_point([source.pitch], target)
        elif source.isChord and target.isNote:
          maximum_point = len(source) * NotePoints.PERFECT_MATCH_POINT
          points = get_best_note_evaluation_point(source, [target.pitch])
        distance += maximum_point - points
      elif source.isNote and target.isNote:
        maximum_point = NotePoints.PERFECT_MATCH_POINT
        points = get_best_note_evaluation_point([source.pitch], [target.pitch])
      elif source.isChord and target.isChord:
        maximum_point = len(source) * NotePoints.PERFECT_MATCH_POINT
        points = get_best_note_evaluation_point(source, target)
      distance += maximum_point - points
    elif is_rest_sound_switch:
      # TODO: Maybe the distance should be even bigger if more sounds are expected
      distance += HarmonicPartPoints.REST_SOUND_SWITCH_POINT
    elif both_are_rests:
      rhythmic_distance = get_rhythmic_distance(source, target)
      distance != rhythmic_distance
  return distance

def get_best_note_evaluation_point(source, target):
  expected_notes = []
  given_notes = []
  if len(source) > 1:
    for note in source:
      expected_notes.append(note.pitch)
  else:
    expected_notes = source
  if len(target) > 1:
    for note in target:
      given_notes.append(note.pitch)
  else:
    given_notes = target
  scenarios = get_note_scenarios(expected_notes, given_notes)
  best_scenario = get_best_scenario(scenarios)
  points = scenarios[best_scenario]
  return points

def get_note_scenarios(expected_notes, given_notes):
  rel_matrix = get_relationship_matrix(expected_notes, given_notes)
  rel_points_matrix = get_relationship_points(rel_matrix)
  scenarios = get_scenarios(rel_matrix, rel_points_matrix)
  return scenarios
