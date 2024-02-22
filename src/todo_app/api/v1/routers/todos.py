# Built-in imports
from typing import Annotated
from uuid import uuid4

# External imports
from fastapi import APIRouter, Header
from aws_lambda_powertools import Logger

# Own imports
from todo_app.access_patterns.todos import Todos
from todo_app.api.v1.schemas.schema import Schema
from todo_app.api.v1.services.exceptions import SchemaValidationException
from todo_app.api.v1.services.validator import validate_json
from todo_app.common.enums import JSONSchemaType


logger = Logger(
    service="todo-app",
    log_uncaught_exceptions=True,
    owner="Santiago Garcia Arango",
)

router = APIRouter()


@router.get("/todos", tags=["todos"])
async def read_all_todos(
    user_email: str,
    correlation_id: Annotated[str | None, Header()] = uuid4(),
):
    try:
        logger.append_keys(correlation_id=correlation_id, user_email=user_email)
        logger.info("Starting todos handler for read_all_todos()")

        todo = Todos(user_email=user_email, logger=logger)
        result = todo.get_all_todos()
        logger.info("Finished read_todo_item() successfully")
        return result

    except Exception as e:
        logger.error(f"Error in read_all_todos(): {e}")
        raise e


@router.get("/todos/{todo_id}", tags=["todos"])
async def read_todo_item(
    user_email: str,
    todo_id: str,
    correlation_id: Annotated[str | None, Header()] = uuid4(),
):
    try:
        logger.append_keys(correlation_id=correlation_id, user_email=user_email)
        logger.info("Starting todos handler for read_todo_item()")

        todo = Todos(user_email=user_email, logger=logger)
        result = todo.get_todo_by_ulid(ulid=todo_id)
        logger.info("Finished read_todo_item() successfully")
        return result

    except Exception as e:
        logger.error(f"Error in read_todo_item(): {e}")
        raise e


@router.post("/todos", tags=["todos"])
async def create_todo(
    todo_details: dict,
    correlation_id: Annotated[str | None, Header()] = uuid4(),
):
    try:
        # Inject additional keys to the logger for cross-referencing logs
        user_email = todo_details.get("user_email")
        logger.append_keys(correlation_id=correlation_id, user_email=user_email)

        # Validate payload with JSON-Schema
        todos_schema = Schema(JSONSchemaType.TODOS, logger=logger).get_schema()
        validation_result = validate_json(
            data=todo_details, json_schema=todos_schema, logger=logger
        )
        if isinstance(validation_result, Exception):
            raise SchemaValidationException(todo_details, validation_result)
        logger.info("Starting todos handler for create_todo()")

        # After schema validation, it's safe to load the TODO element
        todos = Todos(user_email=user_email, logger=logger)
        result = todos.create_todo(todo_details)

        logger.info("Finished create_todo() successfully")
        return result

    except Exception as e:
        logger.error(f"Error in create_todo(): {e}")
        raise e


@router.patch("/todos/{todo_id}", tags=["todos"])
async def patch_todo_item(
    user_email: str,
    todo_id: str,
    todo_details: dict,
    correlation_id: Annotated[str | None, Header()] = uuid4(),
):
    try:
        logger.append_keys(correlation_id=correlation_id, user_email=user_email)
        logger.info("Starting todos handler for patch_todo_item()")

        # Validate payload with JSON-Schema
        todos_schema = Schema(JSONSchemaType.TODOS, logger=logger).get_schema()
        todos_schema.pop(
            "required", None
        )  # For patch, do not enforce mandatory fields in schema
        validation_result = validate_json(
            data=todo_details, json_schema=todos_schema, logger=logger
        )
        if isinstance(validation_result, Exception):
            raise SchemaValidationException(todo_details, validation_result)

        todo = Todos(user_email=user_email, logger=logger)
        result = todo.patch_todo(ulid=todo_id, todo_data=todo_details)

        logger.info("Finished patch_todo_item() successfully")
        return result

    except Exception as e:
        logger.error(f"Error in patch_todo_item(): {e}")
        raise e


@router.delete("/todos/{todo_id}", tags=["todos"])
async def delete_todo_item(
    user_email: str,
    todo_id: str,
    correlation_id: Annotated[str | None, Header()] = uuid4(),
):
    try:
        logger.append_keys(correlation_id=correlation_id, user_email=user_email)
        logger.info("Starting todos handler for delete_todo_item()")

        todo = Todos(user_email=user_email, logger=logger)
        result = todo.delete_todo(ulid=todo_id)

        logger.info("Finished delete_todo_item() successfully")
        return result

    except Exception as e:
        logger.error(f"Error in delete_todo_item(): {e}")
        raise e
