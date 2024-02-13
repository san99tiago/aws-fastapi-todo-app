from enum import Enum
from typing import Optional


class JSONSchemaType(Enum):
    """
    Enumerations for the possible schema types to simplify JSON-Schema usage.
    """

    TODOS = "schema-todos.json"


class DDBPrefixes(Enum):
    """
    Enumerations for DynamoDB Partition Keys and Sort Keys for TODO items and related information to
    centralize and simplify the usage.
    """

    PK_USER = "USER#"
    SK_TODO_DATA = "TODO#"
