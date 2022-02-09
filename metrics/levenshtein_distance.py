import numpy as np
from visualizer.background_colors import *

# TODO: Documenting comments and refactoring where it's needed

def get_levenshtein_distance(source, target):
  size_of_source = len(source) + 1
  size_of_target = len(target) + 1
  distance_matrix = fill_distance_matrix(source, target)
  # Just testing output here
  print(distance_matrix)
  print(f"Distance between {source} and {target} is {distance_matrix[size_of_source - 1][size_of_target - 1]}") 
  return distance_matrix[size_of_source - 1][size_of_target - 1]

def fill_distance_matrix(source, target):
  size_of_source = len(source) + 1
  size_of_target = len(target) + 1
  distance_matrix = initiate_distance_matrix(size_of_source, size_of_target)
  for i in range(1, size_of_source):
    for j in range(1, size_of_target):
      current_source = source[i - 1]
      current_target = target [j - 1]
      both_are_same_type = current_source.isNote == current_target.isNote or current_source.isRest == current_target.isRest
      if current_source == current_target and both_are_same_type:
        substitution_cost = 0
      else:
        substitution_cost = 1
      distance_matrix[i, j] = min(distance_matrix[i - 1, j] + 1,                      # deletion
                                  distance_matrix[i, j - 1] + 1,                      # insertion
                                  distance_matrix[i - 1, j - 1] + substitution_cost)  # substitution
  return distance_matrix

def initiate_distance_matrix(size_of_source, size_of_target):
  distance_matrix = np.zeros((size_of_source, size_of_target))
  for i in range(size_of_source):
    distance_matrix[i, 0] = i
  for j in range(size_of_target):
    distance_matrix[0, j] = j
  return distance_matrix

# TODO: Refactor this function (maybe a separate class for the output)
def get_one_by_one_comparison(source, target, distance_matrix):
  i = len(source)
  j = len(target)
  compared_source_string = f""
  compared_target_string = f""

  current = distance_matrix[i, j] # starting from the bottom right corner
  while (i > 0) or (j > 0):
    current_source = get_current_element_string(source, i - 1)
    current_target = get_current_element_string(target, j - 1)
    print(f"Source: {current_source}, Target: {current_target}")
    if current == 0 or source[i - 1] == target [j - 1]:
      print("same character")
      i = i - 1
      j = j - 1
      compared_source_string = f"{backgroundColors.SAME}{current_source}{backgroundColors.END_COLOR}" \
                                + " " + compared_source_string
      compared_target_string = f"{backgroundColors.SAME}{current_target}{backgroundColors.END_COLOR}" \
                                + " " + compared_target_string
    elif current > 0:
      if current == distance_matrix[i - 1, j] + 1:
        print("deletion")
        i = i - 1
        compared_source_string = f"{backgroundColors.DELETION}{current_source}{backgroundColors.END_COLOR}" \
                                  + " " + compared_source_string
        compared_target_string = " " * len(current_source) + " " + compared_target_string
      elif current == distance_matrix[i, j - 1] + 1:
        print("insertion")
        j = j - 1
        compared_source_string = " " * len(current_target) + " " + compared_source_string
        compared_target_string = f"{backgroundColors.INSERTION}{current_target}{backgroundColors.END_COLOR}" \
                                  + " " + compared_target_string
      elif current == distance_matrix[i - 1, j - 1] + 1:
        print("substitution")
        i = i - 1
        j = j - 1
        compared_source_string = f"{backgroundColors.SUBSTITUTION}{current_source}{backgroundColors.END_COLOR}" \
                                    + " " + compared_source_string
        compared_target_string = f"{backgroundColors.SUBSTITUTION}{current_target}{backgroundColors.END_COLOR}" \
                                  + " " + compared_target_string
    current = distance_matrix[i][j]

  print("Source:", compared_source_string)
  print("Target:", compared_target_string)
  return 0

def get_current_element_string(elements, index):
  current_element = ""
  for i in range(len(elements)):
    if elements[i].isNote:
      type = "N"
    elif elements[i].isRest:
      type = "R"
    if i == index:
      current_element = type + " - " + str(elements[i].duration.quarterLength)
  return current_element

  # ---
  # This is good for checking the whole source and target at each step
  # ---
  # highlighted_element = ""
  # for i in range(len(elements)):
  #   if elements[i].isNote:
  #     type = "N"
  #   elif elements[i].isRest:
  #     type = "R"
  #   if i == index:
  #     highlighted_element += "[" + type + " - " + str(elements[i].duration.quarterLength) + "] "
  #   else:
  #     highlighted_element += type + "-" + str(elements[i].duration.quarterLength) + " "
  # return highlighted_element