import os
from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "TapDev FastAPI Example"
    
    db_host: str = os.getenv("DB_HOSTNAME", "localhost")
    db_name: str = os.getenv("DB_NAME", "fastapidevdb")
    db_username: str = os.getenv("DB_USERNAME", "fastapidevuser")
    db_password: str = os.getenv("DB_PASSWORD", "test1234")