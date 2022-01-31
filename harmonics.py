import music21 as m21

# TODO: Create a universal response object and make sure that all functions
#       use it properly

# TODO: Exception handling all around

# Important notes from music21 documentation
# Note that the tritone is given as diminished fifth, not augmented fourth.
# Simple will reduce an octave to a unison, semiSimple treats octaves as
# distinct intervals (P8.simple: Perfect Unison; P8.semiSimple: Perfect Octave)

# Returns an array of pitches which is the harmonic series from the
# 1st harmonic (fundamental note) to the 16th harmonic
#
# Requires an m21.pitch.Pitch object
def build_harmonic_series(fundamental_note):
  harmonic_series = [fundamental_note]
  for i in range(2, 17):
    harmonic_series.append(fundamental_note.getHarmonic(i))
  return harmonic_series

# Returns a boolean about whether the given note is the first harmonic of the
# supposedly fundamental note (in other words, they are the same note).
# This is necessary because music21's harmonicAndFundamentalFromPitch would
# raise an error in this case.
#
# Requires two m21.pitch.Pitch objects
# TODO: Might need to check microtone differences as well
def is_first_harmonic(note, fundamental_note):
  return note.nameWithOctave == fundamental_note.nameWithOctave

# Returns a boolean regarding whether a note is a harmonic (between 1st
# and 16th) of a supposedly fundamental note
#
# Requires two m21.pitch.Pitch objects
def is_harmonic(note, fundamental_note):
  if is_first_harmonic(note, fundamental_note):
    return True
  else:
    try:
      note.harmonicAndFundamentalFromPitch(fundamental_note)
      return True
    except m21.pitch.PitchException:
      return False

# Returns whether the given note is in the first 16 harmonics of the
# supposedly fundamental note, and if so, which harmonic it is and
# how many cents the variance is
#
# Requires two m21.pitch.Pitch objects
def get_harmonic_information(note, fundamental_note):
  if is_harmonic(note, fundamental_note):
    if is_first_harmonic(note, fundamental_note):
      #print(note, 'is the 1st harmonic of', fundamental_note, '(they are the same note)')
      return (1, fundamental_note)
    else:
      harmonic_information = note.harmonicAndFundamentalFromPitch(fundamental_note)
      #print(note, 'is the', harmonic_information[0], 'st/rd/th harmonic of', harmonic_information[1])
      return harmonic_information
  else:
    #print('Cannot find an equivalent harmonic for a fundamental', fundamental_note, 'that would be', note)
    return 0

# Returns a number between 0 and 1 regarding how probable it is that
# we have misheard a note to one of its harmonics based on the
# variance (which we have in cents)
#
# Requires a number which represents which harmonic we are looking for
# (from 1 and 16)
def probabilty_of_harmonic(harmonic_number):
  example_harmonic_series = build_harmonic_series(m21.pitch.Pitch('C4'))
  variance = example_harmonic_series[harmonic_number - 1].microtone.cents
  if harmonic_number == 1:
    return 0.99
  if variance > 0:
    return 1 / (harmonic_number * variance)
  else:
    return 1 / harmonic_number

# --------------------------------
# |Just trying the functions here|
# --------------------------------

# Build a harmonic series
# hson = build_harmonic_series(m21.pitch.Pitch('C4'))
# for i in range(len(hson)):
#   print(hson[i])

# Check whether C4, G5 and C3 are harmonics of C4
x = m21.pitch.Pitch('C4')
y = m21.pitch.Pitch('G5')
z = m21.pitch.Pitch('C3')

# print(is_harmonic(x, x))
# print(is_harmonic(y, x))
# print(is_harmonic(z, x))

# Get harmonic information for C4, G5 and C3 if C4 is the fundamental
# get_harmonic_information(x, x)
# get_harmonic_information(y, x)
# get_harmonic_information(z, x)

# Print the probability of the first 16 harmonics
# for i in range(1, 16):
#   print(probabilty_of_harmonic(i))

# harmonic_information = get_harmonic_information(y, x)
# if harmonic_information != 0:
#   print('Probability:', probabilty_of_harmonic(harmonic_information[0]))