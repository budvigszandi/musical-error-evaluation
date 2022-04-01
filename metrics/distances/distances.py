import numpy as np
from more_itertools import distinct_permutations
from metrics.rhythms.evaluate_rhythms import *
from metrics.distances.distance_type import *
from metrics.harmonic_parts.evaluate_harmonic_parts import *

# TODO: Documenting comments
# TODO: Correct the +1s in size_of_source and size_of_target in functions

def get_levenshtein_distance(source, target):
  size_of_source = len(source) + 1
  size_of_target = len(target) + 1
  distance_matrix = fill_levenshtein_distance_matrix(source, target)
  # Just testing output here
  print(distance_matrix)
  print("Levenshtein distance:", distance_matrix[size_of_source - 1][size_of_target - 1])
  #print(f"Distance between {source} and {target} is {distance_matrix[size_of_source - 1][size_of_target - 1]}") 
  return distance_matrix[size_of_source - 1][size_of_target - 1]

# len(source) number of rows, len(target) number of columns
def fill_levenshtein_distance_matrix(source, target):
  size_of_source = len(source) + 1
  size_of_target = len(target) + 1
  distance_matrix = initiate_levenshtein_distance_matrix(size_of_source, size_of_target)
  for i in range(1, size_of_source):
    for j in range(1, size_of_target):
      current_source = source[i - 1]
      current_target = target [j - 1]
      both_are_same_type = current_source.isNote == current_target.isNote or current_source.isRest == current_target.isRest
      # if current_source == current_target:
      if current_source == current_target and both_are_same_type:
        substitution_cost = 0
      else:
        substitution_cost = 1
      distance_matrix[i, j] = min(distance_matrix[i - 1, j] + 1,                      # deletion
                                  distance_matrix[i, j - 1] + 1,                      # insertion
                                  distance_matrix[i - 1, j - 1] + substitution_cost)  # substitution
  return distance_matrix

def initiate_levenshtein_distance_matrix(size_of_source, size_of_target):
  distance_matrix = np.zeros((size_of_source, size_of_target))
  for i in range(size_of_source):
    distance_matrix[i, 0] = i
  for j in range(size_of_target):
    distance_matrix[0, j] = j
  return distance_matrix

def dtw(s, t, window, harmonic_parts = False):
  n, m = len(s), len(t)
  w = np.max([window, abs(n - m)])
  dtw_matrix = np.zeros((n + 1, m + 1))
  
  for i in range(n + 1):
    for j in range(m + 1):
      dtw_matrix[i, j] = np.inf
  dtw_matrix[0, 0] = 0
  
  for i in range(1, n + 1):
    for j in range(np.max([1, i - w]), np.min([m, i + w]) + 1):
      dtw_matrix[i, j] = 0
  
  for i in range(1, n + 1):
    for j in range(np.max([1, i - w]), np.min([m, i + w]) + 1):
      if harmonic_parts:
        cost = abs(get_harmonic_part_distance(s[i - 1], t[j - 1]))
      else:
        cost = abs(get_rhythmic_distance(s[i - 1], t[j - 1]))
      # take last min from a square box
      last_min = np.min([dtw_matrix[i - 1, j],       # insertion
                         dtw_matrix[i, j - 1],       # deletion
                         dtw_matrix[i - 1, j - 1]])  # match
      dtw_matrix[i, j] = cost + last_min
  return dtw_matrix

def get_all_step_permutations(source, target):
  number_of_rows = len(source)
  number_of_columns = len(target)
  allowed_down_steps = number_of_rows
  allowed_right_steps = number_of_columns
  if number_of_rows < number_of_columns:
    max_diagonal_steps = number_of_rows
  else:
    max_diagonal_steps = number_of_columns

  allowed_steps_ordered = []

  for i in range(max_diagonal_steps + 1):
    allowed_steps = []
    if i > 0:
      allowed_down_steps -= 1
      allowed_right_steps -= 1
    allowed_diagonal_steps = i
    for j in range(allowed_down_steps):
      allowed_steps.append("L") # lower (go down)
    for j in range(allowed_right_steps):
      allowed_steps.append("R") # right (go right)
    for k in range(allowed_diagonal_steps):
      allowed_steps.append("D") # diagonal (go diagonally down)
    allowed_steps_ordered.append(allowed_steps)

  step_permutations = []
  for i in range(len(allowed_steps_ordered)):
    permutation = distinct_permutations(allowed_steps_ordered[i])
    step_permutations.append(permutation)
    # print(f"{len(allowed_steps_ordered[i])} long permutations: {len(permutation)}")
  
  return step_permutations

def convert_steps_with_points_levenshtein(step_permutations, source, target):
  all_step_permutations = list(step_permutations)
  # print("Amount of different step quantities (8 steps, 6 steps etc.)", len(all_step_permutations))

  # print("Permutations in X amount of steps", len(all_step_permutations[0]))

  steps_of_same_amount = list(all_step_permutations[0])
  # print("One permutation of steps", len(steps_of_same_amount[1]))

  # sum = 0
  # for i in range(len(all_step_permutations)):
  #   sum += len(all_step_permutations[i])
  # print(sum, "permutations")

  converted_permutations = []
  points = [] # TODO: This is a separate array because of the weird indexing
              # in the lower for loop 'for j in range(len(steps_of_same_amount)):'
              # This needs further checking.

  for i in range(len(all_step_permutations)):
    steps_of_same_amount = list(all_step_permutations[i])
    for j in range(len(steps_of_same_amount)):
      current_permutation = steps_of_same_amount[j]
      # print(j, current_permutation)
      current_source_index = 0
      current_target_index = 0
      permutation_as_reltype = []
      for k in range(len(current_permutation)):
        current_step = current_permutation[k]
        # print(current_step)
        if current_step == "L":
          # print("L")
          permutation_as_reltype.append(DistanceType.DELETION)
          current_source_index += 1
        elif current_step == "R":
          # print("R")
          permutation_as_reltype.append(DistanceType.INSERTION)
          current_target_index += 1
        elif current_step == "D":
          # print("D")
          if source[current_source_index] == target[current_target_index]:
            permutation_as_reltype.append(DistanceType.SAME)
          else:
            permutation_as_reltype.append(DistanceType.SUBSTITUTION)
          current_source_index += 1
          current_target_index += 1
      converted_permutations.append(permutation_as_reltype)
      points.append(get_rhythmic_point(permutation_as_reltype, source, target))
      # print(permutation_as_reltype)
  # print(len(permutations_as_reltypes), permutations_as_reltypes)
  
  return converted_permutations, points

def convert_steps_with_points_dtw(step_permutations, source, target, dtw_matrix, harmonic_parts = False):
  print("STEPS W POINTS source", source)
  print("STEPS W POINTS target", target)
  all_step_permutations = step_permutations
  steps_of_same_amount = all_step_permutations[0]

  converted_permutations = []
  points = [] # TODO: This is a separate array because of the weird indexing
              # in the lower for loop 'for j in range(len(steps_of_same_amount)):'
              # This needs further checking, maybe conversion to generator object.
  note_evaluations = []

  if source == [] or target == []:
    permutation_as_reltype = []
    if source == []:
      for i in target:
        permutation_as_reltype.append(DistanceType.INSERTION)
      converted_permutations.append(permutation_as_reltype)
    elif target == []:
      for i in source:
        permutation_as_reltype.append(DistanceType.DELETION)
      converted_permutations.append(permutation_as_reltype)
    note_evaluations.append(None)
    if harmonic_parts:
      points.append(get_harmonic_part_point(permutation_as_reltype, source, target))
    else:
      points.append(get_rhythmic_point(permutation_as_reltype, source, target))
    if not harmonic_parts:
      return converted_permutations, points
    else:
      return converted_permutations, points, note_evaluations

  for i in all_step_permutations:
    steps_of_same_amount = i
    for j in steps_of_same_amount:
      contains_infinity = False
      current_permutation = j
      current_source_index = 0
      current_target_index = 0
      dtw_matrix_i = 0
      dtw_matrix_j = 0
      permutation_as_reltype = []
      current_note_eval = []
      for k in current_permutation:
        current_step = k
        if current_step == "L":
          dtw_matrix_i += 1
          contains_infinity = is_infinity(dtw_matrix[dtw_matrix_i][dtw_matrix_j])
          permutation_as_reltype.append(DistanceType.INSERTION)
          if current_target_index < len(target) - 1: current_target_index += 1
        elif current_step == "R":
          dtw_matrix_j += 1
          contains_infinity = is_infinity(dtw_matrix[dtw_matrix_i][dtw_matrix_j])
          permutation_as_reltype.append(DistanceType.DELETION)
          if current_source_index < len(source) - 1: current_source_index += 1
          current_note_eval.append(None)
        elif current_step == "D":
          dtw_matrix_i += 1
          dtw_matrix_j += 1
          current_source = source[current_source_index]
          current_target = target[current_target_index]
          contains_infinity = is_infinity(dtw_matrix[dtw_matrix_i][dtw_matrix_j])
          rhythms_are_equal = current_source.quarterLength == current_target.quarterLength
          types_are_the_same = (current_source.isNote == current_target.isNote) and (current_source.isChord == current_target.isChord)
          
          if harmonic_parts:
            if current_source == current_target:
              permutation_as_reltype.append(DistanceType.SAME)
              current_note_eval.append(None)
            else:
              permutation_as_reltype.append(DistanceType.SUBSTITUTION)
              if current_source.isRest or current_target.isRest:
                current_note_eval.append(None)
              else:
                current_note_eval.append(get_best_note_evaluation(current_source, current_target, True, False))
          elif rhythms_are_equal and types_are_the_same:
            permutation_as_reltype.append(DistanceType.SAME)
          else:
            permutation_as_reltype.append(DistanceType.SUBSTITUTION)

          if current_source_index < len(source) - 1: current_source_index += 1
          if current_target_index < len(target) - 1: current_target_index += 1
        if contains_infinity:
          break
      if contains_infinity:
        continue
      converted_permutations.append(permutation_as_reltype)
      note_evaluations.append(current_note_eval)
      if harmonic_parts:
        points.append(get_harmonic_part_point(permutation_as_reltype, source, target))
      else:
        points.append(get_rhythmic_point(permutation_as_reltype, source, target))
  
  if not harmonic_parts:
    return converted_permutations, points
  else:
    return converted_permutations, points, note_evaluations

def is_infinity(element):
  return element == np.inf

def get_best_permutation_indices(points):
  max_point = max(points)
  indices = [index for index, value in enumerate(points) if value == max_point]
  return indices
