import music21 as m21
import shutil
from datetime import datetime

def get_score_from_midi(file_path):
  # TODO: Exception when file doesn't exist
  return m21.converter.parse(file_path)

# TODO: consider m21.stream.Voice object (when one note is longer from the harmony)
def get_simplified_data_from_score(score):
  simplified_data = []
  number_of_parts = len(score.parts)
  for i in range(number_of_parts):
    number_of_measures = len(score.parts[i].getElementsByClass(m21.stream.Measure))
    for j in range(number_of_measures):
      current_measure = score.parts[i].getElementsByClass(m21.stream.Measure)[j]
      current_measure_data_count = len(current_measure)
      for k in range(current_measure_data_count):
        current_element = current_measure[k]
        try:
          if current_element.isNote or current_element.isRest or current_element.isChord:
            simplified_data.append(current_element)
        except AttributeError as error:
          pass
  return simplified_data

def put_sheet_in_output_folder(score, given=False):
  filename = score.write('musicxml.png')
  now = datetime.now()
  formatted_time = now.strftime("%Y-%d-%m-%H-%M-%S")
  expected_filename = f"visualizer/output/expected-{formatted_time}.png"
  given_filename = f"visualizer/output/given-{formatted_time}.png"
  if not given:
    shutil.copy(filename, expected_filename)
  else:
    shutil.copy(filename, given_filename)