from ast import expr_context
from visualizer.draw_harmonic_part_results import get_notation_length

NO_OF_CHARS = 256
CHORD_BEGINNING_CHAR = "K"
CHORD_NOTE_CHAR = "Q"
CHORD_ENDING_CHAR = "Z"
MINIMUM_FIXPOINT_LENGTH = 2
BLANK_CHARACTER = "$"

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
      # print("Pattern occur at shift = {}".format(s))
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

def get_possible_fixpoints(song, length):
  fixpoints = []
  fixpoint = []
  current, added, fixpoint_beginning, shift = 0, 0, 0, 0
  while True:
    # --- add next ---
    if song[current] == CHORD_BEGINNING_CHAR:
      chord_end_index = get_chord_end_index(song[current:])
      fixpoint.extend(song[current : current + chord_end_index + 1])
      # print(f"  adding {song[current : current + chord_end_index + 1]}")
      current += chord_end_index + 1
      if added == 0:
        shift = len(fixpoint)
      added += 1
    else:
      octave_index = get_next_number_index(song[current:])
      fixpoint.extend(song[current : current + octave_index + 1])
      # print(f"  adding {song[current : current + octave_index + 1]}")
      current += octave_index + 1
      if added == 0:
        shift = len(fixpoint)
      added += 1
    # ----------------
    if added == length:
      fixpoints.append(fixpoint)
      # print("final chunk", fixpoint)
      # print(f"begin {fixpoint_beginning} len {len(fixpoint)} begin+len {fixpoint_beginning + len(fixpoint)} len(song) {len(song)}")
      if fixpoint_beginning + len(fixpoint) >= len(song):
        break
      fixpoint = []
      added = 0
      fixpoint_beginning += shift
      current = fixpoint_beginning
  return fixpoints

def get_chord_end_index(song_chunk):
  for i in range(len(song_chunk)):
    if song_chunk[i] == CHORD_ENDING_CHAR:
      return i

def get_next_number_index(song_chunk):
  for i in range(len(song_chunk)):
    if song_chunk[i].isnumeric():
      return i

def get_different_parts(expected, given):
  if expected == given:
    print("These two are the same")
    return 0
  fixpoints_by_length = get_possible_fixpoints_by_length(expected)
  expected_copy = expected
  given_copy = given
  found_all = False
  found_biggest = True
  while not found_all:
    if not found_biggest:
      found_all = True
    if found_all:
      print("Found all")
      break
    found_biggest = False
    for i in range(len(fixpoints_by_length) - 2, -1, -1): # going from the biggest (that is not the whole) to lowest
      for fp in fixpoints_by_length[i]:
        occurences = search(given_copy, fp)
        if len(occurences) == 1: # only getting unique fixpoints
          print(f"Found biggest fixpoint {fp} at {occurences[0]}-{occurences[0] + len(fp)}")
          found_biggest = True
          exp_occurences = search(expected_copy, fp)
          # TODO: compare occurences -> only blank the ones close to each other
          expected_copy = make_fixpoint_blank(expected_copy, exp_occurences, fp)
          given_copy = make_fixpoint_blank(given_copy, occurences, fp)
          print("New expected", expected_copy)
          print("New given", given_copy)
          print()
      fixpoints_by_length = fixpoints_by_length[:i]
      if found_biggest:
        break
  
  exp_rem = get_remaining_chunks(expected_copy)
  giv_rem = get_remaining_chunks(given_copy)
  print()
  print("Expected remaining chunks", exp_rem)
  print("Given remaining chunks", giv_rem)
  return exp_rem, giv_rem

def get_possible_fixpoints_by_length(expected):
  fixpoints_by_length = [] # every row is a list of possible fixpoints of the same length
  length = MINIMUM_FIXPOINT_LENGTH
  while True:
    try:
      possible_fixpoints = get_possible_fixpoints(expected, length)
    except IndexError:
      break
    fixpoints_by_length.append(possible_fixpoints)
    length += 1
  return fixpoints_by_length

def make_fixpoint_blank(given_copy, occurences, fixpoint):
  for occ in occurences:
    begin = occ
    end = occ + len(fixpoint)
    for i in range(begin, end):
      given_copy[i] = BLANK_CHARACTER
  return given_copy

def get_remaining_chunks(song):
  chunks = []
  chunk = []
  current = 0
  in_chunk = False
  while True:
    if current == len(song):
      break
    if song[current] == BLANK_CHARACTER and not in_chunk:
      pass
    elif song[current] == BLANK_CHARACTER and in_chunk:
      chunks.append(chunk)
      chunk = []
      in_chunk = False
    elif song[current] != BLANK_CHARACTER:
      in_chunk = True
      chunk.append(song[current])
    current += 1
  return chunks