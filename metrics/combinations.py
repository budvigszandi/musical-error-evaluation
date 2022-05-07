def get_index_variations(rows, columns):
  arr = [[] for i in range(rows)]
  for i in range(rows):
    for j in range(columns):
      arr[i].append(j)
  # print("starting indices", arr)
  index_variations = build_index_variations(arr)
  return index_variations

def build_index_variations(arr):
  index_variations = []
  # number of arrays
  n = len(arr)

  # to keep track of next element
  # in each of the n arrays
  indices = [0 for i in range(n)]

  while (1):

    # print current combination
    current_combination = []
    for i in range(n):
      # print(arr[i][indices[i]], end = " ")
      current_combination.append(arr[i][indices[i]])
    index_variations.append(current_combination)
    # print()

    # find the rightmost array that has more
    # elements left after the current element
    # in that array
    next = n - 1
    while (next >= 0 and
      (indices[next] + 1 >= len(arr[next]))):
      next-=1

    # no such array is found so no more
    # combinations left
    if (next < 0):
      return index_variations

    # if found move to next element in that
    # array
    indices[next] += 1

    # for all arrays to the right of this
    # array current index again points to
    # first element
    for i in range(next + 1, n):
      indices[i] = 0