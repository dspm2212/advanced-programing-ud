"""
This module contains the classes and methods to manage the events of the application

Authors:

Sergio Nicolás Mendivelso  <snmendivelsom@udistrital.edu.co>

Daniel Santiago Pérez <dsperezm@udistrital.edu.co> 

"""

#------------------------------------------------------------

from Users import User
from pydantic import BaseModel

class Event(BaseModel): 
    
    """This class is an abstraction for any event into the application"""

    __name:str
    __id:str
    __description:str
    __organizer:User
    __privated: bool
    __participants:list = []
    __activities:list = []
    __material:list = []


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
            organizer=self.__organizer,
            privated=self.__privated,
            participants=",".join(self.__participants),
            activities=",".join(self.__activities),
            material=",".join(self.__material)
            
        )

        session.add(events_db)
        session.commit()
        session.close()



# Declarative base for SQLAlchemy
Base = declarative_base()

class EventsDB(Base):

    """
    This class provides the events database

    """
    __tablename__ = "events"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)
    organizer = Column(String, index=True)
    privated = Column(Boolean, default=False)
    participants = Column(String, nullable=True)
    activities = Column(String, nullable=True)
    material = Column(String, nullable=True)

# Create the tables in the database
connection = PostgresConnection("Daniel", "perez123", "Virtual_Xperience", 5432, "Virtual_Xperience")
Base.metadata.create_all(bind=connection.engine)


# Create the tables in the database
connection = PostgresConnection("Daniel", "perez123", "Virtual_Xperience", 5432, "Virtual_Xperience")
Base.metadata.create_all(bind=connection.engine)
        