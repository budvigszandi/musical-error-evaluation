import music21 as m21
import harmonics

# Requires two lists of m21.pitch.Pitch objects
def compare_notes(expected_notes, given_notes):
  expected_notes_count = len(expected_notes)
  if expected_notes_count == 1:
    compare_note_one_to_n(expected_notes[0], given_notes)
  else:
    # TODO: what happens if we have more expected notes?
    print()

# Requires a m21.pitch.Pitch object and a list of m21.pitch.Pitch objects
def compare_note_one_to_n(expected_note, given_notes):
  notes_information = []
  if len(given_notes) == 0:
    print("Missing note")
    notes_information.append((-2, "Missing note"))
  elif len(given_notes) == 1:
    note_information = compare_note_one_to_one(expected_note, given_notes[0])
    notes_information.append(note_information)
  else:
    notes_information = get_notes_information_one_to_n(expected_note, given_notes)
  print_results(expected_note, notes_information, len(given_notes))

# Returns an array of lists with information about the given notes in relation
# with the expected note. For the meaning of the lists see
# compare_note_one_to_one(expected_note, given_note)
#
# Requires a m21.pitch.Pitch object and a list of m21.pitch.Pitch objects
def get_notes_information_one_to_n(expected_note, given_notes):
  notes_information = []
  for note in given_notes:
    note_information = compare_note_one_to_one(expected_note, note)
    notes_information.append(note_information)
  return notes_information

# TODO: Modify the evaluation answer according to the new errors, paying
#       attention to different weights
# Returns a list with information about the current note in 2-4 elements.
# 1st element: A number that identifies the type of this note in relation with
#              the expected note.
#              0: Perfect match, 0.5: Cent difference, 1: Harmonic
#             -1: Unrelated,      -2: Missing note
# 2nd element: A string describing the type of this note in relation with the
#              expected note.
# 3rd element: The given note. If a note is missing, the list only contains the
#              1st and 2nd element.
# 4th element: Only exists if there is a cent difference or the note is a harmonic.
#              Cent difference: The difference in a number.
#              Harmonic: A 2-element list of harmonic information
#                        (which_harmonic, fundamental_note)
#
# Requires two m21.pitch.Pitch objects
def compare_note_one_to_one(expected_note, given_note):
  if expected_note == given_note:
    return (0, "Perfect match", given_note)
  elif expected_note.nameWithOctave == given_note.nameWithOctave:
    return (0.5, "Cent difference", given_note, given_note.microtone.cents - expected_note.microtone.cents)
  else:
    harmonic_information = harmonics.get_harmonic_information(given_note, expected_note)
    if harmonic_information != 0:
      return (1, "Harmonic", given_note, harmonic_information)
    else:
      return (-1, "Unrelated", given_note)

def print_results(expected_note, notes_information, notes_count):
  # will use notes_count to multiply error weight
  contains_expected_note = False
  plus_only_cent_difference = 0
  plus_harmonics = 0
  plus_unrelated = 0
  print("Expected note:", expected_note)
  print("Given note(s):")
  for note in notes_information:
    if note[0] == -1:
      print(f"{note[2]}: unrelated")
      plus_unrelated += 1
    elif note[0] == 0:
      print(f"{note[2]}: perfect match")
      contains_expected_note = True
    elif note[0] == 0.5:
      print(f"{note[2]}: note match with {note[3]} cent difference")
      plus_only_cent_difference += 1
    else:
      print(f"{note[2]}: {note[3][0]}. harmonic")
      plus_harmonics += 1
  
  if notes_count > 1:
    if contains_expected_note:
      print("Contains expected note. "
            f"The rest are {(plus_only_cent_difference / (notes_count - 1)) * 100:.2f}% only cent difference, "
            f"{(plus_harmonics / (notes_count - 1)) * 100:.2f}% harmonics and "
            f"{(plus_unrelated / (notes_count - 1)) * 100:.2f}% unrelated.")
    else:
      print("Does not contain expected note. "
            f"The rest are {(plus_only_cent_difference / notes_count) * 100:.2f}% only cent difference, "
            f"{(plus_harmonics / notes_count) * 100:.2f}% harmonics and "
            f"{(plus_unrelated / notes_count) * 100:.2f}% unrelated.")

c4_x = m21.pitch.Pitch('c4')
c4_x.microtone = 20

c4_y = m21.pitch.Pitch('c4')

g5 = m21.pitch.Pitch('g5')

notes_x = [c4_x]
notes_y = [c4_x, c4_y]
notes_z = [g5]
notes_w = [m21.pitch.Pitch('c2'), m21.pitch.Pitch('g5'), m21.pitch.Pitch('a6')]

compare_notes(notes_x, notes_w)