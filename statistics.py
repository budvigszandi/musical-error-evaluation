from metrics.distance_algorithms.distances import convert_steps_with_points_dtw, convert_steps_with_points_levenshtein, dtw, get_all_step_permutations
from metrics.distance_algorithms.dtw_boundaries import get_dtw_dummy_data, get_dtw_runtimes

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