"""
This module contains the classes and methods to manage the activities of the application

Authors:

Sergio Nicolás Mendivelso  <snmendivelsom@udistrital.edu.co>

Daniel Santiago Pérez <dsperezm@udistrital.edu.co> 

"""

#------------------------------------------------------------

from pydantic import BaseModel
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, ARRAY
from sqlalchemy.ext.declarative import declarative_base
from db_conection import PostgresConnection


#========================================= DECLARATION =================================

# Declarative base for SQLAlchemy
Base = declarative_base()

# Create the tables in the database
connection = PostgresConnection("Daniel", "perez123", "Virtual_Xperience", 5432, "Virtual_Xperience")







# ============================= ACTIVITY CLASS =============================

class Activity(BaseModel): 
    
    """This class is an abstraction for any activity into the application"""

    __name:str
    __id:str
    __description:str
    __event_id:str
    __start_date:str
    __final_date:str
    __at_time_list:list = []



#-----------------------------  METHODS ----------------------------------------------


    def add_to_db(self):

        """
        Main function:

        - Add a new Activity to the database.

        Steps:

        - Create a new session
        - Create a new table with the actual attributes of the activity
        - add it the table to the database
        - upload the changes
        - close the session

        Parameters:

        - None

        Returns:

        - None

        """
        session = connection.session()

        activities_db = ActivitiesDB(
            name = self.__name,
            id=self.__id,
            description=self.__description,
            event_id = self.__event_id,
            start_date=self.__start_date,
            final_date=self.__final_date,
            at_time_list=",".join(self.__at_time_list),
        )

        session.add(activities_db)
        session.commit()
        session.close()

#-------------------------- GETTERS AND SETTERS --------------------------------

    @property
    def name(self) -> str:
        return self.__name

    @property
    def id(self) -> str:
        return self.__id

    @property
    def event_id(self) -> str:
        return self.__event_id

    @property
    def start_date(self) -> str:
        return self.__start_date

    @property
    def final_date(self) -> str:
        return self.__final_date

    @property
    def description(self) -> str:
        return self.__description

    @property
    def at_time_list(self) -> list:
        return self.__at_time_list

#-------------------------------------------------------------

    @name.setter
    def name(self, value: str):
        self.__name = value

    @id.setter
    def id(self, value: str):
        self.__id = value

    @id.setter
    def event_id(self, value: str):
        self.__event_id = value

    @start_date.setter
    def start_date(self, value: str):
        self.__start_date = value

    @final_date.setter
    def final_date(self, value: str):
        self.__final_date = value

    @description.setter
    def description(self, value: str):
        self.__description = value

    @at_time_list.setter
    def at_time_list(self, value: list):
        self.__at_time_list = value

#============================================ ACTIVITIES DB CLASS ===================================

class ActivitiesDB(Base):

    __tablename__ = "activities"
    
    name = Column(String, index=True)
    id = Column(String, primary_key=True)
    description = Column(String, index=True)
    event_id = Column(String, index=True)
    start_date = Column(String, index=True)
    final_date = Column(String, index=True)
    at_time_list = Column(ARRAY(String), nullable=True)
