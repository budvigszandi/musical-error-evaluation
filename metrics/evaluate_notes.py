import metrics.harmonics as harmonics
from metrics.note_relationship_type import NoteRelationshipType
from metrics.note_relationship import NoteRelationship
from itertools import combinations
from collections import Counter

# TODO: When there is a chance of a harmonic, it should be only up until the 16th harmonic
# TODO: Scale points according to each other
# TODO: Declaring a maximum point (perfect match * number of expected notes) and
#       making statistics with the gotten points
# TODO: Can the points be the values of the relationship enumerator class?

PERFECT_MATCH_POINT = 20 # Harmonics would be worth more if this were less than 17!
CENT_DIFFERENCE_POINT = 17
HARMONIC_POINT = 1
UNRELATED_POINT = 0
COVERED_NOTE_POINT = 1
DUPLICATE_COVER_POINT = 1

RELATIONSHIP_POINT_WEIGHT = 1
COVERED_NOTE_POINT_WEIGHT = 1
DUPLICATE_POINT_WEIGHT = 1

MAXIMUM_HARMONIC_NUMBER = 17

def get_relationship_matrix(expected_notes, given_notes):
  '''
  Returns the relationship matrix of the expected and given notes. Each row is
  a given note, each column is an expected note, each element is the
  relationship between them.

  Args:
    expected_notes: an ordered list of the expected notes as m21.pitch.Pitch objects
    given_notes: an ordered list of the given notes as m21.pitch.Pitch objects
  '''
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

def get_relationship_points(relationship_matrix):
  '''
  Returns the relationship matrix of the expected and given notes. Each row is
  a given note, each column is an expected note, each element is the
  relationship between them (NoteRelationshipType).

  Args:
    relationship_matrix: a 2-d array of the relationships between the expected
                         and given notes.
  '''
  rows = len(relationship_matrix)
  columns = len(relationship_matrix[0])
  # print(f"Points: {rows} rows {columns} columns")
  relationship_point_matrix = [[0 for i in range(columns)] for j in range(rows)]
  # print(f"Points matrix: {len(relationship_point_matrix)} rows {len(relationship_point_matrix[0])} columns")
  for i in range(rows):
    for j in range(columns):
      # print(f"[{i}][{j}]: {relationship_matrix[i][j]}")
      current_relationship = relationship_matrix[i][j].type
      if current_relationship == NoteRelationshipType.HARMONIC:
        relationship_point_matrix[i][j] = get_current_point(current_relationship, relationship_matrix[i][j].harmonic_info[0])
      else:
        relationship_point_matrix[i][j] = get_current_point(current_relationship)
  # Just testing here
  for i in range(rows):
    for j in range(columns):
      print(f"R[{i}][{j}]: {relationship_point_matrix[i][j]}")
    if i < rows - 1:
      print("---")
  return relationship_point_matrix

def get_current_point(relationship_type, harmonic_number = -1):
  '''
  Returns the number of points the certain type of relationship between
  notes deserve.

  Args:
    relationship_type: a NoteRelationshipType
    (optional) harmonic_number: if the relationship_type is
                                NoteRelationshipType.HARMONIC, we have to give
                                the harmonic number as well
  '''
  if relationship_type == NoteRelationshipType.PERFECT_MATCH: # Perfect match
    return PERFECT_MATCH_POINT
  elif relationship_type == NoteRelationshipType.CENT_DIFFERENCE: # Cent difference
    return CENT_DIFFERENCE_POINT
  elif relationship_type == NoteRelationshipType.HARMONIC: # Harmonic
    return (MAXIMUM_HARMONIC_NUMBER - harmonic_number) * HARMONIC_POINT
  elif relationship_type == NoteRelationshipType.UNRELATED: # Unrelated
    return UNRELATED_POINT

def get_scenarios(relationship_matrix, relationship_point_matrix):
  '''
  Returns a dictionary of all the relationship combinations between the given
  and expected notes. The keys represent one combination of relationships, and
  the value says how many points this particular combination is worth. The
  dictionary is ordered by the value (from highest to lowest).

  Args:
    relationship_matrix: a 2-d array of the relationships between the expected
                         and given notes
    relationship_point_matrix: a 2-d array of the points relating to the
                               relationship_matrix.
  '''
  scenarios = {}
  rows = len(relationship_point_matrix)
  columns = len(relationship_point_matrix[0])
  #print(f"{rows} rows {columns} columns")
  index_variations = get_index_variations(rows, columns)
  for index_list in index_variations:
    sum = get_sum_of_scenario(index_list, relationship_point_matrix)
    scenario = get_current_scenario(relationship_matrix, index_list)
    scenario_tuple = tuple(scenario)
    scenarios[scenario_tuple] = sum
    # sorted_scenarios = sort_scenarios(scenarios)
  # return sorted_scenarios
  return scenarios

def get_index_variations(rows, columns):
  '''
  Returns a list of all the index combinations we can get from an (n x m) matrix
  if we want to get exactly one value from every row.

  Args:
    rows: an integer (>=0) number of rows
    columns: an integer (>=0) number of columns
  '''
  # -------- itertools.combinations approach --------
  # indexes = list(range(columns))
  # extended_indexes = []
  # for i in range(rows):
  #   extended_indexes += indexes
  # # index_variations = list(set(combinations(extended_indexes, rows)))
  # index_variations = combinations(extended_indexes, rows)
  # unique_index_variations = remove_duplicate_index_variations(index_variations)
  # return unique_index_variations
  # return index_variations
  # -------------------------------------------------

  # -------- multivector approach --------
  arr = [[] for i in range(rows)]
  for i in range(rows):
    for j in range(columns):
      arr[i].append(j)
  # print("starting indices", arr)
  index_variations = build_index_variations(arr)
  return index_variations
  # --------------------------------------

def build_index_variations(arr):
  # -------- multivector approach --------
  index_variations = []
  # number of arrays
  n = len(arr)

  # to keep track of next element
  # in each of the n arrays
  indices = [0 for i in range(n)]

  while (1):

    # print current combination
    current_combination = []
    for i in range(n):
      # print(arr[i][indices[i]], end = " ")
      current_combination.append(arr[i][indices[i]])
    index_variations.append(current_combination)
    # print()

    # find the rightmost array that has more
    # elements left after the current element
    # in that array
    next = n - 1
    while (next >= 0 and
      (indices[next] + 1 >= len(arr[next]))):
      next-=1

    # no such array is found so no more
    # combinations left
    if (next < 0):
      return index_variations

    # if found move to next element in that
    # array
    indices[next] += 1

    # for all arrays to the right of this
    # array current index again points to
    # first element
    for i in range(next + 1, n):
      indices[i] = 0
  # --------------------------------------

def remove_duplicate_index_variations(index_variations):
	unique = set()
	for x in index_variations:
		if x not in unique:
			yield x
			unique.add(x)
	return unique

def get_current_scenario(relationship_matrix, index_list):
  '''
  Returns a combination of relationships between the given and expected notes
  from the relationship matrix based on an index_list.

  Args:
    relationship_matrix: a 2-d array of the relationships between the expected
                         and given notes
    index_list: a list of indexes that we want to get from the matrix. The list
                has to contain as many numbers as there are rows in the matrix,
                and the indexes have to be >= 0 and < number of columns.
  '''
  scenario = []
  for i in range(len(index_list)):
    scenario.append(relationship_matrix[i][index_list[i]])
  return scenario

def get_sum_of_scenario(index_list, relationship_point_matrix):
  '''
  Returns a number which represents how many points a particular combination
  of relationships between the expected and given notes is worth.

  Args:
    index_list: a list of indexes that we want to get from the matrix. The list
                has to contain as many numbers as there are rows in the matrix,
                and the indexes have to be >= 0 and < number of columns.
    relationship_point_matrix: a 2-d array of the points relating to the
                               relationship matrix.
  '''
  sum = 0
  for i in range(len(index_list)):
    sum += relationship_point_matrix[i][index_list[i]]
  sum *= RELATIONSHIP_POINT_WEIGHT
  covered_notes_count = get_covered_notes_count(index_list)
  sum += covered_notes_count * COVERED_NOTE_POINT_WEIGHT
  duplicate_covers_count = get_duplicated_count(index_list)
  sum -= duplicate_covers_count * DUPLICATE_POINT_WEIGHT
  return sum

def get_covered_notes_count(index_list):
  '''
  Returns a number representing how many notes are covered by a certain
  combination of indexes.
  
  Args:
    index_list: a list of indexes that we want to get from the matrix. The list
                has to contain as many numbers as there are rows in the matrix,
                and the indexes have to be >= 0 and < number of columns.
  '''
  return len(Counter(index_list).keys()) * COVERED_NOTE_POINT

def get_duplicated_count(index_list):
  '''
  Returns a number representing how many duplications are in the coverage.
  E.g. we have 3 notes, the first covered once, the second covered twice,
  the third covered 3 times, we get 0 + 1 + 2 = 3.
  
  Args:
    index_list: a list of indexes that we want to get from the matrix. The list
                has to contain as many numbers as there are rows in the matrix,
                and the indexes have to be >= 0 and < number of columns.
  '''
  frequency_of_notes = Counter(index_list).values()
  number_of_duplicates_list = [i - 1 for i in frequency_of_notes]
  return sum(number_of_duplicates_list) * DUPLICATE_COVER_POINT

# TODO: Return all the best ones?
def get_best_scenario(scenarios):
  '''
  Returns one of the highest point scenarios.

  Args:
    scenarios: a dictionary of the scenarios
  '''
  return max(scenarios, key=scenarios.get)

def sort_scenarios(scenarios):
  '''
  Returns the sorted dictionary of scenarios (sorted by value, highest to lowest).
  
  Args:
    scenarios: a dictionary of the scenarios
  '''
  sorted_scenarios = {k: v for k, v in sorted(scenarios.items(), key=lambda item: item[1], reverse=True)}
  return sorted_scenarios

def compare_note_pair(given_note, expected_note):
  '''
  Returns a list with information about the current unmatched note pair in
  3-4 elements.
  1st element: The relationship of the given note with the expected note.
               This comes from the Relationship enum.
  2nd element: The given note.
  3rd element: The expected note.
  4th element: Only exists if there is a cent difference or the note is a harmonic.
               Cent difference: The difference in a number.
               Harmonic: A 2-element list of harmonic information
                         (which_harmonic, fundamental_note)
  Args:
    given_note: the given note as a m21.pitch.Pitch objects
    expected_note: the expected note as a m21.pitch.Pitch objects
  '''
  if expected_note.isEnharmonic(given_note):
    return NoteRelationship(NoteRelationshipType.PERFECT_MATCH, given_note, expected_note)
  elif expected_note.nameWithOctave == given_note.nameWithOctave:
    return NoteRelationship(NoteRelationshipType.CENT_DIFFERENCE, given_note, expected_note, given_note.microtone.cents - expected_note.microtone.cents)
  else:
    harmonic_info = harmonics.get_harmonic_info(given_note, expected_note)
    if harmonic_info != 0:
      return NoteRelationship(NoteRelationshipType.HARMONIC, given_note, expected_note, None, harmonic_info)
    else:
      return NoteRelationship(NoteRelationshipType.UNRELATED, given_note, expected_note)
