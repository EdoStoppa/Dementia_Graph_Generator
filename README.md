# *Dementia Graph Generator*
Simple collection of scripts that, starting from multiple csv files, generate a graph representing all the Dementia Features of each patient

## Feature Categories and Subcategories
In this section is described the categories and subcategories structure of every graph. It must be noted that if more categories/subcategories are at the same level and do not have any other sub level they are simply listed separated by a comma. All the feature names are omitted for brevity.
- Acoustic
  - Energy
  - MFCC
    - MFCC1, MFCC2, ..., MFCC13
- Anagraphic
- Discourse-Based
  - General_Discourse-Based
  - Relations
    - Attribution, Background, Cause, Comparison, Condition, Contrast, Elaboration, Enablement, Evaluation, Explanation, Joint, Manner-Means, Same-Unit, Summary, Temporal, TextualOrganization, Topic-Change, Topic-Comment
- Lexical
  - Pos Count
    - Counts, Pos Ratios, Indexes
  - Summary Stats
  - Others
    - Pos Other Ratios, Pos Embeddings
- Syntactic
  - L2SCA
  - Tree Based
    - Tree_General, Parent_Child_Count, Tree_Auxiliaries
  - CFG
- Psycholinguistic
  - Abstract, Factual
- Spatial
  - Halves
    - Left, Right
  - Stripes
    - Far Left, Far Right, Center Left, Center Right
  - Quadrants
    - Nord-West, Nord-East, South-West, South-East

## Graph Types
We can see 2 type of graphs:

#### -> Star-like structure
For each patient we have a single central node from which different features categories branch. The leaf nodes represents the numerical features (one node -> one feature). We have 2 version of this type:
- `Single Name Nodes`: Each node in the graph will be categorized by a single label (be it a feature or a feature category)
- `Double Name Nodes`: Each node in the graph will be categorized by two labels, the first expressing the node type (feature or category), and the second represening the name of the node itself (for a category could be *"Acoustic"*, for a feature could be similar to *"NumDeterminers"*)

#### -> Puppeter-like structure
In this type of graph we have the structure of all feature category generated only once for all the patients, with the feature nodes completely empty. These nodes simply will identify the numerical features, but will not hold any value. This is because, each patient is represented by a node, and that node is directly connected to all the feature nodes. The actual numerical value of each feature is expressed in the weight of the patient-feature relation. So, we can imagine each patient as a puppeter that is connected to the entire categor-feature structure through weighted relationships. We have only one version of this type: `Features on Relationships`

## Prerequisites
### Python Libraries
```
pandas
py2neo
```
### Data
Simply have a folder that contains all the csv files extracted using my other project [Dementia Features Extractor](https://github.com/EdoStoppa/Dementia_Features_Extractor)

### Neo4j
Neo4j must be installed (no matter the version), and a database must be instantiated and run.

## How to Run
After having decided the desiderd graph type, simply run:<br />
`python GRAPH_TYPE_FOLDER/run.py -url XXXXXXX -user XXXXXXX -pwd XXXXXXX -data_path XXXXXX `<br /><br />
Where:
- *GRAPH_TYPE_FOLDER* = folder of one of the 3 graphs types in the project
- *url* = url provided by the Neo4j database instance
- *user* = username used to access the Neo4j database
- *pwd* = password used to access the Neo4j database
- *data_path* = path to the folder containing all the csv files obtained from [Dementia Features Extractor](https://github.com/EdoStoppa/Dementia_Features_Extractor)

