from input.midi_reader import *
from metrics.distances.distances import *
from metrics.distances.boyer_moore import *
from visualizer.draw_harmonic_part_results import *

def get_melody_dtw_evaluation(expected, given):
  print("\n--- DTW evaluation ---")
  print("Expected:")
  print_song(expected)
  print("Given:")
  print_song(given)
  dtw_matrix = dtw(expected, given, 3, True)

  print("DTW matrix")
  print(dtw_matrix, end="\n\n")

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
  print("Points:", point, end="\n\n")

  return best_permutation, note_evaluation

def get_melody_evaluation(expected, given):
  print("-------------------------------- Original data --------------------------------")
  print("Expected song:")
  print_song(expected)
  print("Given song:")
  print_song(given)

  print("--------------------------- Boyer-Moore initializing --------------------------")
  bm_expected = m21_to_boyer_moore(expected)
  bm_given = m21_to_boyer_moore(given)
  print("Expected:")
  print(bm_expected, end="\n\n")
  print("Given:")
  print(bm_given, end="\n\n")

  print("---------------------------- Boyer-Moore fixpoints ----------------------------")
  exp_copy, giv_copy, exp_chunks, giv_chunks = get_different_parts(bm_expected, bm_given)
  if exp_copy == [] and giv_copy == []:
    print("Should draw the same sheet")
  else:
    print("--------------------------------- Evaluation ----------------------------------")
    draw_harmonic_part_differences_from_boyer_moore(expected, given, bm_expected, bm_given, exp_copy, giv_copy, exp_chunks, giv_chunks)

def print_song(song):
  if len(song) == 0:
    print("[]")
  for i in range(len(song)):
    print(f"[{i}] {str(song[i])} - {song[i].duration.fullName}")
  print()