from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sys
import os



os.chdir(sys._MEIPASS)
connection_string = 'sqlite:///BD/coefficient.db'
engine = create_engine(connection_string)
Session = sessionmaker(bind=engine)
