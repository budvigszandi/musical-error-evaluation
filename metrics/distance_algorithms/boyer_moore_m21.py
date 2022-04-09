import copy
from metrics.distance_algorithms.boyer_moore import BLANK_CHARACTER, EMPTY_CHUNK_CHARACTER, get_next_blank_letter_index, get_non_blank_letter_index, make_fixpoint_blank, get_remaining_chunks, print_remaining_chunks, MINIMUM_FIXPOINT_LENGTH
from input.midi_reader import *
from metrics.harmonic_parts.harmonic_part_points import HarmonicPartPoints
from metrics.normalize_points import NORMALIZE_MAXIMUM, NORMALIZE_MINIMUM, normalize
from visualizer.draw_harmonic_part_results import add_matched_chunk_to_notation_string_bm_m21, get_notation_string_from_steps

def m21_bm_search(txt, pat):
  '''
  A pattern searching function that uses Bad Character
  Heuristic of Boyer Moore Algorithm
  '''
  m = len(pat)
  n = len(txt)
  occurences = []

  # s is shift of the pattern with respect to text
  s = 0
  while(s <= n-m):
    j = m-1

    # Keep reducing index j of pattern while
    # characters of pattern and text are matching
    # at this shift s
    while j>=0 and m21_equals(pat[j], txt[s+j]):
      j -= 1

    # If the pattern is present at current shift,
    # then index j will become -1 after the above loop
    if j<0:
      occurences.append(s)

      '''
        Shift the pattern so that the next character in text
          aligns with the last occurrence of it in pattern.
        The condition s+m < n is necessary for the case when
        pattern occurs at the end of text
      '''
      if s+m<n:
        last_occ_index = get_last_occurence(txt[s+m], pat)
        if last_occ_index == -1:
          s += m + 1
        else:
          s += m - last_occ_index
      else:
        break
    else:
      '''
      Shift the pattern so that the bad character in text
      aligns with the last occurrence of it in pattern. The
      max function is used to make sure that we get a positive
      shift. We may get a negative shift if the last occurrence
      of bad character in pattern is on the right side of the
      current character.
      '''
      last_occ_index = get_last_occurence(txt[s+j], pat)

      if last_occ_index == -1:
        s += j + 1
      else:
        s += max(1, m - 1 - last_occ_index)
  
  return occurences

def m21_equals(source, target):
  if source == BLANK_CHARACTER or target == BLANK_CHARACTER or source == EMPTY_CHUNK_CHARACTER or target == EMPTY_CHUNK_CHARACTER:
    return False
  elif source.duration != target.duration:
    return False
  elif source.isChord and target.isChord:
    return m21_chord_equals(source, target)
  elif source.isNote and target.isNote:
    return source.pitch.isEnharmonic(target.pitch)
  elif source.isRest and target.isRest:
    return source == target
  else:
    return False

def m21_chord_equals(source, target):
  if len(source) != len(target):
    return False
  elif source == target:
    return True
  else:
    s_pitches = [note.pitch for note in source]
    t_pitches = [note.pitch for note in target]
    enharmonics = 0
    for s_pitch in s_pitches:
      for i in range(len(t_pitches)):
        if t_pitches[i] != 0:
          if s_pitch.isEnharmonic(t_pitches[i]):
            enharmonics += 1
            t_pitches[i] = 0
    return enharmonics == len(source)

def get_last_occurence(element, pattern):
  index = -1
  for i in range(len(pattern)):
    if m21_equals(pattern[i], element):
      index = i
  return index

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
        occurences = m21_bm_search(giv_copy, fp)
        if len(occurences) == 1: # only getting unique fixpoints
          found_biggest = True
          exp_occurences = m21_bm_search(exp_copy, fp)
          if len(exp_occurences) == 1: # only getting unique fixpoints
            print("\n------ Fixpoint found ------")
            print(f"Found a unique fixpoint: {fp}\nat {occurences[0]}-{occurences[0] + len(fp) - 1} in the given song.\n")
            exp_occurence = exp_occurences[0]
            # Development idea: compare occurences -> only blank the ones close to each other
            exp_copy, giv_copy = make_fixpoint_blank(exp_copy, giv_copy, exp_occurence, occurences[0], fp)
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

def get_possible_fixpoints(song, length):
  fixpoints = []
  fixpoint = []
  current, added, fixpoint_beginning, shift = 0, 0, 0, 0
  while True:
    # --- add next ---
    fixpoint.append(song[current])
    current += 1
    if added == 0:
      shift = len(fixpoint)
    added += 1
    # ----------------
    if added == length:
      fixpoints.append(fixpoint)
      if fixpoint_beginning + len(fixpoint) >= len(song):
        break
      fixpoint = []
      added = 0
      fixpoint_beginning += shift
      current = fixpoint_beginning
  return fixpoints

def get_bm_m21_notation_with_points(orig_exp, orig_giv, exp_copy, giv_copy, exp_chunks, giv_chunks):
  notation_string = ""
  current = 0
  current_exp = 0
  unmatched_chunk_count = 0
  exp_ins_empty_chunks = 0
  giv_ins_empty_chunks = 0
  matched_length = 0
  unmatched_point_sum = 0

  while current < len(orig_giv):    
    if giv_copy[current] == BLANK_CHARACTER:
      print("\n------ Matched chunk ------")
      next_non_blank_letter_index = get_non_blank_letter_index(giv_copy[current:])
      if next_non_blank_letter_index != None:
        matched_chunk = orig_giv[current - giv_ins_empty_chunks : current + next_non_blank_letter_index - giv_ins_empty_chunks]
        print(f"Matched chunk at {current}-{current + next_non_blank_letter_index}")
        print(matched_chunk)
        matched_length += current + next_non_blank_letter_index - current
        notation_string = add_matched_chunk_to_notation_string_bm_m21(notation_string, orig_giv, current - giv_ins_empty_chunks, current + next_non_blank_letter_index - giv_ins_empty_chunks, giv_ins_empty_chunks)
        current += next_non_blank_letter_index
        current_exp += next_non_blank_letter_index
      else:
        matched_chunk = orig_giv[current - giv_ins_empty_chunks :]
        print(f"Matched chunk at {current}-{len(giv_copy)}")
        print(matched_chunk)
        matched_length += len(giv_copy) - current
        notation_string = add_matched_chunk_to_notation_string_bm_m21(notation_string, orig_giv, current - giv_ins_empty_chunks, len(giv_copy) - 1, giv_ins_empty_chunks)
        current = len(giv_copy)
        current_exp = len(exp_copy)
      print("\nCurrent full notation string:")
      print(notation_string)
    else:
      print("\n------ Unmatched chunkpair ------")
      print("Expected chunk:")
      print(exp_chunks[unmatched_chunk_count], end="\n\n")
      print("Given chunk:")
      print(giv_chunks[unmatched_chunk_count])
      if exp_copy[current_exp] == EMPTY_CHUNK_CHARACTER:
        exp_ins_empty_chunks += 1
      if giv_copy[current] == EMPTY_CHUNK_CHARACTER:
        giv_ins_empty_chunks += 1
      next_blank_letter_index = get_next_blank_letter_index(giv_copy[current:])
      exp_chunk_length = len(exp_chunks[unmatched_chunk_count])
      if next_blank_letter_index != None:
        current += next_blank_letter_index
      else:
        current = len(giv_copy)
      current_exp += exp_chunk_length
      dtw_expected = exp_chunks[unmatched_chunk_count]
      dtw_given = giv_chunks[unmatched_chunk_count]
      # This import is here to dodge circular import
      from evaluate import get_song_chunk_dtw_evaluation
      steps, note_eval, point = get_song_chunk_dtw_evaluation(dtw_expected, dtw_given)
      unmatched_point_sum += point
      notation_string += get_notation_string_from_steps(dtw_expected, dtw_given, steps, note_eval)
      print("\nCurrent full notation string:")
      print(notation_string)
      unmatched_chunk_count += 1
      print()
    print("\nUnmatched expected chunk total:", len(exp_chunks))
    print("Unmatched given chunks total:", len(giv_chunks))
    print("Unmatched chunk pairs evaluated:", unmatched_chunk_count)
    print("Unmatched chunk pairs remaining:", len(exp_chunks) - unmatched_chunk_count)
  print("\n------ Final notation string ------")
  print(notation_string)
  final_point = get_final_song_point(len(orig_exp), len(orig_giv), matched_length, unmatched_point_sum)
  return notation_string, final_point

def get_final_song_point(exp_length, giv_length, matched_length, unmatched_point_sum):
  matched_point_sum = matched_length * NORMALIZE_MAXIMUM

  final_minimum = exp_length * HarmonicPartPoints.DELETED_HARMONIC_ELEMENT_POINT + \
                  + giv_length * HarmonicPartPoints.INSERTED_HARMONIC_ELEMENT_POINT
  final_maximum = exp_length * NORMALIZE_MAXIMUM

  final_point_sum = matched_point_sum + unmatched_point_sum
  final_point_normalized = normalize(final_point_sum, final_minimum, final_maximum)
  return final_point_normalized