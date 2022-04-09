from metrics.distance_algorithms.distances import convert_steps_with_points_dtw, convert_steps_with_points_levenshtein, dtw, get_all_step_permutations
from metrics.distance_algorithms.dtw_boundaries import get_dtw_dummy_data, get_dtw_runtimes
from metrics.notes.note_evaluation_stats import NoteEvaluationStats
from metrics.notes.note_points import NotePoints
from metrics.notes.note_relationship_type import NoteRelationshipType

def get_note_eval_stats(expected_notes, given_notes, scenario, points):
  note_eval_stats = NoteEvaluationStats(len(expected_notes), len(given_notes))
  for rel in scenario:
    rel_type = rel.type
    if rel_type == NoteRelationshipType.PERFECT_MATCH:
      note_eval_stats.perfect_matches += 1
    if rel_type == NoteRelationshipType.CENT_DIFFERENCE:
      note_eval_stats.cent_differences += 1
    if rel_type == NoteRelationshipType.HARMONIC:
      note_eval_stats.harmonics[rel.harmonic_info[0]] += 1
    if rel_type == NoteRelationshipType.UNRELATED:
      note_eval_stats.unrelated += 1
    if rel.expected_note == expected_notes[0] and rel_type == NoteRelationshipType.PERFECT_MATCH:
      note_eval_stats.got_lowest = True
    note_eval_stats.uncovered_notes = get_uncovered_notes(expected_notes, scenario)
    note_eval_stats.covered_only_with_harmonics = get_covered_only_with_harmonics(expected_notes, scenario)
    note_eval_stats.multiply_covered_notes = get_multiply_covered_notes(expected_notes, scenario)
    note_eval_stats.points = points

  print("------------ Statistics ------------")
  print(note_eval_stats)

def get_uncovered_notes(expected_notes, scenario):
  uncovered_notes = []
  for note in expected_notes:
    occurred = False
    for rel in scenario:
      if rel.expected_note == note:
        occurred = True
    if not occurred:
      uncovered_notes.append(note)
  return uncovered_notes

def get_covered_only_with_harmonics(expected_notes, scenario):
  only_harmonic_covers = {}
  for note in expected_notes:
    only_harmonics = True
    occurred = False
    harmonics = [0 for i in range(NotePoints.MAXIMUM_HARMONIC_NUMBER)]
    for rel in scenario:
      if rel.expected_note == note:
        occurred = True
        if rel.type != NoteRelationshipType.HARMONIC:
          only_harmonics = False
        if rel.type == NoteRelationshipType.HARMONIC: 
          harmonics[rel.harmonic_info[0]] += 1
    if only_harmonics and occurred:
      only_harmonic_covers[note] = harmonics
  return only_harmonic_covers

def get_multiply_covered_notes(expected_notes, scenario):
  multiple_covers = {}
  for note in expected_notes:
    occurences = 0
    relationships = []
    for rel in scenario:
      if rel.expected_note == note:
        occurences += 1
        relationships.append(rel)
    if occurences > 1:
      multiple_covers[note] = relationships
  return multiple_covers

def get_dtw_boundaries(min_matrix_size, max_matrix_size):
  runtimes = get_dtw_runtimes(min_matrix_size, max_matrix_size)
  for elem in runtimes:
    if float(runtimes[elem]) > 15:
      print(elem, runtimes[elem], "seconds - LONG TIME")
    else:
      print(elem, runtimes[elem], "seconds")

def get_dtw_levenshtein_stats(min_matrix_size, max_matrix_size):
  dummy_data = get_dtw_dummy_data(min_matrix_size, max_matrix_size)

  print(f"Getting amounts of Levenshtein vs. DTW permutations on matrices from {min_matrix_size}x{min_matrix_size} to {max_matrix_size}x{max_matrix_size}")
  
  dtw_amounts = {}
  levenshtein_amounts = {}

  for pair in dummy_data:
    print(f"Counting on {len(pair[0])}x{len(pair[1])} matrix")
    expected = pair[0]
    given = pair[1]
    key = f"{len(expected)}x{len(given)}"

    all_step_permutations = get_all_step_permutations(expected, given)
    dtw_matrix = dtw(expected, given, 3, True)
    converted_permutations_dtw, points = convert_steps_with_points_dtw(all_step_permutations, expected, given, dtw_matrix)
    
    all_step_permutations = get_all_step_permutations(expected, given)
    converted_permutations_lev, points = convert_steps_with_points_levenshtein(all_step_permutations, expected, given)
    
    dtw_amounts[key] = len(converted_permutations_dtw)
    levenshtein_amounts[key] = len(converted_permutations_lev)

  for key in dtw_amounts:
    print(f"\n{key} matrix:")
    print("  Levenshtein permutations:", levenshtein_amounts[key])
    print("  DTW permutations:", dtw_amounts[key])
    print(f"DTW amount is {((dtw_amounts[key] / levenshtein_amounts[key]) * 100):.2f}% of Levenshtein amount")
    print(f"Leveshtein amount is DTW amount * {(levenshtein_amounts[key] / dtw_amounts[key]):.2f}")

  return 0