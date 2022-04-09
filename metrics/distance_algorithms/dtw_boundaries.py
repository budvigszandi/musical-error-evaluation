import time
import music21 as m21
import math

def get_dtw_runtimes(min_matrix_size, max_matrix_size):
  runtimes = {}
  data = get_dtw_dummy_data(min_matrix_size, max_matrix_size)
  print(f"Getting DTW runtimes on matrices from {min_matrix_size}x{min_matrix_size} to {max_matrix_size}x{max_matrix_size}")
  for d in data:
    count = str(len(d[0])) + "x" + str(len(d[1]))
    start = time.time()
    from evaluate import get_song_chunk_dtw_evaluation
    get_song_chunk_dtw_evaluation(d[0], d[1])
    end = time.time()
    runtimes[count] = "{:.2f}".format(end - start)
  return runtimes

def get_dtw_dummy_data(min_matrix_size, max_matrix_size):
  note_c = m21.note.Note("C4")
  dummy_data = []
  exp = []
  giv = []
  for i in range(min_matrix_size, max_matrix_size + 1):
    exp = i * [note_c]
    for j in range(min_matrix_size, max_matrix_size + 1):
      giv = j * [note_c]
      dummy_data.append([exp, giv])
  return dummy_data

def get_permutation_count_for_matrix(number_of_rows, number_of_columns):
  allowed_down_steps = number_of_rows - 1
  allowed_right_steps = number_of_columns - 1
  if number_of_rows < number_of_columns:
    max_diagonal_steps = number_of_rows - 1
  else:
    max_diagonal_steps = number_of_columns - 1

  permutation_count = 0

  for i in range(max_diagonal_steps + 1):
    if i > 0:
      allowed_down_steps -= 1
      allowed_right_steps -= 1
    allowed_diagonal_steps = i
    amount_of_steps = math.factorial(allowed_down_steps + allowed_right_steps + allowed_diagonal_steps)
    repetition_divisor = math.factorial(allowed_down_steps) * math.factorial(allowed_right_steps) * math.factorial(allowed_diagonal_steps)
    permutation_count += amount_of_steps / repetition_divisor
  
  return permutation_count
