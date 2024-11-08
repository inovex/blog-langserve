# LangServe: LangChain REST API Backend

## Currently considered functions

### RAG Use Case
- The project provides API for a RAG use case (`rag`) considering some example documents


## Project Setup

### Setup
- Requirements
    - Docker
    - Python 3.12 or greater; Pip 24.2 or greater

### Setup MongoDB Cloud
- Create a MongoDB cloud account on the website: https://www.mongodb.com/
- Create a cluster on your MongoDB account
- Create a database within the created cluster
- Create a collection within the created database
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


### Setup environment variables
- Create a `.env` file in root directory of the project and copy the contents from the `.env.template` file
- Replace in the file the variables for Azure OpenAI and MongoDB setup

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
1) The APIs under the `rag` sections can be executed (e.g. `/rag/invoke`, `/rag/stream`) "Try it out" button
