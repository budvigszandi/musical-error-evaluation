import music21 as m21
import harmonics

# Requires two lists of m21.pitch.Pitch objects
def compare_notes(expected_notes, given_notes):
  expected_notes_count = len(expected_notes)
  if expected_notes_count == 1:
    compare_note_one_to_n(expected_notes[0], given_notes)

# Requires a m21.pitch.Pitch object and a list of m21.pitch.Pitch objects
def compare_note_one_to_n(expected_note, given_notes):
  if len(given_notes) == 0:
    print("Missing note")
  elif len(given_notes) == 1:
    compare_note_one_to_one(expected_note, given_notes[0])
  else:
    notes_count = len(given_notes) # will use this to multiply error weight
    contains_expected_note = False
    plus_only_cent_difference = 0
    plus_harmonics = 0
    plus_unrelated = 0
    notes_information = get_notes_information_one_to_n(expected_note, given_notes)
    for note in notes_information:
      if note[0] == -1:
        print("Contains something unrelated")
        plus_unrelated += 1
      elif note[0] == 0:
        print("Contains perfect match")
        contains_expected_note = True
      elif note[0] == 0.5:
        print(f"Contains note match with {note[2]} cent difference")
        plus_only_cent_difference += 1
      else:
        print(f"Contains {note[0]}. harmonic")
        plus_harmonics += 1
    
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

def get_notes_information_one_to_n(expected_note, given_notes):
  notes_information = []
  for note in given_notes:
    if note == expected_note:
      notes_information.append((0, "Perfect match"))
    elif note.nameWithOctave == expected_note.nameWithOctave:
      notes_information.append((0.5, "Cent difference", note.microtone.cents - expected_note.microtone.cents))
    else:
      harmonic_information = harmonics.get_harmonic_information(note, expected_note)
      if harmonic_information != 0:
        notes_information.append(harmonic_information)
      else:
        notes_information.append((-1, "Unrelated"))
  return notes_information

# TODO: Modify the evaluation answer according to the new errors, paying
#       attention to different weights
def compare_note_one_to_one(expected_note, given_note):
  if expected_note == given_note:
    print("Perfect match")
  elif expected_note.nameWithOctave == given_note.nameWithOctave:
    print(f"Note match with cent difference. Expected {expected_note.microtone}, got {given_note.microtone}")
  else:
    harmonic_information = harmonics.get_harmonic_information(given_note, expected_note)
    if harmonic_information != 0:
      harmonic_number = harmonic_information[0]
      print(f"Expected {expected_note}, but got the {harmonic_number}. harmonic {given_note}")
    else:
      print("Got something unrelated")

c4_x = m21.pitch.Pitch('c4')
c4_x.microtone = 20

c4_y = m21.pitch.Pitch('c4')

g5 = m21.pitch.Pitch('g5')

notes_x = [c4_x]
notes_y = [c4_x, c4_y]
notes_z = [g5]
notes_w = [m21.pitch.Pitch('c2'), m21.pitch.Pitch('g5'), m21.pitch.Pitch('a6')]

compare_notes(notes_x, notes_w)