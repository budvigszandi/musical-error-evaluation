import time
import music21 as m21

def get_note_eval_runtimes(min_matrix_size, max_matrix_size):
  runtimes = {}
  data = get_note_dummy_data(min_matrix_size, max_matrix_size)
  print(f"Getting note evaluation runtimes on matrices from {min_matrix_size}x{min_matrix_size} to {max_matrix_size}x{max_matrix_size}")
  for d in data:
    print(f"Checking when expected {len(d[1])} and given {len(d[0])}")
    size = "Exp " + str(len(d[1])) + " Giv " + str(len(d[0]))
    start = time.time()
    scenario_count = get_note_eval_scenario_count(d[0], d[1])
    end = time.time()
    runtimes[size] = (str(scenario_count) + " scenarios", "{:.2f}".format(end - start))
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

def get_note_eval_scenario_count(expected_notes, given_notes):
  from metrics.notes.evaluate_notes import get_relationship_matrix, get_relationship_points, get_scenarios, get_best_scenario
  rel_matrix = get_relationship_matrix(expected_notes, given_notes)
  rel_points_matrix = get_relationship_points(rel_matrix)
  scenarios = get_scenarios(rel_matrix, rel_points_matrix)
  best_scenario = get_best_scenario(scenarios)
  return len(scenarios)