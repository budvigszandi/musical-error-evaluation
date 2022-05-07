from metrics.normalize_points import normalize
import metrics.notes.harmonics as harmonics
from metrics.notes.note_relationship_type import NoteRelationshipType
from metrics.notes.note_relationship import NoteRelationship
from metrics.notes.note_points import NotePoints
from metrics.combinations import *
from collections import Counter

def get_relationship_matrix(expected_notes, given_notes):
  expected_notes_count = len(expected_notes)
  given_notes_count = len(given_notes)
  relationship_matrix = [[0 for i in range(expected_notes_count)] for j in range(given_notes_count)] 
  # rows = len(relationship_matrix)
  # columns = len(relationship_matrix[0])
  # print(f"Initializing {rows} rows {columns} columns")
  for i in range(given_notes_count):
    for j in range(expected_notes_count):
      relationship_matrix[i][j] = compare_note_pair(given_notes[i], expected_notes[j])
  # Just testing here
  # for i in range(given_notes_count):
  #   for j in range(expected_notes_count):
  #     current = relationship_matrix[i][j]
  #     print(f"Z[{i}][{j}]: {current.given_note} - {current.expected_note} {current.type} "
  #           f"{current.cent_difference} {current.harmonic_info}")
  #   if i < given_notes_count - 1:
  #     print("---")
  return relationship_matrix

def get_relationship_points(relationship_matrix):
  rows = len(relationship_matrix)
  columns = len(relationship_matrix[0])
  # print(f"Points: {rows} rows {columns} columns")
  relationship_point_matrix = [[0 for i in range(columns)] for j in range(rows)]
  # print(f"Points matrix: {len(relationship_point_matrix)} rows {len(relationship_point_matrix[0])} columns")
  for i in range(rows):
    for j in range(columns):
      # print(f"[{i}][{j}]: {relationship_matrix[i][j]}")
      current_relationship = relationship_matrix[i][j].type
      if current_relationship == NoteRelationshipType.HARMONIC:
        relationship_point_matrix[i][j] = get_current_point(current_relationship, relationship_matrix[i][j].harmonic_info[0])
      else:
        relationship_point_matrix[i][j] = get_current_point(current_relationship)
  # Just testing here
  # for i in range(rows):
  #   for j in range(columns):
  #     print(f"R[{i}][{j}]: {relationship_point_matrix[i][j]}")
  #   if i < rows - 1:
  #     print("---")
  return relationship_point_matrix

def get_current_point(relationship_type, harmonic_number = -1):
  if relationship_type == NoteRelationshipType.PERFECT_MATCH: # Perfect match
    return NotePoints.PERFECT_MATCH_POINT
  elif relationship_type == NoteRelationshipType.CENT_DIFFERENCE: # Cent difference
    return NotePoints.CENT_DIFFERENCE_POINT
  elif relationship_type == NoteRelationshipType.HARMONIC: # Harmonic
    return (NotePoints.MAXIMUM_HARMONIC_NUMBER - harmonic_number) * NotePoints.HARMONIC_POINT
  elif relationship_type == NoteRelationshipType.UNRELATED: # Unrelated
    return NotePoints.UNRELATED_POINT

def get_scenarios(relationship_matrix, relationship_point_matrix):
  scenarios = {}
  rows = len(relationship_point_matrix)
  columns = len(relationship_point_matrix[0])
  index_variations = get_index_variations(rows, columns)
  for index_list in index_variations:
    sum = get_sum_of_scenario(index_list, relationship_matrix, relationship_point_matrix)
    scenario = get_current_scenario(relationship_matrix, index_list)
    scenario_tuple = tuple(scenario)
    scenarios[scenario_tuple] = sum
    # sorted_scenarios = sort_scenarios(scenarios)
  # return sorted_scenarios
  return scenarios

def get_current_scenario(relationship_matrix, index_list):
  scenario = []
  for i in range(len(index_list)):
    scenario.append(relationship_matrix[i][index_list[i]])
  return scenario

def get_sum_of_scenario(index_list, relationship_matrix, relationship_point_matrix):
  expected_notes_count = len(relationship_point_matrix[0])
  minimum_points = len(relationship_point_matrix) * NotePoints.UNRELATED_POINT
  maximum_points = expected_notes_count * NotePoints.PERFECT_MATCH_POINT * NotePoints.RELATIONSHIP_POINT_WEIGHT + \
                   + expected_notes_count * NotePoints.COVERED_NOTE_POINT * NotePoints.COVERED_NOTE_POINT_WEIGHT
  
  sum = 0
  for i in range(len(index_list)):
    is_duplicate = is_duplicate_cover(relationship_matrix, index_list, i)
    if not is_duplicate:
      sum += relationship_point_matrix[i][index_list[i]]
  sum *= NotePoints.RELATIONSHIP_POINT_WEIGHT
  covered_notes_count = get_covered_notes_count(index_list)
  sum += covered_notes_count * NotePoints.COVERED_NOTE_POINT_WEIGHT
  duplicate_reduction_point = get_duplicated_reduction_point(index_list)
  sum += duplicate_reduction_point * NotePoints.DUPLICATE_POINT_WEIGHT

  normalized_sum = normalize(sum, minimum_points, maximum_points)
  return max(0, normalized_sum)

def is_duplicate_cover(relationship_matrix, index_list, index_list_index):
  occurences = []
  for i in range(len(index_list[:index_list_index])):
    if index_list[i] == index_list[index_list_index]:
      occurences.append(i)

  only_unrelated_relationships = True
  if len(occurences) > 0:
    for i in range(len(occurences)):
      if relationship_matrix[i][index_list[occurences[i]]] != NoteRelationshipType.UNRELATED:
        only_unrelated_relationships = False
  return not only_unrelated_relationships

def get_covered_notes_count(index_list):
  return len(Counter(index_list).keys()) * NotePoints.COVERED_NOTE_POINT

def get_duplicated_reduction_point(index_list):
  frequency_of_notes = Counter(index_list).values()
  number_of_duplicates_list = [i - 1 for i in frequency_of_notes]
  return sum(number_of_duplicates_list) * NotePoints.DUPLICATE_COVER_POINT

# TODO: Return all the best ones?
def get_best_scenario(scenarios):
  return max(scenarios, key=scenarios.get)

def sort_scenarios(scenarios):
  sorted_scenarios = {k: v for k, v in sorted(scenarios.items(), key=lambda item: item[1], reverse=True)}
  return sorted_scenarios

def compare_note_pair(given_note, expected_note):
  if expected_note.isEnharmonic(given_note):
    return NoteRelationship(NoteRelationshipType.PERFECT_MATCH, given_note, expected_note)
  elif expected_note.nameWithOctave == given_note.nameWithOctave:
    return NoteRelationship(NoteRelationshipType.CENT_DIFFERENCE, given_note, expected_note, given_note.microtone.cents - expected_note.microtone.cents)
  else:
    harmonic_info = harmonics.get_harmonic_info(given_note, expected_note)
    if harmonic_info != 0:
      if harmonic_info[0] >= NotePoints.MAXIMUM_HARMONIC_NUMBER:
        return NoteRelationship(NoteRelationshipType.UNRELATED, given_note, expected_note)
      else:
        return NoteRelationship(NoteRelationshipType.HARMONIC, given_note, expected_note, None, harmonic_info)
    else:
      return NoteRelationship(NoteRelationshipType.UNRELATED, given_note, expected_note)
