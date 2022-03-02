from metrics.rhythm_relationship_type import RhythmRelationshipType
import numpy as np

CORRECT_RHYTHM_POINT = 10
DELETED_RHYTHM_POINT = -10
INSERTED_RHYTHM_POINT = -5
SUBSTITUTED_RHYTHM_POINT = -5

# TODO: Weigh the points based on
#       - length of rhythm
#       - note-rhythm and rhythm-note substitution
def get_rhythmic_point(step_permutation, source, target):
  # Starting from the maximum possible amount of points
  point = len(source) * CORRECT_RHYTHM_POINT
  for i in range(len(step_permutation)):
    current_step = step_permutation[i]
    if current_step == RhythmRelationshipType.DELETION:
      point += DELETED_RHYTHM_POINT
    elif current_step == RhythmRelationshipType.INSERTION:
      point += INSERTED_RHYTHM_POINT
    elif current_step == RhythmRelationshipType.SAME:
      continue
    elif current_step == RhythmRelationshipType.SUBSTITUTION:
      point += SUBSTITUTED_RHYTHM_POINT
  return point

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
          permutation_as_reltype.append(RhythmRelationshipType.DELETION)
          current_source_index += 1
        elif current_step == "R":
          # print("R")
          permutation_as_reltype.append(RhythmRelationshipType.INSERTION)
          current_target_index += 1
        elif current_step == "D":
          # print("D")
          if source[current_source_index] == target[current_target_index]:
            permutation_as_reltype.append(RhythmRelationshipType.SAME)
          else:
            permutation_as_reltype.append(RhythmRelationshipType.SUBSTITUTION)
          current_source_index += 1
          current_target_index += 1
      converted_permutations.append(permutation_as_reltype)
      points.append(get_rhythmic_point(permutation_as_reltype, source, target))
      # print(permutation_as_reltype)
  # print(len(permutations_as_reltypes), permutations_as_reltypes)
  
  return converted_permutations, points

def convert_steps_with_points_dtw(step_permutations, source, target, dtw_matrix):
  all_step_permutations = list(step_permutations)
  steps_of_same_amount = list(all_step_permutations[0])

  converted_permutations = []
  points = [] # TODO: This is a separate array because of the weird indexing
              # in the lower for loop 'for j in range(len(steps_of_same_amount)):'
              # This needs further checking.ú

  for i in range(len(all_step_permutations)):
    steps_of_same_amount = list(all_step_permutations[i])
    for j in range(len(steps_of_same_amount)):
      contains_infinity = False
      current_permutation = steps_of_same_amount[j]
      current_source_index = 0
      current_target_index = 0
      dtw_matrix_i = 0
      dtw_matrix_j = 0
      permutation_as_reltype = []
      for k in range(len(current_permutation)):
        current_step = current_permutation[k]
        if current_step == "L":
          dtw_matrix_i += 1
          contains_infinity = is_infinity(dtw_matrix[dtw_matrix_i][dtw_matrix_j])
          permutation_as_reltype.append(RhythmRelationshipType.INSERTION)
          current_source_index += 1
        elif current_step == "R":
          dtw_matrix_j += 1
          contains_infinity = is_infinity(dtw_matrix[dtw_matrix_i][dtw_matrix_j])
          permutation_as_reltype.append(RhythmRelationshipType.DELETION)
          current_target_index += 1
        elif current_step == "D":
          dtw_matrix_i += 1
          dtw_matrix_j += 1
          contains_infinity = is_infinity(dtw_matrix[dtw_matrix_i][dtw_matrix_j])
          if source[current_source_index] == target[current_target_index]:
            permutation_as_reltype.append(RhythmRelationshipType.SAME)
          else:
            permutation_as_reltype.append(RhythmRelationshipType.SUBSTITUTION)
          current_source_index += 1
          current_target_index += 1
        if contains_infinity:
          break
      if contains_infinity:
        continue
      converted_permutations.append(permutation_as_reltype)
      points.append(get_rhythmic_point(permutation_as_reltype, source, target))
  
  return converted_permutations, points

def is_infinity(element):
  return element == np.inf

def get_best_permutation_indices(points):
  max_point = max(points)
  indices = [index for index, value in enumerate(points) if value == max_point]
  return indices