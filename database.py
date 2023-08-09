import sqlalchemy 
from sqlalchemy import create_engine,text
import os

db_conn_str=os.environ['DB_CONNECTION_STRING']

engine=create_engine(
  db_conn_str
)

with engine.connect() as conn:
  result=conn.execute(text("SELECT * from postgres.sentiments"))

res=[]
for row in result.all():
  res.append(row._asdict())

print(res)