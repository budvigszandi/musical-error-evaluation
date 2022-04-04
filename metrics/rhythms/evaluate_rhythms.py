from metrics.distances.distance_type import DistanceType
from metrics.rhythms.rhythm_points import RhythmPoints

def get_rhythmic_point(step_permutation, source, target):
  # Starting from the maximum possible amount of points
  point = len(source) * RhythmPoints.CORRECT_RHYTHM_POINT
  current_source_index = 0
  current_target_index = 0
  for i in range(len(step_permutation)):
    current_step = step_permutation[i]
    # print("source", current_source_index, "target", current_target_index, "step", current_step)
    if current_step == DistanceType.DELETION:
      point += RhythmPoints.DELETED_RHYTHM_POINT
      point -= source[current_source_index].quarterLength * RhythmPoints.LENGTH_DIFFERENCE_WEIGHT
      if current_source_index < len(source) - 1: current_source_index += 1
    elif current_step == DistanceType.INSERTION:
      point += RhythmPoints.INSERTED_RHYTHM_POINT
      point -= target[current_target_index].quarterLength * RhythmPoints.LENGTH_DIFFERENCE_WEIGHT
      if current_target_index < len(target) - 1: current_target_index += 1
    elif current_step == DistanceType.SAME:
      if current_source_index < len(source) - 1: current_source_index += 1
      if current_target_index < len(target) - 1: current_target_index += 1
      continue
    elif current_step == DistanceType.SUBSTITUTION:
      point += RhythmPoints.SUBSTITUTED_RHYTHM_POINT
      point -= abs(get_rhythmic_distance(source[current_source_index], target[current_target_index]))
      if current_source_index < len(source) - 1: current_source_index += 1
      if current_target_index < len(target) - 1: current_target_index += 1
  return point

# requires two m21.note.Note objects
# TODO: Points should consider other rhythmic points as well
def get_rhythmic_distance(source, target):
  distance = 0
  if source.isNote != target.isNote and source.isChord != target.isChord and source.isRest != target.isRest:
    distance += RhythmPoints.DIFFERENT_TYPE_POINT
  if source.quarterLength != target.quarterLength:
    if source.quarterLength > target.quarterLength:
      distance += (source.quarterLength - target.quarterLength) * RhythmPoints.LENGTH_DIFFERENCE_WEIGHT
    else:
      distance += (target.quarterLength - source.quarterLength) * RhythmPoints.LENGTH_DIFFERENCE_WEIGHT
  return distance
