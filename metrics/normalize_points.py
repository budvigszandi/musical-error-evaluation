NORMALIZE_MINIMUM = 1
NORMALIZE_MAXIMUM = 10

def normalize(value, min, max):
  start = NORMALIZE_MINIMUM
  end = NORMALIZE_MAXIMUM
  width = end - start
  
  if max == min:
    return NORMALIZE_MAXIMUM
  else:
    return float("{:.2f}".format((value - min) / (max - min) * width + start))
