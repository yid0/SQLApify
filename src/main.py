import sys
import os
from fastapi import FastAPI
from sqlmodel import Session
from db import DbType, Credential, ConnectionFactory
from db.provider.postgres import PostgresDatabase
from src.loader import RouterLoader
from db.query import QuerySchema

from db.setup import Setup


app = FastAPI()

RouterLoader(app, "src/rest")    
 
    
@app.on_event("startup")
def startup_event():
    try: 
        db_type  = os.getenv("BUILD_TARGET")
        setup = Setup(db_type= db_type)
        setup.create_user_app()
    except Exception as e:
        print(e)
        sys.exit(1)

@app.get("/")
def read_root():
    return {"status": "API is running"}