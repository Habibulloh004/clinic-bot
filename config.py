import os
from os import getenv

from dotenv import load_dotenv

load_dotenv()

TOKEN = getenv("BOT_TOKEN")

UZLABS_SERVICES_URL = os.getenv("UZLABS_SERVICES_URL")
UZLABS_TOKEN = os.getenv("UZLABS_TOKEN")

DATABASE_NAME = os.getenv('DATABASE_NAME')
DATABASE_USER = os.getenv('DATABASE_USER')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')
DATABASE_HOST = os.getenv('DATABASE_HOST')
DATABASE_PORT = os.getenv('DATABASE_PORT')
