import music21 as m21
from evaluate import draw_note_evaluation, get_note_evaluation

NOTE_FUNCTION_NAME_BEGINNING = "example_note_evaluation"

def example_note_evaluation_big():
  expected_notes = [m21.pitch.Pitch('d1'), m21.pitch.Pitch('d--1'), m21.pitch.Pitch('c#3'),
                  m21.pitch.Pitch('c#4'), m21.pitch.Pitch('a4'), m21.pitch.Pitch('b4'),
                  m21.pitch.Pitch('c5'), m21.pitch.Pitch('d5')]
  given_notes = [m21.pitch.Pitch('d-3'), m21.pitch.Pitch('d1'),  m21.pitch.Pitch('e2'),
                m21.pitch.Pitch('f3'), m21.pitch.Pitch('g3'), m21.pitch.Pitch('a3'),
                m21.pitch.Pitch('a4')]
  example_get_note_evaluation(expected_notes, given_notes)

def example_note_evaluation_coverage_1():
  expected_notes = [m21.pitch.Pitch('c4'), m21.pitch.Pitch('f4'), m21.pitch.Pitch('c5')]
  given_notes = [m21.pitch.Pitch('c4'), m21.pitch.Pitch('c5'), m21.pitch.Pitch('c6')]
  example_get_note_evaluation(expected_notes, given_notes)

def example_note_evaluation_coverage_2():
  expected_notes = [m21.pitch.Pitch('a1'), m21.pitch.Pitch('c2'), m21.pitch.Pitch('e2')]
  given_notes = [m21.pitch.Pitch('c2'), m21.pitch.Pitch('e3'), m21.pitch.Pitch('b3')]
  example_get_note_evaluation(expected_notes, given_notes)

def example_note_evaluation_multiple_same_in_given():
  expected_notes = [m21.pitch.Pitch('c4'), m21.pitch.Pitch('e4'), m21.pitch.Pitch('g4')]
  given_notes = [m21.pitch.Pitch('c4'), m21.pitch.Pitch('c5'), m21.pitch.Pitch('c5')]
  example_get_note_evaluation(expected_notes, given_notes)

def example_note_evaluation_harmonic():
  expected_notes = [m21.pitch.Pitch('c4'), m21.pitch.Pitch('e4'), m21.pitch.Pitch('g4')]
  given_notes = [m21.pitch.Pitch('c4'), m21.pitch.Pitch('e4'), m21.pitch.Pitch('c5')]
  example_get_note_evaluation(expected_notes, given_notes)

def example_note_evaluation_cent_difference():
  expected_notes = [m21.pitch.Pitch('c4'), m21.pitch.Pitch('e4'), m21.pitch.Pitch('g4')]
  given_notes = [m21.pitch.Pitch('c4', microtone=20), m21.pitch.Pitch('e4'), m21.pitch.Pitch('g5')]
  example_get_note_evaluation(expected_notes, given_notes)

def example_note_evaluation_expected_one_got_more():
  expected_notes = [m21.pitch.Pitch('c4')]
  given_notes = [m21.pitch.Pitch('c3'), m21.pitch.Pitch('c5'), m21.pitch.Pitch('c6')]
  example_get_note_evaluation(expected_notes, given_notes)

def example_note_evaluation_expected_more_got_one():
  expected_notes = [m21.pitch.Pitch('c4'), m21.pitch.Pitch('e4'), m21.pitch.Pitch('g4')]
  given_notes = [m21.pitch.Pitch('e6')]
  example_get_note_evaluation(expected_notes, given_notes)

def example_note_evaluation_duplicate_cover():
  expected_notes = [m21.pitch.Pitch('c4')]
  given_notes = [m21.pitch.Pitch('c4'), m21.pitch.Pitch('c5'), m21.pitch.Pitch('c6')]
  example_get_note_evaluation(expected_notes, given_notes)

def example_note_evaluation_got_only_unrelated():
  expected_notes = [m21.pitch.Pitch('c4'), m21.pitch.Pitch('e4'), m21.pitch.Pitch('g4')]
  given_notes = [m21.pitch.Pitch('a2'), m21.pitch.Pitch('c3'), m21.pitch.Pitch('e3')]
  example_get_note_evaluation(expected_notes, given_notes)

def example_note_evaluation_expected_none_got_some():
  expected_notes = []
  given_notes = [m21.pitch.Pitch('c4'), m21.pitch.Pitch('e4'), m21.pitch.Pitch('g4')]
  example_get_note_evaluation(expected_notes, given_notes)

def example_note_evaluation_expected_some_got_none():
  expected_notes = [m21.pitch.Pitch('c4'), m21.pitch.Pitch('e4'), m21.pitch.Pitch('g4')]
  given_notes = []
  example_get_note_evaluation(expected_notes, given_notes)

def example_note_evaluation_expected_none_got_none():
  expected_notes = []
  given_notes = []
  example_get_note_evaluation(expected_notes, given_notes)

def example_get_note_evaluation(expected_notes, given_notes):
  note_eval = get_note_evaluation(expected_notes, given_notes)
  draw_note_evaluation(expected_notes, given_notes, note_eval)