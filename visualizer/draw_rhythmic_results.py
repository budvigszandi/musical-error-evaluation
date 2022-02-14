from metrics.rhythm_relationship_type import RhythmRelationshipType
from visualizer.background_colors import *
from visualizer.rhythm_difference_string import *

def draw_rhythmic_differences_from_matrix(source, target, distance_matrix):
  i = len(source)
  j = len(target)
  compared_source_string = RhythmDifferenceString()
  compared_target_string = RhythmDifferenceString()
  current = distance_matrix[i, j] # starting from the bottom right corner
  while (i > 0) or (j > 0):
    current_source = get_current_element_string(source, i - 1)
    current_target = get_current_element_string(target, j - 1)
    if i >= 0 and j == 0:
      compared_source_string.add_to_front(current_source, backgroundColors.DELETION)
      compared_target_string.add_to_front(" " * len(current_source), backgroundColors.DELETION)
      i -= 1
      continue
    
    if j >= 0 and i == 0:
      compared_source_string.add_to_front(" " * len(current_target), backgroundColors.INSERTION)
      compared_target_string.add_to_front(current_target, backgroundColors.INSERTION)
      j -= 1
      continue
    # print(f"Source: {current_source}, Target: {current_target}")
    if current == 0 or source[i - 1] == target [j - 1]:
      # print("same character")
      i = i - 1
      j = j - 1
      compared_source_string.add_to_front(current_source, backgroundColors.SAME)
      compared_target_string.add_to_front(current_target, backgroundColors.SAME)
    elif current > 0:
      if current == distance_matrix[i - 1, j] + 1:
        # print("deletion")
        i = i - 1
        compared_source_string.add_to_front(current_source, backgroundColors.DELETION)
        compared_target_string.add_to_front(" " * len(current_source), backgroundColors.DELETION)
      elif current == distance_matrix[i, j - 1] + 1:
        # print("insertion")
        j = j - 1
        compared_source_string.add_to_front(" " * len(current_target), backgroundColors.INSERTION)
        compared_target_string.add_to_front(current_target, backgroundColors.INSERTION)
      elif current == distance_matrix[i - 1, j - 1] + 1:
        # print("substitution")
        i = i - 1
        j = j - 1
        compared_source_string.add_to_front(current_source, backgroundColors.SUBSTITUTION)
        compared_target_string.add_to_front(current_target, backgroundColors.SUBSTITUTION)
    current = distance_matrix[i][j]
  print("Best scenario")
  print("Wanted:", compared_source_string.string)
  print("Got   :", compared_target_string.string)
  print("\n" + get_color_map())

def draw_rhythmic_differences_from_steps(source, target, steps):
  compared_source_string = RhythmDifferenceString()
  compared_target_string = RhythmDifferenceString()

  current_source_index = 0
  current_target_index = 0

  for i in range(len(steps)):
    current_step = steps[i]
    # print("si", current_source_index, "ti", current_target_index)
    current_source = source[current_source_index]
    current_target = target[current_target_index]
    if current_step == RhythmRelationshipType.DELETION:
      # print("deletion", current_source, current_target)
      compared_source_string.add_to_back(current_source, backgroundColors.DELETION)
      compared_target_string.add_to_back(" " * len(current_source), backgroundColors.DELETION)
      if current_source_index < len(source) - 1:
        current_source_index += 1
    elif current_step == RhythmRelationshipType.INSERTION:
      # print("insertion", current_source, current_target)
      compared_source_string.add_to_back(" " * len(current_target), backgroundColors.INSERTION)
      compared_target_string.add_to_back(current_target, backgroundColors.INSERTION)
      if current_target_index < len(target) - 1:
        current_target_index += 1
    elif current_step == RhythmRelationshipType.SAME:
      # print("same", current_source, current_target)
      compared_source_string.add_to_back(current_source, backgroundColors.SAME)
      compared_target_string.add_to_back(current_target, backgroundColors.SAME)
      if current_source_index < len(source) - 1:
        current_source_index += 1
      if current_target_index < len(target) - 1:
        current_target_index += 1
    elif current_step == RhythmRelationshipType.SUBSTITUTION:
      # print("substitution", current_source, current_target)
      compared_source_string.add_to_back(current_source, backgroundColors.SUBSTITUTION)
      compared_target_string.add_to_back(current_target, backgroundColors.SUBSTITUTION)
      if current_source_index < len(source) - 1:
        current_source_index += 1
      if current_target_index < len(target) - 1:
        current_target_index += 1
  
  print("Wanted:", compared_source_string.string)
  print("Got   :", compared_target_string.string)
  print()

def get_current_element_string(elements, index):
  current_element = ""
  for i in range(len(elements)):
    # Commented these because of testing with simple strings instead of notes
    # and rests until the logic is ready
    # if elements[i].isNote:
    #   type = "N"
    # elif elements[i].isRest:
    #   type = "R"
    if i == index:
      # current_element = type + " - " + str(elements[i].duration.quarterLength)
      current_element = str(elements[i])
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