from visualizer.draw_harmonic_part_results import get_notation_length
import time

NO_OF_CHARS = 256
CHORD_BEGINNING_CHAR = "K"
CHORD_NOTE_CHAR = "Q"
CHORD_ENDING_CHAR = "Z"

def badCharHeuristic(string, size):
  '''
  The preprocessing function for
  Boyer Moore's bad character heuristic
  '''

  # Initialize all occurrence as -1
  badChar = [-1]*NO_OF_CHARS

  # Fill the actual value of last occurrence
  for i in range(size):
    badChar[ord(string[i])] = i
  
  # return initialized list
  return badChar

def search(txt, pat):
  '''
  A pattern searching function that uses Bad Character
  Heuristic of Boyer Moore Algorithm
  '''
  m = len(pat)
  n = len(txt)
  occurences = []

  # create the bad character list by calling
  # the preprocessing function badCharHeuristic()
  # for given pattern
  badChar = badCharHeuristic(pat, m)

  # s is shift of the pattern with respect to text
  s = 0
  while(s <= n-m):
    j = m-1

    # Keep reducing index j of pattern while
    # characters of pattern and text are matching
    # at this shift s
    while j>=0 and pat[j] == txt[s+j]:
      j -= 1

    # If the pattern is present at current shift,
    # then index j will become -1 after the above loop
    if j<0:
      print("Pattern occur at shift = {}".format(s))
      occurences.append(s)

      '''
        Shift the pattern so that the next character in text
          aligns with the last occurrence of it in pattern.
        The condition s+m < n is necessary for the case when
        pattern occurs at the end of text
      '''
      s += (m-badChar[ord(txt[s+m])] if s+m<n else 1)
    else:
      '''
      Shift the pattern so that the bad character in text
      aligns with the last occurrence of it in pattern. The
      max function is used to make sure that we get a positive
      shift. We may get a negative shift if the last occurrence
      of bad character in pattern is on the right side of the
      current character.
      '''
      s += max(1, j-badChar[ord(txt[s+j])])
  
  return occurences

def m21_to_boyer_moore(m21_array):
  notes = []
  for element in m21_array:
    if element.isNote:
      for char in element.nameWithOctave:
        notes.append(char)
    elif element.isChord:
      notes.append(CHORD_BEGINNING_CHAR)
      for note in element:
        notes.append(CHORD_NOTE_CHAR)
        for char in note.nameWithOctave:
          notes.append(char)
      notes.append(CHORD_ENDING_CHAR)
    elif element.isRest:
      length = get_notation_length(element)
      notes.append("R")
      for char in length:
        notes.append(char)
  return notes

def get_checkpoints(song, length):
  checkpoints = []
  checkpoint = []
  current, added, checkpoint_beginning, shift = 0, 0, 0, 0
  while True:
    # --- add next ---
    if song[current] == CHORD_BEGINNING_CHAR:
      chord_end_index = get_chord_end_index(song[current:])
      checkpoint.extend(song[current : current + chord_end_index + 1])
      print(f"  adding {song[current : current + chord_end_index + 1]}")
      current += chord_end_index + 1
      if added == 0:
        shift = len(checkpoint)
      added += 1
    else:
      octave_index = get_next_number_index(song[current:])
      checkpoint.extend(song[current : current + octave_index + 1])
      print(f"  adding {song[current : current + octave_index + 1]}")
      current += octave_index + 1
      if added == 0:
        shift = len(checkpoint)
      added += 1
    # ----------------
    if added == length:
      checkpoints.append(checkpoint)
      print("final chunk", checkpoint)
      print(f"begin {checkpoint_beginning} len {len(checkpoint)} begin+len {checkpoint_beginning + len(checkpoint)} len(song) {len(song)}")
      if checkpoint_beginning + len(checkpoint) >= len(song):
        break
      checkpoint = []
      added = 0
      checkpoint_beginning += shift
      current = checkpoint_beginning
  return checkpoints

def get_chord_end_index(song_chunk):
  for i in range(len(song_chunk)):
    if song_chunk[i] == CHORD_ENDING_CHAR:
      return i

def get_next_number_index(song_chunk):
  for i in range(len(song_chunk)):
    if song_chunk[i].isnumeric():
      return i