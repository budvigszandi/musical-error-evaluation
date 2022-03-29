import music21 as m21
from metrics.notes.evaluate_notes import *
from visualizer.draw_note_results import *
from metrics.distances.distances import *
from visualizer.draw_rhythmic_results import *
from metrics.rhythms.evaluate_rhythms import *
from input.midi_reader import *
from visualizer.draw_harmonic_part_results import *
from metrics.distances.compressed_dtw import *
from metrics.distances.boyer_moore import *

# ------------------------------
# Expected and given note arrays
# ------------------------------

# expected_notes = [m21.pitch.Pitch('c4'), m21.pitch.Pitch('e4'), m21.pitch.Pitch('g4')]
# given_notes = [m21.pitch.Pitch('c4'), m21.pitch.Pitch('e4'), m21.pitch.Pitch('c5')]

expected_notes = [m21.pitch.Pitch('d1'), m21.pitch.Pitch('d--1'), m21.pitch.Pitch('c#3'),
                  m21.pitch.Pitch('c#4'), m21.pitch.Pitch('a4'), m21.pitch.Pitch('b4'),
                  m21.pitch.Pitch('c5'), m21.pitch.Pitch('d5')]
given_notes = [m21.pitch.Pitch('d-3'), m21.pitch.Pitch('d1'),  m21.pitch.Pitch('e2'),
               m21.pitch.Pitch('f3'), m21.pitch.Pitch('g3'), m21.pitch.Pitch('a3'),
               m21.pitch.Pitch('a4')]

# Example 1 for harmonics with coverage
# expected_notes = [m21.pitch.Pitch('c4'), m21.pitch.Pitch('f4'), m21.pitch.Pitch('c5')]
# given_notes = [m21.pitch.Pitch('c4'), m21.pitch.Pitch('c5'), m21.pitch.Pitch('c6')]

# Example 2 for harmonics with coverage
# expected_notes = [m21.pitch.Pitch('a1'), m21.pitch.Pitch('c2'), m21.pitch.Pitch('e2')]
# given_notes = [m21.pitch.Pitch('c2'), m21.pitch.Pitch('e3'), m21.pitch.Pitch('b3')]

# expected_notes = [m21.pitch.Pitch('c4'), m21.pitch.Pitch('e4'), m21.pitch.Pitch('g4')]
# given_notes = [m21.pitch.Pitch('c4'), m21.pitch.Pitch('c5'), m21.pitch.Pitch('c5')]

# expected_notes = [m21.pitch.Pitch('c4')]
# given_notes = [m21.pitch.Pitch('c4'), m21.pitch.Pitch('e4'), m21.pitch.Pitch('g4')]

# -----------------
# Getting scenarios
# -----------------

# rel_matrix = get_relationship_matrix(expected_notes, given_notes)
# print("------------------------------")
# rel_points_matrix = get_relationship_points(rel_matrix)
# print("------------------------------")
# scenarios = get_scenarios(rel_matrix, rel_points_matrix)

# ------------------
# Drawing a scenario
# ------------------

# print("Got scenarios, now drawing")
# fig, ax = plt.subplots()
# graph = nx.Graph()
# add_nodes(graph, expected_notes, given_notes)
# group_expected_nodes(expected_notes)
# # scenario = list(scenarios.keys())[0]
# scenario = get_best_scenario(scenarios)
# for rel in scenario:
#   print(str(rel))
# print(scenarios[scenario], "points")
# group_related_nodes_with_edge_creation(graph, expected_notes, scenario)
# group_isolated_expected_nodes(graph)
# draw_graph(graph, ax)

# ----------------------------------
# Expected and given rhythmic arrays
# ----------------------------------

d_quarter = m21.note.Note('d4')
c_quarter = m21.note.Note('c4')

c_half = m21.note.Note('c4')
c_half.duration.quarterLength = 2

d_half = m21.note.Note('d4')
d_half.duration.quarterLength = 2

rest_quarter = m21.note.Rest()

rest_half = m21.note.Rest()
rest_half.duration.quarterLength = 2

# expected_rhythm = [d_quarter, d_quarter, c_half,    rest_half,    d_quarter]  # qqh2q
# given_rhythm =    [c_half,    d_quarter, d_quarter, rest_quarter, d_quarter] # hqq1q

expected_rhythm = [d_quarter, d_quarter, d_half,    rest_half,    d_quarter]
given_rhythm =    [c_half,    c_quarter, c_quarter, rest_quarter, c_quarter]

# --------------------
# Levenshtein distance
# --------------------
# source = expected_rhythm
# target = given_rhythm

# all_step_permutations = get_all_step_permutations(source, target)
# # print(all_step_permutations)
# converted_permutations_lev, points = convert_steps_with_points_levenshtein(all_step_permutations, source, target)
# # print(len(permutations_as_reltypes), permutations_as_reltypes)

# print("All permutations:")
# for i in range(len(converted_permutations_lev)):
#   print(i + 1)
#   draw_rhythmic_differences_from_steps(source, target, converted_permutations_lev[i])
#   print("Point:", points[i])
#   print()

# print("Levenshtein scenario:")
# get_levenshtein_distance(source, target)
# distance_matrix = fill_distance_matrix(source, target)
# draw_rhythmic_differences_from_matrix(source, target, distance_matrix)

# --------------------
# Dynamic time warping
# --------------------
# source = expected_rhythm
# target = given_rhythm

# dtw_matrix = dtw(expected_rhythm, given_rhythm, 3)

# all_step_permutations = get_all_step_permutations(source, target)
# # print(all_step_permutations)
# converted_permutations_dtw, points = convert_steps_with_points_dtw(all_step_permutations, source, target, dtw_matrix)
# # print(len(permutations_as_reltypes), permutations_as_reltypes)

# print("All permutations:")
# for i in range(len(converted_permutations_dtw)):
#   print(i + 1)
#   draw_rhythmic_differences_from_steps(source, target, converted_permutations_dtw[i])
#   print("Point:", points[i])
#   print()

# best_permutation_indices = get_best_permutation_indices(points)

# print("Best permutation(s):\n")
# for index in best_permutation_indices:
#   draw_rhythmic_differences_from_steps(source, target, converted_permutations_dtw[index])
#   print("Point:", points[index])
#   print()

# print(dtw_matrix)

# ----------------------------
# DTW - Levenshtein statistics
# ----------------------------

# print("Levenshtein permutations:", len(converted_permutations_lev))
# print("DTW permutations:", len(converted_permutations_dtw))
# print(f"DTW permutations / Levenshtein permutations: {((len(converted_permutations_dtw) / len(converted_permutations_lev)) * 100):.2f} %")

# ---------------------------
# Expected and given melodies
# ---------------------------

score = get_score_from_midi("../midi/melody-sample-sevennationarmy-onenote.mid")
simplified_data = get_simplified_data_from_score(score)
score_multinote = get_score_from_midi("../midi/melody-sample-sevennationarmy-multinote.mid")
simplified_data_multinote = get_simplified_data_from_score(score_multinote)

# score = get_score_from_midi("../midi/sna-short-onenote.mid")
# simplified_data = get_simplified_data_from_score(score)
# score_multinote = get_score_from_midi("../midi/sna-short-multinote.mid")
# simplified_data_multinote = get_simplified_data_from_score(score_multinote)

expected_harmonic_part = simplified_data
given_harmonic_part    = simplified_data_multinote

# -----------------
# Melody evaluation
# -----------------

# put_sheet_in_output_folder(score)

# print(simplified_data)
# print(simplified_data_multinote)
# dtw_matrix = dtw(simplified_data, simplified_data_multinote, 2, True)
# print(dtw_matrix)

# all_step_permutations = get_all_step_permutations(expected_harmonic_part, given_harmonic_part)
# print("Got all step permutations")
# converted_permutations_dtw, points, note_evaluations = convert_steps_with_points_dtw(all_step_permutations, expected_harmonic_part, given_harmonic_part, dtw_matrix, True)
# print("Converted steps, got points")

# # print("All permutations:")
# # for i in range(len(converted_permutations_dtw)):
# #   print(i + 1)
# #   draw_harmonic_part_differences_from_steps(expected_harmonic_part, given_harmonic_part, converted_permutations_dtw[i], note_evaluations[i])
# #   print("Point:", points[i])
# #   print()

# best_permutation_indices = get_best_permutation_indices(points)
# print("Got best permutation indices")

# print("Best permutation(s):\n")
# for index in best_permutation_indices:
#   draw_harmonic_part_differences_from_steps(expected_harmonic_part, given_harmonic_part, converted_permutations_dtw[index], note_evaluations[index])
#   print("Point:", points[index])
#   print()

# print(dtw_matrix)

# --------------
# Compressed DTW
# --------------
# n = len(simplified_data)
# m = len(simplified_data_multinote)
# window = 2
# constraint = max(window, abs(n - m))
# print("n", n, "m", m, "constraint", constraint)
# print("dtw size", n + 1, "x", m + 1)
# dtw_matrix = dtw(simplified_data, simplified_data_multinote, constraint, True)
# print(dtw_matrix)

# compressed_dtw = get_compressed_dtw(dtw_matrix, constraint)
# print("\ncompressed")
# print(compressed_dtw)

# print("step permutations for", compressed_dtw.shape[0], "rows", compressed_dtw.shape[1], "columns")
# count = 0
# step_permutations = get_all_step_permutations(compressed_dtw.shape[0], compressed_dtw.shape[1])
# print(step_permutations)
# for i in step_permutations:
#   for j in i:
#     count += 1
# print(count)

# -----------
# Boyer-Moore
# -----------
# song = [m21.note.Note('C4'), m21.chord.Chord('C4 E4 G4'), m21.note.Rest(quarterLength = 0.5), m21.note.Note('G4')]
# pattern = [m21.note.Rest(), m21.note.Note('G4')]

song = simplified_data_multinote
pattern = [m21.note.Rest(), m21.note.Note('G4')]

# txt = ["h","e","l","l","o"]
# pat = "o"
txt = m21_to_boyer_moore(song)
pat = m21_to_boyer_moore(pattern)
print("txt", txt, "pattern", pat)
occurences = search(txt, pat)
print(occurences)

print(get_checkpoints(txt, 2))