
"""
This module contains the classes and methods to manage the users of the application.

Authors:

Sergio Nicolás Mendivelso  <snmendivelsom@udistrital.edu.co>

Daniel Santiago Pérez <dsperezm@udistrital.edu.co> 


"""

from pydantic import BaseModel


# ============================= PARCICIPANT CLASS =============================

class Participant(BaseModel):

    """This class is an abstractation for any participant into the application"""   
    _username: str
    _id: str
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

