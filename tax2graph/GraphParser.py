import os
from math import isnan

import numpy as np
import pandas as pd
import py2neo
from py2neo import Graph, Node, Relationship


class GraphParser:


    def __init__(self, file_path):

        if not os.path.exists(file_path):
            raise OSError('Invalid file path! Please verify')
        
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
    

    def build_graph(self):
        """
        Create all records before create reoationships.
        """
        graph = self.__connect()
        tx = graph.begin()
    
        nodes = {}
        for item in self.__clear_dict:
            nodes[item['taxonID']] = Node('Taxon', **item)
            nodes[item['taxonID']].add_label(str(item['scientificName']))
            nodes[item['taxonID']].__primarylabel__ = str(item['scientificName'])
            nodes[item['taxonID']].__primarykey__ = str(item['taxonID'])
            tx.create(nodes[item['taxonID']])

        for index, node in nodes.items():
            if 'parentNameUsageID' in node:
                relationship = Relationship(
                    node, 'PARENT', nodes[int(node['parentNameUsageID'])])
                
                tx.merge(relationship)
        
        tx.commit()
    

    def get_all_child(self):
        """
        Get all child nodes of desired node.
        """

        graph = self.__connect()

        return graph.run("MATCH (n) WHERE size((n)--()) > 0 RETURN n")

    
    def get_clear_dict(self):
        """
        Returns a dict containing imported table.
        """

        return self.__clear_dict


if __name__ == '__main__':

    path = 'data/glomerellales/taxa.txt'
    parser = GraphParser(path)
    parser.build_graph()
    #parser.get_all_child()
