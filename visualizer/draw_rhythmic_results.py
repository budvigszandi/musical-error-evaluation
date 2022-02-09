from visualizer.background_colors import *
from visualizer.rhythm_difference_string import *

def draw_rhythmic_differences(source, target, distance_matrix):
  i = len(source)
  j = len(target)
  compared_source_string = RhythmDifferenceString()
  compared_target_string = RhythmDifferenceString()
  current = distance_matrix[i, j] # starting from the bottom right corner
  while (i > 0) or (j > 0):
    current_source = get_current_element_string(source, i - 1)
    current_target = get_current_element_string(target, j - 1)
    # print(f"Source: {current_source}, Target: {current_target}")
    if current == 0 or source[i - 1] == target [j - 1]:
      # print("same character")
      i = i - 1
      j = j - 1
      compared_source_string.add(current_source, backgroundColors.SAME)
      compared_target_string.add(current_target, backgroundColors.SAME)
    elif current > 0:
      if current == distance_matrix[i - 1, j] + 1:
        # print("deletion")
        i = i - 1
        compared_source_string.add(current_source, backgroundColors.DELETION)
        compared_target_string.add(" " * len(current_source), backgroundColors.DELETION)
      elif current == distance_matrix[i, j - 1] + 1:
        # print("insertion")
        j = j - 1
        compared_source_string.add(" " * len(current_target), backgroundColors.INSERTION)
        compared_target_string.add(current_target, backgroundColors.INSERTION)
      elif current == distance_matrix[i - 1, j - 1] + 1:
        # print("substitution")
        i = i - 1
        j = j - 1
        compared_source_string.add(current_source, backgroundColors.SUBSTITUTION)
        compared_target_string.add(current_target, backgroundColors.SUBSTITUTION)
    current = distance_matrix[i][j]
  print("Wanted:", compared_source_string.string)
  print("Got   :", compared_target_string.string)
  print("\n" + get_color_map())
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

def get_color_map():
  return (f"Color map: {backgroundColors.SAME.value}SAME{backgroundColors.END_COLOR.value} "
                    f"{backgroundColors.DELETION.value}DELETION{backgroundColors.END_COLOR.value} "
                    f"{backgroundColors.INSERTION.value}INSERTION{backgroundColors.END_COLOR.value} "
                    f"{backgroundColors.SUBSTITUTION.value}SUBSTITUTION{backgroundColors.END_COLOR.value}")