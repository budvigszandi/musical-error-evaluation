from metrics.distance_algorithms.distances import *
from input.midi_reader import *
import numpy as np

# "Compressed" DTW matrix idea
# Nice idea, still too slow going through all the steps
# Generating only proper steps is a different issue

def get_compressed_dtw(dtw_matrix, constraint):
  dtw_rows = dtw_matrix.shape[0]
  dtw_columns = dtw_matrix.shape[1]
  compressed_rows = dtw_rows
  compressed_columns = constraint * 2 + 2
  print(f"{compressed_rows} rows, {compressed_columns} columns")
  compressed_dtw = np.zeros((compressed_rows, compressed_columns))
  switch_row = constraint + 2

  for i in range(min(switch_row, compressed_rows)):
    for j in range(constraint - i + 1):
      compressed_dtw[i][j] = np.inf
    for j in range(constraint - i + 1, compressed_columns):
      dtw_j = j - (constraint - i + 1)
      if dtw_j >= dtw_columns:
        compressed_dtw[i][j] = np.inf
      else:
        compressed_dtw[i][j] = dtw_matrix[i][dtw_j]
  
  mod = 0
  for i in range(switch_row, compressed_rows):
    mod += 1
    for j in range(compressed_columns):
      if j + mod >= dtw_columns:
        compressed_dtw[i][j] = np.inf
      else:
        compressed_dtw[i][j] = dtw_matrix[i][min(j + mod, dtw_columns - 1)]
  
  return compressed_dtw

def get_all_step_permutations_compressed_dtw(rows, columns):
  number_of_rows = rows
  number_of_columns = columns
  allowed_down_steps = number_of_rows

  allowed_steps_ordered = []

  for i in range(number_of_rows):
    allowed_steps = []
    for j in range(allowed_down_steps - i):
      allowed_steps.append("L") # lower (go down)
    for j in range(i):
      allowed_steps.append("R") # right (go right)
      allowed_steps.append("D") # diagonal (go diagonally down to the left)
    allowed_steps_ordered.append(allowed_steps)
  
  step_permutations = []
  for i in range(len(allowed_steps_ordered)):
    permutation = distinct_permutations(allowed_steps_ordered[i])
    step_permutations.append(permutation)
    # print(f"{len(allowed_steps_ordered[i])} long permutations: {len(permutation)}")
  
  return step_permutations
