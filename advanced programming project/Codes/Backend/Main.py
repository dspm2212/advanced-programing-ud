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
from DashBoard_services import router_dashboard
from fastapi.middleware.cors import CORSMiddleware


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
app.include_router(router_dashboard)

#Declare the actual online user
user_online:User = None

#Database connection
connection = PostgresConnection("Daniel", "perez123", "Virtual_Xperience", 5432, "Virtual_Xperience")

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
        
        session.close()
        return "No hay usuarios"

    elif user_online == None:

     return "Hay usuarios " + str(len(users_db)) 


    else:
        session.close()
        return "Hay usuarios " + str(len(users_db))+ " online user: " + user_online.username


#------------------------------------


@app.post("/register")
def register(username:str, email:str, password:str, password_confirmation:str) -> dict:


    """

    main function:

    - Registers a new user in the database.


    steps:

    - first create an session to de database
    - if the email hasn't an '@' will be raise an HTTPException (400)
    - if the password confirmation doesn't match with the password it will be raise an HTTPException (400)
    - if the username already exists it will be raise an HTTPException (400)
    - if the email already exists it will be raise an HTTPException (400)
    - if the username and the email doesn't exists the user is created and uploadoded to the database.
    - finally, it closes the session

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
    session = connection.Session()

    if '@' not in email:
        session.close()
        raise HTTPException(status_code=400, detail="The email address is not valid")

    elif password != password_confirmation:

        session.close()
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

    finally:
            session.close()

    return {"message":"User Registered Succesfully" }

#--------------------------------------

@app.post("/login")
def login(username:str, password:str) -> dict:
    """
    
    main function:

    - Logs in a user in the database.

    steps:
    
    - first create an session to de database
    - if the username doesn't exists it will be raise an HTTPException (400)
    - if the password doesn't match with the password in the database it will be raise an HTTPException (400)
    - if the username and the password matchs the user is logged in and it values are copied in the user_online attribute
    - finally, it closes the session
    
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

    session = connection.Session()
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

    except Exception as e:

        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

    finally:
        session.close()
    return {"message":"Login successful"}



@app.post("/search_user_by_id")
def search_user_by_id(user_id:str):
    """
    Main function:
    - Searches a user by id in the database.
    Steps:
    - Create a new session
    - if the users id does not exist, will be raise an HTTPException (400)
    - if the users id exists, will be return the user
    - finally, it closes the session
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
    session = connection.Session()
    user_db = session.query(UsersDB).all() 
    try:
        user_exists = session.query(UsersDB).filter(UsersDB.id == user_id).first()
        if not user_exists:
            raise HTTPException(status_code=400, detail= "Invalid user id")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
    finally:
        session.close()
    return {
                "username": user_exists.username,
            "id": user_exists.id,
            "verified": user_exists.verified,
            "email": user_exists.email,
            "uploaded_activities": user_exists.uploaded_activities_id,
            "participant_events": user_exists.participant_events_id,
            "organized_events": user_exists.organized_events_id
        }
    
        
