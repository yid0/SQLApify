from model.query import Query 
from db import Credential, Connection, Database

queryString = "select * from table"

query= Query(queryString)

print(query.query)

credential = Credential(username= "postgres", password= "postgres")

connection = Connection(protocol="postgresql+asyncpg", host="localhost" , port="5432", db_name= "postgres", credential= credential)

print(connection)

db =  Database(type= "pg", connection= connection)

result = db.connect()

print(result)
