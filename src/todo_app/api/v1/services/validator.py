# Built-in imports
from typing import Union, Literal, Optional

# External imports
import jsonschema
from jsonschema._format import FormatChecker

from aws_lambda_powertools import Logger

# Own imports
from todo_app.common.logger import custom_logger


def validate_json(
    data: dict,
    json_schema: dict,
    logger: Optional[Logger] = None,
) -> Union[Literal[True], Exception]:
    """
    Generic validation function to apply a JSON Schema validation based on payload and a schema.

    :param data (dict): JSON object.
    :param json_schema (dict): JSON Schema to use for the validation.
    :param logger (Optional(Logger)): Logger object.
    """
    logger = logger or custom_logger()
    try:
        jsonschema.validate(
            instance=data,
            schema=json_schema,
            format_checker=FormatChecker(),  # Required to also validate "format" fields in schema
        )
    except jsonschema.ValidationError as validation_error:
        logger.error(
            "JSONSchema ValidationError occurred. "
            f"message: {validation_error.message}."
            f"json_path: {validation_error.json_path}"
        )
        return validation_error
    except jsonschema.SchemaError as schema_error:
        logger.error(
            "JSONSchema SchemaError occured. "
            f"message: {schema_error.message}."
            f"json_path: {schema_error.json_path}"
        )
        return schema_error
    except Exception as e:
        logger.error("Unknown error for JSONSchema validation. " f"message: {str(e)}")
        return e

    return True
