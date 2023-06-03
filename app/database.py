from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker #tuong tac voi database
SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://admin:Congthanh123@database-1.cuzymwi7r2cr.us-east-1.rds.amazonaws.com:3306/mydb"
engine = create_engine(SQLALCHEMY_DATABASE_URL) #ket noi vào database 
sessionlocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
base = declarative_base()

# Dependency
def get_db():
    db = sessionlocal()
    try:
        yield db
    finally:
        db.close()

