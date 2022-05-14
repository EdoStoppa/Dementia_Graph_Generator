import pandas as pd
from py2neo import Graph, Node, Relationship, Subgraph
import util as u

def add_anagraphic(graph: Graph, data_path: str) -> None:
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

        # Create a new CATEGORY node
        anagraphic = Node(*['Feature_Type', 'Anagraphic'])

        # Add the relationship between patient and category
        graph.create(Relationship(patient, 'BASIC_CATEGORY', anagraphic))
        
        nodes, relationships = [], []
        for attribute in attributes:
            node = Node(*['Feature', attribute], **{'value': row[attribute]})
            nodes.append(node)
            rel = Relationship(anagraphic, 'IS', node)
            relationships.append(rel)
        
        graph.create(Subgraph(nodes, relationships))
