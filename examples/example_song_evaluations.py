from evaluate import get_only_dtw_evaluation, run_main_song_evaluation
from input.midi_reader import get_score_from_midi

SONG_FUNCTION_NAME_BEGINNING_BM = "example_song_evaluation_bm"
SONG_FUNCTION_NAME_BEGINNING_DTW = "example_song_evaluation_dtw"

def example_song_evaluation_bm_same():
  exp_score = get_score_from_midi("../midi/regi-francia-dal.mid")
  giv_score = get_score_from_midi("../midi/regi-francia-dal.mid")
  run_main_song_evaluation(exp_score, giv_score, True)

def example_song_evaluation_bm_total_difference():
  exp_score = get_score_from_midi("../midi/regi-francia-dal-rovid.mid")
  giv_score = get_score_from_midi("../midi/nemet-tanc-rovid.mid")
  run_main_song_evaluation(exp_score, giv_score, True)

def example_song_evaluation_bm_french_song():
  exp_score = get_score_from_midi("../midi/regi-francia-dal.mid")
  giv_score = get_score_from_midi("../midi/regi-francia-dal-mod-1.mid")
  run_main_song_evaluation(exp_score, giv_score, True)

def example_song_evaluation_bm_french_song_2():
  exp_score = get_score_from_midi("../midi/regi-francia-dal.mid")
  giv_score = get_score_from_midi("../midi/regi-francia-dal-mod-2.mid")
  run_main_song_evaluation(exp_score, giv_score, True)

def example_song_evaluation_bm_tricky_rhythm():
  exp_score = get_score_from_midi("examples/midis/rhythm-expected.mid")
  giv_score = get_score_from_midi("examples/midis/rhythm-given.mid")
  run_main_song_evaluation(exp_score, giv_score, True)

def example_song_evaluation_dtw_1():
  exp_score = get_score_from_midi("examples/midis/rhythm-expected.mid")
  giv_score = get_score_from_midi("examples/midis/rhythm-given.mid")
  get_only_dtw_evaluation(exp_score, giv_score)
