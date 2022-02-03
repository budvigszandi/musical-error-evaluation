class Relationship:
  def __init__(self, type, given_note, expected_note, cent_difference = None, harmonic_info = None):
    self.type = type
    self.given_note = given_note
    self.expected_note = expected_note
    self.cent_difference = cent_difference
    self.harmonic_info = harmonic_info