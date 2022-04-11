from metrics.distance_algorithms.distance_type import DistanceType
from metrics.distance_algorithms.distances import convert_steps_with_points_dtw, convert_steps_with_points_levenshtein, dtw, get_all_step_permutations
from metrics.distance_algorithms.dtw_boundaries import get_dtw_dummy_data, get_dtw_runtimes
from metrics.notes.note_evaluation_stats import NoteEvaluationStats
from metrics.notes.note_points import NotePoints
from metrics.notes.note_relationship_type import NoteRelationshipType
from metrics.rhythms.rhythm_evaluation_stats import RhythmEvaluationStats

def get_note_eval_stats(expected_notes, given_notes, scenario, points):
  note_eval_stats = NoteEvaluationStats(len(expected_notes), len(given_notes))
  perfect_match_notes = []
  cent_diff_notes = []
  harmonic_exp_notes = []

  for rel in scenario:
    rel_type = rel.type
    if rel_type == NoteRelationshipType.PERFECT_MATCH:
      note_eval_stats.perfect_matches += 1
      if rel.expected_note not in perfect_match_notes:
        perfect_match_notes.append(rel.expected_note)
    if rel_type == NoteRelationshipType.CENT_DIFFERENCE:
      note_eval_stats.cent_differences += 1
      if rel.expected_note not in cent_diff_notes:
        cent_diff_notes.append(rel.expected_note)
    if rel_type == NoteRelationshipType.HARMONIC:
      note_eval_stats.harmonics[rel.harmonic_info[0]] += 1
      if rel.expected_note not in harmonic_exp_notes:
        harmonic_exp_notes.append(rel.expected_note)
    if rel_type == NoteRelationshipType.UNRELATED:
      note_eval_stats.unrelated += 1
    if rel.expected_note == expected_notes[0] and rel_type == NoteRelationshipType.PERFECT_MATCH:
      note_eval_stats.got_lowest = True
  
  note_eval_stats.perfect_match_percentage = "{:.2f}".format((len(perfect_match_notes) / len(expected_notes)) * 100)
  note_eval_stats.cent_diff_percentage = "{:.2f}".format((len(cent_diff_notes) / len(expected_notes)) * 100)
  note_eval_stats.harmonic_exp_percentage = "{:.2f}".format((len(harmonic_exp_notes) / len(expected_notes)) * 100)
  note_eval_stats.harmonic_giv_percentage = "{:.2f}".format((sum(note_eval_stats.harmonics) / len(given_notes)) * 100)
  note_eval_stats.unrelated_percentage = "{:.2f}".format((note_eval_stats.unrelated / len(given_notes)) * 100)
  note_eval_stats.uncovered_notes = get_uncovered_notes(expected_notes, scenario)
  note_eval_stats.uncovered_percentage = "{:.2f}".format((len(note_eval_stats.uncovered_notes) / len(expected_notes)) * 100)
  note_eval_stats.covered_only_with_harmonics = get_covered_only_with_harmonics(expected_notes, scenario)
  note_eval_stats.covered_only_with_harmonics_percentage = "{:.2f}".format((len(note_eval_stats.covered_only_with_harmonics) / len(expected_notes)) * 100)
  note_eval_stats.multiply_covered_notes = get_multiply_covered_notes(expected_notes, scenario)
  note_eval_stats.multiply_covered_percentage = "{:.2f}".format((len(note_eval_stats.multiply_covered_notes) / len(expected_notes)) * 100)
  note_eval_stats.points = points

  print("\n------------ Statistics ------------")
  print(note_eval_stats)

def get_uncovered_notes(expected_notes, scenario):
  uncovered_notes = []
  for note in expected_notes:
    occurred = False
    for rel in scenario:
      if rel.expected_note == note and rel.type != NoteRelationshipType.UNRELATED:
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

def get_rhythm_eval_stats(expected_rhythm, given_rhythm, scenario, points):
  rhythm_eval_stats = RhythmEvaluationStats(len(expected_rhythm), len(given_rhythm))

  total_length_exp = get_total_length(expected_rhythm)
  total_length_giv = get_total_length(given_rhythm)
  current_source_index = 0
  current_target_index = 0
  sep_insertion_length = 0
  sep_deletion_length = 0
  slightly_shorter_length_loss = 0
  slightly_longer_length_gain = 0
  vastly_shorter_length_loss = 0
  vastly_longer_length_gain = 0
  prev_step = None

  for i in range(len(scenario)):
    current_step = scenario[i]
    if len(expected_rhythm) > 0:
      current_source = expected_rhythm[current_source_index]
    else:
      current_source = ""
    if len(given_rhythm) > 0:
      current_target = given_rhythm[current_target_index]
    else:
      current_target = ""
    if current_step == DistanceType.DELETION:
      if current_source_index == 0 or prev_step == DistanceType.DELETION:
        sep_deletion_length += current_source.quarterLength
        if current_source_index == len(expected_rhythm) - 1:
          rhythm_eval_stats.deletions.append(sep_deletion_length)
          sep_deletion_length = 0
      else:
        rhythm_eval_stats.deletions.append(sep_deletion_length)
        sep_deletion_length = 0
      if current_source_index < len(expected_rhythm) - 1:
        current_source_index += 1
    elif current_step == DistanceType.INSERTION:
      if current_target_index == 0 or prev_step == DistanceType.INSERTION:
        sep_insertion_length += current_target.quarterLength
        if current_target_index == len(given_rhythm) - 1:
          rhythm_eval_stats.insertions.append(sep_insertion_length)
          sep_insertion_length = 0
      else:
        rhythm_eval_stats.insertions.append(sep_insertion_length)
        sep_insertion_length = 0
      if current_target_index < len(given_rhythm) - 1:
        current_target_index += 1
    elif current_step == DistanceType.SAME:
      if current_source_index < len(expected_rhythm) - 1:
        current_source_index += 1
      if current_target_index < len(given_rhythm) - 1:
        current_target_index += 1
    elif current_step == DistanceType.SUBSTITUTION:
      # note-rhythm switch
      if (not current_source.isRest) and current_target.isRest:
        rhythm_eval_stats.note_rhythm_switch_length += current_source.quarterLength
      # rhythm-note switch
      if current_source.isRest and not current_target.isRest:
        rhythm_eval_stats.rhythm_note_switch_length += current_source.quarterLength
      # rhythm length differences
      slightly_shorter = is_slightly_shorter(current_source, current_target)
      slightly_longer = is_slightly_longer(current_source, current_target)
      vastly_shorter = is_vastly_shorter(current_source, current_target)
      vastly_longer = is_vastly_longer(current_source, current_target)
      # slightly shorter rhythms: sum the loss for the percentage
      if slightly_shorter:
        rhythm_eval_stats.slighthly_shorter_rhythm_count += 1
        slightly_shorter_length_loss += current_source.quarterLength - current_target.quarterLength
      # slightly longer rhythms: sum the gain for the percentage
      if slightly_longer:
        rhythm_eval_stats.slighthly_longer_rhythm_count += 1
        slightly_longer_length_gain += current_target.quarterLength - current_source.quarterLength
      # vastly shorter rhythms: sum the loss for the percentage
      if vastly_shorter:
        rhythm_eval_stats.vastly_shorter_rhythm_count += 1
        vastly_shorter_length_loss += current_source.quarterLength - current_target.quarterLength
      # vastly longer rhythms: sum the gain for the percentage
      if vastly_longer:
        rhythm_eval_stats.vastly_longer_rhythm_count += 1
        vastly_longer_length_gain += current_target.quarterLength - current_source.quarterLength
      if current_source_index < len(expected_rhythm) - 1:
        current_source_index += 1
      if current_target_index < len(given_rhythm) - 1:
        current_target_index += 1
    prev_step = current_step
  
  if total_length_exp != 0:
    rhythm_eval_stats.insertions_percentage = float("{:.2f}".format((sum(rhythm_eval_stats.insertions) / total_length_exp) * 100))
    rhythm_eval_stats.deletions_percentage = float("{:.2f}".format((sum(rhythm_eval_stats.deletions) / total_length_exp) * 100))
    rhythm_eval_stats.note_rhythm_switch_percentage = float("{:.2f}".format((rhythm_eval_stats.note_rhythm_switch_length / total_length_exp) * 100))
    rhythm_eval_stats.rhythm_note_switch_percentage = float("{:.2f}".format((rhythm_eval_stats.rhythm_note_switch_length / total_length_exp) * 100))
    rhythm_eval_stats.slighthly_shorter_rhythm_percentage = float("{:.2f}".format((slightly_shorter_length_loss / total_length_exp) * 100))
    rhythm_eval_stats.slighthly_longer_rhythm_percentage = float("{:.2f}".format((slightly_longer_length_gain / total_length_exp) * 100))
    rhythm_eval_stats.vastly_shorter_rhythm_percentage = float("{:.2f}".format((vastly_shorter_length_loss / total_length_exp) * 100))
    rhythm_eval_stats.vastly_longer_rhythm_percentage = float("{:.2f}".format((vastly_longer_length_gain / total_length_exp) * 100))
    rhythm_eval_stats.total_length_difference_percentage = float("{:.2f}".format((total_length_giv / total_length_exp) * 100))
  else:
    rhythm_eval_stats.insertions_percentage = float("{:.2f}".format(sum(rhythm_eval_stats.insertions) * 100))
    rhythm_eval_stats.deletions_percentage = 0
    rhythm_eval_stats.note_rhythm_switch_percentage = 0
    rhythm_eval_stats.rhythm_note_switch_percentage = 0
    rhythm_eval_stats.slighthly_shorter_rhythm_percentage = 0
    rhythm_eval_stats.slighthly_longer_rhythm_percentage = 0
    rhythm_eval_stats.vastly_shorter_rhythm_percentage = 0
    rhythm_eval_stats.vastly_longer_rhythm_percentage = 0
    rhythm_eval_stats.total_length_difference_percentage = rhythm_eval_stats.insertions_percentage
  rhythm_eval_stats.points = points

  print("\n------------ Statistics ------------")
  print(rhythm_eval_stats)

def is_slightly_shorter(exp, giv):
  return (exp.quarterLength / giv.quarterLength) > 1 and (exp.quarterLength / giv.quarterLength) <= 2

def is_slightly_longer(exp, giv):
  return (giv.quarterLength / exp.quarterLength) > 1 and (giv.quarterLength / exp.quarterLength) <= 2

def is_vastly_shorter(exp, giv):
  return (exp.quarterLength / giv.quarterLength) > 2

def is_vastly_longer(exp, giv):
  return (giv.quarterLength / exp.quarterLength) > 2

def get_total_length(expected_rhythm):
  total = 0
  for rhythm in expected_rhythm:
    total += rhythm.quarterLength
  return total

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