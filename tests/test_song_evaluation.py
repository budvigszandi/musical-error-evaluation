import os, os.path
import pytest

from evaluate import run_main_song_evaluation
from input.midi_reader import OUTPUT_FOLDER, get_score_from_midi

def test_song_evaluation_bm_same():
  exp_score = get_score_from_midi("../midi/regi-francia-dal.mid")
  giv_score = get_score_from_midi("../midi/regi-francia-dal.mid")

  file_count_before = get_file_count_in_output_folder()
  
  expected_notation_string = ""
  actual_notation_strings = run_main_song_evaluation(exp_score, giv_score, True)

  file_count_after = get_file_count_in_output_folder()

  assert len(actual_notation_strings) == 1
  assert expected_notation_string == actual_notation_strings[0]
  assert file_count_after == file_count_before + 2

def test_song_evaluation_bm_french_song():
  exp_score = get_score_from_midi("../midi/regi-francia-dal.mid")
  giv_score = get_score_from_midi("../midi/regi-francia-dal-mod-1.mid")
  
  file_count_before = get_file_count_in_output_folder()

  expected_notation_string = "chord{g4<black> g'4<purple> } " + \
                             "chord{a4<black> a'4<purple> } b-2<black> " + \
                             "a4<grey> c'8<black> b-8<black> a2<black> a4<black> " + \
                             "b-8<black> a8<black> g4<black> g8<orange> r8<blue> " + \
                             "g8<orange> r8<blue> b-4<black> a2<black> "
  actual_notation_strings = run_main_song_evaluation(exp_score, giv_score, True)

  file_count_after = get_file_count_in_output_folder()

  assert len(actual_notation_strings) == 1
  assert expected_notation_string == actual_notation_strings[0]
  assert file_count_after == file_count_before + 2

def test_song_evaluation_bm_french_song_2():
  exp_score = get_score_from_midi("../midi/regi-francia-dal.mid")
  giv_score = get_score_from_midi("../midi/regi-francia-dal-mod-2.mid")
  
  file_count_before = get_file_count_in_output_folder()

  expected_notation_string = "g8<red> a8<red> b-2<red> b-4<red> c'8<black> " + \
                             "b-8<black> a2<black> a4<black> b-8<black> " + \
                             "a8<black> g4<black> d4<grey> d4<grey> b-4<black> " + \
                             "a4<orange> r2<orange> "
  actual_notation_strings = run_main_song_evaluation(exp_score, giv_score, True)

  file_count_after = get_file_count_in_output_folder()

  assert len(actual_notation_strings) == 1
  assert expected_notation_string == actual_notation_strings[0]
  assert file_count_after == file_count_before + 2

def test_song_evaluation_bm_tricky_rhythm():
  exp_score = get_score_from_midi("examples/midis/rhythm-expected.mid")
  giv_score = get_score_from_midi("examples/midis/rhythm-given.mid")
  
  file_count_before = get_file_count_in_output_folder()

  expected_notation_string = "c8<orange> e8<orange> g4<black> r2<orange> "
  actual_notation_strings = run_main_song_evaluation(exp_score, giv_score, True)

  file_count_after = get_file_count_in_output_folder()
  
  assert len(actual_notation_strings) == 1
  assert expected_notation_string == actual_notation_strings[0]
  assert file_count_after == file_count_before + 2

def test_song_evaluation_bm_empty_expected():
  with pytest.raises(ValueError):
    exp_score = get_score_from_midi("examples/midis/empty.mid")
    giv_score = get_score_from_midi("examples/midis/rhythm-given.mid")
    run_main_song_evaluation(exp_score, giv_score, True)

def test_song_evaluation_bm_empty_given():
  with pytest.raises(ValueError):
    exp_score = get_score_from_midi("examples/midis/rhythm-expected.mid")
    giv_score = get_score_from_midi("examples/midis/empty.mid")
    run_main_song_evaluation(exp_score, giv_score, True)

def get_file_count_in_output_folder():
  return len([entry for entry in os.listdir(OUTPUT_FOLDER) if os.path.isfile(os.path.join(OUTPUT_FOLDER, entry))])