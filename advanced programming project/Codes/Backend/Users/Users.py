
"""
This module contains the classes and methods to manage the users of the application.

Authors:

Sergio Nicolás Mendivelso  <snmendivelsom@udistrital.edu.co>

Daniel Santiago Pérez <dsperezm@udistrital.edu.co> 


"""

from pydantic import BaseModel
from sqlalchemy import Column, String, Integer, Boolean
from sqlalchemy.ext.declarative import declarative_base


# ============================= PARCICIPANT CLASS =============================

class Participant(BaseModel):

    """This class is an abstractation for any participant into the application"""   
    _username: str
    _id: int
    _password: str
    _email: str
    _registered_events: list
    _verified: bool
    _uploaded_activities: list

    @staticmethod
    def register(username, email, password):
  
        """ This method is used to register a new Participant

        Args:
        username: str the name of the participant
        email: str the email of the participant
        password: str the password of the participant

        Returns:
        Participant: Participant 

        """

        return Participant(username = username, email = email, password = password)
  

    @staticmethod
    def login(username, password):
        """
        This method is used to login into the application.

       
        """ 
        return Participant(username = username, password = password, verified ={"publish": True})
    
class Organizer(Participant):

    """This class is an abstractation for any organizer in the application"""

    _organized_events:list


Base = declarative_base()

class UsersDB(Base):

    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)
    registered_events = Column(String)
    verified = Column(String)
    uploaded_activities = Column(String)