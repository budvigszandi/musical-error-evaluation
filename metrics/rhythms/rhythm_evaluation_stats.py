from metrics.normalize_points import NORMALIZE_MAXIMUM

class RhythmEvaluationStats:

  def __init__(self, exp_count, giv_count):
    self.exp_count = exp_count                    # Amount of expected rhythms
    self.giv_count = giv_count                    # Amount of given rhythms
    self.insertions = []                          # List of the rhythmic lengths of the separate inserted parts
    self.insertions_percentage = 0                # Percentage of the rhythmic length of all inserted parts (in respect to the whole expected length)
    self.deletions = []                           # List of the rhythmic lengths of the separate deleted parts
    self.deletions_percentage = 0                 # Percentage of the rhythmic length of all deleted parts (in respect to the whole expected length)
    self.note_rhythm_switch_length = 0            # Length (in quarters) of sounds that were substituted with rests
    self.note_rhythm_switch_percentage = 0        # Percentage of the rhythmic length of all sounds that were substituted with rests (in respect to the whole expected length)
    self.rhythm_note_switch_length = 0            # Length (in quarters) of rests that were substituted with sound
    self.rhythm_note_switch_percentage = 0        # Percentage of the rhythmic length of all rests that were substituted with sound (in respect to the whole expected length)
    self.slighthly_shorter_rhythm_count = 0       # Amount of rhythms that were substituted with a slightly shorter rhythm
    self.slighthly_shorter_rhythm_percentage = 0  # Percentage of the rhythmic length lost by the slightly shorter rhythms (in respect to the whole expected length)
    self.slighthly_longer_rhythm_count = 0        # Amount of rhythms that were substituted with a slightly longer rhythm
    self.slighthly_longer_rhythm_percentage = 0   # Percentage of the rhythmic length gained by the slightly longer rhythms (in respect to the whole expected length)
    self.vastly_shorter_rhythm_count = 0          # Amount of rhythms that were substituted with a vastly shorter rhythm
    self.vastly_shorter_rhythm_percentage = 0     # Percentage of the rhythmic length lost by the vastly shorter rhythms (in respect to the whole expected length)
    self.vastly_longer_rhythm_count = 0           # Amount of rhythms that were substituted with a vastly longer rhythm
    self.vastly_longer_rhythm_percentage = 0      # Percentage of the rhythmic length gained by the vastly longer rhythms (in respect to the whole expected length)
    self.total_length_difference_percentage = 0   # Percentage of the total given rhythmic length (in respect to the whole expected length)
    self.points = 0                               # Amount of points for this scenario out of 10

  def __str__(self):
    insertion_string = get_list_string(self.insertions)
    deletion_string = get_list_string(self.deletions)
    percentage = f"{((self.points / NORMALIZE_MAXIMUM) * 100):.2f}%"

    string_rep = f""
    string_rep += f"Expected {self.exp_count} rhythms, got {self.giv_count} rhythms\n"
    string_rep += f"  Lengths (in quarters) of inserted chunks: {insertion_string}\n"
    string_rep += f"    This is {self.insertions_percentage}% of the whole.\n"
    string_rep += f"  Lengths (in quarters) of deleted chunks: {deletion_string}\n"
    string_rep += f"    This is {self.deletions_percentage}% of the whole.\n"
    string_rep += f"  Length (in quarters) of sounds substituted with rests: {self.note_rhythm_switch_length}\n"
    string_rep += f"    This is {self.note_rhythm_switch_percentage}% of the whole.\n"
    string_rep += f"  Length (in quarters) of rests substituted with sounds: {self.rhythm_note_switch_length}\n"
    string_rep += f"    This is {self.rhythm_note_switch_percentage}% of the whole.\n"
    string_rep += f"  Amount of slightly shorter rhythms: {self.slighthly_shorter_rhythm_count}\n"
    string_rep += f"    These make it {self.slighthly_shorter_rhythm_percentage}% shorter.\n"
    string_rep += f"  Amount of slightly longer rhythms: {self.slighthly_longer_rhythm_count}\n"
    string_rep += f"    These make it {self.slighthly_longer_rhythm_percentage}% longer.\n"
    string_rep += f"  Amount of vastly shorter rhythms: {self.vastly_shorter_rhythm_count}\n"
    string_rep += f"    These make it {self.vastly_shorter_rhythm_percentage}% shorter.\n"
    string_rep += f"  Amount of vastly longer rhythms: {self.vastly_longer_rhythm_count}\n"
    string_rep += f"    These make it {self.vastly_longer_rhythm_percentage}% longer.\n"
    string_rep += f"  The given length is {self.total_length_difference_percentage}% of the expected length.\n"
    string_rep += f"  Points: {self.points} / {NORMALIZE_MAXIMUM} = {percentage}\n"

    return string_rep

def get_list_string(list):
  if len(list) == 0:
    return "0"
  i_string = ""
  for i in range(len(list)):
    if i == len(list) - 1:
      i_string += str(list[i])
    else:
      i_string += str(list[i]) + ", "
  return i_string
