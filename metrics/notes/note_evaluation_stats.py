from metrics.normalize_points import NORMALIZE_MAXIMUM
from metrics.notes.note_points import NotePoints

class NoteEvaluationStats:

  def __init__(self, exp_count, giv_count):
    self.exp_count = exp_count                # Amount of expected notes
    self.giv_count = giv_count                # Amount of given notes
    self.perfect_matches = 0                  # Amount of expected notes that were perfectly matched
    self.perfect_match_percentage = 0         # How many of the expected notes were found (%)
    self.cent_differences = 0                 # Amount of expected notes that had only cent difference
    self.cent_diff_percentage = 0             # How many of the expected notes were found with cent difference (%)
    self.harmonics = [0 for i in range(NotePoints.MAXIMUM_HARMONIC_NUMBER)]  # Distribution of harmonics (e.g. harmonics[5] = amount of 5th harmonics)
    self.harmonic_exp_percentage = 0          # How many of the expected notes had harmonics found (%)
    self.harmonic_giv_percentage = 0          # How many of the given notes are harmonics of expected notes (%)
    self.unrelated = 0                        # Amount of given notes that have no relation with any of the expected notes
    self.unrelated_percentage = 0             # How many of the given notes are unrelated to any expected note (%)
    self.got_lowest = False                   # Determines whether the lowest expected note was exactly found (perfectly matched)
    self.uncovered_notes = []                 # List of the expected notes that have no relation with any of the given notes
    self.uncovered_percentage = 0             # How many of the expected notes had no relationship with any of the given notes (%)
    self.covered_only_with_harmonics = {}     # Dictionary of the expected notes that were only covered by harmonics, not perfect matches
                                              # key = expected note, value = list distribution of harmonics (e.g. value[5] = amount of 5th harmonics)
    self.covered_only_with_harmonics_percentage = 0  # How many of the expected notes were covered only with harmonics (%)
    self.multiply_covered_notes = {}          # Dictionary of expected notes that were covered by multiple given notes
                                              # key = expected note, value = list of NoteRelationships
    self.multiply_covered_percentage = 0      # How many of the expected notes were multiply covered (%)
    self.points = 0                           # Amount of points for this scenario

  def __str__(self):
    harmonic_string = get_harmonic_distribution_string(self)
    uncovered_string = get_uncovered_notes_string(self)
    covered_only_with_harmonics_string = get_covered_only_with_harmonics_string(self)
    multiply_covered_string = get_multiply_covered_string(self)
    point_percentage = f"{((self.points / NORMALIZE_MAXIMUM) * 100):.2f}%"

    string_rep = f""
    string_rep += f"Expected {self.exp_count} notes, got {self.giv_count} notes\n"
    string_rep += f"  Perfect match count: {self.perfect_matches}, {self.perfect_match_percentage:.2f}% of the expected notes\n"
    string_rep += f"  Cent difference count: {self.cent_differences}, {self.cent_diff_percentage:.2f}% of the expected notes\n"
    string_rep += f"  Harmonics distribution:\n{harmonic_string}"
    string_rep += f"    Found harmonics for {self.harmonic_exp_percentage:.2f}% of the expected notes\n"
    string_rep += f"    {self.harmonic_giv_percentage:.2f}% of the given notes were harmonics of something\n"
    string_rep += f"  Unrelated note count: {self.unrelated}, {self.unrelated_percentage:.2f}% of the given notes\n"
    string_rep += f"  Got lowest expected note: {self.got_lowest}\n"
    string_rep += f"  Uncovered {self.uncovered_percentage:.2f}% of the expected notes:\n"
    string_rep += f"{uncovered_string}"
    string_rep += f"  Covered {self.covered_only_with_harmonics_percentage:.2f}% of the expected notes with only harmonics:\n"
    string_rep += f"{covered_only_with_harmonics_string}"
    string_rep += f"  Multiply covered {self.multiply_covered_percentage:.2f}% of the expected notes:\n"
    string_rep += f"{multiply_covered_string}"
    string_rep += f"  Points: {self.points} / {NORMALIZE_MAXIMUM} = {point_percentage}\n"
    
    return string_rep

def get_harmonic_distribution_string(self):
  if sum(self.harmonics) == 0:
    return "    None\n"
  
  h_string = ""
  for i in range(len(self.harmonics)):
    if self.harmonics[i] > 0:
      h_string += "    "+ str(i) + ". harmonic count: " + str(self.harmonics[i]) + "\n"
  return h_string

def get_uncovered_notes_string(self):
  if len(self.uncovered_notes) == 0:
    return "    None\n"
  
  u_string = ""
  for i in range(len(self.uncovered_notes)):
    if i == len(self.uncovered_notes) - 1:
      u_string += self.uncovered_notes[i].nameWithOctave
    else:
      u_string += self.uncovered_notes[i].nameWithOctave + ", "
  return u_string

def get_covered_only_with_harmonics_string(self):
  if len(self.covered_only_with_harmonics) == 0:
    return "    None\n"
  
  h_string = ""
  for note in self.covered_only_with_harmonics:
    h_string += "    " + note.nameWithOctave + ":\n"
    for i in range(len(self.covered_only_with_harmonics[note])):
      if self.covered_only_with_harmonics[note][i] > 0:
        h_string += "      " + str(i) + ". harmonic count: " + str(self.covered_only_with_harmonics[note][i]) + "\n"
  return h_string

def get_multiply_covered_string(self):
  if len(self.multiply_covered_notes) == 0:
    return "    None\n"
  
  m_string = ""
  for note in self.multiply_covered_notes:
    m_string += "    " + note.nameWithOctave + ":\n"
    for i in range(len(self.multiply_covered_notes[note])):
      rel = self.multiply_covered_notes[note][i]
      m_string += "      " + rel.given_note.nameWithOctave + ": " + rel.type.name + "\n"
  return m_string