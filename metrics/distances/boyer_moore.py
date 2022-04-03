import music21 as m21
import copy

NO_OF_CHARS = 256
REST_CHARACTER = "R"
CHORD_BEGINNING_CHAR = "K"
CHORD_NOTE_CHAR = "Q"
CHORD_ENDING_CHAR = "Z"
MINIMUM_FIXPOINT_LENGTH = 2
BLANK_CHARACTER = "$"
EMPTY_CHUNK_CHARACTER = "@"

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
  bm_array = []
  for element in m21_array:
    if element.isNote:
      for char in element.nameWithOctave:
        bm_array.append(char)
    elif element.isChord:
      bm_array.append(CHORD_BEGINNING_CHAR)
      for note in element:
        bm_array.append(CHORD_NOTE_CHAR)
        for char in note.nameWithOctave:
          bm_array.append(char)
      bm_array.append(CHORD_ENDING_CHAR)
    elif element.isRest:
      # This import is here to dodge circular import
      from visualizer.draw_harmonic_part_results import get_notation_length
      length = get_notation_length(element)
      bm_array.append(REST_CHARACTER)
      for char in length:
        bm_array.append(char)
  return bm_array

def boyer_moore_to_m21(bm_array):
  m21_array = []
  current = 0
  while current < len(bm_array):
    if bm_array[current] == CHORD_BEGINNING_CHAR:
      chord_end_index = get_chord_end_index(bm_array[current:])
      chord_notes = ""
      current_beginning = current
      while current != current_beginning + chord_end_index:
        octave_index = get_next_number_index(bm_array[current:])
        note_bm = ""
        note_bm = note_bm.join(bm_array[current : current + octave_index + 1])
        note_bm = note_bm.replace(CHORD_BEGINNING_CHAR, "")
        note_bm = note_bm.replace(CHORD_NOTE_CHAR, "")
        chord_notes += note_bm + " "
        current += octave_index + 1
      m21_array.append(m21.chord.Chord(chord_notes))
      current += 1
    else:
      note = ""
      octave_index = get_next_number_index(bm_array[current:])
      note = note.join(bm_array[current : current + octave_index + 1])
      if bm_array[current] == REST_CHARACTER:
        m21_array.append(m21.note.Rest(note))
      else:
        m21_array.append(m21.note.Note(note))
      current += octave_index + 1
  return m21_array

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

def get_next_letter_index(song_chunk):
  for i in range(len(song_chunk)):
    if song_chunk[i] != BLANK_CHARACTER:
      return i

def get_next_blank_letter_index(song_chunk):
  for i in range(len(song_chunk)):
    if song_chunk[i] == BLANK_CHARACTER:
      return i

def get_different_parts(expected, given):
  if expected == given:
    print("The expected and given songs are exactly the same.")
    return [], [], [], []
  fixpoints_by_length = get_possible_fixpoints_by_length(expected)
  exp_copy = copy.copy(expected)
  giv_copy = copy.copy(given)
  found_all = False
  found_biggest = True
  while not found_all:
    if not found_biggest:
      found_all = True
    if found_all:
      print("\n------------ All fixpoints found ------------")
      print("Found all unique fixpoints.")
      break
    found_biggest = False
    for i in range(len(fixpoints_by_length) - 2, -1, -1): # going from the biggest (that is not the whole) to lowest
      for fp in fixpoints_by_length[i]:
        occurences = search(giv_copy, fp)
        if len(occurences) == 1: # only getting unique fixpoints
          found_biggest = True
          exp_occurences = search(exp_copy, fp)
          if len(exp_occurences) == 1: # only getting unique fixpoints
            print("\n------ Fixpoint found ------")
            print(f"Found a unique fixpoint: {fp}\nat {occurences[0]}-{occurences[0] + len(fp)} in the given song.\n")
            exp_occurence = exp_occurences[0]
            # TODO: Chance for development: compare occurences -> only blank the ones close to each other
            exp_copy, giv_copy = make_fixpoint_blank(exp_copy, giv_copy, exp_occurence, occurences[0], fp)
            # given_copy = make_fixpoint_blank(given_copy, occurences, fp)
            print("New expected:")
            print(exp_copy, end="\n\n")
            print("New given:")
            print(giv_copy, end="\n\n")
      fixpoints_by_length = fixpoints_by_length[:i]
      if found_biggest:
        break
  
  exp_chunks = get_remaining_chunks(exp_copy)
  giv_chunks = get_remaining_chunks(giv_copy)
  print("\n------------ Remaining chunks ------------")
  print("Expected remaining chunks:")
  print_remaining_chunks(exp_chunks)
  print("Given remaining chunks:")
  print_remaining_chunks(giv_chunks)
  return exp_copy, giv_copy, exp_chunks, giv_chunks

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

def make_fixpoint_blank(exp_copy, giv_copy, exp_occurence, giv_occurence, fixpoint):
  exp_begin = exp_occurence
  exp_end = exp_begin + len(fixpoint)
  giv_begin = giv_occurence
  giv_end = giv_begin + len(fixpoint)
  for i in range(exp_begin, exp_end):
    exp_copy[i] = BLANK_CHARACTER
  for i in range(giv_begin, giv_end):
    giv_copy[i] = BLANK_CHARACTER
  exp_copy, giv_copy = insert_empty_chunks(exp_copy, giv_copy, exp_begin, exp_end, giv_begin, giv_end)
  return exp_copy, giv_copy

def insert_empty_chunks(exp_copy, giv_copy, exp_begin, exp_end, giv_begin, giv_end):
  if exp_end == len(exp_copy):
    exp_end -= 1
  if giv_end == len(giv_copy):
    giv_end -= 1
  blank_before_exp = exp_copy[exp_begin - 1] == BLANK_CHARACTER
  blank_after_exp = exp_copy[exp_end] == BLANK_CHARACTER
  blank_before_giv = giv_copy[giv_begin - 1] == BLANK_CHARACTER
  blank_after_giv = giv_copy[giv_end] == BLANK_CHARACTER
  if blank_before_exp and not blank_before_giv:
    exp_copy.insert(exp_begin, EMPTY_CHUNK_CHARACTER)
  elif blank_before_giv and not blank_before_exp:
    giv_copy.insert(giv_begin, EMPTY_CHUNK_CHARACTER)
  elif blank_after_exp and not blank_after_giv:
    exp_copy.insert(exp_end, EMPTY_CHUNK_CHARACTER)
  elif blank_after_giv and not blank_after_exp:
    giv_copy.insert(giv_end, EMPTY_CHUNK_CHARACTER)
  return exp_copy, giv_copy

def get_remaining_chunks(song):
  chunks = []
  chunk = []
  current = 0
  in_chunk = False
  while True:
    if current == len(song):
      if in_chunk:
        chunks.append(chunk)
      break
    if song[current] == BLANK_CHARACTER and not in_chunk:
      pass
    elif song[current] == EMPTY_CHUNK_CHARACTER:
      if in_chunk:
        chunks.append(chunk)
      chunks.append([])
      in_chunk = False
    elif song[current] == BLANK_CHARACTER and in_chunk:
      chunks.append(chunk)
      chunk = []
      in_chunk = False
    elif song[current] != BLANK_CHARACTER:
      in_chunk = True
      chunk.append(song[current])
    current += 1
  return chunks

def print_remaining_chunks(chunks):
  for i in range(len(chunks)):
    print(f"[{i}] {chunks[i]}")
  print()