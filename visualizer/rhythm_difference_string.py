from visualizer.background_colors import *

class RhythmDifferenceString:
  string = None

  def __init__(self):
    self.string = f""
  
  def add(self, rhythm_string, bg_color):
    self.string = f"{bg_color.value}{rhythm_string}{backgroundColors.END_COLOR.value}" + " " + self.string