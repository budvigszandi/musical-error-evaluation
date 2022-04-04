class NoteRelationship:
  def __init__(self, type, given_note, expected_note, cent_difference = None, harmonic_info = None):
    self.type = type
    self.given_note = given_note
    self.expected_note = expected_note
    self.cent_difference = cent_difference
    self.harmonic_info = harmonic_info
  
  def __str__(self):
    return "Expected [" + str(self.expected_note) + "] " + \
           "Given [" + str(self.given_note) + "]:" + \
           "\n  Relationship: " + str(self.type.name) + \
           "\n  Cent difference: " + str(self.cent_difference) + \
           "\n  Harmonic info: " + str(self.harmonic_info)