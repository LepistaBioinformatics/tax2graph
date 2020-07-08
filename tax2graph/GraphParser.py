import os
from math import isnan
from typing import Any, Dict, List, TypedDict

import numpy as np
import pandas as pd
import py2neo
from py2neo import Graph, Node, Relationship


class CustomNodeType(TypedDict):
        """
        Define a type for custom nodes.
        """

        taxonRank: str
        description: str


class GraphParser:


    class PARENT(Relationship): pass


    def __init__(self, file_path):

        if not os.path.exists(file_path):
            raise OSError('Invalid file path! Please verify.')
        
        self.__read(file_path)
    

    def __connect(self):
        """
        Connect to local database.
        """
        
        return Graph(password=os.getenv('NEO_PASSWORD'))


    def __read(self, file_path):
        """
        Read the tab separated file and return a dict.
        """

        df = pd \
            .read_csv(file_path, sep='\t', header=0) \
            .replace(np.nan, "None")
        
        self.__clear_dict = [
            { k: v for k, v in item.items() if v != "None" }
            for item in df.to_dict('records')
        ]

        for item in self.__clear_dict:
            if 'parentNameUsageID' in item:
                item['parentNameUsageID'] = int(item['parentNameUsageID'])
    

    def build_col_graph(self):
        """
        Create all records before create reoationships.
        """
        graph = self.__connect()
        tx = graph.begin()
    
        nodes = {}
        for item in self.__clear_dict:
            nodes[item['taxonID']] = Node(item['taxonRank'], **item)
            nodes[item['taxonID']].__primarylabel__ = 'taxonRank'
            nodes[item['taxonID']].__primarykey__ = 'taxonID'
            tx.create(nodes[item['taxonID']])

        for index, node in nodes.items():
            if 'parentNameUsageID' in node:
                relationship = self.PARENT(node, nodes[int(node['parentNameUsageID'])])
                tx.merge(relationship)
        
        tx.commit()
    

    def get_clear_dict(self):
        """
        Returns a dict containing imported table.
        """

        return self.__clear_dict
    

    def __remove_keys(self, dict_item: Dict[str, Any], keys: List[str]) -> Dict[str, Any]:
        """
        Remove keys from dict.
        """

        return { x: dict_item[x] for x in dict_item if x not in keys }


    def get_node(self, term: str) -> Dict:
        """
        Serch the parent of a specified node.
        """

        graph = self.__connect()

        query = graph \
            .run(
                "MATCH (t {scientificName:$term}) \
                    RETURN t", 
                term=term)

        return query.evaluate()
    

    def get_parent(self, term: str) -> Dict:
        """
        Serch the parent of a specified node.
        """

        graph = self.__connect()

        query = graph \
            .run("MATCH (t {scientificName:$term})-[r:PARENT]->(p) \
                    RETURN p", 
                term=term)

        return query.evaluate()
    

    def set_custom_node(self, term: CustomNodeType, parent: str) -> None:
        """
        Set a custom node. Require a parent node to create a relationship with.
        """

        parent = self.get_node(parent)

        if not parent:
            raise ValueError('Parent not exits.')

        graph = self.__connect()
        tx = graph.begin()

        node = Node(term['taxonRank'], **term)
        node.add_label('Custom')
        tx.create(node)
        relationship = self.PARENT(node, parent)
        tx.merge(relationship)
        tx.commit()


if __name__ == '__main__':

    path = 'data/sordariomycetes/taxa.txt'
    parser = GraphParser(path)
    #parser.build_col_graph()
    print(parser.get_node('Glomerellales'))
    print(parser.get_parent('Glomerellales'))

    """ custom_node: CustomNodeType = {
        'taxonRank': 'species',
        'description': 'A custom clade 3'
    }
    parser.set_custom_node(custom_node, 'Colletotrichum') """
