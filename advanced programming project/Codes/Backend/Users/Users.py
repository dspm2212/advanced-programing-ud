"""
This module contains the classes and methods to manage the users of the application.

Authors:

Sergio Nicolás Mendivelso  <snmendivelsom@udistrital.edu.co>

Daniel Santiago Pérez <dsperezm@udistrital.edu.co> 

"""

from pydantic import BaseModel
from sqlalchemy import Column, String, Integer, Boolean, ARRAY
from sqlalchemy.ext.declarative import declarative_base
from db_conection import PostgresConnection


#========================================= DECLARATION =================================

# Declarative base for SQLAlchemy
Base = declarative_base()

# Create the tables in the database
connection = PostgresConnection("Daniel", "perez123", "Virtual_Xperience", 5432, "Virtual_Xperience")

# ============================= USER CLASS =============================

class User(BaseModel):

    """This class is an abstraction for any User into the application"""
    
    # Attributes declaration
    __username: str
    __id: str
    __password: str
    __email: str
    __registered_events: list = []
    __verified: bool = False
    __uploaded_activities_id: list = []
    __participant_events_id: list = []
    __organized_events_id: list = []



 #--------------------------------------- METHODS --------------------------------------------------------

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
            uploaded_activities_id=",".join(self.__uploaded_activities_id),
            participant_events_id=",".join(self.__participant_events_id),
            organized_events_id=",".join(self.__organized_events_id)
        )

        session.add(user_db)
        session.commit()
        session.close()

#-------------------------- GETTERS AND SETTERS --------------------------------


    @property
    def username(self) -> str:
        return self.__username


    @property
    def id(self) -> int:
        return self.__id

    @property
    def password(self) -> str:
        return self.__password

    @property
    def email(self) -> str:
        return self.__email

    @property
    def registered_events(self) -> list:
        return self.__registered_events

    @property
    def verified(self) -> bool:
        return self.__verified

    @property
    def uploaded_activities(self) -> list:
        return self.__uploaded_activities

    @property
    def organized_events(self) -> list:
        return self.__organized_events

#----------------------------------------------------------------

    @username.setter
    def username(self, username: str):
        self.__username = username

    @id.setter
    def id(self, id: int):
        self.__id = id

    @password.setter
    def password(self, password: str):
        self.__password = password

    @email.setter
    def email(self, email: str):
        self.__email = email

    @registered_events.setter
    def registered_events(self, registered_events: list):
        self.__registered_events = registered_events

    @verified.setter
    def verified(self, verified: bool):
        self.__verified = verified


    @uploaded_activities.setter
    def uploaded_activities(self, uploaded_activities: list):
        self.__uploaded_activities = uploaded_activities

    @organized_events.setter
    def organized_events(self, organized_events: list):
        self.__organized_events = organized_events


#=========================================== USERSDB CLASS ==================================================

class UsersDB(Base):

    """
    This class provides the users database

    """

    __tablename__ = "users"

    id = Column(String, primary_key=True)
    username = Column(String, index=True)
    email = Column(String, index=True)
    password = Column(String, index = True)
    registered_events = Column(ARRAY(String), nullable=True)
    verified = Column(Boolean, default=False)
    uploaded_activities_id = Column(ARRAY(String), nullable=True)
    participant_events_id = Column(ARRAY(String), nullable=True)   
    organized_events_id = Column(ARRAY(String), nullable=True)