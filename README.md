# LangServe: LangChain REST API Backend

## Currently considered functions
### Chat history
- chat histories are managed in a MongoDB (managed with a Docker container) collection
- user ids and conversation ids are stored in the "SessionId" field (with value: {user_id}%{conversation_id})
- messages are stored in the "history" field 


## Project Setup

### Setup
- Requirements
    - Docker

### Setup environment variables
- Create a `.env` file in root directory of the project and copy the contents from the `.env.template` file
- Replace in the file the variables for Azure OpenAI

### Start MongoDB and LangServe App
1) Nativate to the root directory of the project in your terminal and execute the command:
    ```
    docker compose up --build
    ```

2) You can access now the Swagger UI with http://localhost:8000/docs on your browser


## Interaction with Swagger UI
1) Before trying out any APIs, the `/set-cookie/` GET API (available under the `default` section) needs to be executed with an example user ID to set the `user_id` cookie on your browser
3) Now the APIs under the `base` section can be executed (e.g. `/base/invoke`, `/base/stream`)
    - For the `base` APIs it it necessary to set the `conversation_id` value in the request body (setting `user_id` is not necessary since it was already set in the `user_id` cookie).
