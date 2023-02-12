from pydantic import BaseSettings
from dotenv import load_dotenv

class Settings(BaseSettings):
    load_dotenv()
    