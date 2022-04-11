from metrics.normalize_points import NORMALIZE_MAXIMUM

class HarmonicPartEvaluationStats:
  
  def __init__(self, exp_count, giv_count):
    self.exp_count = exp_count                    # Amount of expected harmonic parts
    self.giv_count = giv_count                    # Amount of given harmonic parts
    self.matched_percentage = 0                   # Percentage of the rhythmic length of all matched parts (in respect to the whole expected length)
    self.unmatched_percentage = 0                 # Percentage of the rhythmic length of all unmatched parts (in respect to the whole expected length)
    self.note_eval_stats = []                     # List of merged note evaluation statistics (MergedNoteEvaluationStats) for separate unmatched parts
    self.rhythm_eval_stats = []                   # List of rhythm evaluation statistics (RhythmEvaluationStats) for separate unmatched parts
    self.merged_note_eval_stats = None            # Collective note evaluation statistics for the whole harmonic part
    self.merged_rhythm_eval_stats = None          # Collective rhythm evaluation statistics for the whole harmonic part
    self.point = 0

  def __str__(self):
    percentage = f"{((self.points / NORMALIZE_MAXIMUM) * 100):.2f}%"

    string_rep = f""
    string_rep += f"Expected {self.exp_count} notes and rests, got {self.giv_count} notes and rests\n"
    string_rep += f"  {self.matched_percentage}% was a total match\n"
    string_rep += f"  {self.unmatched_percentage}% was not a total match\n"
    string_rep += f"--- Merged note evaluations for the unmatched parts ---\n"
    string_rep += self.merged_note_eval_stats
    string_rep += f"--- Merged rhythm evaluations for the unmatched parts ---\n"
    string_rep += self.merged_rhythm_eval_stats
    string_rep += f"  Points: {self.points} / {NORMALIZE_MAXIMUM} = {percentage}\n"

    return string_rep