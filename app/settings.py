import os
from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    app_name: str = "TapDev FastAPI Example"
    
    db_host: str = Field("localhost", env='DB_HOSTNAME')
    db_name: str = Field("fastapidevdb", env='DB_NAME')
    db_username: str = Field("fastapidevuser", env='DB_USERNAME')
    db_password: str = Field("test1234", env='DB_PASSWORD')

    # db_host: str = os.getenv("DB_HOSTNAME", "localhost")
    # db_name: str = os.getenv("DB_NAME", "fastapidevdb")
    # db_username: str = os.getenv("DB_USERNAME", "fastapidevuser")
    # db_password: str = os.getenv("DB_PASSWORD", "test1234")