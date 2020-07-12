# tax2graph
## Goal

A simple way to convert i4Life tabled taxonomy to Neo4J graph representation.

## Example data

A example data are available on data folder. It contains the Sordariomycetes taxonomy downloaded from "i4Life WP4 Download Service of the Catalogue of Life:
Darwin Core Archive Export".

## Usage

As example set the path to taxa.txt file available in sordariomycetes filder. To this run:
''''python

path = 'data/sordariomycetes/taxa.txt'

''''

Now, initialize a connection dict containing at last the password to perform queries to Neo4J database:

''''python

from tax2graph import ConnectionType

connection_variables: ConnectionType = {
    "password": str(os.getenv('NEO_PASSWORD'))
}

parser = GraphParser(connection_variables)

''''

And build the graph from Sordariomycetes:
''''python

parser.build_col_graph()

''''

To perform simple queries use:
''''python

parser.get_node('Glomerellales')

parser.get_parent('Glomerellales')

''''

The former code get the Glomerellales node, and the further get the first parent node (Sordariomycetes).

To create custom nodes simple run:
''''python

from tax2graph import CustomNodeType

custom_node: CustomNodeType = {
    'taxonRank': 'species',
    'description': 'A custom clade 4'
}
parser.set_custom_node(custom_node, 'Colletotrichum')

''''

Feel free to add new features and contribute through pull requests. Be happy!!
