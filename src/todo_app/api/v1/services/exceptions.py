# Built-in imports
from typing import Optional, Union

# External imports
from fastapi import HTTPException
import jsonschema


class SchemaValidationException(HTTPException):
    """
    Custom JSON-Schema Validation exception when Payload or Schema have a failure in the validation
    process of a FastAPI request.
    """

    def __init__(
        self,
        payload: str,
        base_exception: Optional[
            Union[jsonschema.ValidationError, jsonschema.SchemaError, Exception]
        ] = None,
        status_code=400,
    ):
        """
        :param payload (str): JSON payload of the request that failed validation.
        :param base_exception: base_exception that could be from jsonschema or generic Exception.
        :param status_code (int): Status Code to send in the exception.
        """
        detail = {
            "error": "Input JSON body failed schema validation",
            "input": payload,
            "message": base_exception.message or base_exception,
            "schema": base_exception.schema or None,
            "json_path": base_exception.json_path or None,
        }
        super().__init__(status_code=status_code, detail=detail)
