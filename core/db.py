from pymongo import MongoClient
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

try:
    client = MongoClient(settings.MONGO_URI, serverSelectionTimeoutMS=5000)
    # Test the connection
    client.server_info()
    db = client[settings.MONGO_DB_NAME]
    
    employee_logs = db.employee_logs
    projects = db.projects
    
    logger.info(f"Successfully connected to MongoDB at {settings.MONGO_URI}")
except Exception as e:
    logger.error(f"Failed to connect to MongoDB: {str(e)}")
    raise Exception(f"MongoDB Connection Error: {str(e)}")
