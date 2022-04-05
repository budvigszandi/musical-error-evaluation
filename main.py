import music21 as m21
from dtw_boundaries import get_dtw_runtimes
from evaluate import get_melody_dtw_evaluation, get_only_dtw_evaluation, run_main_melody_evaluation
from metrics.notes.evaluate_notes import *
from visualizer.draw_note_results import *
from metrics.distances.distances import *
from visualizer.draw_rhythmic_results import *
from metrics.rhythms.evaluate_rhythms import *
from input.midi_reader import *
from visualizer.draw_harmonic_part_results import *
from metrics.distances.compressed_dtw import *
from metrics.distances.boyer_moore import *

# TODO: Refactor main

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

# ---------------------------
# Expected and given melodies
# ---------------------------

exp_score = get_score_from_midi("../midi/deja-vu.mid")
giv_score = get_score_from_midi("../midi/deja-vu-1csuszas-1felharm.mid")

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

# ----------------------------
# DTW - Levenshtein statistics
# ----------------------------

# print("Levenshtein permutations:", len(converted_permutations_lev))
# print("DTW permutations:", len(converted_permutations_dtw))
# print(f"DTW permutations / Levenshtein permutations: {((len(converted_permutations_dtw) / len(converted_permutations_lev)) * 100):.2f} %")

# --------------
# Compressed DTW
# --------------
# n = len(exp_harmonic_part)
# m = len(giv_harmonic_part)
# window = 2
# constraint = max(window, abs(n - m))
# print("n", n, "m", m, "constraint", constraint)
# print("dtw size", n + 1, "x", m + 1)
# dtw_matrix = dtw(exp_harmonic_part, giv_harmonic_part, constraint, True)
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

# ---------------
# Note evaluation
# ---------------

# note_eval = get_note_evaluation(expected_notes, given_notes)
# draw_note_evaluation(expected_notes, given_notes, note_eval)

# --------------------------------
# Melody evaluation using only DTW 
# --------------------------------

# get_only_dtw_evaluation(exp_score, giv_score)

# ------------------------------------------
# Melody evaluation with Boyer-Moore and DTW
# ------------------------------------------

run_main_melody_evaluation(exp_score, giv_score, True)

# -----------------
# DTW runtime check
# -----------------

# runtimes = get_dtw_runtimes()
# for elem in runtimes:
#   if float(runtimes[elem]) > 15:
#     print(elem, runtimes[elem], "seconds - LONG TIME")
#   else:
#     print(elem, runtimes[elem], "seconds")
