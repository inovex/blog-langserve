import os
import sys
from pymongo import MongoClient
import logging


# Configure logging to output to the console
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout  # Log to standard output (console)
)

logger = logging.getLogger(__name__)


# Extract env variables
mongodb_user = os.environ.get("MONGODB_USER")
mongodb_password = os.environ.get("MONGODB_PASSWORD")
mongodb_port = os.environ.get("MONGODB_PORT")

db_name = os.environ.get("DB_NAME")
collection_name = os.environ.get("CHAT_HISTORIES_COLLECTION")

# Connect to MongoDB with connection string
logger.info("Connect to MongoDB")
connection_string = (
    f"mongodb://{mongodb_user}:{mongodb_password}@mongo:{mongodb_port}/?directConnection=true"
)
client = MongoClient(connection_string)

# Create a database
logger.info(f"Create database: {db_name}")
db = client[str(db_name)]

# Create a collection
logger.info(f"Create collection: {db_name}")
collection = db[str(collection_name)]

# Insert a sample document
collection.insert_one({"username": "testUser", "email": "test@example.com"})

# Delete all documents
result = collection.delete_many({})  # Empty filter deletes all documents

# Print the number of deleted documents
logger.info(f"Deleted all {result.deleted_count} documents.")

logger.info("Database and collection created successfully.")
