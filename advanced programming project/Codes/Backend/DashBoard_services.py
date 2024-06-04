"""
This module contains the services of the dashboard into the application

Authors:

Sergio Nicolás Mendivelso  <snmendivelsom@udistrital.edu.co>

Daniel Santiago Pérez <dsperezm@udistrital.edu.co> 


"""
#----------------------------------------------------------------

from fastapi import APIRouter, HTTPException
from Users.Users import User, UsersDB
from db_conection import PostgresConnection
from Events_activities.Event import Event, EventsDB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import func
import Hash_password
import Main


#======================================== DECLARATION =================================

#Create Router
router_dashboard = APIRouter()

# Declarative base for SQLAlchemy
Base = declarative_base()


#Database Connection
connection = PostgresConnection("Daniel", "perez123", "Virtual_Xperience", 5432, "Virtual_Xperience")

#======================================== SERVICES ====================================
@router_dashboard.post("/dashboard/create_event")
def create_event(event_name:str,  event_description:str, event_privated:bool):

    """
    Main function:

    - create an event

    Steps:

    - create a new session
    - update the tables with the actual attributes of the event
    - add it the table to the database
    - Close the session

    Parameters:

    - event_name (str): name of the event
    - event_description (str): description of the event
    - event_privated (bool): if the event is privated or not

    Raises:

    - HTTPException: if an error ocurred while creating the event.

    Returns:

    - str: message of the event creation


    """

    session = connection.Session()

    events_db = session.query(EventsDB).all()
    users_db = session.query(UsersDB).all()
    user_online = Main.user_online

    try:

        new_id =  "E" + str(len(session.query(EventsDB).all()) + 1)
        event = EventsDB()
        event.name = event_name
        event.id = new_id 
        event.description = event_description 
        event.organizer_id = user_online.id
        event.privated = event_privated
        session.add(event)


        organizer = session.query(UsersDB).filter(UsersDB.id == user_online.id).first()

        organizer.organized_events_id = func.array_append(organizer.organized_events_id, event.id)
        
        session.commit()
    
    except Exception as e:
    
        raise HTTPException(status_code=500, detail= f"an error ocurred {str(e)}")

    finally:

        session.close()

    return {
                "message": "event created successfully"
    }


# ----------------------------------------------------------------


@router_dashboard.post("/dashboard/create_event/add_password")
def add_password_to_event(event_id:int, password:str, confirm_password:str):

    """
    Main function:

    - add a password to an event

    Steps:

    - create a new session
    - if the passwords don't coincide, will be raise an HTTPException (400) 
    - if the passwords coincide, will be add the password to the event
    - close the session

    Parameters:
    - event_id (int): id of the event
    - password (str):  password of the event
    - confirm_password (str):  confirm password of the event

    Raises:

    - HTTPException: if the passwords don't coincide
    - HTTPException: if the event id doesn't exist


    """

    session = connection.Session()
    events_db = session.query(EventsDB).all()

    event_exists = session.query(EventsDB).filter(UsersDB.id == event_id).first()

    if not password == confirm_password:

        session.close()
        raise HTTPException(status_code=400, detail="The passwords doesn't match")

    else:

        if event_exists:
            hashed_password = hash_password(password)
            event_exists.password = hashed_password

    session.close()
  

#----------------------------------------------------------------

@router_dashboard.post("/dashboard/join_event/public_event")
def join_event_public(id:str):

    """

    Main function:

    - 

    """

    session = connection.Session()

    events_db = session.query(EventsDB).all()
    event_exists = session.query(EventsDB).filter(EventsDB.id == id).first()
    try:
        if not event_exists:

            session.close()
            raise HTTPException(status_code=400, detail= "Invalid id, it does not exist")

        else:
            organizer = session.query(UsersDB).filter(UsersDB.id == user_online.id).first()
            organizer.participant_events_id = func.array_append(organizer.participant_events_id, id)

    except Exception as e:
        raise HTTPException(status_code=400, detail= f"an error ocurred{str(e)}")

    finally:
        
        session.close()

    return {
            "Message" : "Event joined succesfully"
        }


#----------------------------------------------------------------

@router_dashboard.post("/dashboard/join_event/private_event")
def join_event_private(id:str, password:str):

    """

    Main function:

    - 

    """

    session = connection.Session()

    events_db = session.query(EventsDB).all()
    event_exists = session.query(EventsDB).filter(EventsDB.id == id).first()
    try:

        
        if not event_exists:

            session.close()
            raise HTTPException(status_code=400, detail= "Invalid id, it does not exist")

        elif not Hash_password.verify_password(password, event_exists.password):

            session.close()
            raise HTTPException(status_code=400, detail= "Invalid password")

        else:
            
            organizer = session.query(UsersDB).filter(UsersDB.id == user_online.id).first()
            organizer.participant_events_id = func.array_append(organizer.participant_events_id, id)

    except Exception as e:
        raise HTTPException(status_code=400, detail= f"an error ocurred{str(e)}")

    finally:
        
        session.close()

    return {
            "Message" : "Event joined succesfully"
        }

#--------------------------------------------------------------------

@router_dashboard.post("/dashboard/search_event")
def join_event(id:str):

    """

    Main function:

    - 

    """

    session = connection.Session()

    events_db = session.query(EventsDB).all()
    event_exists = session.query(EventsDB).filter(EventsDB.id == id).first()
    try:
        if not event_exists:

            session.close()
            raise HTTPException(status_code=400, detail= "Invalid id, it does not exist")


    except Exception as e:
        raise HTTPException(status_code=400, detail= f"an error ocurred{str(e)}")

    finally:
        
        session.close()

    return {
            "name": event_exists.name,
            "id": event_exists.id,
            "description": event_exists.description,
            "organizer": event_exists.organizer_id,
            "privated": event_exists.privated,
            "participants": event_exists.participants_id,
            "activities": event_exists.activities_id,
        }
