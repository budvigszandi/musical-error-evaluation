import music21 as m21
from evaluate import get_dtw_rhythm_evaluation, get_levenshtein_rhythm_evaluation

RHYTHM_FUNCTION_NAME_BEGINNING_DTW = "example_rhythm_evaluation_dtw"
RHYTHM_FUNCTION_NAME_BEGINNING_LEV = "example_rhythm_evaluation_lev"

def example_rhythm_evaluation_dtw_1():
  expected_rhythm = [m21.note.Note('d4', quarterLength=1), m21.note.Note('d4', quarterLength=1),
                     m21.note.Note('d4', quarterLength=2), m21.note.Rest(quarterLength=2),
                     m21.note.Note('d4', quarterLength=1)]
  given_rhythm =    [m21.note.Note('c4', quarterLength=2), m21.note.Note('c4', quarterLength=1),
                     m21.note.Note('c4', quarterLength=1), m21.note.Rest(quarterLength=1),
                     m21.note.Note('c4', quarterLength=1)]
  get_dtw_rhythm_evaluation(expected_rhythm, given_rhythm)

def example_rhythm_evaluation_dtw_expected_one_got_more():
  expected_rhythm = [m21.note.Note('c4', quarterLength=2)]
  given_rhythm =    [m21.note.Note('d4', quarterLength=1), m21.note.Note('e4', quarterLength=1),
                     m21.note.Note('f4', quarterLength=1)]
  get_dtw_rhythm_evaluation(expected_rhythm, given_rhythm)

def example_rhythm_evaluation_dtw_expected_more_got_one():
  expected_rhythm = [m21.note.Note('d4', quarterLength=4), m21.note.Note('e4', quarterLength=1),
                     m21.note.Note('f4', quarterLength=4)]
  given_rhythm =    [m21.note.Note('c4', quarterLength=1)]
  get_dtw_rhythm_evaluation(expected_rhythm, given_rhythm)

def example_rhythm_evaluation_dtw_rest_note_switch():
  expected_rhythm = [m21.note.Rest(quarterLength=1), m21.note.Note('e4', quarterLength=1),
                     m21.note.Note('f4', quarterLength=1)]
  given_rhythm =    [m21.note.Note('d4', quarterLength=1), m21.note.Note('e4', quarterLength=1),
                     m21.note.Note('f4', quarterLength=1)]
  get_dtw_rhythm_evaluation(expected_rhythm, given_rhythm)

def example_rhythm_evaluation_dtw_missing_beginning():
  expected_rhythm = [m21.note.Note('d4', quarterLength=1), m21.note.Note('e4', quarterLength=1),
                     m21.note.Rest(quarterLength=2), m21.note.Note('g4', quarterLength=1),
                     m21.note.Note('f4', quarterLength=1)]
  given_rhythm =    [m21.note.Rest(quarterLength=2), m21.note.Note('c4', quarterLength=1),
                     m21.note.Note('g4', quarterLength=1)]
  get_dtw_rhythm_evaluation(expected_rhythm, given_rhythm)

def example_rhythm_evaluation_dtw_missing_middle():
  expected_rhythm = [m21.note.Note('d4', quarterLength=1), m21.note.Note('e4', quarterLength=1),
                     m21.note.Rest(quarterLength=2), m21.note.Note('g4', quarterLength=1),
                     m21.note.Note('f4', quarterLength=1)]
  given_rhythm =    [m21.note.Note('c4', quarterLength=1), m21.note.Note('f4', quarterLength=1),
                     m21.note.Note('g4', quarterLength=1), m21.note.Note('d4', quarterLength=1)]
  get_dtw_rhythm_evaluation(expected_rhythm, given_rhythm)

def example_rhythm_evaluation_dtw_missing_end():
  expected_rhythm = [m21.note.Note('d4', quarterLength=1), m21.note.Note('e4', quarterLength=1),
                     m21.note.Rest(quarterLength=2), m21.note.Note('g4', quarterLength=1),
                     m21.note.Note('f4', quarterLength=1)]
  given_rhythm =    [m21.note.Note('c4', quarterLength=1), m21.note.Note('g4', quarterLength=1),
                     m21.note.Rest(quarterLength=2)]
  get_dtw_rhythm_evaluation(expected_rhythm, given_rhythm)

def example_rhythm_evaluation_dtw_missing_beginning_middle():
  expected_rhythm = [m21.note.Rest(quarterLength=1), m21.note.Note('d4', quarterLength=1),
                     m21.note.Note('e4', quarterLength=1), m21.note.Rest(quarterLength=2),
                     m21.note.Note('g4', quarterLength=1), m21.note.Note('f4', quarterLength=1)]
  given_rhythm =    [m21.note.Note('d4', quarterLength=1), m21.note.Note('e4', quarterLength=1),
                     m21.note.Note('f4', quarterLength=1), m21.note.Note('g4', quarterLength=1)]
  get_dtw_rhythm_evaluation(expected_rhythm, given_rhythm)

def example_rhythm_evaluation_dtw_missing_beginning_end():
  expected_rhythm = [m21.note.Rest(quarterLength=1), m21.note.Note('d4', quarterLength=1),
                     m21.note.Note('e4', quarterLength=1), m21.note.Note('f4', quarterLength=1),
                     m21.note.Note('g4', quarterLength=1), m21.note.Rest(quarterLength=1)]
  given_rhythm =    [m21.note.Note('e4', quarterLength=1), m21.note.Note('f4', quarterLength=1)]
  get_dtw_rhythm_evaluation(expected_rhythm, given_rhythm)

def example_rhythm_evaluation_dtw_missing_middle_end():
  expected_rhythm = [m21.note.Note('d4', quarterLength=1), m21.note.Note('e4', quarterLength=1),
                     m21.note.Rest(quarterLength=2), m21.note.Note('g4', quarterLength=1),
                     m21.note.Note('f4', quarterLength=1)]
  given_rhythm =    [m21.note.Note('d4', quarterLength=1), m21.note.Note('e4', quarterLength=1),
                     m21.note.Note('f4', quarterLength=1)]
  get_dtw_rhythm_evaluation(expected_rhythm, given_rhythm)

def example_rhythm_evaluation_dtw_missing_middle_middle():
  expected_rhythm = [m21.note.Note('d4', quarterLength=1), m21.note.Note('e4', quarterLength=1),
                     m21.note.Rest(quarterLength=2), m21.note.Note('g4', quarterLength=1),
                     m21.note.Rest(quarterLength=2), m21.note.Note('g4', quarterLength=1),
                     m21.note.Note('f4', quarterLength=1)]
  given_rhythm =    [m21.note.Note('f4', quarterLength=1), m21.note.Note('e4', quarterLength=1),
                     m21.note.Note('g4', quarterLength=1), m21.note.Note('c4', quarterLength=1),
                     m21.note.Note('e4', quarterLength=1)]
  get_dtw_rhythm_evaluation(expected_rhythm, given_rhythm)

def example_rhythm_evaluation_dtw_expected_none_got_none():
  expected_rhythm = []
  given_rhythm =    []
  get_dtw_rhythm_evaluation(expected_rhythm, given_rhythm)

def example_rhythm_evaluation_dtw_expected_some_got_none():
  expected_rhythm = [m21.note.Note('d4', quarterLength=1), m21.note.Note('d4', quarterLength=1),
                     m21.note.Note('d4', quarterLength=2), m21.note.Rest(quarterLength=2),
                     m21.note.Note('d4', quarterLength=1)]
  given_rhythm =    []
  get_dtw_rhythm_evaluation(expected_rhythm, given_rhythm)

def example_rhythm_evaluation_dtw_expected_none_got_some():
  expected_rhythm = []
  given_rhythm =    [m21.note.Note('c4', quarterLength=2), m21.note.Note('c4', quarterLength=1),
                     m21.note.Note('c4', quarterLength=1), m21.note.Rest(quarterLength=1),
                     m21.note.Note('c4', quarterLength=1)]
  get_dtw_rhythm_evaluation(expected_rhythm, given_rhythm)

def example_rhythm_evaluation_lev_1():
  expected_rhythm = [m21.note.Note('d4', quarterLength=1), m21.note.Note('d4', quarterLength=1),
                     m21.note.Note('d4', quarterLength=2), m21.note.Rest(quarterLength=2),
                     m21.note.Note('d4', quarterLength=1)]
  given_rhythm =    [m21.note.Note('c4', quarterLength=2), m21.note.Note('c4', quarterLength=1),
                     m21.note.Note('c4', quarterLength=1), m21.note.Rest(quarterLength=1),
                     m21.note.Note('c4', quarterLength=1)]
  get_levenshtein_rhythm_evaluation(expected_rhythm, given_rhythm)
