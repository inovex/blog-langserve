import os

import re
from typing import Any, Callable, Dict

from fastapi import HTTPException, Request
from langchain_mongodb.chat_message_histories import MongoDBChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.runnables import ConfigurableFieldSpec
from langchain_core.runnables.base import RunnableSequence


def _is_valid_identifier(value: str) -> bool:
    """Check if the value is a valid identifier."""
    # Use a regular expression to match the allowed characters
    valid_characters = re.compile(r"^[a-zA-Z0-9-_]+$")
    return bool(valid_characters.match(value))


def create_session_factory(
    mongodb_user: str,
    mongodb_password: str,
    mongodb_cluster: str,
    db_name: str,
    chat_history_collection: str
) -> Callable[[str], BaseChatMessageHistory]:
    """Create a factory that can retrieve chat histories.

    The chat histories are keyed by user ID and conversation ID.

    Args:
        mongodb_user: MongoDB username.
        mongodb_password: MongoDB password.
        mongodb_cluster: MongoDB cluster.
        db_name: Name of the database to be used.
        chat_history_collection: Name of the collection inside
            the specified database to be used.

    Returns:
        A factory that can retrieve chat histories keyed
        by user ID and conversation ID.
    """

    # MongoDB connection string including user, password, cluster
    connection_string = (
        f"mongodb+srv://{mongodb_user}:{mongodb_password}@{mongodb_cluster}"
    )

    def get_chat_history(
        user_id: str,
        conversation_id: str) -> MongoDBChatMessageHistory:
        """Get a chat history from a user id and conversation id."""
        if not _is_valid_identifier(user_id):
            raise ValueError(
                f"User ID {user_id} is not in a valid format. "
                "User ID must only contain alphanumeric characters, "
                "hyphens, and underscores."
                "Please include a valid cookie in the request "
                "headers called 'user-id'."
            )
        if not _is_valid_identifier(conversation_id):
            raise ValueError(
                f"Conversation ID {conversation_id} is not in a valid format. "
                "Conversation ID must only contain alphanumeric characters, "
                "hyphens, and underscores. Please provide a valid "
                "conversation id via config. For example, "
                "chain.invoke(.., {'configurable': {'conversation_id': '123'}})"
            )

        session_id = f"{user_id}%{conversation_id}"
        return MongoDBChatMessageHistory(
                session_id=session_id,
                connection_string=connection_string,
                database_name=db_name,
                collection_name=chat_history_collection,
            )
    
    return get_chat_history


def _per_request_config_modifier(
    config: Dict[str, Any], request: Request
) -> Dict[str, Any]:
    """Update the config"""
    config = config.copy()
    configurable = config.get("configurable", {})
    # Look for a cookie named "user_id"
    user_id = request.cookies.get("user_id", None)

    if user_id is None:
        raise HTTPException(
            status_code=400,
            detail="No user id found. Please set a cookie named 'user_id'. \n"
                   "If you use Swagger UI use /set-cookie/ GET API to set it.",
        )

    configurable["user_id"] = user_id
    config["configurable"] = configurable
    return config


def chain_with_history(
    chain: RunnableSequence,
    input_messages_key: str,
    history_message_key: str
) -> RunnableSequence:
    """Creates a chain supporting chat history from a chain.
    
    Args:
        chain: Langchain chain without chat history support.
        input_messages_key: Input message key name.
        history_message_key: MongoDB host.

    Returns:
        A langchain chain considering chat histories by user ID and conversation ID.
    """
    return RunnableWithMessageHistory(
        chain,
        create_session_factory(
            os.environ.get("MONGODB_USER"),
            os.environ.get("MONGODB_PASSWORD"),
            os.environ.get("MONGODB_CLUSTER"),
            os.environ.get("DB_NAME"),
            os.environ.get("CHAT_HISTORIES_COLLECTION")
        ),
        input_messages_key=input_messages_key,
        history_messages_key=history_message_key,
        history_factory_config=[
            ConfigurableFieldSpec(
                id="user_id",
                annotation=str,
                name="User ID",
                description="Unique identifier for the user.",
                default="",
                is_shared=True,
            ),
            ConfigurableFieldSpec(
                id="conversation_id",
                annotation=str,
                name="Conversation ID",
                description="Unique identifier for the conversation.",
                default="",
                is_shared=True,
            ),
        ],
    )
