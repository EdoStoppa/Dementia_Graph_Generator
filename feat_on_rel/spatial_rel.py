import pandas as pd
from py2neo import Graph, Node, Relationship, Subgraph
import util_rel as u

def add_sub_category_struct(graph: Graph, spatial: Node, attributes, name, attr_names, base, feat_dict: dict):
    # Work on the new sub node and sub relation
    sub = Node(*['Category', name])
    sub_rel = Relationship(spatial, 'SUB_CATEGORY', sub)
    graph.create(Subgraph([sub], [sub_rel]))

    # Add all the features
    idx = base
    for attr_name in attr_names:
        u.add_cat_feat(graph, sub, attributes[idx:idx+4], attr_name, feat_dict)
        idx += 4

def add_spatial(graph: Graph, data_path: str) -> None:
    # Load data into pandas
    data = pd.read_csv(data_path)
    # Get the columns names
    feat_names = list(data.columns)[1:]

    # Create a new CATEGORY node and BASE relationship
    spatial = Node(*['Feature_Type', 'Spatial'])

    # Add the base node
    graph.create(spatial)

    # Dictionary containing all feature nodes
    feat_dict = {}

    # Work on the HALVES category
    name = 'Halves'
    cat_names = ['Left', 'Right']
    add_sub_category_struct(graph, spatial, feat_names, name, cat_names, 0, feat_dict)

    # Work on the STRIPES category
    name = 'Stripes'
    cat_names = ['Far_Left', 'Center_Left', 'Far_Right', 'Center_Right']
    add_sub_category_struct(graph, spatial, feat_names, name, cat_names, 8, feat_dict)

    # Work on the QUADRANTS category
    name = 'Quadrants'
    cat_names = ['Nord_West', 'Nord_East', 'South_East', 'South_West']
    add_sub_category_struct(graph, spatial, feat_names, name, cat_names, 24, feat_dict)
    
    rels = []
    for index, row in data.iterrows():
        print(f"    Working on {row['id']}...")

        # Get the patient node
        patient = u.get_patient_node(graph, row['id'])
        if patient is None: continue

        # Add the base relation patient -> feature type
        rels.append(Relationship(patient, 'FEATURE_TYPE', spatial))

        for feat in feat_names:
            rels.append(Relationship(patient, 'VALUE', feat_dict[feat], **{'value': row[feat]}))
        
    # Add the feature relationships
    graph.create(Subgraph(relationships=rels))