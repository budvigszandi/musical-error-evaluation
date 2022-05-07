import music21 as m21

from evaluate import get_note_evaluation
from metrics.notes.note_relationship import NoteRelationship
from metrics.notes.note_relationship_type import NoteRelationshipType

def test_note_evaluation_empty_expected():
  expected_notes = []
  given_notes = [m21.pitch.Pitch('c4'), m21.pitch.Pitch('e4'), m21.pitch.Pitch('g4')]
  
  expected_note_eval = [
    NoteRelationship(
      NoteRelationshipType.UNRELATED,
      m21.pitch.Pitch('c4'),
      None
      ),
    NoteRelationship(
      NoteRelationshipType.UNRELATED,
      m21.pitch.Pitch('e4'),
      None
      ),
    NoteRelationship(
      NoteRelationshipType.UNRELATED,
      m21.pitch.Pitch('g4'),
      None
      )
  ]
  actual_note_eval = get_note_evaluation(expected_notes, given_notes)

  for i in range(len(actual_note_eval)):
    assert note_rel_equals(expected_note_eval[i], actual_note_eval[i])

def test_note_evaluation_empty_given():
  expected_notes = [m21.pitch.Pitch('c4'), m21.pitch.Pitch('e4'), m21.pitch.Pitch('g4')]
  given_notes = []
  
  expected_note_eval = [
    NoteRelationship(
      NoteRelationshipType.UNRELATED,
      None,
      m21.pitch.Pitch('c4'),
      ),
    NoteRelationship(
      NoteRelationshipType.UNRELATED,
      None,
      m21.pitch.Pitch('e4'),
      ),
    NoteRelationship(
      NoteRelationshipType.UNRELATED,
      None,
      m21.pitch.Pitch('g4'),
      )
  ]
  actual_note_eval = get_note_evaluation(expected_notes, given_notes)

  for i in range(len(actual_note_eval)):
    assert note_rel_equals(expected_note_eval[i], actual_note_eval[i])

def test_note_evaluation_empty():
  expected_notes = []
  given_notes = []
  
  expected_note_eval = []
  actual_note_eval = get_note_evaluation(expected_notes, given_notes)

  assert expected_note_eval == actual_note_eval

def test_note_evaluation_harmonic():
  expected_notes = [m21.pitch.Pitch('c4'), m21.pitch.Pitch('e4'), m21.pitch.Pitch('g4')]
  given_notes = [m21.pitch.Pitch('c4'), m21.pitch.Pitch('e4'), m21.pitch.Pitch('c5')]
  
  expected_note_eval = [
    NoteRelationship(
      NoteRelationshipType.PERFECT_MATCH,
      m21.pitch.Pitch('c4'),
      m21.pitch.Pitch('c4')
      ),
    NoteRelationship(
      NoteRelationshipType.PERFECT_MATCH,
      m21.pitch.Pitch('e4'),
      m21.pitch.Pitch('e4')
      ),
    NoteRelationship(
      NoteRelationshipType.HARMONIC,
      m21.pitch.Pitch('c5'),
      m21.pitch.Pitch('c4'),
      None,
      (2, m21.pitch.Pitch('c4'))
      )
  ]
  actual_note_eval = get_note_evaluation(expected_notes, given_notes)

  for i in range(len(actual_note_eval)):
    assert note_rel_equals(expected_note_eval[i], actual_note_eval[i])

def test_note_evaluation_same():
  expected_notes = [m21.pitch.Pitch('c4'), m21.pitch.Pitch('e4'), m21.pitch.Pitch('g4')]
  given_notes = [m21.pitch.Pitch('c4'), m21.pitch.Pitch('e4'), m21.pitch.Pitch('g4')]
  
  expected_note_eval = [
    NoteRelationship(
      NoteRelationshipType.PERFECT_MATCH,
      m21.pitch.Pitch('c4'),
      m21.pitch.Pitch('c4')
      ),
    NoteRelationship(
      NoteRelationshipType.PERFECT_MATCH,
      m21.pitch.Pitch('e4'),
      m21.pitch.Pitch('e4')
      ),
    NoteRelationship(
      NoteRelationshipType.PERFECT_MATCH,
      m21.pitch.Pitch('g4'),
      m21.pitch.Pitch('g4')
      ),
  ]
  actual_note_eval = get_note_evaluation(expected_notes, given_notes)

  for i in range(len(actual_note_eval)):
    assert note_rel_equals(expected_note_eval[i], actual_note_eval[i])

def test_note_evaluation_coverage_1():
  expected_notes = [m21.pitch.Pitch('c4'), m21.pitch.Pitch('f4'), m21.pitch.Pitch('c5')]
  given_notes = [m21.pitch.Pitch('c4'), m21.pitch.Pitch('c5'), m21.pitch.Pitch('c6')]
  
  expected_note_eval = [
    NoteRelationship(
      NoteRelationshipType.PERFECT_MATCH,
      m21.pitch.Pitch('c4'),
      m21.pitch.Pitch('c4')
      ),
    NoteRelationship(
      NoteRelationshipType.PERFECT_MATCH,
      m21.pitch.Pitch('c5'),
      m21.pitch.Pitch('c5')
      ),
    NoteRelationship(
      NoteRelationshipType.HARMONIC,
      m21.pitch.Pitch('c6'),
      m21.pitch.Pitch('f4'),
      None,
      (3, m21.pitch.Pitch('f4', microtone=-2))
      )
  ]
  actual_note_eval = get_note_evaluation(expected_notes, given_notes)

  for i in range(len(actual_note_eval)):
    assert note_rel_equals(expected_note_eval[i], actual_note_eval[i])

def note_rel_equals(source: NoteRelationship, target: NoteRelationship):
  rel_equals = True
  if source.type != target.type: rel_equals = False
  if source.given_note != target.given_note: rel_equals = False
  if source.expected_note != target.expected_note: rel_equals = False
  if source.cent_difference != target.cent_difference: rel_equals = False
  if source.harmonic_info != target.harmonic_info: rel_equals = False
  print("Rel_equals", rel_equals)
  return rel_equals