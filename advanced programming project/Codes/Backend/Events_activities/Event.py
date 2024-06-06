"""
This module contains the classes and methods to manage the events of the application

Authors:

Sergio Nicolás Mendivelso  <snmendivelsom@udistrital.edu.co>

Daniel Santiago Pérez <dsperezm@udistrital.edu.co> 

"""

#------------------------------------------------------------

from Users.Users import User
from pydantic import BaseModel
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, ARRAY
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from db_conection import PostgresConnection

#===================================== DECLARATION ====================================

# Declarative base class
Base = declarative_base()
connection = PostgresConnection("Daniel", "perez123", "Virtual_Xperience", 5432, "Virtual_Xperience")

#================================== EVENT CLASS =====================================


class Event(BaseModel): 
    
    """This class is an abstraction for any event into the application"""

    __name:str
    __id:str
    __description:str
    __organizer_id:int
    __privated: bool
    __password:str = None
    __participants_id:list = []
    __activities_id:list = []
    __material:list = []

#-------------------------- METHODS ----------------------------------------

    def add_to_db(self):
            """
            Main function:

            - Add a new Event to the database.

            Steps:

            - Create a new session
            - Create a new table with the actual attributes of the event
            - add it the table to the database
            - upload the changes
            - close the session

            Parameters:

            - None

            Returns:

            - None

            """

            session = connection.session()

            events_db = EventsDB(
                name = self.__name,
                id=self.__id,
                description=self.__description,
                organizer_id=self.__organizer_id,
                privated=self.__privated,
                password=self.__password,
                participants_id=",".join(self.__participants_id),
                activities_id=",".join(self.__activities_id),
                material=",".join(self.__material)

            )

            session.add(events_db)
            session.commit()
            session.close()

#---------------------------------------- GETTERS AND SETTERS --------------------------------

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, name: str):
        self.__name = name

    @property
    def id(self) -> str:
        return self.__id

    @id.setter
    def id(self, event_id: str):
        self.__id = event_id

    @property
    def description(self) -> str:
        return self.__description

    @description.setter
    def description(self, description: str):
        self.__description = description

    @property
    def organizer_id(self) -> int:
        return self.__organizer_id

    @organizer_id.setter
    def organizer_id(self, organizer_id: int):
        self.__organizer_id = organizer_id

    @property
    def privated(self) -> bool:
        return self.__privated

    @privated.setter
    def privated(self, privated: bool):
        self.__privated = privated

    @property
    def password(self) -> str:
        return self.__password

    @password.setter
    def password(self, password: str):
        self.__password = password

    @property
    def participants(self) -> list:
        return self.__participants

    @participants.setter
    def participants(self, participants: list):
        self.__participants = participants

    @property
    def activities(self) -> list:
        return self.__activities

    @activities.setter
    def activities(self, activities: list):
        self.__activities = activities

    @property
    def material(self) -> list:
        return self.__material

    @material.setter
    def material(self, material: list):
        self.__material = material

#======================================== EVENTS DB CLASS ============================================

class EventsDB(Base):

    """
    This class provides the events database

    """
    __tablename__ = "events"
    
    id = Column(String, primary_key=True)
    name = Column(String, index=True)
    description = Column(String, index=True)
    organizer_id = Column(String, index=True)    
    privated = Column(Boolean, default=False)
    password = Column(String, nullable=True)
    participants_id = Column(ARRAY(String), nullable=True)
    activities_id = Column(ARRAY(String), nullable=True)
    material = Column(String, nullable=True)

