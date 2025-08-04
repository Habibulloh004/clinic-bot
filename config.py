import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

# Ensure UZLABS_SERVICES_URL has proper format
UZLABS_SERVICES_URL = os.getenv("UZLABS_SERVICES_URL", "")
if UZLABS_SERVICES_URL and not UZLABS_SERVICES_URL.endswith('/'):
    UZLABS_SERVICES_URL += '/'

UZLABS_TOKEN = os.getenv("UZLABS_TOKEN")

DATABASE_NAME = os.getenv('DATABASE_NAME')
DATABASE_USER = os.getenv('DATABASE_USER')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')
DATABASE_HOST = os.getenv('DATABASE_HOST')
DATABASE_PORT = os.getenv('DATABASE_PORT')

# Validate required environment variables
required_vars = ['BOT_TOKEN', 'UZLABS_SERVICES_URL', 'UZLABS_TOKEN']
missing_vars = [var for var in required_vars if not os.getenv(var)]
if missing_vars:
    print(f"Warning: Missing environment variables: {', '.join(missing_vars)}")