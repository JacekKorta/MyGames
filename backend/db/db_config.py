import os

username = os.getenv("MONGODB_USERNAME")
password = os.getenv("MONGODB_PASSWORD")
host = os.getenv("MONGODB_HOST", "mongo")
port = os.getenv("MONGODB_PORT", "27017")
auth_source = os.getenv("MONGODB_AUTH_SOURCE", "admin")

path = f"mongodb://{username}:{password}@{host}:{port}/?authSource={auth_source}"
