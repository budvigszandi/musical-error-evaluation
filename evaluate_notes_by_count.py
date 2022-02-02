from math import comb
import music21 as m21
from sqlalchemy import column
import harmonics

# Idea: check the number of given notes (less, equal, more) by checking
#       the relationship matrix rows and columns (<, =, >)

# Requires two lists of m21.pitch.Pitch objects
def compare_notes(expected_notes, given_notes):
  expected_notes_count = len(expected_notes)
  given_notes_count = len(given_notes)
  relationship_matrix = [[0 for i in range(expected_notes_count)] for j in range(given_notes_count)] 
  for i in range(expected_notes_count):
    for j in range(given_notes_count):
      relationship_matrix[i][j] = compare_note_pair(expected_notes[i], given_notes[j])
  # Just testing here
  for i in range(expected_notes_count):
    for j in range(given_notes_count):
      print(f"Z[{i}][{j}]: {expected_notes[i]} - {given_notes[j]} {relationship_matrix[i][j]}")
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

def get_scenarios(relationship_point_matrix):
  scenarios = {}
  rows = len(relationship_point_matrix)
  columns = len(relationship_point_matrix[0])
  print(f"{rows} rows {columns} columns")

  # sum = get_sum_of_scenario(scenario, relationship_point_matrix)
  # print("sum", sum)
  # scenario_tuple = tuple(scenario)
  # scenarios[scenario_tuple] = sum

  comblist = list(range(columns))
  extended_comblist = []
  for i in range(rows):
    extended_comblist += comblist
  from itertools import combinations
  variations = list(dict.fromkeys(combinations(extended_comblist, rows)))
  for i in list(variations):
    sum = get_sum_of_scenario(i, relationship_point_matrix)
    print(i, sum)
  return scenarios

def get_sum_of_scenario(scenario, relationship_point_matrix):
  sum = 0
  for i in range(len(scenario)):
    j = scenario[i]
    sum += relationship_point_matrix[i][j]
  return sum

# Requires two ordered lists of m21.pitch.Pitch objects
def compare_notes_n_to_n(expected_notes, given_notes):
  expected_notes_count = len(given_notes)
  perfect_match_count = 0
  matched_expected_notes = []
  unmatched_expected_notes = []
  unmatched_given_notes = []
  # --- Case 1: compare with 1st harmonics in the picture ---
  for i in range(expected_notes_count):
    print(expected_notes[i], "=?", given_notes[i])
    if expected_notes[i] == given_notes[i]:
      perfect_match_count += 1
      matched_expected_notes.append(expected_notes[i])
    else:
      unmatched_expected_notes.append(expected_notes[i])
      unmatched_given_notes.append(given_notes[i])
  # See how many unmatched and go on with those
  if perfect_match_count == expected_notes_count:
    print("100% match")
  else:
    # Working on unmatched notes
    unmatched_count = expected_notes_count - perfect_match_count
    print(f"{unmatched_count} unmatched notes")
    for i in range(unmatched_count):
      print(unmatched_given_notes[i], "could be:")
      # What the given note could be paired up with remaining expected notes:
      unmatched_with_unmatched_info = compare_note_pair(unmatched_expected_notes[i], unmatched_given_notes[i])
      print("Pairing with unmatched:")
      #print(unmatched_with_unmatched_info)
      print_unmatched_note_case(unmatched_expected_notes[i], unmatched_with_unmatched_info)
      # What the given note could be paired up with already matched expected notes
      # TODO: Unmatched are looked at twice, make it so that we check everything just once
      print("Pairing with matched:")
      unmatched_with_matched = []
      for note in expected_notes:
        unmatched_with_matched_info = compare_note_pair(note, unmatched_given_notes[i])
        unmatched_with_matched.append(unmatched_with_matched_info)
        #print(unmatched_with_matched_info)
        print_unmatched_note_case(note, unmatched_with_matched_info)
  return 0

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
def compare_note_pair(expected_note, given_note):
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

notes_ceg = [m21.pitch.Pitch('c4'), m21.pitch.Pitch('e4'), m21.pitch.Pitch('g4')]
notes_cec = [m21.pitch.Pitch('c4'), m21.pitch.Pitch('e4'), m21.pitch.Pitch('c5')]
notes_ace = [m21.pitch.Pitch('a3'), m21.pitch.Pitch('c3'), m21.pitch.Pitch('e3')]

# compare_notes_n_to_n(notes_ceg, notes_ceg)
# print("----------------------------------")
# compare_notes_n_to_n(notes_ceg, notes_cec)
# print("----------------------------------")
# compare_notes_n_to_n(notes_ceg, notes_ace)

rel_matrix = compare_notes(notes_ceg, notes_cec)
print("------------------------------")
rel_points_matrix = get_relationship_points(rel_matrix)
print("------------------------------")
print(get_scenarios(rel_points_matrix))

# one way to get index combinations
#matrix = [[0, 1, 2, 3], [3, 4, 5, 6], [6, 7, 8, 9]]
#matrix = [[0,0,0], [0,0,0], [0,0,0], [0,0,0]]
# scenario = [0, 0, 0]
# print(scenario)
# rows = len(matrix)
# columns = len(matrix[0])
# print(rows, "rows", columns, "columns")
# for i in range(rows):
#   for j in range(rows * pow(columns, i)):
#     for k in range(i+1):
#       if i > k-1:
#         if j % (pow(columns, k)) == 0:
#           scenario[- k - 1] += 1
#           for l in range(k):
#             scenario[- l -1] = 0
#     print(scenario)

# other way to get index combinations
# matrix = [[0,0,0], [0,0,0], [0,0,0]]
# rows = len(matrix)
# columns = len(matrix[0])
# comblist = list(range(columns))
# extended_comblist = []
# for i in range(rows):
#   extended_comblist += comblist
# from itertools import combinations
# variations = list(dict.fromkeys(combinations(extended_comblist, rows)))
# for i in list(variations):
#   print(i)