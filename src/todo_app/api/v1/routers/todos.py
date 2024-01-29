# Built-in imports
from typing import Annotated
from uuid import uuid4

# External imports
from fastapi import APIRouter, Header
from aws_lambda_powertools import Logger

# Own imports
# TODO: add own imports when src code grows (schemas, models, database, validations, etc...)

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

        # TODO: add actual database connectivity for to-dos
        result = [
            {
                "id": "dummy-id-1",
                "title": "todo1",
                "done": "no",
                "category": "Personal",
                "is_closed": "no",
            },
            {
                "id": "dummy-id-2",
                "title": "todo2",
                "done": "yes",
                "category": "Personal",
                "is_closed": "no",
            },
        ]

        logger.info("Finished read_all_todos() successfully")
        return result

    except Exception as e:
        logger.error(f"Error in read_all_todos(): {e}")
        raise e


@router.get("/todos/{todo_id}", tags=["todos"])
async def read_all_todos(
    user_email: str,
    todo_id: str,
    correlation_id: Annotated[str | None, Header()] = uuid4(),
):
    try:
        logger.append_keys(correlation_id=correlation_id, user_email=user_email)
        logger.info("Starting todos handler for read_all_todos()")

        # TODO: add actual database connectivity for to-dos
        result = {
            "id": todo_id,
            "title": "Some message",
            "done": "no",
            "category": "Personal",
            "is_closed": "no",
        }

        logger.info("Finished read_all_todos() successfully")
        return result

    except Exception as e:
        logger.error(f"Error in read_all_todos(): {e}")
        raise e


@router.post("/todos", tags=["todos"])
async def create_todo(
    user_details: dict,
    correlation_id: Annotated[str | None, Header()] = uuid4(),
):
    try:
        # Inject additional keys to the logger for cross-referencing logs
        user_email = user_details.get("user_email")
        logger.append_keys(correlation_id=correlation_id, user_email=user_email)

        # TODO: Add payload/schema validation of todo element

        logger.info("Starting todos handler for create_todo()")

        # TODO: add actual database connectivity for to-dos
        result = {"title": "TODO was created successfully"}

        logger.info("Finished create_todo() successfully")
        return result

    except Exception as e:
        logger.error(f"Error in create_todo(): {e}")
        raise e
