from uuid import UUID
from datetime import datetime
from typing import Any, Dict, NewType, Optional, TypedDict

from py2neo import Node, Graph

from tax2graph.abstract_connection import Connection, ConnectionType
from tax2graph.graph_builder import PARENT


Datetime = NewType('Datetime', datetime)
Uuid = NewType('Uuid', UUID)


class CustomNodeType(TypedDict):
    """
    Define a type for custom nodes.
    """

    taxonRank: str
    description: str
    node_description_id: Uuid


class UserType(TypedDict):
    """
    Define the basic type for user.
    """

    user_id: Uuid
    name: str


class CustomRelPropertiesType(TypedDict, total=False):
    """
    Define the basic properties that a custom relationship would include.
    """

    created: Optional[Datetime]
    updated: Optional[Datetime]
    user: Optional[UserType]


class Manager(Connection):

    
    def __init__(self, connection_variables: ConnectionType):
        """
        Initialization requires at lats that the password key would be defined.
        it allows to connnect to localhost. For connections woth non-local
        hosts, aditional keypairs would be defined.
        """
        
        if not connection_variables['password']:
            raise OSError('Define at last password to start the class.')

        self.connection_variables = connection_variables


    def get_node(self, term: str) -> Dict:
        """
        Serch the parent of a specified node.
        """

        graph = self._validate_and_connect()

        query = graph \
            .run("MATCH (t {scientificName:$term}) \
                    RETURN t", 
                term=term)

        return query.evaluate()
    

    def get_parent(self, term: str) -> Dict:
        """
        Serch the parent of a specified node.
        """

        graph = self._validate_and_connect()

        query = graph \
            .run("MATCH (t {scientificName:$term})-[r:PARENT]->(p) \
                    RETURN p", 
                term=term)

        return query.evaluate()


    def set_custom_node(self, 
        custom_node: CustomNodeType, 
        parent_name: str,
        relationship_properties: CustomRelPropertiesType = None
    ) -> Node:
        """
        Set a custom node. Require a parent node to create a relationship with.
        """

        parent_node: Graph = self.get_node(parent_name)

        if not parent_node:
            raise ValueError('Parent not exits.')

        graph = self._validate_and_connect()
        tx = graph.begin()

        node = Node(custom_node['taxonRank'], **custom_node)
        node.add_label('custom')
        tx.create(node)
        
        if relationship_properties:
            relationship = PARENT(node, parent_node, **relationship_properties)
        else:
            relationship = PARENT(node, parent_node)
        
        tx.merge(relationship)        
        tx.commit()

        return node
