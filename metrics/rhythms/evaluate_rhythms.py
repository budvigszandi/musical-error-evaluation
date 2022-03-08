from metrics.distances.distance_type import DistanceType
import numpy as np

CORRECT_RHYTHM_POINT = 10
DELETED_RHYTHM_POINT = -10
INSERTED_RHYTHM_POINT = -5
SUBSTITUTED_RHYTHM_POINT = -5

DIFFERENT_TYPE_POINT = 10
LENGTH_DIFFERENCE_WEIGHT = 1

# TODO: Weigh the points based on
#       - length of rhythm
#       - note-rhythm and rhythm-note substitution
def get_rhythmic_point(step_permutation, source, target):
  # Starting from the maximum possible amount of points
  point = len(source) * CORRECT_RHYTHM_POINT
  current_source_index = 0
  current_target_index = 0
  for i in range(len(step_permutation)):
    current_step = step_permutation[i]
    print("source", current_source_index, "target", current_target_index, "step", current_step)
    if current_step == DistanceType.DELETION:
      point += DELETED_RHYTHM_POINT
      point -= source[current_source_index].quarterLength * LENGTH_DIFFERENCE_WEIGHT
      if current_source_index < len(source) - 1: current_source_index += 1
    elif current_step == DistanceType.INSERTION:
      point += INSERTED_RHYTHM_POINT
      point -= target[current_target_index].quarterLength * LENGTH_DIFFERENCE_WEIGHT
      if current_target_index < len(target) - 1: current_target_index += 1
    elif current_step == DistanceType.SAME:
      if current_source_index < len(source) - 1: current_source_index += 1
      if current_target_index < len(target) - 1: current_target_index += 1
      continue
    elif current_step == DistanceType.SUBSTITUTION:
      point += SUBSTITUTED_RHYTHM_POINT
      point -= abs(get_rhythmic_distance(source[current_source_index], target[current_target_index]))
      if current_source_index < len(source) - 1: current_source_index += 1
      if current_target_index < len(target) - 1: current_target_index += 1
  return point

# requires two m21.note.Note objects
# TODO: Points should consider other rhythmic points as well
def get_rhythmic_distance(source, target):
  distance = 0
  if source.isNote != target.isNote:
    distance += DIFFERENT_TYPE_POINT
  if source.quarterLength != target.quarterLength:
    if source.quarterLength > target.quarterLength:
      distance += (source.quarterLength - target.quarterLength) * LENGTH_DIFFERENCE_WEIGHT
    else:
      distance += (target.quarterLength - source.quarterLength) * LENGTH_DIFFERENCE_WEIGHT
  return distance
