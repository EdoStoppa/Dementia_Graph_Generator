import pandas as pd
from py2neo import Graph, Node, Relationship, Subgraph
import util as u

def add_energy(graph: Graph, acoustic: Node, row, attributes: list) -> None:
    nodes, rels = [], []

    energy = Node('Energy')
    nodes.append(energy)
    rels.append(Relationship(acoustic, 'SUB_CATEGORY', energy))

    attrs = [attributes[:4], attributes[4:8], attributes[8:]]
    names = ['Energy_Basic', 'Energy_Velocity', 'Energy_Acceleration']

    for attr, name in zip(attrs, names):
        # Create node for section of basic feature
        new_node = Node(name)
        nodes.append(new_node)

        # Create relation between master node and new subnode
        rels.append(Relationship(energy, 'SUB_CATEGORY', new_node))

        # Create feature nodes and relationships
        n, r = u.one_to_features(attr, row, new_node)
        nodes += n
        rels += r

    graph.create(Subgraph(nodes, rels))

    return

def add_mfcc(graph: Graph, acoustic: Node, row, attributes: list) -> None:
    nodes, rels = [], []

    # Create general sub category of MFCC
    mfcc = Node('MFCC')
    nodes.append(mfcc)
    rels.append(Relationship(acoustic, 'SUB_CATEGORY', mfcc))

    # Add kurtosis for general MFCC
    mfcc_kurt = Node('Feature', *{attributes[-1]: row[attributes[-1]]})
    nodes.append(mfcc_kurt)
    rels.append(Relationship(mfcc, 'IS', mfcc_kurt))
    # Add skew for general MFCC
    mfcc_skew = Node('Feature', *{attributes[-2]: row[attributes[-2]]})
    nodes.append(mfcc_skew)
    rels.append(Relationship(mfcc, 'IS', mfcc_skew))

    attributes = attributes[:-2]
    for idx in range(1, 14):
        mfcc_num = Node(f'MFCC{idx}')
        nodes.append(mfcc_num)
        rels.append(Relationship(mfcc, 'SUB_CATEGORY', mfcc_num))

        _idx = (idx-1)*12
        attrs = [attributes[_idx:4+_idx], attributes[4+_idx:8+_idx], attributes[8+_idx:12+_idx]]
        names = [f'MFCC{idx}_base', f'MFCC{idx}_vel', f'MFCC{idx}_acc']

        for attr, name in zip(attrs, names):
            # Create node for section of basic feature
            new_node = Node(name)
            nodes.append(new_node)

            # Create relation between master node and new subnode
            rels.append(Relationship(mfcc_num, 'SUB_CATEGORY', new_node))

            # Create feature nodes and relationships
            n, r = u.one_to_features(attr, row, new_node)
            nodes += n
            rels += r

    graph.create(Subgraph(nodes, rels))

    return

def add_acoustic(graph: Graph, data_path: str) -> None:
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
        acoustic = Node('Acoustic')
        acoustic_rel = Relationship(patient, 'BASIC_CATEGORY', acoustic)

        # Add the node and relationship between patient and category
        graph.create(Subgraph([acoustic], [acoustic_rel]))

        # Add all the energy features in the graph
        add_energy(graph, acoustic, row, attributes[:12])

        # Add all the MFCC features in the graph
        add_mfcc(graph, acoustic, row, attributes[12:])
        
    return