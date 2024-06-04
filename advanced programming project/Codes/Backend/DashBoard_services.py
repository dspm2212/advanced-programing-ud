from fastapi import APIRouter, HTTPException
from Users.Users import User, UsersDB
from db_conection import PostgresConnection
from Events_activities.Event import Event, EventsDB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import func
import Hash_password
import Main

router_dashboard = APIRouter()

# Declarative base for SQLAlchemy
Base = declarative_base()



connection = PostgresConnection("Daniel", "perez123", "Virtual_Xperience", 5432, "Virtual_Xperience")
Base.metadata.create_all(bind=connection.engine)


@router_dashboard.post("/dashboard/create_event")
def create_event(event_name:str,  event_description:str, event_privated:bool):


    global connection

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
        

        if len(organizer.organized_events_id) == 0 :

            organizer.organized_events_id = [event.id]
        else:


            organizer.organized_events_id = func.array_append(organizer.organized_events_id, event.id)
        
        session.commit()
    
    except Exception as e:
    
        raise HTTPException(status_code=400, detail= f"an error ocurred {str(e)}")
    finally:

        session.close()

    return {
                "message": "event created successfully"
    }



@router_dashboard.post("/dashboard/create_event/add_password")
def add_password_to_event(event_id:int, password:str, confirm_password:str):

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

  

@router_dashboard.post("/dashboard/join_event")
def join_event(id:str):



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

