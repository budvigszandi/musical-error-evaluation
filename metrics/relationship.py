class Relationship:
  def __init__(self, type, given_note, expected_note, cent_difference = None, harmonic_info = None):
    self.type = type
    self.given_note = given_note
    self.expected_note = expected_note
    self.cent_difference = cent_difference
    self.harmonic_info = harmonic_info
  
  def __str__(self):
    return str(self.given_note) + " - " + \
           str(self.expected_note) + ": " + \
           str(self.type) + " " + \
           str(self.cent_difference) + " " + \
           str(self.harmonic_info)