# import pymongo
# mongoUrl="mongodb://localhost:27017"
# client=pymongo.MongoClient(mongoUrl)
# db=client["todo"] #todo is database name
# collection = db["todo"]


from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


engine=create_engine('sqlite:///./sql_app.db',connect_args={"check_same_thread":False}) # Connect to a Database: SQLAlchemy supports various database engines such as SQLite, MySQL, PostgreSQL, and more. To connect to a database, create an engine object using the create_engine function and specify the database URL.
# (./ means same directory) , check_same_thread is set to False, which means that the SQLite connection can be used from multiple threads. This is useful in scenarios where you want to share the connection among multiple threads.
base= declarative_base( ) # Define a Database Model: Using SQLAlchemy's declarative base, define a class that represents a table in your database. Each table is represented as a subclass of the declarative_base() object. Define columns as class variables within the class, specifying their data types.
SessionLocal=sessionmaker(autocommit=False,bind=engine)#Create a Session: To interact with the database, you need to create a session. The session acts as an interface for querying, inserting, updating, and deleting data.
