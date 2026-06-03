from fastapi import FastAPI
import models 
from database import engine
from routers import auth, todos, admin


app = FastAPI()

#This line is used to create database tables defined in your SQLAlchemy MOdels

#Metadata attribute holds all you schema defined in the models

#Create_all constructs the tables inside your configured database base on hte strcutre defined in your models
# when you call it, it checks the metadata for all defined tables and creates them in the database that engine is connected to


models.Base.metadata.create_all(bind = engine)

#Engine represents the connection to your specific database which was created in the database.py file 
# allowing SQLAlchemy to know which database to be operated on



app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)


