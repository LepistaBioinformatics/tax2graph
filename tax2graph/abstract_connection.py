from abc import ABC, abstractmethod, abstractproperty
from typing import Optional, TypedDict

from py2neo import Graph


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


class Connection(ABC):


    connection_variables: ConnectionType


    def _validate_and_connect(self) -> Graph:
        """
        Connect to local database.
        """

        connection_variables = {
            k: v for k, v in self.connection_variables.items() if v is not None
        }
        
        return Graph(**connection_variables)
