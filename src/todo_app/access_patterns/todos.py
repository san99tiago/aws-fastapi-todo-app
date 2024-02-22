# Built-in imports
import os
from datetime import datetime
from typing import Optional

# External imports
from fastapi import HTTPException
from ulid import ULID
from aws_lambda_powertools import Logger

# Own imports
from todo_app.common.logger import custom_logger
from todo_app.helpers.dynamodb_helper import DynamoDBHelper
from todo_app.common.enums import DDBPrefixes
from todo_app.models.todos import TodoModel, TodoModelUpdates

# Initialize DynamoDB helper for item's abstraction
DYNAMODB_TABLE = os.environ.get("DYNAMODB_TABLE")
ENDPOINT_URL = os.environ.get("ENDPOINT_URL")
dynamodb_helper = DynamoDBHelper(DYNAMODB_TABLE, ENDPOINT_URL)


class Todos:
    """Class to define TODO items in a simple fashion."""

    def __init__(self, user_email: str, logger: Optional[Logger] = None) -> None:
        """
        :param user_email (str): User email user to identify the TODO items.
        :param logger (Optional(Logger)): Logger object.
        """
        self.user_email = user_email
        self.partition_key = f"{DDBPrefixes.PK_USER.value}{self.user_email}"
        self.logger = logger or custom_logger()

    def get_all_todos(self) -> list:
        """
        Method to get all TODO items for a given user.
        """
        self.logger.info(f"Retrieving all TODO items for user_email: {self.user_email}")

        results = dynamodb_helper.query_by_pk_and_sk_begins_with(
            partition_key=self.partition_key,
            sort_key_portion="TODO#",
        )
        self.logger.debug(results)
        self.logger.info(f"Items from query: {len(results)}")
        return results

    def get_todo_by_ulid(self, ulid: str) -> dict:
        """
        Method to get a TODO item by its ULID.
        :param ulid (str): ULID for a specific TODO item.
        """
        self.logger.info(
            f"Retrieving TODO item by ULID: {ulid} for user_email: {self.user_email}"
        )

        result = dynamodb_helper.get_item_by_pk_and_sk(
            partition_key=self.partition_key,
            sort_key=f"TODO#{ulid}",
        )

        formatted_todo = TodoModel.from_dynamodb_item(result) if result else {}
        self.logger.debug(formatted_todo)
        return formatted_todo

    def create_todo(self, todo_data: dict) -> Optional[TodoModel]:
        """
        Method to create a new TODO item.
        :param todo_data (dict): Data for the new TODO item.
        """
        todo_data["PK"] = self.partition_key
        todo_data["SK"] = f"TODO#{ULID()}"
        current_time = datetime.now().isoformat()
        todo_data["created_at"] = current_time
        todo_data["updated_at"] = current_time

        todo = TodoModel(**todo_data)

        result = dynamodb_helper.put_item(todo.to_dynamodb_dict())
        self.logger.debug(result)

        if result.get("ResponseMetadata", {}).get("HTTPStatusCode") == 200:
            return todo

        return {}

    def patch_todo(self, ulid: str, todo_data: dict) -> Optional[TodoModel]:
        """
        Method to patch an existing TODO item.
        :param ulid (str): ULID for a specific TODO item.
        :param todo_data (dict): Data for the new TODO item.
        """

        # Validate that TODO item exists
        existing_todo_item = self.get_todo_by_ulid(ulid)
        if not existing_todo_item:
            self.logger.error(
                f"patch_todo failed due to non-existing TODO item to update: {ulid}"
            )
            raise HTTPException(
                status_code=400,
                detail=f"TODO patch request for ULID {ulid} "
                "is not valid because item does not exist",
            )

        current_time = datetime.now().isoformat()
        todo_data["updated_at"] = current_time

        result = dynamodb_helper.update_item(
            partition_key=self.partition_key,
            sort_key=f"TODO#{ulid}",
            data_attributes_only=todo_data,
        )
        self.logger.debug(result)

        if result.get("ResponseMetadata", {}).get("HTTPStatusCode") == 200:
            return self.get_todo_by_ulid(ulid)

        return {}

    def delete_todo(self, ulid: str) -> Optional[TodoModel]:
        """
        Method to delete an existing TODO item.
        :param ulid (str): ULID for a specific TODO item.
        :param todo_data (dict): Data for the new TODO item.
        """

        # Validate that TODO item exists
        existing_todo_item = self.get_todo_by_ulid(ulid)
        if not existing_todo_item:
            self.logger.error(
                f"delete_todo failed due to non-existing TODO item to delete: {ulid}"
            )
            raise HTTPException(
                status_code=400,
                detail=f"TODO delete request for ULID {ulid} "
                "is not valid because item does not exist",
            )

        result = dynamodb_helper.delete_item(
            partition_key=self.partition_key,
            sort_key=f"TODO#{ulid}",
        )
        self.logger.debug(result)

        return {}
