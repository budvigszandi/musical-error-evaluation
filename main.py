import music21 as m21
from evaluate_notes import *
from draw_harmonic_results import *
from levenshtein_distance import *

# ------------------------------
# Expected and given note arrays
# ------------------------------

# expected_notes = [m21.pitch.Pitch('c4'), m21.pitch.Pitch('e4'), m21.pitch.Pitch('g4')]
# given_notes = [m21.pitch.Pitch('c4'), m21.pitch.Pitch('e4'), m21.pitch.Pitch('c5')]

# expected_notes = [m21.pitch.Pitch('d1'),
#                   m21.pitch.Pitch('d--1'), m21.pitch.Pitch('c#3'), m21.pitch.Pitch('c#4')]
# given_notes = [m21.pitch.Pitch('d-3'), m21.pitch.Pitch('d1'),  m21.pitch.Pitch('e2')]

# Example 1 for harmonics with coverage
# expected_notes = [m21.pitch.Pitch('c4'), m21.pitch.Pitch('f4'), m21.pitch.Pitch('c5')]
# given_notes = [m21.pitch.Pitch('c4'), m21.pitch.Pitch('c5'), m21.pitch.Pitch('c6')]

# Example 2 for harmonics with coverage
# expected_notes = [m21.pitch.Pitch('a1'), m21.pitch.Pitch('c2'), m21.pitch.Pitch('e2')]
# given_notes = [m21.pitch.Pitch('c2'), m21.pitch.Pitch('e3'), m21.pitch.Pitch('b3')]

expected_notes = [m21.pitch.Pitch('c4'), m21.pitch.Pitch('e4'), m21.pitch.Pitch('g4')]
given_notes = [m21.pitch.Pitch('c4'), m21.pitch.Pitch('c5'), m21.pitch.Pitch('c5')]

# ----------------------------------
# Expected and given rhythmic arrays
# ----------------------------------

c_quarter = m21.note.Note('c4')

c_half = m21.note.Note('c4')
c_half.duration.quarterLength = 2

rest_quarter = m21.note.Rest()

rest_half = m21.note.Rest()
rest_half.duration.quarterLength = 2

expected_rhythm = [c_quarter, c_quarter, c_half,    rest_half,    rest_quarter, c_quarter]  # qqh21q
given_rhythm =    [c_half,    c_quarter, c_quarter, rest_quarter, rest_half,    c_quarter ] # hqq12q

# -----------------
# Getting scenarios
# -----------------

# rel_matrix = get_relationship_matrix(expected_notes, given_notes)
# print("------------------------------")
# rel_points_matrix = get_relationship_points(rel_matrix)
# print("------------------------------")
# scenarios = get_scenarios(rel_matrix, rel_points_matrix)

# ------------------
# Drawing a scenario
# ------------------

# print("Got scenarios, now drawing")
# fig, ax = plt.subplots()
# graph = nx.Graph()
# add_nodes(graph, expected_notes, given_notes)
# group_expected_nodes(expected_notes)
# scenario = list(scenarios.keys())[0]
# for rel in scenario:
#   print(str(rel))
# print(scenarios[scenario], "points")
# group_related_nodes_with_edge_creation(graph, expected_notes, scenario)
# group_isolated_expected_nodes(graph)
# draw_graph(graph, ax)

# --------------------
# Levenshtein distance
# --------------------
# source = '1234567890'
# target = '125690'

# source = "qqh21q"
# target = "hqq12q"
source = expected_rhythm
target = given_rhythm
get_levenshtein_distance(source, target)
distance_matrix = fill_distance_matrix(source, target)
get_one_by_one_comparison(source, target, distance_matrix)