import pandas as pd
from py2neo import Graph, Node, Relationship, Subgraph
import util as u

def add_psycholinguistic(graph: Graph, data_path: str) -> None:
    # Load data into pandas
    data = pd.read_csv(data_path)
    # Get the columns names
    attributes = list(data.columns)[1:]
    
    for index, row in data.iterrows():
        # Printing progress bar
        u.printProgressBar(index+1, len(data), bar_size=40)

        # Get the patient node
        patient = u.get_patient_node(graph, row['id'])
        if patient is None: continue

        # Create a new CATEGORY node and BASE relationship
        psycho = Node(*['Feature_Type', 'Psycholinguistic'])
        psycho_rel = Relationship(patient, 'BASIC_CATEGORY', psycho)

        # Add the node and relationship between patient and category
        graph.create(Subgraph([psycho], [psycho_rel]))

        # Add all the energy features in the graph
        attrs = [attributes[0], attributes[1], attributes[2], attributes[5]]
        u.add_cat_feat(graph, psycho, row, attrs, 'Abstract')

        # Add all the MFCC features in the graph
        attrs = [attributes[3], attributes[4]]
        u.add_cat_feat(graph, psycho, row, attrs, 'Factual')
