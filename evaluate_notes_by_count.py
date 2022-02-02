import music21 as m21
import harmonics
from itertools import combinations

# Idea: check the number of given notes (less, equal, more) by checking
#       the relationship matrix rows and columns (<, =, >)

# Requires two lists of m21.pitch.Pitch objects
def compare_notes(expected_notes, given_notes):
  expected_notes_count = len(expected_notes)
  given_notes_count = len(given_notes)
  relationship_matrix = [[0 for i in range(expected_notes_count)] for j in range(given_notes_count)] 
  for i in range(expected_notes_count):
    for j in range(given_notes_count):
      relationship_matrix[i][j] = compare_note_pair(given_notes[i], expected_notes[j])
  # Just testing here
  for i in range(expected_notes_count):
    for j in range(given_notes_count):
      print(f"Z[{i}][{j}]: {given_notes[i]} - {expected_notes[j]} {relationship_matrix[i][j]}")
    if i < expected_notes_count - 1:
      print("---")
  return relationship_matrix

def get_relationship_points(relationship_matrix):
  rows = len(relationship_matrix)
  columns = len(relationship_matrix[0])
  relationship_point_matrix = [[0 for i in range(rows)] for j in range(columns)]
  for i in range(rows):
    for j in range(columns):
      relationship_point_matrix[i][j] = get_current_point(relationship_matrix[i][j][0])
  # Just testing here
  for i in range(rows):
    for j in range(columns):
      print(f"R[{i}][{j}]: {relationship_point_matrix[i][j]}")
    if i < rows - 1:
      print("---")
  return relationship_point_matrix

def get_current_point(relationship_id):
  if relationship_id == 0: # Perfect match
    return 10
  elif relationship_id == 0.5: # Cent difference
    return 8
  elif relationship_id == 1: # Harmonic TODO: Scale through different harmonics
    return 5
  elif relationship_id == -1: # Unrelated
    return -1

# Scenario: dictionary of sums with index lists (key: index list, value: sum)
def get_scenarios(relationship_point_matrix):
  scenarios = {}
  rows = len(relationship_point_matrix)
  columns = len(relationship_point_matrix[0])
  print(f"{rows} rows {columns} columns")
  index_variations = get_index_variations(rows, columns)
  for index_list in list(index_variations):
    sum = get_sum_of_scenario(index_list, relationship_point_matrix)
    scenario_tuple = tuple(index_list)
    scenarios[scenario_tuple] = sum
  return scenarios

def get_index_variations(rows, columns):
  indexes = list(range(columns))
  extended_indexes = []
  for i in range(rows):
    extended_indexes += indexes
  index_variations = list(dict.fromkeys(combinations(extended_indexes, rows)))
  return index_variations

def get_sum_of_scenario(scenario, relationship_point_matrix):
  sum = 0
  for i in range(len(scenario)):
    sum += relationship_point_matrix[i][scenario[i]]
  return sum

# Returns a list with information about the current unmatched note pair in
# 2-4 elements.
# 1st element: A number that identifies the type of this note in relation with
#              the expected note.
#              0: Perfect match, 0.5: Cent difference, 1: Harmonic, -1: Unrelated
#              (-2: Missing note <- this can come from other function) TODO: Can it?
# 2nd element: A string describing the type of this note in relation with the
#              expected note.
# 3rd element: The given note. If a note is missing, the list only contains the
#              1st and 2nd element.
# 4th element: Only exists if there is a cent difference or the note is a harmonic.
#              Cent difference: The difference in a number.
#              Harmonic: A 2-element list of harmonic information
#                        (which_harmonic, fundamental_note)
#
# Requires two m21.pitch.Pitch objects
def compare_note_pair(given_note, expected_note):
  if expected_note == given_note:
    return (0, "Perfect match", given_note)
  elif expected_note.nameWithOctave == given_note.nameWithOctave:
    return (0.5, "Cent difference", given_note, given_note.microtone.cents - expected_note.microtone.cents)
  else:
    harmonic_info = harmonics.get_harmonic_info(given_note, expected_note)
    if harmonic_info != 0:
      return (1, "Harmonic", given_note, harmonic_info)
    else:
      return (-1, "Unrelated", given_note)

def print_unmatched_note_case(expected_note, info):
  if info[0] == -1:
    print(f"- {expected_note}: unrelated")
  elif info[0] == 0:
    print(f"- {expected_note}: duplicate")
  elif info[0] == 0.5:
    print(f"- {expected_note}: note match with {info[3]} cent difference")
  else:
    print(f"- {expected_note}: {info[3][0]}. harmonic of {info[3][1]}")

# --------------------------------
# |Just trying the functions here|
# --------------------------------

c_20cent = m21.pitch.Pitch('c4')
c_20cent.microtone = 20
notes_ceg = [m21.pitch.Pitch('c4'), m21.pitch.Pitch('e4'), m21.pitch.Pitch('g4')]
notes_ceg20 = [c_20cent, m21.pitch.Pitch('e4'), m21.pitch.Pitch('g4')]
notes_cec = [m21.pitch.Pitch('c4'), m21.pitch.Pitch('e4'), m21.pitch.Pitch('c5')]
notes_ace = [m21.pitch.Pitch('a3'), m21.pitch.Pitch('c3'), m21.pitch.Pitch('e3')]

# compare_notes_n_to_n(notes_ceg, notes_ceg)
# print("----------------------------------")
# compare_notes_n_to_n(notes_ceg, notes_cec)
# print("----------------------------------")
# compare_notes_n_to_n(notes_ceg, notes_ace)

rel_matrix = compare_notes(notes_ceg, notes_ceg20)
print("------------------------------")
rel_points_matrix = get_relationship_points(rel_matrix)
print("------------------------------")
scenarios = get_scenarios(rel_points_matrix)
for key, value in scenarios.items():
    print(key, ':', value)