from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os


path = os.path.abspath(__file__)
while not path.endswith("ICBM"):
    path = os.path.dirname(path)
connection_string = 'sqlite:///'+path+'\\BaseDeDonnees\\coefficient.db'
engine = create_engine(connection_string)
Session = sessionmaker(bind=engine)
