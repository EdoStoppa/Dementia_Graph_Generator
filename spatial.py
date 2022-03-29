import pandas as pd
from py2neo import Graph, Node, Relationship, Subgraph
import util as u

def add_sub_category(graph: Graph, spatial: Node, row, attributes, name, attr_names, base):
    # Work on the new sub node and sub relation
    sub = Node(name)
    sub_rel = Relationship(spatial, 'SUB_CATEGORY', sub)
    graph.create(Subgraph([sub], [sub_rel]))
    
    # Add all the features
    idx = base
    for attr_name in attr_names:
        u.add_new_cat(graph, sub, row, attributes[idx:idx+4], attr_name)
        idx += 4

def add_spatial(graph: Graph, data_path: str) -> None:
    # Load data into pandas
    data = pd.read_csv(data_path)
    # Get the columns names
    attributes = list(data.columns)[1:]
    
    for index, row in data.iterrows():
        print(f"    Working on {row['id']}...")

        # Get the patient node
        patient = u.get_patient_node(graph, row['id'])
        if patient is None: continue

        # Create a new CATEGORY node and BASE relationship
        spatial = Node('Spatial')
        spatial_rel = Relationship(patient, 'BASIC_CATEGORY', spatial)

        # Add the node and relationship between patient and category
        graph.create(Subgraph([spatial], [spatial_rel]))

        # Work on the HALVES category
        name = 'Halves'
        attr_names = ['Left', 'Right']
        add_sub_category(graph, spatial, row, attributes, name, attr_names, 0)

        # Work on the STRIPES category
        name = 'Stripes'
        attr_names = ['Far_Left', 'Center_Left', 'Far_Right', 'Center_Right']
        add_sub_category(graph, spatial, row, attributes, name, attr_names, 8)

        # Work on the QUADRANTS category
        name = 'Quadrants'
        attr_names = ['Nord_West', 'Nord_East', 'South_East', 'South_West']
        add_sub_category(graph, spatial, row, attributes, name, attr_names, 24)


    return