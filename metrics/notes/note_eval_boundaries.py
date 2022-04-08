import time
import music21 as m21

def get_note_eval_runtimes(min_matrix_size, max_matrix_size):
  runtimes = {}
  data = get_note_dummy_data(min_matrix_size, max_matrix_size)
  print(f"Getting note evaluation runtimes on matrices from {min_matrix_size}x{min_matrix_size} to {max_matrix_size}x{max_matrix_size}")
  for d in data:
    count = str(len(d[0])) + "x" + str(len(d[1]))
    start = time.time()
    from evaluate import get_note_evaluation
    get_note_evaluation(d[0], d[1])
    end = time.time()
    runtimes[count] = "{:.2f}".format(end - start)
  return runtimes

def get_note_dummy_data(min_matrix_size, max_matrix_size):
  note_c = m21.pitch.Pitch("C4")
  dummy_data = []
  exp = []
  giv = []
  for i in range(min_matrix_size, max_matrix_size + 1):
    exp = i * [note_c]
    for j in range(min_matrix_size, max_matrix_size + 1):
      giv = j * [note_c]
      dummy_data.append([exp, giv])
  return dummy_data
