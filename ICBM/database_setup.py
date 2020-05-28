from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os


path = os.path.abspath(__file__)
while path != 'C:\\Users\\Samuel\\PycharmProjects\\OGEMOS\\ICBM':
    path = os.path.dirname(path)
connection_string = 'sqlite:///'+path+'\\CoefficientDocumentation\\coefficient.db'
engine = create_engine(connection_string)
Session = sessionmaker(bind=engine)
