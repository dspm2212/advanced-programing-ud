"""
This module contains the Main of the application.

Authors:

Sergio Nicolás Mendivelso  <snmendivelsom@udistrital.edu.co>

Daniel Santiago Pérez <dsperezm@udistrital.edu.co> 

"""

#----------------------------------------------------------------

from fastapi import FastAPI, HTTPException
from Users.Users import User, UsersDB, Base
from Events_activities.Event import EventsDB
from db_conection import PostgresConnection
from Hash_password import hash_password, verify_password
from fastapi.middleware.cors import CORSMiddleware
from fastapi import APIRouter, HTTPException
from Users.Users import User, UsersDB
from db_conection import PostgresConnection
from Events_activities.Event import Event, EventsDB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import func
import Hash_password



# ========================== DECLARATION =========================

# Initialize the application
app = FastAPI()

# Added CORS middleware to allow cross-origin requests, and don't create conflicts
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#Starts the app
app = FastAPI()

#Declare the actual online user
user_online:User = None

#Database connection

connection = PostgresConnection("Daniel", "perez123", "Virtual_Xperience", 5432, "Virtual_Xperience")
session = connection.Session()

# Create the tables in the database
Base.metadata.create_all(bind=connection.engine, tables=[UsersDB.__table__])
Base.metadata.create_all(bind=connection.engine, tables=[EventsDB.__table__])

#==================================== SERVICES =================================

@app.get("/test")
def test():

    """
     Simple test to verify that the database connection is working

    """

    global user_online

    if not users_db:
        

        return "No hay usuarios"

    elif user_online == None:

     return "Hay usuarios " + str(len(users_db)) 


    else:

        return "Hay usuarios " + str(len(users_db))+ " online user: " + user_online.username


#------------------------------------


@app.post("/register")
def register(username:str, email:str, password:str, password_confirmation:str) -> dict:


    """

    main function:

    - Registers a new user in the database.


    steps:


    - if the email hasn't an '@' will be raise an HTTPException (400)
    - if the password confirmation doesn't match with the password it will be raise an HTTPException (400)
    - if the username already exists it will be raise an HTTPException (400)
    - if the email already exists it will be raise an HTTPException (400)
    - if the username and the email doesn't exists the user is created and uploadoded to the database.


    Parameters:
    - username (str): The username of the new user.
    - password (str): The password of the new user.
    - email (str): The email of the new user.

    Raises:
    - HTTPException: If the email address is not valid, if the username already exists, or if the email already exists.

    Returns:
    - str: "User Registered Succesfully" if the user is registered successfully.

    Example:
    ```
    register("new_user", "password123", "new_user@example.com")
    ```

    """

    if '@' not in email:

        raise HTTPException(status_code=400, detail="The email address is not valid")

    elif password != password_confirmation:


        raise HTTPException(status_code=400, detail="The passwords doesn't match")

    try: 

        user_db = session.query(UsersDB).all()       

        user_exists = session.query(UsersDB).filter(UsersDB.username == username).first()
        email_exists = session.query(UsersDB).filter(UsersDB.email == email).first()

        if user_exists:
             raise HTTPException(status_code=400, detail="The username already exists")

        elif email_exists:
             raise HTTPException(status_code=400, detail="The email already exists")

        else: 
            hashed_pass = hash_password(password=password)
            new_id =  "U"+ str (len(user_db) + 1)
            user = User()

            user.username=username 
            user.id = new_id
            user.password=hashed_pass 
            user.email=email

            user.add_to_db()

    except Exception as e:

        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


    return {"message":"User Registered Succesfully" }

#--------------------------------------

@app.post("/login")
def login(username:str, password:str) -> dict:
    """
    
    main function:

    - Logs in a user in the database.

    steps:
    

    - if the username doesn't exists it will be raise an HTTPException (400)
    - if the password doesn't match with the password in the database it will be raise an HTTPException (400)
    - if the username and the password matchs the user is logged in and it values are copied in the user_online attribute

    
    Parameters:
    - username (str): The username of the new user.
    - password (str): The password of the new user.
    - password_confirmation (str): The password confirmation of the new user.
    
    Raises:
    - HTTPException: If the username doesn't exists, or if the password doesn't match.
    
    Returns:
    - str: "User Logged In Succesfully" if the user is logged in successfully.

    Example:

     ```
     login("new_user", "password123")

      ```

    """
    global user_online

    user_db = session.query(UsersDB).all() 


    try:

        user_exists = session.query(UsersDB).filter(UsersDB.username == username).first()

        if not user_exists:

            raise HTTPException(status_code=400, detail= "Invalid username or password")

        elif not verify_password(password, user_exists.password):
            raise HTTPException(status_code=400, detail="Invalid username or password")

        else: 

            user_exists.verified = True
            user_online = user_exists
            session.commit()

    except Exception as e:

        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

    return {"message":"Login successful"}


#----------------------------------------------------------------

@app.post("/search_user_by_id")
def search_user_by_id(user_id:str):
    """
    Main function:
    - Searches a user by id in the database.
    Steps:

    - if the users id does not exist, will be raise an HTTPException (400)
    - if the users id exists, will be return the user

    Parameters:
    - user_id (int): The id of the user.
    Raises:
    - HTTPException: If the user id doesn't exists.
    
    Returns:
    - user info
    Example:
    
    ```
    search_user_by_id(U30)
     ```

    """

    user_db = session.query(UsersDB).all() 
    try:
        user_exists = session.query(UsersDB).filter(UsersDB.id == user_id).first()
        if not user_exists:
            raise HTTPException(status_code=400, detail= "Invalid user id")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

    return {
                "username": user_exists.username,
            "id": user_exists.id,
            "verified": user_exists.verified,
            "email": user_exists.email,
            "uploaded_activities": user_exists.uploaded_activities_id,
            "participant_events": user_exists.participant_events_id,
            "organized_events": user_exists.organized_events_id
        }


#=================================================== DASHBOARD SERVICES ===============================

#======================================== DECLARATION =================================

# Declarative base for SQLAlchemy
connection = PostgresConnection("Daniel", "perez123", "Virtual_Xperience", 5432, "Virtual_Xperience")

#======================================== SERVICES ====================================
@app.post("/dashboard/create_event")
def create_event(event_name:str,  event_description:str, event_privated:bool):

    """
    Main function:

    - create an event

    Steps:


    - update the tables with the actual attributes of the event
    - add it the table to the database


    Parameters:

    - event_name (str): name of the event
    - event_description (str): description of the event
    - event_privated (bool): if the event is privated or not

    Raises:

    - HTTPException: if an error ocurred while creating the event.

    Returns:

    - str: message of the event creation


    """


    try:

        new_id =  "E" + str(len(session.query(EventsDB).all()) + 1)
        event = Event()
        event.name = event_name
        event.id = new_id 
        event.description = event_description 
        event.organizer_id = user_online.id
        event.privated = event_privated

        event.add_to_db()


        organizer = session.query(UsersDB).filter(UsersDB.id == user_online.id).first()
        organizer.organized_events_id = func.array_append(organizer.organized_events_id, event.id)
        session.commit()
        

    
    except Exception as e:
    
        raise HTTPException(status_code=500, detail= f"an error ocurred {str(e)}")

    return {
                "message": "event created successfully"
    }


# ----------------------------------------------------------------


@app.post("/dashboard/create_event/add_password")
def add_password_to_event(event_id:str, password:str, confirm_password:str):

    """
    Main function:

    - add a password to an event

    Steps:


    - if the passwords don't coincide, will be raise an HTTPException (400) 
    - if the passwords coincide, will be add the password to the event


    Parameters:
    - event_id (int): id of the event
    - password (str):  password of the event
    - confirm_password (str):  confirm password of the event

    Raises:

    - HTTPException: if the passwords don't coincide
    - HTTPException: if the event id doesn't exist


    """
   

    events_db = session.query(EventsDB).all()

    event_exists = session.query(EventsDB).filter(UsersDB.id == event_id).first()

    if not password == confirm_password:


        raise HTTPException(status_code=400, detail="The passwords doesn't match")

    else:

        if event_exists:
            hashed_password = hash_password(password)
            event_exists.password = hashed_password
            session.commit()


    return {
            "message": "password added successfully"
    }
  

#----------------------------------------------------------------

@app.post("/dashboard/join_event/public_event")
def join_event_public(id:str):

    """

    Main function:

    - 

    """



    events_db = session.query(EventsDB).all()
    event_exists = session.query(EventsDB).filter(EventsDB.id == id).first()
    try:
        if not event_exists:

            raise HTTPException(status_code=400, detail= "Invalid id, it does not exist")

        else:
            organizer = session.query(UsersDB).filter(UsersDB.id == user_online.id).first()
            organizer.participant_events_id = func.array_append(organizer.participant_events_id, id)
            session.commit()


    except Exception as e:
        raise HTTPException(status_code=400, detail= f"an error ocurred{str(e)}")


    return {
            "Message" : "Event joined succesfully"
        }


#----------------------------------------------------------------

@app.post("/dashboard/join_event/private_event")
def join_event_private(id:str, password:str):

    """

    Main function:

    - 

    """


    
    events_db = session.query(EventsDB).all()
    event_exists = session.query(EventsDB).filter(EventsDB.id == id).first()
    try:

        
        if not event_exists:


            raise HTTPException(status_code=400, detail= "Invalid id, it does not exist")

        elif not Hash_password.verify_password(password, event_exists.password):


            raise HTTPException(status_code=400, detail= "Invalid password")

        else:

            organizer = session.query(UsersDB).filter(UsersDB.id == user_online.id).first()
            organizer.participant_events_id = func.array_append(organizer.participant_events_id, id)
            session.commit()


    except Exception as e:
        raise HTTPException(status_code=400, detail= f"an error ocurred{str(e)}")


    return {
            "Message" : "Event joined succesfully"
        }

#--------------------------------------------------------------------

@app.post("/dashboard/search_event")
def join_event(id:str):

    """

    Main function:

    - 

    """




    events_db = session.query(EventsDB).all()
    event_exists = session.query(EventsDB).filter(EventsDB.id == id).first()
    try:
        if not event_exists:


            raise HTTPException(status_code=400, detail= "Invalid id, it does not exist")


    except Exception as e:
        raise HTTPException(status_code=400, detail= f"an error ocurred{str(e)}")


    return {
            "name": event_exists.name,
            "id": event_exists.id,
            "description": event_exists.description,
            "organizer": event_exists.organizer_id,
            "privated": event_exists.privated,
            "participants": event_exists.participants_id,
            "activities": event_exists.activities_id,
        }

    
        
