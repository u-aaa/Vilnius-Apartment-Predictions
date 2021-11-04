from dotenv import load_dotenv
from pathlib import Path
import os

dotenv_path = Path('database/.env')
load_dotenv(dotenv_path=dotenv_path)

class Config:
    db_host = os.environ['HOST']
    db_database = os.environ['DATABASE']
    db_user = os.environ['USER']
    db_password = os.environ['PASSWORD']
    db_port = os.environ['PORT']
    SQLALCHEMY_DATABASE_URI = f'postgresql://{db_user}:{db_password}@{db_host}/{db_database}'
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
