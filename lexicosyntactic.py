import pandas as pd
from py2neo import Graph, Node, Relationship, Subgraph
import util as u

def create_sub_node_and_rel(graph: Graph, name: str, father: Node) -> Node:
    sub = Node(name)
    sub_rel = Relationship(father, 'SUB_CATEGORY', sub)
    graph.create(Subgraph([sub], [sub_rel]))

    return sub

def add_lexical_features(graph: Graph, lex: Node, row) -> None:
    # ******** POS FEATURES ********
    pos_count = create_sub_node_and_rel(graph, 'Pos_Count', lex)

    feat_names = ['NumNouns', 'NumVerbs', 'NumAdverbs', 'NumAdjectives',
                    'NumDeterminers', 'NumInterjections', 'NumInflectedVerbs',
                    'NumCoordinateConjunctions', 'NumSubordinateConjunctions']
    u.add_cat_feat(graph, pos_count, row, feat_names, 'Counts')

    feat_names = ['RatioNoun', 'RatioVerb', 'RatioPronoun', 'RatioCoordinate']
    u.add_cat_feat(graph, pos_count, row, feat_names, 'Pos_Ratios')

    feat_names = ['TTR', 'MATTR', 'BrunetIndex', 'HonoreStatistic']
    u.add_cat_feat(graph, pos_count, row, feat_names, 'Indexes')

    # ******** SUMMARY STATS ********
    feat_names = ['NumberOfNID', 'MeanWordLength', 'TotalNumberOfWords', 'DisfluencyFrequency']
    u.add_cat_feat(graph, lex, row, feat_names, 'Summary_Stats')

    # ******** OTHERS *********
    pos_others = create_sub_node_and_rel(graph, 'Pos_Others', lex)

    feat_names = ['NPTypeRate', 'VPTypeRate', 'PPTypeRate', 'PProportion',
                    'NPProportion', 'VPProportion']
    u.add_cat_feat(graph, pos_others, row, feat_names, 'Pos_Other_Ratios')

    feat_names = ['AvgNPTypeLengthEmbedded', 'AvgVPTypeLengthEmbedded',
                    'AvgPPTypeLengthEmbedded', 'AvgPPTypeLengthNonEmbedded', 
                    'AvgNPTypeLengthNonEmbedded', 'AvgVPTypeLengthNonEmbedded']
    u.add_cat_feat(graph, pos_others, row, feat_names, 'Pos_Embeddings')

def add_syntactic_features(graph: Graph, syn: Node, row) -> None:
    # ******** L2SCA ********
    feat_names = ['W', 'S', 'VP', 'C', 'T', 'DC', 'CT', 'CP', 'CN', 'MLS',
                  'MLT', 'MLC', 'C_S', 'VP_T', 'C_T', 'DC_C', 'DC_T', 'T_S',
                  'CT_T', 'CP_T', 'CP_C', 'CN_T', 'CN_C']
    u.add_cat_feat(graph, syn, row, feat_names, 'L2SCA')

    # ******** TREE BASED ********
    tree_based = create_sub_node_and_rel(graph, 'Tree_Based', syn)

    feat_names = ['tree_height']
    u.add_cat_feat(graph, tree_based, row, feat_names, 'Tree_General')

    feat_names = ['NP_to_PRP', 'ADVP_to_RB', 'NP_to_DT_NN', 'VP_to_VBG',
                  'VP_to_VBG_PP', 'VP_to_VBD_NP', 'INTJ_to_UH', 'ROOT_to_FRAG']
    u.add_cat_feat(graph, tree_based, row, feat_names, 'Parent_Child_Count')

    feat_names = ['VP_to_AUX_VP', 'VP_to_AUX_ADJP', 'VP_to_AUX']
    u.add_cat_feat(graph, tree_based, row, feat_names, 'Tree_Auxiliaries')

    # ******** CONTEXT FREE GRAMMAR *********
    feat_names = ['ADJP', 'ADVP', 'CONJP', 'FRAG', 'INTJ', 'LST', 'NAC', 'NP',
                  'NX', 'PP', 'PRN', 'PRT', 'QP', 'RRC', 'UCP', 'WHADJP', 'WHAVP',
                  'WHNP', 'WHPP', 'X']
    u.add_cat_feat(graph, syn, row, feat_names, 'CFG')


def add_lexicosyntactic(graph: Graph, data_path: str) -> None:
    # Load data into pandas
    data = pd.read_csv(data_path)
    # Get the columns names
    attributes = list(data.columns)[1:]
    
    for index, row in data.iterrows():
        print(f"    Working on {row['id']}...")
        # Get the patient node
        patient = u.get_patient_node(graph, row['id'])
        if patient is None: continue
        
        # ******** LEXICAL ********
        lex = Node('Lexical')
        graph.create(Relationship(patient, 'BASIC_CATEGORY', lex))
        add_lexical_features(graph, lex, row)

        # ******** SYNTACTIC ********
        syn = Node('Syntactic')
        graph.create(Relationship(patient, 'BASIC_CATEGORY', syn))
        add_syntactic_features(graph, syn, row)
        

    return