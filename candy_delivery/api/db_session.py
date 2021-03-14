from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def create_db_session(db_url):
    """
    возвращает сессию для работы с базой данных
    """
    engine = create_engine(db_url, connect_args={"check_same_thread": False})
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return Session
