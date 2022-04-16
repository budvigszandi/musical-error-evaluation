import music21 as m21

# Important notes from music21 documentation
# Note that the tritone is given as diminished fifth, not augmented fourth.
# Simple will reduce an octave to a unison, semiSimple treats octaves as
# distinct intervals (P8.simple: Perfect Unison; P8.semiSimple: Perfect Octave)

# Returns a boolean about whether the given note is the first harmonic of the
# supposedly fundamental note (in other words, they are the same note
# or enharmonically equal). This is necessary because music21's
# harmonicAndFundamentalFromPitch would raise an error in this case.
#
# Requires two m21.pitch.Pitch objects
# TODO: Might need to check microtone differences as well
def is_first_harmonic(note, fundamental_note):
  return (note.nameWithOctave == fundamental_note.nameWithOctave) or (note.isEnharmonic(fundamental_note))

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
def get_harmonic_info(note, fundamental_note):
  if is_harmonic(note, fundamental_note):
    if is_first_harmonic(note, fundamental_note):
      #print(note, 'is the 1st harmonic of', fundamental_note, '(they are the same note)')
      return (1, fundamental_note)
    else:
      harmonic_information = note.harmonicAndFundamentalFromPitch(fundamental_note)
      if abs(harmonic_information[1].microtone.cents) > 50 : # TODO: Research on whether it should be around 50 or 100
        return 0
      else:
        #print(note, 'is the', harmonic_information[0], 'st/rd/th harmonic of', harmonic_information[1])
        return harmonic_information
  else:
    #print('Cannot find an equivalent harmonic for a fundamental', fundamental_note, 'that would be', note)
    return 0
