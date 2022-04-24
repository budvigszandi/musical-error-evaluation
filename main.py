from examples.example_note_evaluations import *
from examples.example_rhythm_evaluations import *
from examples.example_song_evaluations import *
from inspect import getmembers, isfunction
from examples import example_note_evaluations, example_rhythm_evaluations, example_song_evaluations
from statistics import get_compressed_dtw_dtw_stats, get_dtw_boundary_stats, get_dtw_levenshtein_stats
from metrics.notes.note_eval_boundaries import get_note_eval_runtimes

def choose_from_main_menu():
  print("What would you like to run?")
  print("1 - Song evaluation")
  print("2 - Song evaluation with only DTW")
  print("3 - Note evaluation")
  print("4 - Rhythm evaluation by DTW")
  print("5 - Rhythm evaluation by Levenshtein")
  print("6 - Runtime statistics")
  print("7 - Exit")
  index = int(input())
  return index

def run_chosen_method(index):
  while index < 1 or index > 6:
    print("That is not an existing option. Try again:")
    index = int(input())

  # TODO: Exceptions when choosing non-existing options
  if index == 1:
    choose_from_evaluations(example_song_evaluations, SONG_FUNCTION_NAME_BEGINNING_BM)
  elif index == 2:
    choose_from_evaluations(example_song_evaluations, SONG_FUNCTION_NAME_BEGINNING_DTW)
  elif index == 3:
    choose_from_evaluations(example_note_evaluations, NOTE_FUNCTION_NAME_BEGINNING)
  elif index == 4:
    choose_from_evaluations(example_rhythm_evaluations, RHYTHM_FUNCTION_NAME_BEGINNING_DTW)
  elif index == 5:
    choose_from_evaluations(example_rhythm_evaluations, RHYTHM_FUNCTION_NAME_BEGINNING_LEV)
  elif index == 6:
    print("Choose from the following:")
    print("1 - DTW - Levenshtein statistics")
    print("2 - Compressed DTW vs DTW statistics")
    print("3 - DTW runtime check")
    print("4 - Note evaluation runtime check")
    stat_index = int(input())
    run_chosen_statistics(stat_index)
  elif index == 7:
    print("Exiting")

def run_chosen_statistics(index):
  while index < 1 or index > 4:
    print("That is not an existing option. Try again:")
    index = int(input())

  if index == 1:
    get_dtw_levenshtein_stats(1, 9)
  elif index == 2:
    get_compressed_dtw_dtw_stats(1, 7)
  elif index == 3:
    get_dtw_boundary_stats(1, 9)
  elif index == 4:
    get_note_eval_runtimes(1, 8)

def choose_from_evaluations(evaluations, function_name_beginning):
  print("Examples:")
  functions = getmembers(evaluations, isfunction)
  for f in functions:
    if function_name_beginning in f[0]:
      print(f"[-] {f[0]}")
  print("Enter the name of the example you'd like to run:")
  f_name = input()
  f_name += "()"
  eval(f_name)

index = choose_from_main_menu()
run_chosen_method(index)
