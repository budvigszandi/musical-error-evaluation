from input.midi_reader import *
from metrics.distance_algorithms.distances import *
from metrics.distance_algorithms.boyer_moore import *
from metrics.distance_algorithms.boyer_moore_m21 import get_bm_m21_notation_with_stats, get_different_parts as get_different_parts_bm_m21
from metrics.harmonic_parts.harmonic_part_evaluation_stats import HarmonicPartEvaluationStats
from metrics.normalize_points import NORMALIZE_MAXIMUM, NORMALIZE_MINIMUM
from statistics import get_final_song_stats, get_perfect_song_stats, get_rhythmic_length, get_song_chunk_note_eval_stats, get_note_eval_stats, get_rhythm_eval_stats, get_stat_elem_count
from visualizer.draw_harmonic_part_results import *
from visualizer.draw_note_results import *
from visualizer.draw_rhythmic_results import draw_rhythmic_differences_from_matrix, draw_rhythmic_differences_from_steps, get_color_map

def get_song_chunk_dtw_evaluation(expected, given):
  print("\n--- DTW song chunk evaluation ---")
  print("Expected:")
  print_song(expected)
  print("Given:")
  print_song(given)

  dtw_matrix = dtw(expected, given, 3, True)

  print("DTW matrix")
  print(dtw_matrix, end="\n\n")

  if (len(expected) >= 8 and len(given) >= 8):
    print("[!!!] DTW evaluations this big can take a very long time")
    print("[!!!] (from 1.5 minutes [exp:8, got:9] to 4.5 minutes [exp:9, got:9] and beyond)!")

  print("[-] Getting all step permuations for DTW matrix...")
  all_step_permutations = get_all_step_permutations(expected, given)
  print("[X] Got all step permutations")

  print("[-] Converting steps, counting permutation points...")
  converted_permutations_dtw, points, note_evaluations = convert_steps_with_points_dtw(all_step_permutations, expected, given, dtw_matrix, True)
  print("[X] Converted steps, got permutation points")

  print("[-] Getting best permutations...")
  best_permutation_indices = get_best_permutation_indices(points)
  print("[X] Got best permutations")

  print("\nAmount of best permutations:", len(best_permutation_indices))

  print("\n--- Chosen best permutation ---")
  best_permutation = converted_permutations_dtw[best_permutation_indices[0]]
  note_evaluation = note_evaluations[best_permutation_indices[0]]
  point = points[best_permutation_indices[0]]
  print(best_permutation)
  percentage = f"{((point / NORMALIZE_MAXIMUM) * 100):.2f}%"
  print("Points:", point, "/", NORMALIZE_MAXIMUM, "=", percentage, end="\n\n")

  song_chunk_note_eval_stats = get_song_chunk_note_eval_stats(expected, given, best_permutation, note_evaluation, point)
  rhythm_eval_stats = get_rhythm_eval_stats(expected, given, best_permutation, point)
  print("\n------------ Song chunk note statistics ------------")
  print(song_chunk_note_eval_stats)
  print("\n------------ Song chunk rhythm statistics ------------")
  print(rhythm_eval_stats)

  return best_permutation, note_evaluation, point, song_chunk_note_eval_stats, rhythm_eval_stats

def get_only_dtw_evaluation(exp_score, giv_score):
  if len(exp_score.parts) != len(giv_score.parts):
    raise ValueError(f"These scores have different amount of parts. Expected {len(exp_score.parts)} parts, given {len(giv_score.parts)} parts.")

  print("------ Drawing sheet music ------")
  for i in range(len(exp_score.parts)):
    put_sheet_in_output_folder(exp_score.parts[i])

  print("[-] Simplifying MIDI data...")
  expected_data = get_simplified_data_from_score(exp_score)
  given_data = get_simplified_data_from_score(giv_score)
  print("[X] Simplified MIDI data")

  print(f"[-] Examining {len(expected_data)} part(s) of music")

  exp_count = 0
  giv_count = 0
  points = 0
  for i in range(len(expected_data)):
    exp_count += get_stat_elem_count(expected_data[i])
    giv_count += get_stat_elem_count(given_data[i])
  exp_rhythmic_length = 0
  giv_rhythmic_length = 0
  song_stats = HarmonicPartEvaluationStats(exp_count, giv_count)

  for i in range(len(expected_data)):
    print(f"\n[-] Evaluating part {i + 1} of {len(expected_data)}...")
    expected = expected_data[i]
    given = given_data[i]
    if (len(expected) >= 8 and len(given) >= 8):
      print("[!!!] DTW evaluations this big can take a very long time")
      print("[!!!] (from 1.5 minutes [exp:8, got:9] to 4.5 minutes [exp:9, got:9] and beyond)!")
    exp_rhythmic_length += get_rhythmic_length(expected)
    giv_rhythmic_length += get_rhythmic_length(given)
    best_permutation, note_evaluations, point, note_stat, rhythm_stat = get_song_chunk_dtw_evaluation(expected, given)
    notation_string = get_notation_string_from_steps(expected, given, best_permutation, note_evaluations)
    draw_sheet_music(notation_string)
    song_stats.note_eval_stats.append(note_stat)
    song_stats.rhythm_eval_stats.append(rhythm_stat)
    points += point
    print(f"\n[X] Evaluated part {i + 1} of {len(expected_data)}")
  
  normalized_point = normalize(points, NORMALIZE_MINIMUM, NORMALIZE_MAXIMUM * len(expected_data))
  song_stats.point = "{:.2f}".format(points / len(expected_data))
  song_stats = get_final_song_stats(song_stats, exp_rhythmic_length, giv_rhythmic_length, 0, giv_rhythmic_length, normalized_point)
  print("\n------------------------------ Song statistics ------------------------------")
  print(song_stats)
  
  print("\n[X] Examined all parts of the music")

def run_main_song_evaluation(exp_score, giv_score, m21=False):
  if len(exp_score.parts) != len(giv_score.parts):
    raise ValueError(f"These scores have different amount of parts. Expected {len(exp_score.parts)} parts, given {len(giv_score.parts)} parts.")
  
  print("------ Drawing sheet music ------")
  for i in range(len(exp_score.parts)):
    put_sheet_in_output_folder(exp_score.parts[i])

  print("[-] Simplifying MIDI data...")
  expected_data = get_simplified_data_from_score(exp_score)
  given_data = get_simplified_data_from_score(giv_score)
  print("[X] Simplified MIDI data")

  print(f"[-] Examining {len(expected_data)} part(s) of music")

  for i in range(len(expected_data)):
    print(f"\n[-] Evaluating part {i + 1} of {len(expected_data)}...")
    expected = expected_data[i]
    given = given_data[i]

    print("-------------------------------- Original data --------------------------------")
    print("Expected song:")
    print_song(expected)
    print("Given song:")
    print_song(given)

    # if not m21:
    #   # Here we call the logic of metrics.distance_algorithms.boyer_moore, which is not
    #   # used now, but kept for chance of future development
    #   get_bm_char_evaluation(expected, given, giv_score)
    # else:
    #   get_bm_m21_evaluation(expected, given, giv_score)
    get_bm_m21_evaluation(expected, given, giv_score)
    print(f"\n[X] Evaluated part {i + 1} of {len(expected_data)}")
  
  print("\n[X] Examined all parts of the music")

# This is a function for metrics.distance_algorithms.boyer_moore, which is not
# used, but kept for chance of future development
# def get_bm_char_evaluation(expected, given, giv_score):
#   print("--------------------------- Boyer-Moore initializing --------------------------")
#   bm_expected = m21_to_boyer_moore(expected)
#   bm_given = m21_to_boyer_moore(given)
#   print("Expected:")
#   print(bm_expected, end="\n\n")
#   print("Given:")
#   print(bm_given, end="\n\n")

#   print("---------------------------- Boyer-Moore fixpoints ----------------------------")
#   exp_copy, giv_copy, exp_chunks, giv_chunks = get_different_parts(bm_expected, bm_given)
#   if exp_copy == [] and giv_copy == []:
#     print("\n------ Drawing sheet music ------")
#     put_sheet_in_output_folder(giv_score, True)
#   else:
#     print("--------------------------------- Evaluation ----------------------------------")
#     draw_from_bm_chars(expected, given, bm_expected, bm_given, exp_copy, giv_copy, exp_chunks, giv_chunks)

def get_bm_m21_evaluation(expected, given, giv_score):
  print("--------------------------- Boyer-Moore initializing --------------------------")

  print("---------------------------- Boyer-Moore fixpoints ----------------------------")
  exp_copy, giv_copy, exp_chunks, giv_chunks = get_different_parts_bm_m21(expected, given)

  print("--------------------------------- Evaluation ----------------------------------")
  if exp_copy == [] and giv_copy == []:
    print("\n------ Drawing sheet music ------")
    put_sheet_in_output_folder(giv_score, True)
    exp_count = get_stat_elem_count(expected)
    giv_count = get_stat_elem_count(given)
    song_stats = get_perfect_song_stats(exp_count, giv_count)
    print("\n------------------------------ Song statistics ------------------------------")
    print(song_stats)
  else:
    notation_string, song_stats = get_bm_m21_notation_with_stats(expected, given, exp_copy, giv_copy, exp_chunks, giv_chunks)
    print("\n------------------------------ Song statistics ------------------------------")
    print(song_stats)
    draw_sheet_music(notation_string)

def get_note_evaluation(expected_notes, given_notes):
  print("------------------------------- Note evaluation -------------------------------")

  print("Expected notes:")
  print_notes(expected_notes)
  print("Given notes:")
  print_notes(given_notes)

  if len(expected_notes) == 0 and len(given_notes) == 0:
    best_scenario = []
    points = NORMALIZE_MAXIMUM
    note_eval_stats = get_note_eval_stats(expected_notes, given_notes, best_scenario, points)
    print("\n------------ Statistics ------------")
    print(note_eval_stats)
    return best_scenario
  if len(expected_notes) == 0:
    best_scenario = []
    for note in given_notes:
      best_scenario.append(NoteRelationship(NoteRelationshipType.UNRELATED, note, None))
    points = NORMALIZE_MINIMUM
    note_eval_stats = get_note_eval_stats(expected_notes, given_notes, best_scenario, points)
    print("\n------------ Statistics ------------")
    print(note_eval_stats)
    return best_scenario
  if len(given_notes) == 0:
    best_scenario = []
    for note in expected_notes:
      best_scenario.append(NoteRelationship(NoteRelationshipType.UNRELATED, None, note))
    points = NORMALIZE_MINIMUM
    note_eval_stats = get_note_eval_stats(expected_notes, given_notes, best_scenario, points)
    print("\n------------ Statistics ------------")
    print(note_eval_stats)
    return best_scenario

  print("[-] Building relationship matrix...")
  rel_matrix = get_relationship_matrix(expected_notes, given_notes)
  print("[X] Built relationship matrix.")

  print("[-] Building relationship point matrix...")
  rel_points_matrix = get_relationship_points(rel_matrix)
  print("[X] Built relationship point matrix.")

  if (len(expected_notes) >= 6 and len(given_notes) >= 8) or (len(expected_notes) >= 8 and len(given_notes) >= 7):
    print("[!!!] Note evaluations this big can take a very long time")
    print("[!!!] (from 45 seconds [exp:8, got:7] to 6 minutes [exp:8, got:8] and beyond)!")

  print("[-] Getting scenarios...")
  scenarios = get_scenarios(rel_matrix, rel_points_matrix)
  print("[-] Got scenarios.")

  print("[-] Getting best scenario...")
  best_scenario = get_best_scenario(scenarios)
  print("[X] Got best scenario...")

  print("\n------ Chosen best scenario ------")
  for rel in best_scenario:
    print(rel)
  points = scenarios[best_scenario]
  percentage = f"{((points / NORMALIZE_MAXIMUM) * 100):.2f}%"
  print("Points:", points, "/", NORMALIZE_MAXIMUM, "=", percentage, end="\n\n")

  note_eval_stats = get_note_eval_stats(expected_notes, given_notes, best_scenario, points)
  print("\n------------ Statistics ------------")
  print(note_eval_stats)

  return best_scenario

def draw_note_evaluation(expected_notes, given_notes, note_eval):
  print("[-] Assembling result graph...")
  fig, ax = plt.subplots()
  graph = nx.Graph()
  add_nodes(graph, expected_notes, given_notes)
  group_expected_nodes(expected_notes)
  group_related_nodes_with_edge_creation(graph, expected_notes, given_notes, note_eval)
  group_isolated_expected_nodes(graph)
  print("[X] Assembled result graph, now drawing.")
  draw_graph(graph, ax)

def get_levenshtein_rhythm_evaluation(expected_rhythm, given_rhythm):
  print("------------------------ Levenshtein rhythm evaluation ------------------------")

  print("[-] Getting Levenshtein distance matrix...")
  distance_matrix = fill_levenshtein_distance_matrix(expected_rhythm, given_rhythm)
  print("[X] Got Levenshtein distance matrix:")
  print(distance_matrix)

  print("[-] Getting all step permuations for Levenshtein distance matrix...")
  all_step_permutations = get_all_step_permutations(expected_rhythm, given_rhythm)
  print("[X] Got all step permutations")

  print("[-] Converting steps, counting permutation points...")
  converted_permutations_lev, points = convert_steps_with_points_levenshtein(all_step_permutations, expected_rhythm, given_rhythm)
  print("[X] Converted steps, got permutation points")

  print("[-] Getting best permutations...")
  best_permutation_indices = get_best_permutation_indices(points)
  print("[X] Got best permutations")

  print("\nAmount of best permutations:", len(best_permutation_indices))
  best_permutation = converted_permutations_lev[best_permutation_indices[0]]

  print("\n--- Chosen best permutation (Levenshtein distance with points) ---")
  draw_rhythmic_differences_from_steps(expected_rhythm, given_rhythm, best_permutation)
  point = points[best_permutation_indices[0]]
  percentage = f"{((point / NORMALIZE_MAXIMUM) * 100):.2f}%"
  print("Points:", point, "/", NORMALIZE_MAXIMUM, "=", percentage, end="\n\n")

  rhythm_eval_stats = get_rhythm_eval_stats(expected_rhythm, given_rhythm, best_permutation, point)
  print("\n------------ Statistics ------------")
  print(rhythm_eval_stats)

  print("\n--- Permutation based on Levenshtein distance matrix without points ---")
  draw_rhythmic_differences_from_matrix(expected_rhythm, given_rhythm, distance_matrix)

def get_dtw_rhythm_evaluation(expected_rhythm, given_rhythm):
  print("---------------------------- DTW rhythm evaluation ----------------------------")
  print("Expected:")
  print_rhythms(expected_rhythm)
  print("Given:")
  print_rhythms(given_rhythm)

  dtw_matrix = dtw(expected_rhythm, given_rhythm, 3)

  print("DTW matrix")
  print(dtw_matrix, end="\n\n")

  if (len(expected_rhythm) >= 8 and len(given_rhythm) >= 8):
    print("[!!!] DTW evaluations this big can take a very long time")
    print("[!!!] (from 1.5 minutes [exp:8, got:9] to 4.5 minutes [exp:9, got:9] and beyond)!")

  print("[-] Getting all step permuations for DTW matrix...")
  all_step_permutations = get_all_step_permutations(expected_rhythm, given_rhythm)
  print("[X] Got all step permutations")

  print("[-] Converting steps, counting permutation points...")
  converted_permutations_dtw, points = convert_steps_with_points_dtw(all_step_permutations, expected_rhythm, given_rhythm, dtw_matrix)
  print("[X] Converted steps, got permutation points")

  print("[-] Getting best permutations...")
  best_permutation_indices = get_best_permutation_indices(points)
  print("[X] Got best permutations")

  print("\nAmount of best permutations:", len(best_permutation_indices))

  print("\n--- Chosen best permutation ---")
  best_permutation = converted_permutations_dtw[best_permutation_indices[0]]
  point = points[best_permutation_indices[0]]
  # print(best_permutation)
  percentage = f"{((point / NORMALIZE_MAXIMUM) * 100):.2f}%"
  draw_rhythmic_differences_from_steps(expected_rhythm, given_rhythm, converted_permutations_dtw[best_permutation_indices[0]])
  print("Points:", point, "/", NORMALIZE_MAXIMUM, "=", percentage, end="\n\n")
  print(get_color_map())

  rhythm_eval_stats = get_rhythm_eval_stats(expected_rhythm, given_rhythm, best_permutation, point)
  print("\n------------ Statistics ------------")
  print(rhythm_eval_stats)

  return best_permutation, point

def print_song(song):
  if len(song) == 0:
    print("[]")
  for i in range(len(song)):
    if song[i].isRest:
      print(f"[{i}] Rest - {song[i].duration.fullName}")
    elif song[i].isNote:
      print(f"[{i}] {str(song[i].nameWithOctave)} - {song[i].duration.fullName}")
    elif song[i].isChord:
      notes = [note.nameWithOctave for note in song[i]]
      print(f"[{i}] Chord{notes} - {song[i].duration.fullName}")
  print()

def print_notes(notes):
  if len(notes) == 0:
    print("[]")
  for i in range(len(notes)):
    print(f"[{i}] {notes[i].nameWithOctave}")
  print()

def print_rhythms(rhythms):
  if len(rhythms) == 0:
    print("[]")
  for i in range(len(rhythms)):
    if rhythms[i].isRest:
      print(f"[{i}] Rest - {rhythms[i].duration.fullName}")
    else:
      print(f"[{i}] Note/Chord - {rhythms[i].duration.fullName}")
  print()