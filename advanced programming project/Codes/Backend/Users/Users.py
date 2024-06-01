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

    """This class is an abstraction for any User into the application"""
    
    # Attributes declaration
    __username: str
    __id: int
    __password: str
    __email: str
    __registered_events: list = []
    __verified: bool = False
    __uploaded_activities: list = []
    __organized_events: list = []



    # Add user to the database
    def add_to_db(self):
        
        """
        Main function:

        - Add a new user to the database.

        Steps:

        - Create a new session
        - Create a new table with the actual attributes of the user
        - add it the table to the database
        - upload the changes
        - close the session

        Parameters:

        - None

        Returns:

        - None

        """
        
        session = connection.session()

        user_db = UsersDB(
            username=self.__username,
            id=self.__id,
            email=self.__email,
            password=self.__password,
            registered_events=",".join(self.__registered_events),
            verified=self.verified,
            uploaded_activities=",".join(self.__uploaded_activities),
            organized_events=",".join(self.__organized_events)
        )

        session.add(user_db)
        session.commit()
        session.close()

    @classmethod
    def hash_password(self, password:str) -> str:
        
        """ 
        Main function:
        
        - Is used to hash the password of the user

        Parameters:

        - password (str) the password to be hashed

        Returns:
        - str: the hashed password of the user

        """
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        return pwd_context.hash(password)

    @classmethod
    def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        """ This method is used to verify the password of the user """
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        return pwd_context.verify(plain_password, hashed_password)

#-------------------------- GETTERS AND SETTERS --------------------------------

    """
    
    # Getter and Setter for username
    def get_username(self):
        return self.__username

    def set_username(self, username: str):
        self.__username = username

    # Getter and Setter for id
    def get_id(self):
        return self.__id

    def set_id(self, user_id: int):
        self.__id = user_id

    # Getter and Setter for password
    def get_password(self):
        return self.__password

    def set_password(self, password: str):
        self.__password = password

    # Getter and Setter for email
    def get_email(self):
        return self.__email

    def set_email(self, email: str):
        self.__email = email

    # Getter and Setter for registered_events
    def get_registered_events(self):
        return self.__registered_events

    def set_registered_events(self, registered_events: list):
        self.__registered_events = registered_events

    # Getter and Setter for verified
    def get_verified(self):
        return self.__verified

    def set_verified(self, verified: bool):
        self.__verified = verified

    # Getter and Setter for uploaded_activities
    def get_uploaded_activities(self):
        return self.__uploaded_activities

    def set_uploaded_activities(self, uploaded_activities: list):
        self.__uploaded_activities = uploaded_activities

    # Getter and Setter for organized_events
    def get_organized_events(self):
        return self.__organized_events

    def set_organized_events(self, organized_events: list):
        self.__organized_events = organized_events

    """
# Declarative base for SQLAlchemy
Base = declarative_base()


#=========================================== USERSDB CLASS ==================================================

class UsersDB(Base):

    """
    This class provides the users database

    """

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