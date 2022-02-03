import music21 as m21
import harmonics
from relationship_type import RelationshipType
from relationship import Relationship
from itertools import combinations

# Idea: check the number of given notes (less, equal, more) by checking
#       the relationship matrix rows and columns (<, =, >)

# Returns the relationship matrix of the expected and given notes. Each row is
# a given note, each column is an expected note, each element is the
# relationship between them.
#
# Requires two lists of m21.pitch.Pitch objects
def get_relationship_matrix(expected_notes, given_notes):
  expected_notes_count = len(expected_notes)
  given_notes_count = len(given_notes)
  relationship_matrix = [[0 for i in range(expected_notes_count)] for j in range(given_notes_count)] 
  # rows = len(relationship_matrix)
  # columns = len(relationship_matrix[0])
  # print(f"Initializing {rows} rows {columns} columns")
  for i in range(given_notes_count):
    for j in range(expected_notes_count):
      relationship_matrix[i][j] = compare_note_pair(given_notes[i], expected_notes[j])
  # Just testing here
  for i in range(given_notes_count):
    for j in range(expected_notes_count):
      current = relationship_matrix[i][j]
      print(f"Z[{i}][{j}]: {current.given_note} - {current.expected_note} {current.type} "
            f"{current.cent_difference} {current.harmonic_info}")
    if i < given_notes_count - 1:
      print("---")
  return relationship_matrix

# Returns the relationship matrix of the expected and given notes. Each row is
# a given note, each column is an expected note, each element is the
# relationship between them.
#
# Requires a matrix (2-d array) of the relationships between the expected and
# given notes.
def get_relationship_points(relationship_matrix):
  rows = len(relationship_matrix)
  columns = len(relationship_matrix[0])
  # print(f"Points: {rows} rows {columns} columns")
  relationship_point_matrix = [[0 for i in range(columns)] for j in range(rows)]
  # print(f"Points matrix: {len(relationship_point_matrix)} rows {len(relationship_point_matrix[0])} columns")
  for i in range(rows):
    for j in range(columns):
      # print(f"[{i}][{j}]: {relationship_matrix[i][j]}")
      relationship_point_matrix[i][j] = get_current_point(relationship_matrix[i][j].type)
  # Just testing here
  for i in range(rows):
    for j in range(columns):
      print(f"R[{i}][{j}]: {relationship_point_matrix[i][j]}")
    if i < rows - 1:
      print("---")
  return relationship_point_matrix

# Returns the number of points the certain type of relationship between
# notes deserve.
#
# Requires a RelationshipType
def get_current_point(relationship):
  if relationship == RelationshipType.PERFECT_MATCH: # Perfect match
    return 10
  elif relationship == RelationshipType.CENT_DIFFERENCE: # Cent difference
    return 8
  elif relationship == RelationshipType.HARMONIC: # Harmonic TODO: Scale through different harmonics
    return 5
  elif relationship == RelationshipType.UNRELATED: # Unrelated
    return -1

# Returns a dictionary of all the relationship combinations between the given
# and expected notes. The keys represent one combination of relationships, and
# the value is how many points this particular combination is worth.
#
# Requires a matrix (2-d array) of the relationships between the expected and
# given notes and a matrix (2-d array) of the points relating to the other
# matrix.
def get_scenarios(relationship_matrix, relationship_point_matrix):
  scenarios = {}
  rows = len(relationship_point_matrix)
  columns = len(relationship_point_matrix[0])
  #print(f"{rows} rows {columns} columns")
  index_variations = get_index_variations(rows, columns)
  for index_list in list(index_variations):
    sum = get_sum_of_scenario(index_list, relationship_point_matrix)
    scenario = get_current_scenario(relationship_matrix, index_list)
    scenario_tuple = tuple(scenario)
    scenarios[scenario_tuple] = sum
  return scenarios

# Returns a list of all the index combinations we can get from an n x m matrix
# if we want to get exactly one value from every row.
#
# Requires the number of rows and number of columns
def get_index_variations(rows, columns):
  indexes = list(range(columns))
  extended_indexes = []
  for i in range(rows):
    extended_indexes += indexes
  index_variations = list(dict.fromkeys(combinations(extended_indexes, rows)))
  # print(index_variations)
  return index_variations

# Returns a combination of relationships between the given and expected notes
# from the relationship matrix based on an index_list.
#
# Requires a matrix (2-d array) of the relationships between the expected and
# given notes and a list of indexes that we want to get from the matrix.
def get_current_scenario(relationship_matrix, index_list):
  scenario = []
  for i in range(len(index_list)):
    scenario.append(relationship_matrix[i][index_list[i]])
  return scenario

# Returns a number which represents how many points a particular combination
# of relationships between the expected and given notes is worth.
#
# Requires a list of numbers that represent the indexes we need from each line
# in the relationship matrix, and a matrix (2-d array) of the points relating
# to the relationship matrix.
def get_sum_of_scenario(index_list, relationship_point_matrix):
  sum = 0
  for i in range(len(index_list)):
    sum += relationship_point_matrix[i][index_list[i]]
  return sum

# Returns one of the highest point scenarios. TODO: Return all the best ones?
#
# Requires a dictionary of the scenarios
def get_best_scenario(scenarios):
  return max(scenarios, key=scenarios.get)

# Returns a list with information about the current unmatched note pair in
# 3-4 elements.
# 1st element: The relationship of the given note with the expected note.
#              This comes from the Relationship enum.
# 2nd element: The given note.
# 3rd element: The expected note.
# 4th element: Only exists if there is a cent difference or the note is a harmonic.
#              Cent difference: The difference in a number.
#              Harmonic: A 2-element list of harmonic information
#                        (which_harmonic, fundamental_note)
#
# Requires two m21.pitch.Pitch objects
# TODO: Create a separate object for this
def compare_note_pair(given_note, expected_note):
  if expected_note.isEnharmonic(given_note):
    return Relationship(RelationshipType.PERFECT_MATCH, given_note, expected_note)
    #return (RelationshipType.PERFECT_MATCH, given_note, expected_note)
  elif expected_note.nameWithOctave == given_note.nameWithOctave:
    return Relationship(RelationshipType.CENT_DIFFERENCE, given_note, expected_note, given_note.microtone.cents - expected_note.microtone.cents)
    #return (RelationshipType.CENT_DIFFERENCE, given_note, expected_note, given_note.microtone.cents - expected_note.microtone.cents)
  else:
    harmonic_info = harmonics.get_harmonic_info(given_note, expected_note)
    if harmonic_info != 0:
      return Relationship(RelationshipType.HARMONIC, given_note, expected_note, None, harmonic_info)
      #return (RelationshipType.HARMONIC, given_note, expected_note, harmonic_info)
    else:
      return Relationship(RelationshipType.UNRELATED, given_note, expected_note)
      #return (RelationshipType.UNRELATED, given_note, expected_note)

# --------------------------------
# |Just trying the functions here|
# --------------------------------

c_20cent = m21.pitch.Pitch('c4')
c_20cent.microtone = 20
expected_notes = [m21.pitch.Pitch('c4'), m21.pitch.Pitch('e4'), m21.pitch.Pitch('g4')]
notes_ceg20 = [c_20cent, m21.pitch.Pitch('e4'), m21.pitch.Pitch('g4')]
given_notes = [m21.pitch.Pitch('c4'), m21.pitch.Pitch('e4'), m21.pitch.Pitch('c5')]
notes_ace = [m21.pitch.Pitch('a3'), m21.pitch.Pitch('c3'), m21.pitch.Pitch('e3')]

# rel_matrix = compare_notes(expected_notes, given_notes)
# print("------------------------------")
# rel_points_matrix = get_relationship_points(rel_matrix)
# print("------------------------------")
# scenarios = get_scenarios(rel_matrix, rel_points_matrix)
# best_scenario = get_best_scenario(scenarios)
# print(best_scenario, scenarios[best_scenario])
# for key, value in scenarios.items():
#     print(key, ':', value)