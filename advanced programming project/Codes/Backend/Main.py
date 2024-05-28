"""
This module contains the Main of the application.

Authors:

Sergio Nicolás Mendivelso  <snmendivelsom@udistrital.edu.co>

Daniel Santiago Pérez <dsperezm@udistrital.edu.co> 

"""

#----------------------------------------------------------------

from fastapi import FastAPI, HTTPException
from Users.Users import User, UsersDB, connection
from db_conection import PostgresConnection


#Starts the app

user_online:User = None
app = FastAPI()


#==================================== METHODS =================================


@app.get("/")
def test():


    """
    Simple test to verify that the database connection is working

    """

    session = connection.Session()
    
    users_db = session.query(UsersDB).all()

    if not users_db:
        
        session.close()
        return "No hay usuarios"

    else:
        session.close()
        return "Hay usuarios " + str(len(users_db)) + " online user: " + user_online.username



#------------------------------------


@app.post("/register/")
def register(username:str, email:str, password:str, password_confirmation:str) -> str:


    """

    main function:

    - Registers a new user in the database.


    steps:

    -first create an session to de database
    -if the email hasn't an '@' will be raise an HTTPException (400)
    -if the username already exists it will be raise an HTTPException (400)
    -if the email already exists it will be raise an HTTPException (400)
    -if the username and the email doesn't exists the user is created and uploadoded to the database.
    -finally, it closes the session

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
            hashed_pass = User.hash_password(password=password)
            new_id =  len(user_db) + 1
            user = User(username=username, id = new_id ,password=hashed_pass, email=email)
            user.add_to_db()

    except Exception as e:

        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

    finally:
            session.close()

    return "User Registered Succesfully" 

#--------------------------------------

@app.post("/login/")
def login(username:str, password:str) -> str:
    """
    
    main function:

    - Logs in a user in the database.

    steps:
    
    -first create an session to de database
    -if the password confirmation doesn't match with the password it will be raise an HTTPException (400)
    -if the username doesn't exists it will be raise an HTTPException (400)
    -if the password doesn't match with the password in the database it will be raise an HTTPException (400)
    -if the username and the password matchs the user is logged in.
    -finally, it closes the session
    
    Parameters:
    - username (str): The username of the new user.
    - password (str): The password of the new user.
    - password_confirmation (str): The password confirmation of the new user.
    
    Raises:
    - HTTPException: If the username doesn't exists, or if the password doesn't match.
    
    Returns:
    - str: "User Logged In Succesfully" if the user is logged in successfully.

    """
    global user_online
    session = connection.Session()
    user_db = session.query(UsersDB).all() 


    try:

        user_exists = session.query(UsersDB).filter(UsersDB.username == username).first()

        if not user_exists:

            raise HTTPException(status_code=400, detail= "Invalid username or password")

        elif not User.verify_password(password, user_exists.password):
            raise HTTPException(status_code=400, detail="Invalid username or password")

        else: 

            user_exists.verified = True
            user_online = user_exists

    except Exception as e:

        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

    finally:
        session.close()

    return "Login successful"
        
