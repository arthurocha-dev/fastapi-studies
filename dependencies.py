from database import model
from sqlalchemy.orm import sessionmaker

def pegar_session():
    try:
        Session = sessionmaker(bind=model.db)
        session = Session()
        yield session
    finally:
        session.close()