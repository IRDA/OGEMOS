from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///CoefficientDocumentation/coefficient.db')
Session = sessionmaker(bind=engine)
