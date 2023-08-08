import sqlalchemy
from sqlalchemy import create_engine,text
import os

# db_conn_str=os.environ['DB_CONNECTION_STRING']
db_conn_str="mysql+pymysql://bartzabel:kartik0511"

engine=create_engine(
    db_conn_str,
    connect_args={
        db_conn_str
    }
)