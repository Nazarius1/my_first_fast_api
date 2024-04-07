from venv import create
from requests import session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
# import psycopg2
# from psycopg2.extras import RealDictCursor
# import time


load_dotenv()
pswd_postgre = os.getenv('pswd_postgre')
database_host = os.getenv('database_host')
database_name = os.getenv('database_name')
database_user = os.getenv("database_user")

#print('password:',pswd_postgre)


# SQLALCHEMY_DATABASE_URL = 'postgresql://<username>:<password>@<ip-address or hostname>/<database_name>'
# here is where the connection is established
SQLALCHEMY_DATABASE_URL = f'postgresql://{database_user}:{pswd_postgre}@{database_host}/{database_name}'

#print(SQLALCHEMY_DATABASE_URL)

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    except:
        db.close()


# while True: #retry connection as long as the connection is not properly established
#     try:
#         conn = psycopg2.connect(host=database_host, database=database_name,
#                                 user=database_user, password=pswd_postgre, cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Database connection was succesfull")
#         break
#     except Exception as error:
#         print("Connecting to database failed")
#         print("Error: ", error)
#         time.sleep(3)

