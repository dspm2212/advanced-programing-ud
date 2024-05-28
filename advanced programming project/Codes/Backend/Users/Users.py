"""
This module contains the classes and methods to manage the users of the application.

Authors:

Sergio Nicolás Mendivelso  <snmendivelsom@udistrital.edu.co>

Daniel Santiago Pérez <dsperezm@udistrital.edu.co> 

"""

from pydantic import BaseModel
from sqlalchemy import Column, String, Integer, Boolean
from sqlalchemy.ext.declarative import declarative_base
from db_conection import PostgresConnection
from passlib.context import CryptContext

# ============================= USER CLASS =============================

class User(BaseModel):

    """This class is an abstraction for any participant into the application"""
    
    # Attributes declaration
    username: str
    id: int
    password: str
    email: str
    registered_events: list = []
    verified: bool = False
    uploaded_activities: list = []
    organized_events: list = []



    # Add user to the database
    def add_to_db(self):
        session = connection.session()

        user_db = UsersDB(
            username=self.username,
            id=self.id,
            email=self.email,
            password=self.password,
            registered_events=",".join(self.registered_events),
            verified=self.verified,
            uploaded_activities=",".join(self.uploaded_activities),
            organized_events=",".join(self.organized_events)
        )

        session.add(user_db)
        session.commit()
        session.close()

    @classmethod
    def hash_password(self, password:str) -> str:
        
        """ This method is used to hash the password of the user

        Args:
        password: str the password of the user

        Returns:
        password: str the hashed password of the user

        """
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        return pwd_context.hash(password)

    @classmethod
    def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        """ This method is used to verify the password of the user """
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        return pwd_context.verify(plain_password, hashed_password)

# Declarative base for SQLAlchemy
Base = declarative_base()


#=========================================== USERSDB CLASS ==================================================

class UsersDB(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    email = Column(String, index=True)
    password = Column(String)
    registered_events = Column(String, nullable=True)
    verified = Column(Boolean, default=False)
    uploaded_activities = Column(String, nullable=True)
    organized_events = Column(String, nullable=True)

# Create the tables in the database
connection = PostgresConnection("Daniel", "perez123", "Virtual_Xperience", 5432, "Virtual_Xperience")
Base.metadata.create_all(bind=connection.engine)