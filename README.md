# tax2graph

![Glomerellales graph](https://github.com/sgelias/tax2graph/blob/master/tax2graph/data/glomerellales-graph.png)

## Goal

`tax2graph` provide a simple way to convert i4Life tabled taxonomy to Neo4J graph representation.

## Example data

A example data are available on data folder. It contains the Sordariomycetes taxonomy downloaded from "i4Life WP4 Download Service of the Catalogue of Life:
Darwin Core Archive Export" (see http://www.catalogueoflife.org/DCA_Export/).

## Usage

Initialize a connection dict containing at last the password key to perform queries to Neo4J database:

```python

import os
from tax2graph import GraphBuilder, ConnectionType

connection_variables: ConnectionType = {
    "password": str(os.getenv('NEO_PASSWORD'))
}

builder = GraphBuilder(connection_variables)

```

And build the graph from Sordariomycetes tab-separated file:

```python

builder.read('tax2graph/data/sordariomycetes/taxa.txt', low_memory=False)

builder.build_col_graph()

```

The second parameter (low_memoty) is optional and is the same of `pandas.read_csv()` (see details in https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_csv.html).

After load the base taxonomy, the Manager class can be used to perform queries. To perform simple queries use:

```python

from tax2graph import Manager

manager = Manager(connection_variables)

manager.get_node('Glomerellales')

manager.get_parent('Glomerellales')

```

In the above code the constructor of Manager class require the 'connection_variables' to be started, like GraphBuilder class. After started both methods `get_node` and `get_parent` are called. Both receives a simgle parameter as string indicating the name of the Node to search. The former return an dict containing the target (e.g. order Glomerellales) node and the last return the parent node (e.g. class Sordariomycetes).

The manager class also contain a single method to create custom nodes. To this, simpleously use `set_custom_node`, as example:

```python

from tax2graph import CustomNodeType

custom_node: CustomNodeType = {
    'taxonRank': 'species',
    'description': 'A custom clade'
}

manager.set_custom_node(custom_node, 'Colletotrichum')

```

This method receive two parameters: the first is a dict of CustomNodeType type that contains two keys, as `taxonRank` and `description`; and the second is a string indicating the parent node in with the *custom_node* will be connected.

You can also include properties to relationships. To do, simpleously create an instance of CustomRelPropertiesType and include an additional parameter as the third argument of `set_custom_node` method.

```python

from datetime import datetime
from tax2graph import CustomRelPropertiesType

relationship_properties: CustomRelPropertiesType = {
    'created': datetime.now()
}

manager.set_custom_node(custom_node, 'Colletotrichum', relationship_properties)

```

---

Feel free to add new features and contribute through pull requests. Be happy!!
