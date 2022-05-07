import music21 as m21
import shutil
from datetime import datetime

OUTPUT_FOLDER = "visualizer/output/"

def get_score_from_midi(file_path):
  return m21.converter.parse(file_path)

def get_simplified_data_from_score(score):
  simplified_data = []
  number_of_parts = len(score.parts)
  for i in range(number_of_parts):
    part = []
    number_of_measures = len(score.parts[i].getElementsByClass(m21.stream.Measure))
    for j in range(number_of_measures):
      current_measure = score.parts[i].getElementsByClass(m21.stream.Measure)[j]
      current_measure_data_count = len(current_measure)
      for k in range(current_measure_data_count):
        current_element = current_measure[k]
        try:
          if current_element.isNote or current_element.isRest or current_element.isChord:
            part.append(current_element)
        except AttributeError as error:
          pass
    simplified_data.append(part)
  return simplified_data

def put_sheet_in_output_folder(score, given=False):
  filename = score.write('musicxml.png')
  now = datetime.now()
  formatted_time = now.strftime("%Y-%m-%d-%H-%M-%S-%f")[:-3]
  expected_filename = f"{OUTPUT_FOLDER}expected-{formatted_time}.png"
  given_filename = f"{OUTPUT_FOLDER}given-{formatted_time}.png"
  if not given:
    shutil.copy(filename, expected_filename)
    print(f"Drawn expected sheet to [{expected_filename}]")
  else:
    shutil.copy(filename, given_filename)
    print(f"Drawn given sheet to [{given_filename}]")