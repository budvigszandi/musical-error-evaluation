import music21 as m21
from evaluate import *
from metrics.notes.evaluate_notes import *
from statistics import get_dtw_boundaries, get_dtw_levenshtein_stats
from metrics.notes.note_eval_boundaries import get_note_eval_runtimes
from visualizer.draw_note_results import *
from metrics.distance_algorithms.distances import *
from visualizer.draw_rhythmic_results import *
from metrics.rhythms.evaluate_rhythms import *
from input.midi_reader import *
from visualizer.draw_harmonic_part_results import *
from metrics.distance_algorithms.compressed_dtw import *
from metrics.distance_algorithms.boyer_moore import *

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

exp_score = get_score_from_midi("../midi/rhythm-expected.mid")
giv_score = get_score_from_midi("../midi/rhythm-given.mid")

# ----------------------------------------
# Song evaluation with Boyer-Moore and DTW
# ----------------------------------------

# run_main_song_evaluation(exp_score, giv_score, True)

# ------------------------------
# Song evaluation using only DTW 
# ------------------------------

# get_only_dtw_evaluation(exp_score, giv_score)

# ---------------
# Note evaluation
# ---------------

# note_eval = get_note_evaluation(expected_notes, given_notes)
# draw_note_evaluation(expected_notes, given_notes, note_eval)

# -------------------------------------------
# Rhythm evaluation with Levenshtein distance
# -------------------------------------------

# get_levenshtein_rhythm_evaluation(expected_rhythm, given_rhythm)

# --------------------------
# Rhythm evaluation with DTW
# --------------------------

get_dtw_rhythm_evaluation(expected_rhythm, given_rhythm)

# ----------------------------
# DTW - Levenshtein statistics
# ----------------------------

# get_dtw_levenshtein_stats(1, 7)

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

# -----------------
# DTW runtime check
# -----------------

# runtimes = get_dtw_boundaries(1, 10)

# -----------------------------
# Note evaluation runtime check
# -----------------------------

# runtimes = get_note_eval_runtimes(1, 8)
