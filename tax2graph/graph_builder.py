import os
from typing import Any, Dict, List, Optional, TypedDict

import numpy as np
import pandas as pd
import py2neo
from py2neo import Graph, Node, Relationship

from tax2graph.abstract_connection import Connection, ConnectionType


class PARENT(Relationship):
        """
        Define a custom class for PARENT relationship's.
        """

        pass


class GraphBuilder(Connection):


    def __init__(self, connection_variables: ConnectionType):
        """
        Initialization requires at lats that the password key would be defined.
        it allows to connnect to localhost. For connections woth non-local
        hosts, aditional keypairs would be defined.
        """
        
        if not connection_variables['password']:
            raise OSError('Define at last password to start the class.')

        self.connection_variables = connection_variables


    def read(self, file_path: str, low_memory: bool = True) -> None:
        """
        Read the tab separated file and return a dict.
        """

        if not os.path.exists(file_path):
            raise OSError('Invalid file path! Please verify.')

        df = pd \
            .read_csv(file_path, sep='\t', header=0, low_memory=low_memory) \
            .replace(np.nan, "None")
        
        self.__clear_dict: List[Dict[Any, Any]] = [
            { k: v for k, v in item.items() if v != "None" }
            for item in df.to_dict('records')
        ]

        for item in self.__clear_dict:
            if 'parentNameUsageID' in item:
                item['parentNameUsageID'] = int(item['parentNameUsageID'])
    

    def build_col_graph(self) -> None:
        """
        Create all records before create reoationships.
        """

        graph = self._validate_and_connect()
        tx = graph.begin()
    
        nodes = {}
        for item in self.__clear_dict:
            nodes[item['taxonID']] = Node(item['taxonRank'], **item)
            nodes[item['taxonID']].__primarylabel__ = 'taxonRank'
            nodes[item['taxonID']].__primarykey__ = 'taxonID'
            tx.create(nodes[item['taxonID']])

        for index, node in nodes.items():
            if 'parentNameUsageID' in node:
                relationship = PARENT(node, nodes[int(node['parentNameUsageID'])])
                tx.merge(relationship)
        
        tx.commit()
    

    def get_table_as_dict(self) -> List[Dict[Any, Any]]:
        """
        Returns a dict containing imported table.
        """

        return self.__clear_dict
