"""
This module contains the classes and methods to manage the activities of the application

Authors:

Sergio Nicolás Mendivelso  <snmendivelsom@udistrital.edu.co>

Daniel Santiago Pérez <dsperezm@udistrital.edu.co> 

"""

#------------------------------------------------------------

from Users import User
from pydantic import BaseModel


# ============================= ACTIVITY CLASS =============================

class Activity(BaseModel): 
    
    """This class is an abstraction for any activity into the application"""

    __name:str
    __id:str
    __start_date:str
    __final_date:str
    __description:str
    __at_time_list:list = []



#-----------------------------  METHODS ----------------------------------------------


#--------------------------

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
            start_date=self.__start_date,
            final_date=self.__final_date,
            description=self.__description,
            at_time_list=",".join(self.__at_time_list),
        )

        session.add(activities_db)
        session.commit()
        session.close()

#----------------------------------------------------------------

# Declarative base for SQLAlchemy
Base = declarative_base()

#============================================ ACTIVITIES DB CLASS ===================================

class ActivitiesDB(Base):
    __tablename__ = "activities"
    
    name = Column(String, index=True)
    id = Column(String, index=True)
    start_date = Column(String, index=True)
    final_date = Column(String, index=True)
    description = Column(String, index=True)
    at_time_list = Column(String, nullable=True)


# Create the tables in the database
connection = PostgresConnection("Daniel", "perez123", "Virtual_Xperience", 5432, "Virtual_Xperience")
Base.metadata.create_all(bind=connection.engine)
