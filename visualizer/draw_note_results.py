import networkx as nx
import matplotlib.pyplot as plt
from metrics.notes.evaluate_notes import *
from metrics.notes.note_relationship_type import NoteRelationshipType

expected_nodes = []
perfect_match_nodes = []
cent_difference_nodes = []
harmonic_nodes = []
unrelated_nodes = []
expected_with_no_pair_nodes = []
edge_labels = {}

NODE_SIZE = 750
FONT_SIZE = 9

def add_nodes(graph, expected_notes, given_notes):
  for i in range(len(expected_notes)):
    node_name = get_node_name(i, expected_notes[i])
    graph.add_node(node_name, pos = (1, len(expected_notes) - i))

  for i in range(len(given_notes)):
    node_name = get_node_name(i, given_notes[i], True)
    graph.add_node(node_name, pos = (2, len(given_notes) - i))

def get_node_name(index, note, given = False):
  if given:
    # Inserting a space to the front and back to differentiate from expected nodes
    node_name = f" ({index}) {note.nameWithOctave} "
  else:
    node_name = f"({index}) {note.nameWithOctave}"
  cent_difference = note.microtone.cents
  if cent_difference != 0:
    node_name += "(" + str(cent_difference) + ")"
  return node_name

def group_expected_nodes(expected_notes):
  for i in range(len(expected_notes)):
    node_name = get_node_name(i, expected_notes[i])
    expected_nodes.append(node_name)

def group_related_nodes_with_edge_creation(graph, expected_notes, scenario):
  for i in range(len(scenario)):
    current_rel = scenario[i]
    rel_type = current_rel.type
    expected_note = scenario[i].expected_note
    exp_index = get_expected_node_index(expected_note, expected_notes) 
    giv_index = i
    given_note_node_name = get_node_name(giv_index, scenario[i].given_note, True)
    expected_note_node_name = get_node_name(exp_index, scenario[i].expected_note)
    if rel_type == NoteRelationshipType.PERFECT_MATCH:
      graph.add_edges_from([(expected_note_node_name, given_note_node_name)])
      perfect_match_nodes.append(given_note_node_name)
      #print("Perfect match edge", expected_note_node_name, given_note_node_name)
    elif rel_type == NoteRelationshipType.CENT_DIFFERENCE:
      graph.add_edges_from([(expected_note_node_name, given_note_node_name)])
      edge_labels[(expected_note_node_name, given_note_node_name)] = current_rel.cent_difference
      cent_difference_nodes.append(given_note_node_name)
      #print("Cent diff edge", expected_note_node_name, given_note_node_name)
    elif rel_type == NoteRelationshipType.HARMONIC:
      graph.add_edges_from([(expected_note_node_name, given_note_node_name)])
      edge_labels[(expected_note_node_name, given_note_node_name)] = f"{current_rel.harmonic_info[0]}. harmonic"
      harmonic_nodes.append(given_note_node_name)
      #print("Harmonic edge", expected_note_node_name, given_note_node_name)
    elif rel_type == NoteRelationshipType.UNRELATED:
      unrelated_nodes.append(given_note_node_name)
      #print("Unrelated, no edge", expected_note_node_name, given_note_node_name)

def get_expected_node_index(expected_note, expected_notes):
  return expected_notes.index(expected_note)

def get_given_node_index(given_note, given_notes):
  return given_notes.index(given_note)

def group_isolated_expected_nodes(graph):
  for node in list(nx.isolates(graph)):
    if node[0] != " ":
      expected_with_no_pair_nodes.append(node)

def draw_graph(graph, ax):
  pos = nx.get_node_attributes(graph,'pos')
  nx.draw_networkx_nodes(graph, pos, nodelist=expected_nodes, node_color="tab:blue", node_size = NODE_SIZE)
  nx.draw_networkx_nodes(graph, pos, nodelist=expected_with_no_pair_nodes, node_color="gray", node_size = NODE_SIZE)
  nx.draw_networkx_nodes(graph, pos, nodelist=perfect_match_nodes, node_color="tab:green", node_size = NODE_SIZE)
  nx.draw_networkx_nodes(graph, pos, nodelist=cent_difference_nodes, node_color="tab:olive", node_size = NODE_SIZE)
  nx.draw_networkx_nodes(graph, pos, nodelist=harmonic_nodes, node_color="tab:purple", node_size = NODE_SIZE)
  nx.draw_networkx_nodes(graph, pos, nodelist=unrelated_nodes, node_color="tab:red", node_size = NODE_SIZE)
  nx.draw_networkx_labels(graph, pos, font_size = FONT_SIZE)
  nx.draw_networkx_edges(graph, pos, edgelist=graph.edges(), arrows=False)
  nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, label_pos = 0.25, font_color='tab:purple')
  ax.axis("off")
  plt.show()

