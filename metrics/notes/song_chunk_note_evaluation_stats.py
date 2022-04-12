from metrics.notes.note_evaluation_stats import *
from metrics.notes.note_points import NotePoints

# Using this for harmonic parts
class SongChunkNoteEvaluationStats:

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
    self.got_lowest_count = 0                 # Amount of points where lowest expected note was exactly found (perfectly matched)
    self.got_lowest_percentage = 0            # Percentage of the amount of points where lowest expected note in respect of the amount of all lowest notes
    self.uncovered_percentage = 0             # How many of the expected notes had no relationship with any of the given notes (%)
    self.covered_only_with_harmonics_percentage = 0  # How many of the expected notes were covered only with harmonics (%)
    self.multiply_covered_percentage = 0      # How many of the expected notes were multiply covered (%)
  
  def __str__(self):
    harmonic_string = get_harmonic_distribution_string(self)

    string_rep = f""
    string_rep += f"Expected {self.exp_count} notes and rests, got {self.giv_count} notes and rests\n"
    string_rep += f"  Perfect match count: {self.perfect_matches}, {self.perfect_match_percentage}% of the expected notes\n"
    string_rep += f"  Cent difference count: {self.cent_differences}, {self.cent_diff_percentage}% of the expected notes\n"
    string_rep += f"  Harmonics distribution:\n{harmonic_string}"
    string_rep += f"    Found harmonics for {self.harmonic_exp_percentage}% of the expected notes\n"
    string_rep += f"    {self.harmonic_giv_percentage}% of the given notes were harmonics of something\n"
    string_rep += f"  Unrelated note count: {self.unrelated}, {self.unrelated_percentage}% of the given notes\n"
    string_rep += f"  Got lowest expected note {self.got_lowest_count} times, {self.got_lowest_percentage}% of all\n"
    string_rep += f"  Uncovered {self.uncovered_percentage}% of the expected notes\n"
    string_rep += f"  Covered {self.covered_only_with_harmonics_percentage}% of the expected notes with only harmonics:\n"
    string_rep += f"  Multiply covered {self.multiply_covered_percentage}% of the expected notes:\n"
    
    return string_rep