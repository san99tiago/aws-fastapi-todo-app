# Built-in imports
from typing import Optional, Self

# External imports
from pydantic import BaseModel, Field


class TodoModel(BaseModel):
    """
    Class that represents a TODO item.
    """

    PK: str = Field(pattern=r"^USER#[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
    SK: str = Field(pattern=r"^TODO#")
    todo_title: str
    todo_details: Optional[str] = Field(None)
    todo_date: str
    is_done: Optional[bool] = Field(False)
    created_at: str
    updated_at: str

    def to_dynamodb_dict(self) -> dict:
        dynamodb_dict = {
            "PK": {"S": self.PK},
            "SK": {"S": self.SK},
            "todo_title": {"S": self.todo_title},
            "todo_details": {"S": self.todo_details},
            "todo_date": {"S": self.todo_date},
            "is_done": {"S": str(self.is_done)},
            "created_at": {"S": self.created_at},
            "updated_at": {"S": self.updated_at},
        }

        # Remove None values from the dictionary
        dynamodb_dict = {
            key: value for key, value in dynamodb_dict.items() if value is not None
        }

        return dynamodb_dict

    @classmethod
    def from_dynamodb_item(cls, dynamodb_item: dict) -> "TodoModel":
        return cls(
            PK=dynamodb_item["PK"]["S"],
            SK=dynamodb_item["SK"]["S"],
            todo_title=dynamodb_item["todo_title"]["S"],
            todo_details=dynamodb_item.get("todo_details", {}).get("S"),
            todo_date=dynamodb_item["todo_date"]["S"],
            is_done=dynamodb_item.get("is_done", {}).get("S"),
            created_at=dynamodb_item["created_at"]["S"],
            updated_at=dynamodb_item["updated_at"]["S"],
        )


# TODO: Instead of a duplicated model for "PATCH" requests, create an abstraction for both
class TodoModelUpdates(BaseModel):
    """
    Class that represents a TODO item.
    """

    PK: str = Field(pattern=r"^USER#[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
    SK: str = Field(pattern=r"^TODO#")
    todo_title: Optional[str] = Field(None)
    todo_details: Optional[str] = Field(None)
    todo_date: Optional[str] = Field(None)
    is_done: Optional[bool] = Field(False)
    created_at: Optional[str] = Field(None)
    updated_at: Optional[str] = Field(None)

    def to_dynamodb_dict(self) -> dict:
        dynamodb_dict = {
            "PK": {"S": self.PK},
            "SK": {"S": self.SK},
            "todo_title": {"S": self.todo_title},
            "todo_details": {"S": self.todo_details},
            "todo_date": {"S": self.todo_date},
            "is_done": {"S": str(self.is_done)},
            "created_at": {"S": self.created_at},
            "updated_at": {"S": self.updated_at},
        }

        # Remove None values from the dictionary
        dynamodb_dict = {
            key: value
            for key, value in dynamodb_dict.items()
            if value.get("S") is not None
        }

        return dynamodb_dict

    @classmethod
    def from_dynamodb_item(cls, dynamodb_item: dict) -> "TodoModel":
        return cls(
            PK=dynamodb_item["PK"]["S"],
            SK=dynamodb_item["SK"]["S"],
            todo_title=dynamodb_item.get("todo_title", {}).get("S"),
            todo_details=dynamodb_item.get("todo_details", {}).get("S"),
            todo_date=dynamodb_item.get("todo_date", {}).get("S"),
            is_done=dynamodb_item.get("is_done", {}).get("S"),
            created_at=dynamodb_item.get("created_at", {}).get("S"),
            updated_at=dynamodb_item.get("updated_at", {}).get("S"),
        )


if __name__ == "__main__":
    # Example usage 1
    todo_data = {
        "PK": "USER#rick@example.com",
        "SK": "TODO#ULID1234",
        "todo_title": "Complete project",
        "todo_details": "Finish the report",
        "todo_date": "2024-02-29",
        "is_done": False,
        "created_at": "2024-01-05T05:51:02.350Z",
        "updated_at": "2024-01-06T02:31:02.350Z",
    }

    todo_instance = TodoModel(**todo_data)
    todo_dict = todo_instance.to_dynamodb_dict()
    print(todo_dict)

    # Example usage 2
    dynamodb_item = {
        "PK": {"S": "USER#rick@example.com"},
        "SK": {"S": "TODO#ULID1234"},
        "todo_title": {"S": "Complete project 123"},
        "todo_details": {"S": "Finish the project 123 with notes and diagrams"},
        "todo_date": {"S": "2024-08-14"},
        "is_done": {"S": "False"},
        "created_at": {"S": "2024-01-05T05:51:02.350Z"},
        "updated_at": {"S": "2024-01-06T02:31:02.350Z"},
    }

    todo_instance = TodoModel.from_dynamodb_item(dynamodb_item)
    print(todo_instance)

    # Example usage 3
    todo_data = {
        "PK": "USER#rick@example.com",
        "SK": "TODO#ULID1234",
        "todo_details": "Finish the report",
        "is_done": True,
    }

    todo_instance = TodoModelUpdates(**todo_data)
    todo_dict = todo_instance.to_dynamodb_dict()
    print(todo_dict)
