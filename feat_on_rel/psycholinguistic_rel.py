import pandas as pd
from py2neo import Graph, Node, Relationship, Subgraph
import util_rel as u

def add_psycholinguistic(graph: Graph, data_path: str) -> None:
    # Load data into pandas
    data = pd.read_csv(data_path)
    # Get the columns names
    attributes = list(data.columns)[1:]

    # Create a new CATEGORY node and BASE relationship
    psycho = Node(*['Feature_Type', 'Psycholinguistic'])

    # Add the base node
    graph.create(psycho)

    # Dictionary containing all feature nodes
    feat_dict = {}

    # Add all the energy features in the graph (only structure)
    attrs = [attributes[0], attributes[1], attributes[2], attributes[5]]
    u.add_cat_feat(graph, psycho, attrs, 'Abstract', feat_dict)

    # Add all the MFCC features in the graph (only structure)
    attrs = [attributes[3], attributes[4]]
    u.add_cat_feat(graph, psycho, attrs, 'Factual', feat_dict)

    rels = []
    for index, row in data.iterrows():
        print(f"    Working on {row['id']}...")

        # Get the patient node
        patient = u.get_patient_node(graph, row['id'])
        if patient is None: continue

        # Add the base relation patient -> feature type
        rels.append(Relationship(patient, 'FEATURE_TYPE', psycho))
        
        for feat in attributes:
            rels.append(Relationship(patient, 'VALUE', feat_dict[feat], **{'value': row[feat]}))
        
    # Add the feature relationships
    graph.create(Subgraph(relationships=rels))
