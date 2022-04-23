from metrics.notes.evaluate_notes import *
from metrics.harmonic_parts.harmonic_part_points import HarmonicPartPoints
from metrics.notes.note_points import NotePoints
from metrics.rhythms.evaluate_rhythms import get_rhythmic_distance
from metrics.distance_algorithms.distance_type import DistanceType
from metrics.rhythms.rhythm_points import RhythmPoints
from metrics.notes.note_points import NotePoints
from metrics.normalize_points import normalize

def get_harmonic_part_point(step_permutation, source, target):
  minimum_points = len(source) * HarmonicPartPoints.DELETED_HARMONIC_ELEMENT_POINT + \
                   + len(target) * HarmonicPartPoints.INSERTED_HARMONIC_ELEMENT_POINT
  maximum_points = len(source) * HarmonicPartPoints.CORRECT_HARMONIC_ELEMENT_POINT

  # Starting from the maximum possible amount of points
  point = len(source) * HarmonicPartPoints.CORRECT_HARMONIC_ELEMENT_POINT
  current_source_index = 0
  current_target_index = 0
  for i in range(len(step_permutation)):
    current_step = step_permutation[i]
    if len(source) > 0: current_source = source[current_source_index]
    if len(target) > 0: current_target = target[current_target_index]
    # print("source", current_source_index, "target", current_target_index, "step", current_step)
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
      if current_target.isNote:
        point += HarmonicPartPoints.INSERTED_NOTE_POINT
      elif current_target.isChord:
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
  
  normalized_point = normalize(point, minimum_points, maximum_points)
  return normalized_point

def get_harmonic_part_distance(source, target):
  distance = 0
  if source != target:
    neither_is_rest = (not source.isRest) and (not target.isRest)
    is_chord_note_switch = (source.isNote and target.isChord) or (source.isChord and target.isNote)
    is_rest_sound_switch = (source.isRest and (not target.isRest)) or ((not source.isRest) and target.isRest)
    both_are_rests = source.isRest and target.isRest
    if neither_is_rest:
      if is_chord_note_switch:
        distance -= HarmonicPartPoints.CHORD_NOTE_SWITCH_POINT
      if source.isNote:
        maximum_point = NotePoints.PERFECT_MATCH_POINT
        points = get_best_note_evaluation(source, target, False, True)
      elif source.isChord:
        maximum_point = len(source) * NotePoints.PERFECT_MATCH_POINT
        points = get_best_note_evaluation(source, target, False, True)
      distance += maximum_point - points
    elif is_rest_sound_switch:
      # Development idea: the distance could be even bigger if more sounds are expected (if necessary)
      distance -= HarmonicPartPoints.REST_SOUND_SWITCH_POINT
    rhythmic_distance = get_rhythmic_distance(source, target)
    distance += rhythmic_distance
  return round(distance, 2)

def get_best_note_evaluation(source, target, get_scenario, get_points):
  expected_notes = []
  given_notes = []

  try:
    if source.isNote:
      expected_notes.append(source.pitch)
    elif source.isChord:
      for note in source:
        expected_notes.append(note.pitch)
  except AttributeError as error:
    expected_notes.append(source)
  
  try:
    if target.isNote:
      given_notes.append(target.pitch)
    elif target.isChord:
      for note in target:
        given_notes.append(note.pitch)
  except AttributeError as error:
    given_notes.append(target)
  
  scenarios = get_note_scenarios(expected_notes, given_notes)
  best_scenario = get_best_scenario(scenarios)
  points = scenarios[best_scenario]
  if get_scenario and get_points:
    return best_scenario, points
  elif get_scenario:
    return best_scenario
  elif get_points:
    return points

def get_note_scenarios(expected_notes, given_notes):
  rel_matrix = get_relationship_matrix(expected_notes, given_notes)
  rel_points_matrix = get_relationship_points(rel_matrix)
  scenarios = get_scenarios(rel_matrix, rel_points_matrix)
  return scenarios
