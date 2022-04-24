from enum import Enum

class backgroundColors(Enum):
  SAME = "\033[0;30;42m"         # green
  DELETION = "\033[0;30;41m"     # red
  INSERTION = "\033[0;30;44m"    # blue
  SUBSTITUTION = "\033[0;30;45m" # purple
  END_COLOR = "\033[0;0m"
