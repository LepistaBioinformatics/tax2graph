import os
from typing import Any, Dict, List, Optional, TypedDict

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


class ConnectionType(TypedDict, total=False):
    """
    Define the initial structure of connectio dict. Observe that only the
    'password' are not defined, thus it is the unique obligate key to be
    provided on class initialization.
    """

    auth: Optional[str]
    host: Optional[str]
    password: str
    port: Optional[int]
    scheme: Optional[str]
    secure: Optional[str]
    user: Optional[str]
    user_agent: Optional[str]
    max_connections: Optional[str]


class GraphParser:


    class PARENT(Relationship):
        """
        Define a custom class for PARENT relationship's.
        """
        pass

    
    def __init__(self, connection_variables: ConnectionType):
        """
        Initialization requires at lats that the password key would be defined.
        it allows to connnect to localhost. For connections woth non-local
        hosts, aditional keypairs would be defined.
        """
        
        if not connection_variables['password']:
            raise OSError('Define at last password to start the class.')

        self.connection_variables = connection_variables


    def __validate_and_connect(self) -> Graph:
        """
        Connect to local database.
        """

        connection_variables = {
            k: v for k, v in self.connection_variables.items() if v is not None
        }
        
        return Graph(**connection_variables)


    def read(self, file_path: str) -> None:
        """
        Read the tab separated file and return a dict.
        """

        if not os.path.exists(file_path):
            raise OSError('Invalid file path! Please verify.')

        df = pd \
            .read_csv(file_path, sep='\t', header=0) \
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

        graph = self.__validate_and_connect()
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
    

    def get_table_as_dict(self) -> List[Dict[Any, Any]]:
        """
        Returns a dict containing imported table.
        """

        return self.__clear_dict
    

    def __remove_keys(self, dict_item: Dict[str, Any], keys: List[str]) -> Dict:
        """
        Remove keys from dict.
        """

        return { x: dict_item[x] for x in dict_item if x not in keys }


    def get_node(self, term: str) -> Dict:
        """
        Serch the parent of a specified node.
        """

        graph = self.__validate_and_connect()

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

        graph = self.__validate_and_connect()

        query = graph \
            .run("MATCH (t {scientificName:$term})-[r:PARENT]->(p) \
                    RETURN p", 
                term=term)

        return query.evaluate()
    

    def set_custom_node(self, custom_node: CustomNodeType, parent_name: str) -> None:
        """
        Set a custom node. Require a parent node to create a relationship with.
        """

        parent_node: Dict[Any, Any] = self.get_node(parent_name)

        if not parent_node:
            raise ValueError('Parent not exits.')

        graph = self.__validate_and_connect()
        tx = graph.begin()

        node = Node(custom_node['taxonRank'], **custom_node)
        node.add_label('Custom')
        tx.create(node)
        relationship = self.PARENT(node, parent_node)
        tx.merge(relationship)        
        tx.commit()
