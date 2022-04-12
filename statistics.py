from metrics.distance_algorithms.distance_type import DistanceType
from metrics.distance_algorithms.distances import convert_steps_with_points_dtw, convert_steps_with_points_levenshtein, dtw, get_all_step_permutations
from metrics.distance_algorithms.dtw_boundaries import get_dtw_dummy_data, get_dtw_runtimes
from metrics.harmonic_parts.harmonic_part_evaluation_stats import HarmonicPartEvaluationStats
from metrics.normalize_points import NORMALIZE_MAXIMUM
from metrics.notes.song_chunk_note_evaluation_stats import SongChunkNoteEvaluationStats
from metrics.notes.note_evaluation_stats import NoteEvaluationStats
from metrics.notes.note_points import NotePoints
from metrics.notes.note_relationship_type import NoteRelationshipType
from metrics.rhythms.rhythm_evaluation_stats import RhythmEvaluationStats
from operator import add

def get_perfect_song_stats(exp_count, giv_count):
  song_stats = HarmonicPartEvaluationStats(exp_count, giv_count)
  song_stats.matched_percentage = 100
  song_stats.points = NORMALIZE_MAXIMUM
  return song_stats

def get_final_song_stats(song_stats, exp_total_rhythmic_length, giv_total_rhythmic_length, matched_length, unmatched_length, point):
  song_stats.matched_percentage = "{:.2f}".format((matched_length / exp_total_rhythmic_length) * 100)
  song_stats.unmatched_percentage = "{:.2f}".format((unmatched_length / exp_total_rhythmic_length) * 100)
  merged_note_stats = get_merged_note_stats(0, 0, song_stats.note_eval_stats)
  merged_rhythm_stats = get_merged_rhythm_stats(0, 0, exp_total_rhythmic_length, giv_total_rhythmic_length, song_stats.rhythm_eval_stats)
  song_stats.merged_note_eval_stats = merged_note_stats
  song_stats.merged_rhythm_eval_stats = merged_rhythm_stats
  song_stats.points = point
  return song_stats

def get_merged_note_stats(exp_count, giv_count, note_stats_list):
  merged_note_stats = SongChunkNoteEvaluationStats(exp_count, giv_count)
  note_stat_count = len(note_stats_list)
  perfect_match_percentages = []
  cent_diff_percentages = []
  harmonic_exp_percentages = []
  harmonic_giv_percentages = []
  uncovered_percentages = []
  covered_only_with_harmonics_percentages = []
  multiply_covered_percentages = []

  for note_stat in note_stats_list:
    merged_note_stats.exp_count += note_stat.exp_count
    merged_note_stats.giv_count += note_stat.giv_count
    merged_note_stats.perfect_matches += note_stat.perfect_matches
    perfect_match_percentages.append(float(note_stat.perfect_match_percentage))
    merged_note_stats.cent_differences += note_stat.cent_differences
    cent_diff_percentages.append(float(note_stat.cent_diff_percentage))
    merged_note_stats.harmonics = list(map(add, merged_note_stats.harmonics, note_stat.harmonics))
    harmonic_exp_percentages.append(float(note_stat.harmonic_exp_percentage))
    harmonic_giv_percentages.append(float(note_stat.harmonic_giv_percentage))
    merged_note_stats.unrelated += note_stat.unrelated
    merged_note_stats.got_lowest_count += note_stat.got_lowest_count
    uncovered_percentages.append(float(note_stat.uncovered_percentage))
    covered_only_with_harmonics_percentages.append(float(note_stat.covered_only_with_harmonics_percentage))
    multiply_covered_percentages.append(float(note_stat.multiply_covered_percentage))
  
  merged_note_stats.perfect_match_percentage = "{:.2f}".format(sum(perfect_match_percentages) / len(perfect_match_percentages))
  merged_note_stats.cent_diff_percentage = "{:.2f}".format(sum(cent_diff_percentages) / len(cent_diff_percentages))
  merged_note_stats.harmonic_exp_percentage = "{:.2f}".format(sum(harmonic_exp_percentages) / len(harmonic_exp_percentages))
  merged_note_stats.harmonic_giv_percentage = "{:.2f}".format(sum(harmonic_giv_percentages) / len(harmonic_giv_percentages))
  merged_note_stats.unrelated_percentage = "{:.2f}".format(merged_note_stats.unrelated / merged_note_stats.giv_count)
  merged_note_stats.got_lowest_percentage = "{:.2f}".format(merged_note_stats.got_lowest_count / note_stat_count)
  merged_note_stats.uncovered_percentage = "{:.2f}".format(sum(uncovered_percentages) / len(uncovered_percentages))
  merged_note_stats.covered_only_with_harmonics_percentage = "{:.2f}".format(sum(covered_only_with_harmonics_percentages) / len(covered_only_with_harmonics_percentages))
  merged_note_stats.multiply_covered_percentage = "{:.2f}".format(sum(multiply_covered_percentages) / len(multiply_covered_percentages))
  
  return merged_note_stats

def get_merged_rhythm_stats(exp_count, giv_count, exp_total_rhythmic_length, giv_total_rhythmic_length, rhythm_stats_list):
  merged_rhythm_stats = RhythmEvaluationStats(exp_count, giv_count)
  slightly_shorter_rhythm_percentages = []
  slightly_longer_rhythm_percentages = []
  vastly_shorter_rhythm_percentages = []
  vastly_longer_rhythm_percentages = []

  for rhythm_stat in rhythm_stats_list:
    merged_rhythm_stats.exp_count += rhythm_stat.exp_count
    merged_rhythm_stats.giv_count += rhythm_stat.giv_count
    merged_rhythm_stats.insertions.extend(rhythm_stat.insertions)
    merged_rhythm_stats.deletions.extend(rhythm_stat.deletions)
    merged_rhythm_stats.note_rhythm_switch_length += rhythm_stat.note_rhythm_switch_length
    merged_rhythm_stats.rhythm_note_switch_length += rhythm_stat.rhythm_note_switch_length
    merged_rhythm_stats.slightly_shorter_rhythm_count += rhythm_stat.slightly_shorter_rhythm_count
    slightly_shorter_rhythm_percentages.append(float(rhythm_stat.slightly_shorter_rhythm_percentage))
    merged_rhythm_stats.slightly_longer_rhythm_count += rhythm_stat.slightly_longer_rhythm_count
    slightly_longer_rhythm_percentages.append(float(rhythm_stat.slightly_longer_rhythm_percentage))
    merged_rhythm_stats.vastly_shorter_rhythm_count += rhythm_stat.vastly_shorter_rhythm_count
    vastly_shorter_rhythm_percentages.append(float(rhythm_stat.vastly_shorter_rhythm_percentage))
    merged_rhythm_stats.vastly_longer_rhythm_count += rhythm_stat.vastly_longer_rhythm_count
    vastly_longer_rhythm_percentages.append(float(rhythm_stat.vastly_longer_rhythm_percentage))
  
  if exp_total_rhythmic_length != 0:
    merged_rhythm_stats.insertions_percentage = float("{:.2f}".format((sum(merged_rhythm_stats.insertions) / exp_total_rhythmic_length) * 100))
    merged_rhythm_stats.deletions_percentage = float("{:.2f}".format((sum(merged_rhythm_stats.deletions) / exp_total_rhythmic_length) * 100))
    merged_rhythm_stats.note_rhythm_switch_percentage = float("{:.2f}".format((merged_rhythm_stats.note_rhythm_switch_length / exp_total_rhythmic_length) * 100))
    merged_rhythm_stats.rhythm_note_switch_percentage = float("{:.2f}".format((merged_rhythm_stats.rhythm_note_switch_length / exp_total_rhythmic_length) * 100))
    if len(slightly_shorter_rhythm_percentages) > 0:
      merged_rhythm_stats.slightly_shorter_rhythm_percentage = float("{:.2f}".format(sum(slightly_shorter_rhythm_percentages) / len(slightly_shorter_rhythm_percentages)))
    if len(slightly_longer_rhythm_percentages) > 0:
      merged_rhythm_stats.slightly_longer_rhythm_percentage = float("{:.2f}".format(sum(slightly_longer_rhythm_percentages) / len(slightly_longer_rhythm_percentages)))
    if len(vastly_shorter_rhythm_percentages) > 0:
      merged_rhythm_stats.vastly_shorter_rhythm_percentage = float("{:.2f}".format(sum(vastly_shorter_rhythm_percentages) / len(vastly_shorter_rhythm_percentages)))
    if len(vastly_longer_rhythm_percentages) > 0:
      merged_rhythm_stats.vastly_longer_rhythm_percentage = float("{:.2f}".format(sum(vastly_longer_rhythm_percentages) / len(vastly_longer_rhythm_percentages)))
    merged_rhythm_stats.total_length_difference_percentage = float("{:.2f}".format((giv_total_rhythmic_length / exp_total_rhythmic_length) * 100))
  else:
    merged_rhythm_stats.insertions_percentage = float("{:.2f}".format(sum(merged_rhythm_stats.insertions) * 100))
    merged_rhythm_stats.total_length_difference_percentage = merged_rhythm_stats.insertions_percentage
  merged_rhythm_stats.points = 0

  return merged_rhythm_stats

def get_song_chunk_note_eval_stats(expected, given, scenario, note_evals, points):
  exp_count = get_stat_elem_count(expected)
  giv_count = get_stat_elem_count(given)
  song_chunk_note_stats = SongChunkNoteEvaluationStats(exp_count, giv_count)

  perfect_match_percentages = []
  cent_diff_percentages = []
  harmonic_exp_percentages = []
  harmonic_giv_percentages = []
  uncovered_count = 0
  covered_only_with_harmonics_count = 0
  multiply_covered_count = 0
  
  current_source_index = 0
  current_target_index = 0

  for i in range(len(scenario)):
    current_step = scenario[i]
    if len(expected) > 0: current_source = expected[current_source_index]
    if len(given) > 0: current_target = given[current_target_index]
    chunk_exp_count = get_stat_elem_count([current_source])
    chunk_giv_count = get_stat_elem_count([current_target])

    if current_step == DistanceType.DELETION:
      uncovered_count += chunk_exp_count
      perfect_match_percentages.append(0)
      cent_diff_percentages.append(0)
      harmonic_exp_percentages.append(0)
      harmonic_giv_percentages.append(0)
      if current_source_index < len(expected) - 1:
        current_source_index += 1
    elif current_step == DistanceType.INSERTION:
      song_chunk_note_stats.unrelated += chunk_giv_count
      perfect_match_percentages.append(0)
      cent_diff_percentages.append(0)
      harmonic_exp_percentages.append(0)
      harmonic_giv_percentages.append(0)
      if current_target_index < len(given) - 1:
        current_target_index += 1
    elif current_step == DistanceType.SAME:
      if current_source.isChord:
        song_chunk_note_stats.perfect_matches += len(current_source)
      else:
        song_chunk_note_stats.perfect_matches += 1
      perfect_match_percentages.append(100)
      cent_diff_percentages.append(0)
      harmonic_exp_percentages.append(0)
      harmonic_giv_percentages.append(0)
      if current_source_index < len(expected) - 1:
        current_source_index += 1
      if current_target_index < len(given) - 1:
        current_target_index += 1
    elif current_step == DistanceType.SUBSTITUTION:
      note_eval = note_evals[current_source_index]
      note_eval_stats = get_note_eval_stats([current_source], [current_target], note_eval, points)
      song_chunk_note_stats.perfect_matches += note_eval_stats.perfect_matches
      perfect_match_percentages.append(float(note_eval_stats.perfect_match_percentage))
      song_chunk_note_stats.cent_differences += note_eval_stats.cent_differences
      cent_diff_percentages.append(float(note_eval_stats.cent_diff_percentage))
      song_chunk_note_stats.harmonics = list(map(add, song_chunk_note_stats.harmonics, note_eval_stats.harmonics))
      harmonic_exp_percentages.append(float(note_eval_stats.harmonic_exp_percentage))
      harmonic_giv_percentages.append(float(note_eval_stats.harmonic_giv_percentage))
      song_chunk_note_stats.unrelated += note_eval_stats.unrelated
      if note_eval_stats.got_lowest:
        song_chunk_note_stats.got_lowest_count += 1
      uncovered_count += len(note_eval_stats.uncovered_notes)
      covered_only_with_harmonics_count += len(note_eval_stats.covered_only_with_harmonics)
      multiply_covered_count += len(note_eval_stats.multiply_covered_notes)
      
      if current_source_index < len(expected) - 1:
        current_source_index += 1
      if current_target_index < len(given) - 1:
        current_target_index += 1

  song_chunk_note_stats.perfect_match_percentage = "{:.2f}".format(sum(perfect_match_percentages) / len(perfect_match_percentages))
  song_chunk_note_stats.cent_diff_percentage = "{:.2f}".format(sum(cent_diff_percentages) / len(cent_diff_percentages))
  song_chunk_note_stats.harmonic_exp_percentage = "{:.2f}".format(sum(harmonic_exp_percentages) / len(harmonic_exp_percentages))
  song_chunk_note_stats.harmonic_giv_percentage = "{:.2f}".format(sum(harmonic_giv_percentages) / len(harmonic_giv_percentages))
  song_chunk_note_stats.unrelated_percentage = "{:.2f}".format((song_chunk_note_stats.unrelated / exp_count) * 100)
  song_chunk_note_stats.uncovered_percentage = "{:.2f}".format((uncovered_count / exp_count) * 100)
  song_chunk_note_stats.covered_only_with_harmonics_percentage = "{:.2f}".format((covered_only_with_harmonics_count / exp_count) * 100)
  song_chunk_note_stats.multiply_covered_percentage = "{:.2f}".format((multiply_covered_count / exp_count) * 100)

  return song_chunk_note_stats

def get_stat_elem_count(simplified_data):
  count = 0
  for d in simplified_data:
    if d.isRest or d.isNote:
      count += 1
    elif d.isChord:
      count += len(d)
  return count

def get_note_eval_stats(expected_notes, given_notes, scenario, points):
  note_eval_stats = NoteEvaluationStats(len(expected_notes), len(given_notes))

  if scenario == None:
    note_eval_stats.perfect_matches = note_eval_stats.exp_count
    note_eval_stats.perfect_match_percentage = 100
    if not expected_notes[0].isRest:
      note_eval_stats.got_lowest = True
    note_eval_stats.points = points
    return note_eval_stats
  else:
    perfect_match_notes = []
    cent_diff_notes = []
    harmonic_exp_notes = []
    exp_count = len(expected_notes)
    giv_count = len(given_notes)

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
    
    note_eval_stats.perfect_match_percentage = "{:.2f}".format((len(perfect_match_notes) / exp_count) * 100)
    note_eval_stats.cent_diff_percentage = "{:.2f}".format((len(cent_diff_notes) / exp_count) * 100)
    note_eval_stats.harmonic_exp_percentage = "{:.2f}".format((len(harmonic_exp_notes) / exp_count) * 100)
    note_eval_stats.harmonic_giv_percentage = "{:.2f}".format((sum(note_eval_stats.harmonics) / giv_count) * 100)
    note_eval_stats.unrelated_percentage = "{:.2f}".format((note_eval_stats.unrelated / giv_count) * 100)
    note_eval_stats.uncovered_notes = get_uncovered_notes(expected_notes, scenario)
    note_eval_stats.uncovered_percentage = "{:.2f}".format((len(note_eval_stats.uncovered_notes) / exp_count) * 100)
    note_eval_stats.covered_only_with_harmonics = get_covered_only_with_harmonics(expected_notes, scenario)
    note_eval_stats.covered_only_with_harmonics_percentage = "{:.2f}".format((len(note_eval_stats.covered_only_with_harmonics) / exp_count) * 100)
    note_eval_stats.multiply_covered_notes = get_multiply_covered_notes(expected_notes, scenario)
    note_eval_stats.multiply_covered_percentage = "{:.2f}".format((len(note_eval_stats.multiply_covered_notes) / exp_count) * 100)
    note_eval_stats.points = points

    return note_eval_stats

def get_uncovered_notes(expected_notes, scenario):
  uncovered_notes = []
  if scenario != None:
    for note in expected_notes:
      occurred = False
      for rel in scenario:
        if rel.expected_note.nameWithOctave == note.nameWithOctave and rel.type != NoteRelationshipType.UNRELATED:
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

  total_length_exp = get_rhythmic_length(expected_rhythm)
  total_length_giv = get_rhythmic_length(given_rhythm)
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
        rhythm_eval_stats.slightly_shorter_rhythm_count += 1
        slightly_shorter_length_loss += current_source.quarterLength - current_target.quarterLength
      # slightly longer rhythms: sum the gain for the percentage
      if slightly_longer:
        rhythm_eval_stats.slightly_longer_rhythm_count += 1
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
    rhythm_eval_stats.slightly_shorter_rhythm_percentage = float("{:.2f}".format((slightly_shorter_length_loss / total_length_exp) * 100))
    rhythm_eval_stats.slightly_longer_rhythm_percentage = float("{:.2f}".format((slightly_longer_length_gain / total_length_exp) * 100))
    rhythm_eval_stats.vastly_shorter_rhythm_percentage = float("{:.2f}".format((vastly_shorter_length_loss / total_length_exp) * 100))
    rhythm_eval_stats.vastly_longer_rhythm_percentage = float("{:.2f}".format((vastly_longer_length_gain / total_length_exp) * 100))
    rhythm_eval_stats.total_length_difference_percentage = float("{:.2f}".format((total_length_giv / total_length_exp) * 100))
  else:
    rhythm_eval_stats.insertions_percentage = float("{:.2f}".format(sum(rhythm_eval_stats.insertions) * 100))
    rhythm_eval_stats.deletions_percentage = 0
    rhythm_eval_stats.note_rhythm_switch_percentage = 0
    rhythm_eval_stats.rhythm_note_switch_percentage = 0
    rhythm_eval_stats.slightly_shorter_rhythm_percentage = 0
    rhythm_eval_stats.slightly_longer_rhythm_percentage = 0
    rhythm_eval_stats.vastly_shorter_rhythm_percentage = 0
    rhythm_eval_stats.vastly_longer_rhythm_percentage = 0
    rhythm_eval_stats.total_length_difference_percentage = rhythm_eval_stats.insertions_percentage
  rhythm_eval_stats.points = points

  return rhythm_eval_stats

def is_slightly_shorter(exp, giv):
  return (exp.quarterLength / giv.quarterLength) > 1 and (exp.quarterLength / giv.quarterLength) <= 2

def is_slightly_longer(exp, giv):
  return (giv.quarterLength / exp.quarterLength) > 1 and (giv.quarterLength / exp.quarterLength) <= 2

def is_vastly_shorter(exp, giv):
  return (exp.quarterLength / giv.quarterLength) > 2

def is_vastly_longer(exp, giv):
  return (giv.quarterLength / exp.quarterLength) > 2

def get_rhythmic_length(expected_rhythm):
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