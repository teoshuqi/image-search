import os

from dotenv import load_dotenv

# Load environment variables from a specific path
config_path = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(config_path)


# POSTGRES
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PWD = os.getenv("POSTGRES_PWD")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_DATABASE = os.getenv("POSTGRES_DB")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")

# APP
IMAGE_DIR = os.getenv("IMAGE_DIR")
WEBSCRAPER_CONFIG = os.getenv("WEBSCRAPER_CONFIG")
WEBDRIVER_HOST = os.getenv("WEBDRIVER_HOST")
WEBDRIVER_PORT = os.getenv("WEBDRIVER_PORT")
APP_PORT = os.getenv("APP_PORT")
APP_HOST = os.getenv("APP_HOST")

# VECTOR DB
HUGGINGFACE_MODEL = os.getenv("HUGGINGFACE_MODEL")
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
VECTORDB_NAME = os.getenv("VECTORDB_NAME")
VECTORDB_HOST = os.getenv("VECTORDB_HOST")
VECTORDB_PORT = os.getenv("VECTORDB_PORT")

if __name__ == "__main__":
    print(WEBSCRAPER_CONFIG)
