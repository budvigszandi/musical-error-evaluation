from evaluate import get_only_dtw_evaluation, run_main_song_evaluation
from input.midi_reader import get_score_from_midi

SONG_FUNCTION_NAME_BEGINNING_BM = "example_song_evaluation_bm"
SONG_FUNCTION_NAME_BEGINNING_DTW = "example_song_evaluation_dtw"

def example_song_evaluation_bm_1():
  exp_score = get_score_from_midi("../midi/rhythm-expected.mid")
  giv_score = get_score_from_midi("../midi/rhythm-given.mid")
  run_main_song_evaluation(exp_score, giv_score, True)

def example_song_evaluation_dtw_1():
  exp_score = get_score_from_midi("../midi/rhythm-expected.mid")
  giv_score = get_score_from_midi("../midi/rhythm-given.mid")
  get_only_dtw_evaluation(exp_score, giv_score)
