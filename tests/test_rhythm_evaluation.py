import music21 as m21

from evaluate import get_dtw_rhythm_evaluation
from metrics.distance_algorithms.distance_type import DistanceType
from metrics.normalize_points import NORMALIZE_MAXIMUM

def test_rhythm_evaluation_dtw_expected_one_got_more():
  expected_rhythm = [m21.note.Note('c4', quarterLength=2)]
  given_rhythm =    [m21.note.Note('d4', quarterLength=1), m21.note.Note('e4', quarterLength=1),
                     m21.note.Note('f4', quarterLength=1)]
  
  expected_permutation = [
    DistanceType.SUBSTITUTION,
    DistanceType.INSERTION,
    DistanceType.INSERTION
    ]
  actual_permutation, points = get_dtw_rhythm_evaluation(expected_rhythm, given_rhythm)

  assert expected_permutation == actual_permutation

def test_rhythm_evaluation_dtw_expected_more_got_one():
  expected_rhythm = [m21.note.Note('d4', quarterLength=4), m21.note.Note('e4', quarterLength=1),
                     m21.note.Note('f4', quarterLength=4)]
  given_rhythm =    [m21.note.Note('c4', quarterLength=1)]
  
  expected_permutation = [
    DistanceType.DELETION,
    DistanceType.SAME,
    DistanceType.DELETION
    ]
  actual_permutation, points = get_dtw_rhythm_evaluation(expected_rhythm, given_rhythm)

  assert expected_permutation == actual_permutation

def test_rhythm_evaluation_dtw_rest_note_switch():
  expected_rhythm = [m21.note.Rest(quarterLength=1), m21.note.Note('e4', quarterLength=1),
                     m21.note.Note('f4', quarterLength=1)]
  given_rhythm =    [m21.note.Note('d4', quarterLength=1), m21.note.Note('e4', quarterLength=1),
                     m21.note.Note('f4', quarterLength=1)]
  
  expected_permutation = [
    DistanceType.SUBSTITUTION,
    DistanceType.SAME,
    DistanceType.SAME
    ]
  actual_permutation, points = get_dtw_rhythm_evaluation(expected_rhythm, given_rhythm)

  assert expected_permutation == actual_permutation

def test_rhythm_evaluation_dtw_missing_beginning():
  expected_rhythm = [m21.note.Note('d4', quarterLength=1), m21.note.Note('e4', quarterLength=1),
                     m21.note.Rest(quarterLength=2), m21.note.Note('g4', quarterLength=1),
                     m21.note.Note('f4', quarterLength=1)]
  given_rhythm =    [m21.note.Rest(quarterLength=2), m21.note.Note('c4', quarterLength=1),
                     m21.note.Note('g4', quarterLength=1)]
  
  expected_permutation = [
    DistanceType.DELETION,
    DistanceType.DELETION,
    DistanceType.SAME,
    DistanceType.SAME,
    DistanceType.SAME
    ]
  actual_permutation, points = get_dtw_rhythm_evaluation(expected_rhythm, given_rhythm)

  assert expected_permutation == actual_permutation

def test_rhythm_evaluation_dtw_missing_middle():
  expected_rhythm = [m21.note.Note('d4', quarterLength=1), m21.note.Note('e4', quarterLength=1),
                     m21.note.Rest(quarterLength=2), m21.note.Note('g4', quarterLength=1),
                     m21.note.Note('f4', quarterLength=1)]
  given_rhythm =    [m21.note.Note('c4', quarterLength=2), m21.note.Note('f4', quarterLength=1),
                     m21.note.Note('g4', quarterLength=1), m21.note.Note('d4', quarterLength=1)]
  
  expected_permutation = [
    DistanceType.SUBSTITUTION,
    DistanceType.SAME,
    DistanceType.DELETION,
    DistanceType.SAME,
    DistanceType.SAME
    ]
  actual_permutation, points = get_dtw_rhythm_evaluation(expected_rhythm, given_rhythm)

  assert expected_permutation == actual_permutation

def test_rhythm_evaluation_dtw_missing_end():
  expected_rhythm = [m21.note.Note('d4', quarterLength=1), m21.note.Note('e4', quarterLength=1),
                     m21.note.Rest(quarterLength=2), m21.note.Note('g4', quarterLength=1),
                     m21.note.Note('f4', quarterLength=1)]
  given_rhythm =    [m21.note.Note('c4', quarterLength=1), m21.note.Note('g4', quarterLength=1),
                     m21.note.Rest(quarterLength=2)]
  
  expected_permutation = [
    DistanceType.SAME,
    DistanceType.SAME,
    DistanceType.SAME,
    DistanceType.DELETION,
    DistanceType.DELETION
    ]
  actual_permutation, points = get_dtw_rhythm_evaluation(expected_rhythm, given_rhythm)

  assert expected_permutation == actual_permutation

def test_rhythm_evaluation_dtw_missing_beginning_middle():
  expected_rhythm = [m21.note.Rest(quarterLength=1), m21.note.Note('d4', quarterLength=1),
                     m21.note.Note('e4', quarterLength=1), m21.note.Rest(quarterLength=2),
                     m21.note.Note('g4', quarterLength=1), m21.note.Note('f4', quarterLength=1)]
  given_rhythm =    [m21.note.Note('d4', quarterLength=1), m21.note.Note('e4', quarterLength=1),
                     m21.note.Note('f4', quarterLength=1), m21.note.Note('g4', quarterLength=1)]
  
  expected_permutation = [
    DistanceType.DELETION,
    DistanceType.SAME,
    DistanceType.SAME,
    DistanceType.DELETION,
    DistanceType.SAME,
    DistanceType.SAME
    ]
  actual_permutation, points = get_dtw_rhythm_evaluation(expected_rhythm, given_rhythm)

  assert expected_permutation == actual_permutation

def test_rhythm_evaluation_dtw_missing_beginning_end():
  expected_rhythm = [m21.note.Rest(quarterLength=1), m21.note.Note('d4', quarterLength=1),
                     m21.note.Note('e4', quarterLength=1), m21.note.Note('f4', quarterLength=1),
                     m21.note.Note('g4', quarterLength=1), m21.note.Rest(quarterLength=1)]
  given_rhythm =    [m21.note.Note('e4', quarterLength=1), m21.note.Note('f4', quarterLength=1)]
  
  expected_permutation = [
    DistanceType.DELETION,
    DistanceType.SAME,
    DistanceType.SAME,
    DistanceType.DELETION,
    DistanceType.DELETION,
    DistanceType.DELETION
    ]
  actual_permutation, points = get_dtw_rhythm_evaluation(expected_rhythm, given_rhythm)

  assert expected_permutation == actual_permutation

def test_rhythm_evaluation_dtw_missing_middle_end():
  expected_rhythm = [m21.note.Note('d4', quarterLength=1), m21.note.Note('e4', quarterLength=1),
                     m21.note.Rest(quarterLength=2), m21.note.Note('g4', quarterLength=1),
                     m21.note.Note('f4', quarterLength=1)]
  given_rhythm =    [m21.note.Note('d4', quarterLength=1), m21.note.Note('e4', quarterLength=1),
                     m21.note.Note('f4', quarterLength=1)]
  
  expected_permutation = [
    DistanceType.SAME,
    DistanceType.SAME,
    DistanceType.DELETION,
    DistanceType.SAME,
    DistanceType.DELETION
    ]
  actual_permutation, points = get_dtw_rhythm_evaluation(expected_rhythm, given_rhythm)

  assert expected_permutation == actual_permutation

def test_rhythm_evaluation_dtw_missing_middle_middle():
  expected_rhythm = [m21.note.Note('d4', quarterLength=1), m21.note.Note('e4', quarterLength=1),
                     m21.note.Rest(quarterLength=2), m21.note.Note('g4', quarterLength=1),
                     m21.note.Rest(quarterLength=2), m21.note.Note('g4', quarterLength=1),
                     m21.note.Note('f4', quarterLength=1)]
  given_rhythm =    [m21.note.Note('f4', quarterLength=1), m21.note.Note('e4', quarterLength=1),
                     m21.note.Note('g4', quarterLength=1), m21.note.Note('c4', quarterLength=1),
                     m21.note.Note('e4', quarterLength=1)]
  
  expected_permutation = [
    DistanceType.SAME,
    DistanceType.SAME,
    DistanceType.DELETION,
    DistanceType.SAME,
    DistanceType.DELETION,
    DistanceType.SAME,
    DistanceType.SAME
    ]
  actual_permutation, points = get_dtw_rhythm_evaluation(expected_rhythm, given_rhythm)

  assert expected_permutation == actual_permutation

def test_rhythm_evaluation_dtw_expected_none_got_none():
  expected_rhythm = []
  given_rhythm =    []

  expected_permutation = []
  actual_permutation, points = get_dtw_rhythm_evaluation(expected_rhythm, given_rhythm)

  assert expected_permutation == actual_permutation
  assert points == NORMALIZE_MAXIMUM

def test_rhythm_evaluation_dtw_expected_some_got_none():
  expected_rhythm = [m21.note.Note('d4', quarterLength=1), m21.note.Note('d4', quarterLength=1),
                     m21.note.Note('d4', quarterLength=2), m21.note.Rest(quarterLength=2),
                     m21.note.Note('d4', quarterLength=1)]
  given_rhythm =    []
  
  expected_permutation = [
    DistanceType.DELETION,
    DistanceType.DELETION,
    DistanceType.DELETION,
    DistanceType.DELETION,
    DistanceType.DELETION
    ]
  actual_permutation, points = get_dtw_rhythm_evaluation(expected_rhythm, given_rhythm)

  assert expected_permutation == actual_permutation

def test_rhythm_evaluation_dtw_expected_none_got_some():
  expected_rhythm = []
  given_rhythm =    [m21.note.Note('c4', quarterLength=2), m21.note.Note('c4', quarterLength=1),
                     m21.note.Note('c4', quarterLength=1), m21.note.Rest(quarterLength=1),
                     m21.note.Note('c4', quarterLength=1)]
  
  expected_permutation = [
    DistanceType.INSERTION,
    DistanceType.INSERTION,
    DistanceType.INSERTION,
    DistanceType.INSERTION,
    DistanceType.INSERTION
    ]
  actual_permutation, points = get_dtw_rhythm_evaluation(expected_rhythm, given_rhythm)

  assert expected_permutation == actual_permutation