from input.midi_reader import *
from metrics.distances.distances import *

def get_melody_dtw_evaluation(expected, given):
  # print(expected)
  # print(given)
  dtw_matrix = dtw(expected, given, 3, True)
  # print(dtw_matrix)

  all_step_permutations = get_all_step_permutations(expected, given)
  # print("Got all step permutations")
  converted_permutations_dtw, points, note_evaluations = convert_steps_with_points_dtw(all_step_permutations, expected, given, dtw_matrix, True)
  # print("Converted steps, got points")

  best_permutation_indices = get_best_permutation_indices(points)
  # print("Got best permutation indices")

  return converted_permutations_dtw[best_permutation_indices[0]], note_evaluations[best_permutation_indices[0]]

  # print("Best permutation(s):\n")
  # for index in best_permutation_indices:
  #   draw_harmonic_part_differences_from_steps(expected, given, converted_permutations_dtw[index], note_evaluations[index])
  #   print("Point:", points[index])
  #   print()

  # print(dtw_matrix)