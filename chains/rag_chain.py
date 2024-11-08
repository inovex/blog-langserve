from langchain_core.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain_openai import AzureChatOpenAI

from functions.rag_services import vectorstore, format_docs
from models.request_models import QuestionWithFilter


# AzureChatOpenAI model
llm = AzureChatOpenAI(deployment_name="gpt-4-turbo")

# Prompt
system_prompt = """
                Based on the question and the given context 
                write a natural language response that will answer the customer query:
                        context: {context}
                """

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{question}"),
    ]
)

# Create chain
rag_chain = (
    RunnablePassthrough.assign(
        context=lambda x: format_docs(
            vectorstore.similarity_search(
                x["question"],
                k=3,
                pre_filter=x["filter"]
            )
        ),
    )
    | prompt
    | llm
).with_types(input_type=QuestionWithFilter)
