"""
This class implements the postgress conecction

Authors:

Sergio Nicolás Mendivelso  <snmendivelsom@udistrital.edu.co>

Daniel Santiago Pérez <dsperezm@udistrital.edu.co> 


"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class PostgresConnection:

    def __init__(
        self, user: str, password: str, host: str, port: int, database_name: str
    ):      
            self.engine = create_engine(f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{database_name}')
            self.Session = sessionmaker(bind=self.engine)

    def session(self):
        return self.Session()