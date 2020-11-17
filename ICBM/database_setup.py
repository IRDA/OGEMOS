from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sys
import os



current_directory = os.getcwd()
connection_string = 'sqlite:///'+current_directory+"/coefficient.db"
engine = create_engine(connection_string)
Session = sessionmaker(bind=engine)
