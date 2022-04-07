import argparse
import os, sys
import pandas as pd
from py2neo import Graph, Node, Subgraph

from acoustic import add_acoustic
from anagraphic import add_anagraphic
from discourse_based import add_discourse_based
from lexicosyntactic import add_lexicosyntactic
from psycholinguistic import add_psycholinguistic
from spatial import add_spatial


def add_patients(graph: Graph, data_path: str) -> None:
    # Load data into pandas
    data = pd.read_csv(data_path)
    # Get only the ids
    data = data['id']

    # Create all the patient nodes
    nodes = []
    for id in data:
        nodes.append(Node('Patient', name=id))
    
    # Load into graph database
    graph.create(Subgraph(nodes=nodes))

def main(args):
    base_data_path = args.data_path
    
    # Create the Graph connection
    print('\nTrying to connect to the database...')
    try:
        graph = Graph(args.url, auth=(args.user, args.pwd))
        print('Connection complete!')
    except:
        print('Something went wrong while connecting with your database.\nKilling the process...')
        sys.exit()


    # First add all patients
    print('\nAdding all the patient nodes...')
    add_patients(graph, os.path.join(base_data_path, 'acoustic_info.csv'))

    # Add all the anagraphic info
    print('\nAdding all the anagraphic info...')
    data_path = os.path.join(base_data_path, 'anagraphic_info.csv')
    add_anagraphic(graph, data_path)

    # Add all the acoustic info
    print('\nAdding all the acoustic info...')
    data_path = os.path.join(base_data_path, 'acoustic_info.csv')
    add_acoustic(graph, data_path)

    # Add all the discourse-based info
    print('\nAdding all the discourse-based info...')
    data_path = os.path.join(base_data_path, 'discourse_info.csv')
    add_discourse_based(graph, data_path)

    # Add all the lexicosyntactic info
    print('\nAdding all the lexicosyntactic info...')
    data_path = os.path.join(base_data_path, 'lexicosyntactic_info.csv')
    add_lexicosyntactic(graph, data_path)

    # Add all the psycholinguistic info
    print('\nAdding all the psycholinguistic info...')
    data_path = os.path.join(base_data_path, 'psycholinguistic_info.csv')
    add_psycholinguistic(graph, data_path)

    # Add all the spatial info
    print('\nAdding all the spatial info...')
    data_path = os.path.join(base_data_path, 'spatial_info.csv')
    add_spatial(graph, data_path)

    print('\nEverything complete!')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("url", nargs="?", help="Graph Database URL", type=str, default='bolt://localhost:7687')
    parser.add_argument("user", nargs="?", help="Username", type=str, default='neo4j')
    parser.add_argument("pwd", nargs="?", help="Password", type=str, default='password')
    parser.add_argument("data_path", nargs="?", help="Path to all the data in csv format", type=str, default='')

    args = parser.parse_args()
    args.data_path = os.path.join('..', 'dementia_feature_extraction', 'data', 'extracted')

    main(args)