import networkx as nx
import matplotlib.pyplot as plt
from evaluate_notes import *
from relationship_type import RelationshipType

# TODO: Finish refactoring

def add_nodes(expected_notes, given_notes):
  for i in range(len(expected_notes)):
    node_name = get_node_name(expected_notes[i])
    G.add_node(node_name, pos = (1, len(expected_notes) - i))

  for i in range(len(given_notes)):
    node_name = get_node_name(given_notes[i], True)
    G.add_node(node_name, pos = (2, len(given_notes) - i))

def get_node_name(note, given = False):
  if given:
    node_name = " " + note.nameWithOctave + " "
  else:
    node_name = note.nameWithOctave
  cent_difference = note.microtone.cents
  if cent_difference != 0:
    node_name += "(" + str(cent_difference) + ")"
  return node_name

def group_expected_nodes(expected_notes):
  for i in range(len(expected_notes)):
    node_name = get_node_name(expected_notes[i])
    expected_nodes.append(node_name)

def group_related_nodes_with_edge_creation(scenario):
  for i in range(len(scenario)):
    rel_type = scenario[i].type
    current_rel = scenario[i]
    given_note_node_name = get_node_name(scenario[i].given_note, True)
    expected_note_node_name = get_node_name(scenario[i].expected_note)
    if rel_type == RelationshipType.PERFECT_MATCH:
      G.add_edges_from([(expected_note_node_name, given_note_node_name)])
      perfect_match_nodes.append(given_note_node_name)
    elif rel_type == RelationshipType.CENT_DIFFERENCE:
      G.add_edges_from([(expected_note_node_name, given_note_node_name)])
      edge_labels[(expected_note_node_name, given_note_node_name)] = current_rel.cent_difference
      cent_difference_nodes.append(given_note_node_name)
    elif rel_type == RelationshipType.HARMONIC:
      G.add_edges_from([(expected_note_node_name, given_note_node_name)])
      edge_labels[(expected_note_node_name, given_note_node_name)] = f"{current_rel.harmonic_info[0]}. harmonic"
      harmonic_nodes.append(given_note_node_name)
    elif rel_type == RelationshipType.UNRELATED:
      unrelated_nodes.append(given_note_node_name)

def group_isolated_expected_nodes():
  for node in list(nx.isolates(G)):
    if node[0] != " ":
      expected_with_no_pair_nodes.append(node)

# Grouping the nodes to do their coloring
expected_nodes = []
perfect_match_nodes = []
cent_difference_nodes = []
harmonic_nodes = []
unrelated_nodes = []
expected_with_no_pair_nodes = []

fig, ax = plt.subplots()

# Initialize graph
G = nx.Graph()

# ----- Just putting this here to test the graph -----
# expected_notes = [m21.pitch.Pitch('c4'), m21.pitch.Pitch('e4'), m21.pitch.Pitch('g4')]
# given_notes = [m21.pitch.Pitch('c4'), m21.pitch.Pitch('e4'), m21.pitch.Pitch('c5')]
expected_notes = [m21.pitch.Pitch('c4'), m21.pitch.Pitch('e4'), m21.pitch.Pitch('g4'),
                  m21.pitch.Pitch('a3'), m21.pitch.Pitch('b2'), m21.pitch.Pitch('d1'),
                  m21.pitch.Pitch('d--1'), m21.pitch.Pitch('c#3'), m21.pitch.Pitch('c#4')]
given_notes = [m21.pitch.Pitch('c4'), m21.pitch.Pitch('e4'), m21.pitch.Pitch('g4'),
               m21.pitch.Pitch('d-3'), m21.pitch.Pitch('d1'),
               m21.pitch.Pitch('e2')]

rel_matrix = get_relationship_matrix(expected_notes, given_notes)
print("------------------------------")
rel_points_matrix = get_relationship_points(rel_matrix)
print("------------------------------")
scenarios = get_scenarios(rel_matrix, rel_points_matrix)
# ----------------------------------------------------

add_nodes(expected_notes, given_notes)



group_expected_nodes(expected_notes)

# Grouping nodes with edge creation
scenario = get_best_scenario(scenarios)

edge_labels = {}

group_related_nodes_with_edge_creation(scenario) # TODO: Get scenario

group_isolated_expected_nodes()

# Need to create a layout when doing
# separate calls to draw nodes and edges
pos = nx.get_node_attributes(G,'pos')

nx.draw_networkx_nodes(G, pos, nodelist=expected_nodes, node_color="tab:blue", node_size = 500)
nx.draw_networkx_nodes(G, pos, nodelist=expected_with_no_pair_nodes, node_color="gray", node_size = 500)
nx.draw_networkx_nodes(G, pos, nodelist=perfect_match_nodes, node_color="tab:green", node_size = 500)
nx.draw_networkx_nodes(G, pos, nodelist=cent_difference_nodes, node_color="tab:olive", node_size = 500)
nx.draw_networkx_nodes(G, pos, nodelist=harmonic_nodes, node_color="tab:purple", node_size = 500)
nx.draw_networkx_nodes(G, pos, nodelist=unrelated_nodes, node_color="tab:red", node_size = 500)

nx.draw_networkx_labels(G, pos)

nx.draw_networkx_edges(G, pos, edgelist=G.edges(), arrows=False)

nx.draw_networkx_edge_labels(
    G, pos,
    edge_labels=edge_labels,
    label_pos = 0.25,
    font_color='tab:purple'
)

ax.axis("off")
plt.show()