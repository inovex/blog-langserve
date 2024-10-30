from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import AzureChatOpenAI

from functions.chat_history import chain_with_history
from models.request_models import Question


# Prompt
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You're a helpful assistant answering questions."),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{question}"),
    ]
)

# Create chain
chain = prompt | AzureChatOpenAI(deployment_name="gpt-4-turbo")


# Chain with history
chain_with_history = chain_with_history(
    chain,
    input_messages_key= "question",
    history_message_key="history"
).with_types(input_type=Question)