# LangServe: LangChain REST API Backend

## Currently considered functions
### Chat history
- chat histories are managed in a MongoDB collection
- user ids and conversation ids are stored in the "SessionId" field (with value: {user_id}%{conversation_id})
- messages are stored in the "history" field 

### Authentication
- Azure Authentication realized with the package [FastAPI-Azure-Auth](https://intility.github.io/fastapi-azure-auth/)

### General Conversations and RAG Use Case
- The project provides API for general chat conversations (`base`) and for a RAG use case (`rag`) considering some example documents


## Project Setup

### Setup
- Requirements
    - Docker
    - Azure Account
    - Python 3.12 or greater; Pip 24.2 or greater

### Setup MongoDB Cloud
- Create a MongoDB cloud account on the website: https://www.mongodb.com/
- Create a cluster on your MongoDB account
- Create a database within the created cluster
- Create two collections within the created database
    - A collection for managing chat history (e.g. `chat_histories`)
    - A collection for storing embedding documents for the rag use case (e.g. `vector_collection`)
- Create for the collection `vector_collection` an Atlas Search Index (e.g. `vsearch_index`) with the following properties
    ```
    {
      "fields": [
        {
          "numDimensions": 1536,
          "path": "embedding",
          "similarity": "cosine",
          "type": "vector"
        },
        {
          "path": "source",
          "type": "filter"
        }
      ]
    }
    ```
- Extract the MongoDB connection string for your created cluster
    - Navigate to Overview page of your created cluster and click on the `Connect` button
    - On the popup window select Python driver as option and extract the connection string with the structure
        ```
        mongodb+srv://<mongodb_username>:<mongodb_password>@<mongodb_cluster>
        ```
    - where `mongodb_cluster` has the structure: <cluster_name>.<additional_str>.mongodb.net

### Setup Azure AD App Registration for Authentication
- Follow the [instructions for the setup of the Azure configuration for the Single-tenant Setup](https://intility.github.io/fastapi-azure-auth/single-tenant/azure_setup)

### Setup environment variables
- Create a `.env` file in root directory of the project and copy the contents from the `.env.template` file
- Replace in the file the variables for Azure OpenAI, Azure App Registration, and MongoDB setup

### Setup Python virtual environment and start the LangServe App
1) Create a Python virtual environment
    ```
    virtualenv path/to/venv/langserve_env
    ```
    or use anaconda
    ```
    conda create --name langserve_env python=3.12
    ```
2) Activate the virtual environment
    ```
    source path/to/venv/langserve_env/bin/activate
    ```
    or for anaconda
    ```
    conda activate langserve_env
    ```
3) Install packages
    ```
    pip install -r requirements.txt
    ```

Alternative using Docker:

1) Nativate to the root directory of the project in your terminal and build the docker image with the command

    ```
    docker build -t langservegpt .
    ```

### Insert example documents into vector collection
1) On your terminal (with the activated Python virtual environment) execute `jupyter notebook` on your terminal and open the `embeddings/mongodb_atlas.ipynb` notebook file

2) Execute all cells of the notebook from top to down to insert the example documents into the vector collection

3) Check on your MongoDB cloud account whether the documents are inserted correctly


### Start the LangServe App
1) If project setup was realized with virtualenv or conda, execute the following command on your terminal (with activated Python virtual environment and on the root directory of the project):
    ```
    python app.py
    ```

    If project setup was realized with docker, execute the following command on your terminal:

    ```
    docker run -p 8000:8000 langservegpt
    ```

2) You can access now the Swagger UI with http://localhost:8000/docs on your browser


## Interaction with Swagger UI
1) Before trying out any APIs, it is necessary to authorize youself on the Swagger UI by clicking on the `Authorize` button on the top-right corner of the page and to login into your Microsoft Azure Account
2) After login successfully into your Microsof Azure Account on the Swagger UI, the `/set-cookie/` GET API (available under the `default` section) needs to be executed with an example user ID to set the `user_id` cookie on your browser
3) Now the APIs under the `base` and `rag` sections can be executed (e.g. `/base/invoke` `/base/stream`, `/rag/invoke`, `/rag/stream`)
    - For the `base` and `rag` APIs it it necessary to set the `conversation_id` value in the request body (setting `user_id` is not necessary since it was already set in the `user_id` cookie).
