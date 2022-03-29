from metrics.distances.distances import *
from input.midi_reader import *
import numpy as np

def get_compressed_dtw(dtw_matrix, constraint):
  dtw_rows = dtw_matrix.shape[0]
  dtw_columns = dtw_matrix.shape[1]
  compressed_rows = dtw_rows
  compressed_columns = min(dtw_columns, constraint * 2 + 2)
  print(f"{compressed_rows} rows, {compressed_columns} columns")
  compressed_dtw = np.zeros((compressed_rows, compressed_columns))
  switch_row = constraint + 2

  for i in range(min(switch_row, compressed_rows)):
    for j in range(compressed_columns):
      compressed_dtw[i][j] = dtw_matrix[i][j]
  
  mod = 0
  for i in range(switch_row, compressed_rows):
    mod += 1
    for j in range(compressed_columns):
      if j + mod >= dtw_columns:
        compressed_dtw[i][j] = np.inf
      else:
        compressed_dtw[i][j] = dtw_matrix[i][min(j + mod, dtw_columns - 1)]
  
  return compressed_dtw

def get_all_step_permutations(rows, columns):
  number_of_rows = rows
  number_of_columns = columns
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

def get_dtw_constraint(rows, columns, window):
  return max(window, abs(n - m))

def convert_steps_with_points_compressed_dtw(step_permutations, source, target, dtw_matrix, switch_row, harmonic_parts = False):
  all_step_permutations = step_permutations
  steps_of_same_amount = all_step_permutations[0]

  converted_permutations = []
  points = [] # TODO: This is a separate array because of the weird indexing
              # in the lower for loop 'for j in range(len(steps_of_same_amount)):'
              # This needs further checking, maybe conversion to generator object.
  note_evaluations = []

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
        is_switched_row = dtw_matrix_i >= switch_row
        current_step = get_current_step(k, is_switched_row)
        if current_step == "L":
          dtw_matrix_i += 1
          contains_infinity = is_infinity(dtw_matrix[dtw_matrix_i][dtw_matrix_j])
          permutation_as_reltype.append(DistanceType.INSERTION)
          current_target_index += 1
        elif current_step == "R":
          dtw_matrix_j += 1
          contains_infinity = is_infinity(dtw_matrix[dtw_matrix_i][dtw_matrix_j])
          permutation_as_reltype.append(DistanceType.DELETION)
          current_source_index += 1
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

          current_source_index += 1
          current_target_index += 1
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

def get_current_step(step, is_switched_row):
  if step == "L":
    if is_switched_row:
      return "D"
    else:
      return "L"
  elif step == "R":
    return "R"
  elif step == "D":
    if is_switched_row:
      return 0
    else:
      return "D"
  return 0

score = get_score_from_midi("../midi/rhythm-expected.mid")
simplified_data = get_simplified_data_from_score(score)
score_multinote = get_score_from_midi("../midi/melody-sample-sevennationarmy-onenote.mid")
simplified_data_multinote = get_simplified_data_from_score(score_multinote)

expected_harmonic_part = simplified_data
given_harmonic_part    = simplified_data_multinote

print(simplified_data)
print(simplified_data_multinote)

n = len(simplified_data)
m = len(simplified_data_multinote)
window = 2
constraint = max(window, abs(n - m))
print("n", n, "m", m, "constraint", constraint)
print("dtw size", n + 1, "x", m + 1)
dtw_matrix = dtw(simplified_data, simplified_data_multinote, constraint, True)
print(dtw_matrix)

compressed_dtw = get_compressed_dtw(dtw_matrix, constraint)
print("\ncompressed")
print(compressed_dtw)

print("step permutations for", compressed_dtw.shape[0], "rows", compressed_dtw.shape[1], "columns")
count = 0
step_permutations = get_all_step_permutations(compressed_dtw.shape[0], compressed_dtw.shape[1])
for i in step_permutations:
  for j in i:
    count += 1
print(count)

# "összecsúsztatott" mátrix
# az utakat az összecsúsztatott mátrix szerint legenerálom,
# majd azokat átkonvertálom és végigmegyek az igazi mátrixon
# (tehát nem kell másikat csinálni belőle, csak mintha létezne)