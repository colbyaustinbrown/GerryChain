import sys
import networkx
import pandas as pd
import geopandas as gp


def get_list_of_data(filepath, col_name):
    '''Pull a column data from a shape or CSV file.

    :param filepath: The path to where your data is located.
    :param col_name: The column of data you want to grab.
    :returns: List of specified data.

    '''
    # Checks if you have inputed a csv or shp file then captures the data
    if filepath.split('.')[-1] == 'csv':
        df = pd.read_csv(filepath)
        data = df[col_name]
        return data.tolist()
    if filepath.split('.')[-1] == 'shp':
        df = gp.read_file(filepath)
        data = df[col_name]
        return list(data)


def add_data_to_graph(data, graph, data_name):
    '''Add a list of data to graph nodes.

    :data: A column with the data you would like to add to the nodes(VTDs).
    :graph: The graph you constructed and want to run chain on.
    :data_name: Field name to use for data in nodes.
    :returns: Nothing.

    '''
    # Check to make sure threre is a one-to-one between data and VTDs
    if len(graph) != len(data):
        print("Your column length doesn't match the number of nodes!")
        sys.exit(1)

    # Adding data to the nodes
    for i, j in enumerate(graph.nodes()):
        graph.nodes[i][data_name] = your_data[i]


def construct_graph(lists_of_neighbors, lists_of_perims, geoid):
    '''Construct initial graph from neighbor and perimeter information.

    :lists_of_neighbors: A list of lists stating the neighbors of each VTD.
    :lists_of_perims: List of lists of perimeters.
    :district_list: List of congressional districts associated to each node(VTD).
    :returns: Networkx Graph.

    The three arguments can be built from shape files with :func:`.ingest`.

    '''
    graph = networkx.Graph()

    # Creating the graph itself
    for vtd, list_nbs in enumerate(lists_of_neighbors):
        for d in list_nbs:
            graph.add_edge(vtd, d)

    # Add perims to edges
    for i, nbs in enumerate(lists_of_neighbors):
        for x, nb in enumerate(nbs):
            graph.add_edge(i, nb, perim=lists_of_perims[i][x])

    # Add districts to each node(VTD)
    for i, j in enumerate(graph.nodes()):
        graph.nodes[j]['GEOID'] = geoid[i]

    return graph
