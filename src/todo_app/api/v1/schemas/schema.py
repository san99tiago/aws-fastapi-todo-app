# Built-in imports
import os
import json
from typing import Optional

# External imports
from aws_lambda_powertools import Logger

# Own imports
from todo_app.common.enums import JSONSchemaType
from todo_app.common.logger import custom_logger


# TODO: add capability of multiple schema versions in the future
class Schema:
    """
    Class that loads in memory a JSON Schema object depending on the JSON Schema type.
    """

    def __init__(
        self, json_schema_type: JSONSchemaType, logger: Optional[Logger] = None
    ) -> None:
        """
        :param json_schema_type (JSONSchemaType): Enumeration for the JSON Schema type.
        :param logger (Optional(Logger)): Logger object.
        """
        self.logger = logger or custom_logger()

        self.logger.info(f"Loading schema for json_schema_type: {json_schema_type}")
        file_path = os.path.join(os.path.dirname(__file__), json_schema_type.value)
        with open(file_path, "r") as file:
            self.json_schema = json.loads(file.read())

    def get_schema(self) -> dict:
        return self.json_schema
