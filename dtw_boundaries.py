import time
import music21 as m21
from evaluate import get_melody_dtw_evaluation

def get_dtw_runtimes():
  runtimes = {}
  data = get_dtw_dummy_data()
  for d in data:
    count = str(len(d[0])) + "x" + str(len(d[1]))
    start = time.time()
    get_melody_dtw_evaluation(d[0], d[1])
    end = time.time()
    runtimes[count] = "{:.2f}".format(end - start)
  return runtimes

def get_dtw_dummy_data():
  note_c = m21.note.Note("C4")
  dummy_data = []
  exp = []
  giv = []
  for i in range(1, 11):
    exp = i * [note_c]
    for j in range(1, 11):
      giv = j * [note_c]
      dummy_data.append([exp, giv])
  return dummy_data
