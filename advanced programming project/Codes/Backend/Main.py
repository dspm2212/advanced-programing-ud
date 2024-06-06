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
    - email (str): The email of the new user.
    - password (str): The password of the new user.
    - password_confirmation (str): The password confirmation


    Raises:
    - HTTPException: If the email address is not valid, if the username already exists, or if the email already exists.

    Returns:
    
    - str: "The email address is not valid" , if the email has not an '@' 
    - str: "The passwords doesn't match" if the passwords do not match
    - str: "The username already exists" if the username already exists
    - str: "The email already exists" if the email already exists
    - dict: "User Registered Succesfully" if the user is registered successfully.

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
def login(email:str, password:str) -> dict:
    """
    
    main function:

    - Logs in a user in the database.

    steps:
    

    - if the email doesn't exists it will be raise an HTTPException (400)
    - if the password doesn't match with the password in the database it will be raise an HTTPException (400)
    - if the email and the password matchs the user is logged in and it values are copied in the user_online attribute

    
    Parameters:

    - email (str): The email of the user.
    - password (str): The password of the user.

    
    Raises:

    - HTTPException: If the email doesn't exists, or if the password doesn't match.
    
    Returns:

    - str: "Invalid email or password" if the user doesn't exist or if the password is incorrect. 
    - dict: "User Logged In Succesfully" if the user is logged in successfully.

    Example:

     ```
     login("email@email.com", "password123")

      ```

    """

    global user_online

    user_db = session.query(UsersDB).all() 


    try:

        user_exists = session.query(UsersDB).filter(UsersDB.email == email).first()

        if not user_exists:

            raise HTTPException(status_code=400, detail= "Invalid email or password")

        elif not verify_password(password, user_exists.password):

            raise HTTPException(status_code=400, detail="Invalid email or password")

        else: 

            user_exists.verified = True
            user_online = user_exists
            session.commit()
            print(user_online.id)

    except Exception as e:

        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

    return {"message":"User Logged In Succesfully"}


#----------------------------------------------------------------

@app.post("/search_user_by_id")
def search_user_by_id(user_id:str):
    """
    Main function:

    - Searches a user by id in the database.

    Steps:

    - if the users id does not exist, will be raise an HTTPException (400)
    - if the users id exists, will be return the user data 

    Parameters:

    - user_id (int): The id of the user.

    Raises:
    
    - HTTPException: If the user id doesn't exists.
    
    Returns:

    - str: "Invalid user id" if the user id doesn't exists
    - dict: user info except password if the user id exists

    Example:
    
    ```
    search_user_by_id(U30)
     ```

    """

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

#----------------------------------------------------------------

@app.get("/show_users")
def show_users():

    """

    Main function:

    - Shows all the users in the database.

    Steps:

    - get all the users in the database.
    - return all the users in the database.

    Parameters:

    - None

    Returns:

    - list: all the dictionary of the users info in the database (Except password).

    """

    users = session.query(UsersDB).all()

    return {
        "users": [
            {
                "username": user.username,
                "id": user.id,
                "verified": user.verified,
                "email": user.email,
                "uploaded_activities": user.uploaded_activities_id,
                "participant_events": user.participant_events_id,
                "organized_events": user.organized_events_id
            }
            for user in users
        ]
    }
#=================================================== DASHBOARD SERVICES ===============================

#======================================== EVENT SERVICES ====================================

@app.post("/dashboard/create_event/public")
def create_event(event_name:str,  event_description:str):

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

    - dict: message of the event creation

    Example:
    
    ```
    create_event ("E30", "Description")
     ```

    """
    global user_online


    try:

        new_id =  "E" + str(len(session.query(EventsDB).all()) + 1)
        event = Event()
        event.name = event_name
        event.id = new_id 
        event.description = event_description 
        event.organizer_id = user_online.id
        event.privated = False

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

@app.post("/dashboard/create_event/privated")
def create_event(event_name:str,  event_description:str, password: str, password_confirmation:str):

    """
    Main function:

    - create a private event

    Steps:


    - update the tables with the actual attributes of the event
    - add it the table to the database


    Parameters:

    - event_name (str): name of the event
    - event_description (str): description of the event

    Raises:

    - HTTPException: if the passwords don't match (400).
    - HTTPException: if an error ocurred while creating the event.

    Returns:

    - str: "Passwords don't match" if passwords do not match.
    - dict: message of the event creation

    Example:

    ```
    
    create_event("Name", "Description", "Password", "Password")


     ```


    """


    try:

        if not password == password_confirmation:

            raise HTTPException(status_code=400, detail= "Passwords don't match")


        new_id =  "E" + str(len(session.query(EventsDB).all()) + 1)
        event = Event()
        event.name = event_name
        event.id = new_id 
        event.description = event_description
        event.password = hash_password(password)
        event.organizer_id = user_online.id
        event.privated = True

        event.add_to_db()


        organizer = session.query(UsersDB).filter(UsersDB.id == user_online.id).first()
        organizer.organized_events_id = func.array_append(organizer.organized_events_id, event.id)
        session.commit()
        

    
    except Exception as e:
    
        raise HTTPException(status_code=500, detail= f"an error ocurred {str(e)}")

    return {
                "message": "event created successfully"
    }



#----------------------------------------------------------------

@app.post("/dashboard/join_event/public_event")
def join_event(id:str):

    """

    Main function: Join a public event

    Steps:

    - if the event's  id doesn't exist, will be raise an HTTPException (400)
    - if the event's id is already associated with the user (if the events is in the participant o organaized event lists), will be raise an HTTPException (400)
    - if the event's privacy is True, will be raise an HTTPException (400)
    - if the event's id exists, will be add the event id to the participant_events_id of the user_online attribute

    Parameters:

    - event_id (str): id of the event
    - password (str):  password of the event
    - confirm_password (str):  confirm password of the event

    Raises:

    - HTTPException: if the event's id doesn't exist
    - HTTPException: if the event's id is already  in the organaized events lists
    - HTTPException: if the event's id is already  in the participant events 
    - HTTPException: if the event's  privacy is True 

    Returns:

    - str: "Invalid id, it does not exist" if the event id doesn't exist
    - str: "Invalid, the user is the organizer of the event" if the event's id is already  in the organized events list
    - str: "Invalid, the user is already a participant of the event" if the event's id is already in the participant events list
    - str: "Invalid id" if the event's privacy is True
    - dict: Message of the join succesfully

    Example:

    ```
    
    join_event("U30")


     ```

    """

    event_exists = session.query(EventsDB).filter(EventsDB.id == id).first()

    try:
        if not event_exists:

            raise HTTPException(status_code=400, detail= "Invalid id, it does not exist")

        elif id in user_online.organized_events_id:

            raise HTTPException(status_code=400, detail= "Invalid, the user is the organizer of the event")

        elif id in user_online.participant_events_id:

            raise HTTPException(status_code=400, detail= "Invalid, the user is already a participant of the event")

        elif event_exists.privated == True:

            raise HTTPException(status_code=400, detail= "Invalid id, it is not a public event")

        else:
            participant = session.query(UsersDB).filter(UsersDB.id == user_online.id).first()
            participant.participant_events_id = func.array_append(participant.participant_events_id, id)

            session.commit()


    except Exception as e:
        raise HTTPException(status_code=400, detail= f"an error ocurred{str(e)}")


    return {

            "Message" : "Event joined succesfully"

        }


#----------------------------------------------------------------

@app.post("/dashboard/join_event/private_event")
def join_event(id:str, password:str):

    """

    Main function:

    - Join a private event

    Steps:

    - if the event id doesn't exist, will be raise an HTTPException (400)
    - if the event privacy is False, will be raise an HTTPException (400)
    - if the password doesn't match, will be raise an HTTPException (400)
    - if the event id exists, will be add the event id to the participant_events_id of the user_online attribute

    Parameters:

    - event_id (str): id of the event
    - password (str):  password of the event

    Raises:

    - HTTPException: if the event id doesn't exist
    - HTTPException: if the event's id is already  in the organaized events lists
    - HTTPException: if the event's id is already  in the participant events 
    - HTTPException: if the event privacy is False 
    - HTTPException: if the password doesn't match

    Returns:

    - str: "Invalid id, it does not exist" if the event id doesn't exist
    - str: "Invalid, the user is the organizer of the event" if the event's id is already  in the organized events list
    - str: "Invalid, the user is already a participant of the event" if the event's id is already in the participant events list
    - str: "Invalid id" if the event privacy is False
    - str: "Invalid password" if the password doesn't match
    - dict: Message of the join succesfully

    Example:

    ```

    join_event("U30", "correct_password")

     ```


    """

    event_exists = session.query(EventsDB).filter(EventsDB.id == id).first()
    try:

        
        if not event_exists:

            raise HTTPException(status_code=400, detail= "Invalid id, it does not exist")

        elif id in user_online.organized_events_id:

            raise HTTPException(status_code=400, detail= "Invalid, the user is the organizer of the event")

        elif id in user_online.participant_events_id:

            raise HTTPException(status_code=400, detail= "Invalid, the user is already a participant of the event")

        elif event_exists.privated == False:

            raise HTTPException(status_code=400, detail= "Invalid id, it is not an private event")

        elif not verify_password(password, event_exists.password):


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

@app.post("/dashboard/search_event_by_id")
def search_event_by_id(id:str):

    """

    Main function:

    - Search an event by id

    Steps:

    - if the event id doesn't exist, will be raise an HTTPException (400)
    - if the event id exists, will be return the event info, except password

    Parameters:

    - event_id (str): id of the event

    Raises:

    - HTTPException: if the event id doesn't exist
    
    Returns:

    - str: "Invalid id, it does not exist" if the event id doesn't exist
    - dict: Message of the join succesfully

    Example:

    
    ```

    search_event_by_id("U30")

     ```

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

#--------------------------------------------------------------------

@app.get("/show_public_events")

def show_public_events():

    """
    Main function:

    - Shows all the public events in the database.

    Steps:

    - get all the public events in the database.
    - return all the public events in the database.

    Parameters:

    - None

    Returns:

    - list: all the dictionary of the users info in the database (Except password).

    """

    public_events = session.query(EventsDB).filter(EventsDB.privated == False).all()

    return {
        "Public Events": [
            {

            "name":event.name,
            "id":event.id,
            "description":event.description,
            "organizer":event.organizer_id,
            "privated":event.privated,
            "participants":event.participants_id,
            "activities":event.activities_id,
            "material": event.material

            }
            for event in public_events
        ]
    }

@app.get("/show_private_events")

def show_private_events():

    private_events = session.query(EventsDB).filter(EventsDB.privated == True).all()

    return {
        "Public Events": [
            {
                
            "name":event.name,
            "id":event.id,
            "description":event.description,
            "organizer":event.organizer_id,
            "privated":event.privated,
            "participants":event.participants_id,
            "activities":event.activities_id,
            "material": event.material

            }
            for event in private_events
        ]
    }

    
        
