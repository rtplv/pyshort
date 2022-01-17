import os

from dotenv import load_dotenv
from databases import Database

load_dotenv()

# OS
ROOT_PATH = os.path.dirname(os.path.abspath(__file__))

# DB
DB_URL = os.environ.get("DB_URL")
DB_DATABASE = os.environ.get("DB_DATABASE")
DB_POOL_MIN = 5
DB_POOL_MAX = 20

# JWT
JWT_EXPIRATION = 21600

db = Database(DB_URL + DB_DATABASE, min_size=DB_POOL_MIN, max_size=DB_POOL_MAX)
