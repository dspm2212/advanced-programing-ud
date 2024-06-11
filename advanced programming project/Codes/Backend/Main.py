"""
This module contains the main web services of the application.

Authors:

Sergio Nicolás Mendivelso  <snmendivelsom@udistrital.edu.co>

Daniel Santiago Pérez <dsperezm@udistrital.edu.co> 

"""

#----------------------------------------------------------------

from fastapi import FastAPI, HTTPException, APIRouter
from Users.Users import User, UsersDB, Base
from Events_activities.Event import Event, EventsDB
from Events_activities.Activity import Activity, ActivitiesDB
from db_conection import PostgresConnection
from Hash_password import hash_password, verify_password
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import func
from datetime import datetime,timezone, timedelta
import json



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
Base.metadata.create_all(bind=connection.engine, tables=[ActivitiesDB.__table__])

#==================================== SERVICES =================================

@app.post("/home/register")
def register(username: str, email: str, password: str, password_confirmation: str) -> dict:
    """
    Main function:

    - Registers a new user in the database.

    Steps:

    - Validates the email format to ensure it contains an '@', otherwise raises an HTTPException (400).
    - Verifies that the password and password confirmation match, otherwise raises an HTTPException (400).
    - Checks if the username already exists in the database, and if so, raises an HTTPException (400).
    - Checks if the email already exists in the database, and if so, raises an HTTPException (400).
    - If the username and email do not exist, hashes the password, creates a new user, and uploads it to the database.

    Parameters:

    - username (str): The username of the new user.
    - email (str): The email of the new user.
    - password (str): The password of the new user.
    - password_confirmation (str): The password confirmation.

    Raises:

    - HTTPException: If the email address is not valid 
    - HTTPException: if the passwords do not match 
    - HTTPException: if the username already exists 
    - HTTPException: if the email already exists.

    Returns:
    
    - dict: Contains a message indicating the result of the registration process.
        - "The email address is not valid" if the email does not contain an '@'.
        - "The passwords don't match" if the passwords do not match.
        - "The username already exists" if the username already exists.
        - "The email already exists" if the email already exists.
        - "User Registered Successfully" if the user is registered successfully.

    Example:

    ```
    register("new_user", "new_user@example.com", "password123", "password123")

    ```

    """

    # Check if the email contains an '@'

    if '@' not in email:

        raise HTTPException(status_code=400, detail="The email address is not valid")

    # Check if the password matches the password confirmation

    elif password != password_confirmation:

        raise HTTPException(status_code=400, detail="The passwords don't match")

    try:

        # Retrieve all users from the database
        user_db = session.query(UsersDB).all()      


        # Check if the username already exists
        user_exists = session.query(UsersDB).filter(UsersDB.username == username).first()


        # Check if the email already exists
        email_exists = session.query(UsersDB).filter(UsersDB.email == email).first()


        if user_exists:

            raise HTTPException(status_code=400, detail="The username already exists")


        elif email_exists:

            raise HTTPException(status_code=400, detail="The email already exists")

        else:
            # Hash the password
            hashed_pass = hash_password(password=password)


            # Generate a new user id
            new_id = "U" + str(len(user_db) + 1)


            # Create a new user object
            user = User()
            user.username = username 
            user.id = new_id
            user.password = hashed_pass 
            user.email = email


            # Add the new user to the database
            user.add_to_db()


    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

    # Return a success message

    return {"message": "User Registered Successfully"}

#--------------------------------------

@app.post("/home/login")
def login(email: str, password: str) -> dict:
    """
    Main function:

    - Logs in a user from the database.

    Steps:

    - Checks if the email exists in the database, otherwise raises an HTTPException (400).
    - Verifies that the provided password matches the stored password, otherwise raises an HTTPException (400).
    - If the email and password match, logs in the user and updates the `user_online` attribute.

    Parameters:

    - email (str): The email of the user.
    - password (str): The password of the user.

    Raises:

    - HTTPException: If the email doesn't exist 
    - HTTPException: If the password doesn't match.

    Returns:

    - dict: Contains a message indicating the result of the login process.
        - "Invalid email or password" if the user doesn't exist or if the password is incorrect.
        - "User Logged In Successfully" if the user is logged in successfully.

    Example:

    ```
    login("email@email.com", "password123")

    ```

    """

    global user_online

    # Retrieve all users from the database

    user_db = session.query(UsersDB).all() 

    try:

        # Check if the user exists by email
        user_exists = session.query(UsersDB).filter(UsersDB.email == email).first()

        if not user_exists:

            raise HTTPException(status_code=400, detail="Invalid email or password")

        # Verify if the provided password matches the stored password
        elif not verify_password(password, user_exists.password):

            raise HTTPException(status_code=400, detail="Invalid email or password")

        else:


            # Set the user's verified status to True
            user_exists.verified = True
            

            # Update the global user_online to the logged-in user
            user_online = user_exists
            

            # Commit the changes to the database
            session.commit()
            print(user_online.id)


    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


    # Return a success message
    return {"message": "User Logged In Successfully"}

#=================================================== DASHBOARD SERVICES ===============================

#======================================== EVENT SERVICES ====================================

@app.post("/dashboard/{online_user.id}/create_event/public")
def create_event(event_name: str, event_description: str) -> dict:
    """
    Main function:

    - Creates a public event.

    Steps:

    - Generates a new event ID.
    - Creates a new event with the provided name and description.
    - Sets the organizer ID to the currently logged-in user.
    - Adds the event to the database.
    - Updates the organizer's list of organized events.
    - Commits the changes to the database.

    Parameters:

    - event_name (str): The name of the event.
    - event_description (str): The description of the event.

    Raises:

    - HTTPException: If an error occurs while creating the event.

    Returns:

    - dict: Contains a message indicating the result of the event creation.
        - "event created successfully" if the event is created successfully.

    Example:

    ```
    create_event("Event Name", "Event Description")

    ```

    """
    global user_online

    try:

        
        # Generate a new event ID
        new_id = "E" + str(len(session.query(EventsDB).all()) + 1)
        

        # Create a new event object
        event = Event()
        event.name = event_name
        event.id = new_id
        event.description = event_description
        event.organizer_id = user_online.id
        event.privated = False


        # Add the new event to the database
        event.add_to_db()


        # Retrieve the organizer from the database
        organizer = session.query(UsersDB).filter(UsersDB.id == user_online.id).first()
        
        
        # Update the organizer's list of organized events
        organizer.organized_events_id = func.array_append(organizer.organized_events_id, event.id)
        

        # Commit the changes to the database
        session.commit()


    except Exception as e:


        # Raise an HTTPException if an error occurs
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


    # Return a success message
    return {"message": "event created successfully"}


# ----------------------------------------------------------------

@app.post("/dashboard/{online_user.id}/create_event/privated")
def create_event(event_name: str, event_description: str, password: str, password_confirmation: str) -> dict:
    """
    Main function:

    - Creates a private event.

    Steps:

    - Verifies that the password and password confirmation match, otherwise raises an HTTPException (400).
    - Generates a new event id.
    - Creates a new event with the provided name, description, and hashed password.
    - Sets the organizer id to the currently logged-in user.
    - Adds the event to the database.
    - Updates the organizer's list of organized events.
    - Commits the changes to the database.

    Parameters:

    - event_name (str): The name of the event.
    - event_description (str): The description of the event.
    - password (str): The password for the private event.
    - password_confirmation (str): The confirmation of the password for the private event.

    Raises:

    - HTTPException: If the passwords do not match.
    - HTTPException: If an error occurs while creating the event.

    Returns:

    - dict: Contains a message indicating the result of the event creation.
        - "Passwords don't match" if the passwords do not match.
        - "event created successfully" if the event is created successfully.

    Example:

    ```
    create_event("Event Name", "Event Description", "Password123", "Password123")

    ```

    """

    global user_online

    try:


        # Check if the password matches the password confirmation
        if password != password_confirmation:


            raise HTTPException(status_code=400, detail="Passwords don't match")

        # Generate a new event ID
        new_id = "E" + str(len(session.query(EventsDB).all()) + 1)

        
        # Create a new event object
        event = Event()
        event.name = event_name
        event.id = new_id
        event.description = event_description
        event.password = hash_password(password)
        event.organizer_id = user_online.id
        event.privated = True


        # Add the new event to the database
        event.add_to_db()


        # Retrieve the organizer from the database
        organizer = session.query(UsersDB).filter(UsersDB.id == user_online.id).first()
        

        # Update the organizer's list of organized events
        organizer.organized_events_id = func.array_append(organizer.organized_events_id, event.id)
        

        # Commit the changes to the database
        session.commit()


    except Exception as e:


        # Raise an HTTPException if an error occurs
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


    # Return a success message
    return {"message": "event created successfully"}

#----------------------------------------------------------------

@app.post("/dashboard/{online_user.id}/join_event/public_event")
def join_event(id: str)->dict:
    """
    Main function: Join a public event

    Steps:

    - If the event's id doesn't exist, raise an HTTPException (400)
    - If the event's id is already associated with the user (if the events is in the participant or organized event lists), raise an HTTPException (400)
    - If the event's privacy is True, raise an HTTPException (400)
    - If the event's id exists, add the event id to the participant_events_id of the user_online attribute

    Parameters:

    - id (str): ID of the event

    Raises:

    - HTTPException: If the event's id doesn't exist
    - HTTPException: If the event's id is already in the organized events list
    - HTTPException: If the event's id is already in the participant events list
    - HTTPException: If the event's privacy is True

    Returns:

    - str: "Invalid id, it does not exist" if the event id doesn't exist
    - str: "Invalid, the user is the organizer of the event" if the event's id is already in the organized events list
    - str: "Invalid, the user is already a participant of the event" if the event's id is already in the participant events list
    - str: "Invalid id" if the event's privacy is True
    - dict: Message of the join successfully

    Example:
    ```
    join_event("E30")

    ```

    """

    # Check if the event exists in the database
    event_exists = session.query(EventsDB).filter(EventsDB.id == id).first()


    try:

        if not event_exists:

            # Raise exception if the event does not exist
            raise HTTPException(status_code=400, detail="Invalid id, it does not exist")


        elif event_exists.privated == True:

            # Raise exception if the event is private
            raise HTTPException(status_code=400, detail="Invalid id, it is not a public event")
        

        elif id in user_online.organized_events_id:

            # Raise exception if the user is the organizer of the event
            raise HTTPException(status_code=400, detail="Invalid, the user is the organizer of the event")


        elif id in user_online.participant_events_id:

            # Raise exception if the user is already a participant of the event
            raise HTTPException(status_code=400, detail="Invalid, the user is already a participant of the event")


        else:

            # Update participant and event tables with new associations
            participant = session.query(UsersDB).filter(UsersDB.id == user_online.id).first()
            participant.participant_events_id = func.array_append(participant.participant_events_id, id)
            event_exists.participants_id = func.array_append(event_exists.participants_id, participant.id)
            session.commit()


    except Exception as e:


        # Raise exception if any error occurs
        raise HTTPException(status_code=400, detail=f"an error occurred: {str(e)}")


    # Return success message if the event is joined successfully
    return {
        "Message": "Event joined successfully"
    }
#----------------------------------------------------------------

@app.post("/dashboard/{online_user.id}/join_event/private_event")
def join_event(id: str, password: str) -> dict:
    """
    Main function: Join a private event

    Steps:

    - If the event id doesn't exist, raise an HTTPException (400)
    - If the event privacy is False, raise an HTTPException (400)
    - If the password doesn't match, raise an HTTPException (400)
    - If the event id exists, add the event id to the participant_events_id of the user_online attribute

    Parameters:

    - id (str): ID of the event
    - password (str): Password of the event

    Raises:

    - HTTPException: If the event id doesn't exist
    - HTTPException: If the event's id is already in the organized events list
    - HTTPException: If the event's id is already in the participant events 
    - HTTPException: If the event privacy is False 
    - HTTPException: If the password doesn't match

    Returns:

    - str: "Invalid id, it does not exist" if the event id doesn't exist
    - str: "Invalid, the user is the organizer of the event" if the event's id is already in the organized events list
    - str: "Invalid, the user is already a participant of the event" if the event's id is already in the participant events list
    - str: "Invalid id" if the event privacy is False
    - str: "Invalid password" if the password doesn't match
    - dict: Message of the join successfully

    Example:
    ```
    join_event("E30", "correct_password")

    ```

    """

    # Check if the event exists in the database
    event_exists = session.query(EventsDB).filter(EventsDB.id == id).first()

    try:

        if not event_exists:

            # Raise exception if the event does not exist
            raise HTTPException(status_code=400, detail="Invalid id, it does not exist")


        elif id in user_online.organized_events_id:

            # Raise exception if the user is the organizer of the event
            raise HTTPException(status_code=400, detail="Invalid, the user is the organizer of the event")


        elif event_exists.privated == False:

            # Raise exception if the event is not private
            raise HTTPException(status_code=400, detail="Invalid id, it is not a private event")


        elif id in user_online.participant_events_id:


            # Raise exception if the user is already a participant of the event
            raise HTTPException(status_code=400, detail="Invalid, the user is already a participant of the event")


        elif not verify_password(password, event_exists.password):


            # Raise exception if the password doesn't match
            raise HTTPException(status_code=400, detail="Invalid password")

        else:


            # Update participant and event tables with new associations
            participant = session.query(UsersDB).filter(UsersDB.id == user_online.id).first()
            participant.participant_events_id = func.array_append(participant.participant_events_id, id)
            event_exists.participants_id = func.array_append(event_exists.participants_id, participant.id)
            session.commit()

    except Exception as e:

        # Raise exception if any error occurs
        raise HTTPException(status_code=400, detail=f"an error occurred: {str(e)}")


    # Return success message if the event is joined successfully
    return {
        "Message": "Event joined successfully"
    }


#--------------------------------------------------------------------

@app.get("/dashboard/{online_user.id}/show_public_events")
def show_public_events() -> dict:

    """
    Main function: Shows all the public events in the database.

    Steps:

    - Get all the public events in the database.
    - Return all the public events in the database.

    Parameters:

    - None

    Returns:

    - list: All the dictionary of the public events info in the database.

    """

    # save all public events from the database where it privacy is False

    public_events = session.query(EventsDB).filter(EventsDB.privated == False).all()

    return {
        "Public Events": [
            {
                "name": event.name,
                "id": event.id,
                "description": event.description,
                "organizer": event.organizer_id,
                "privated": event.privated,
                "participants": event.participants_id,
                "activities": event.activities_id,
                "material": event.material
            }
            for event in public_events
        ]
    }



#--------------------------------------------------------------------

@app.get("/dashboard/{online_user.id}/show_private_events")
def show_private_events() -> dict:

    """
    Main function: Shows all the private events in the database.

    Steps:

    - Get all the private events in the database.
    - Return all the private events in the database.

    Parameters:

    - None

    Returns:

    - list: All the dictionary of the private events info in the database (Except password).
    """

    # save all private events from the database where it privacy is True
    private_events = session.query(EventsDB).filter(EventsDB.privated == True).all()

    return {
        "Private Events": [
            {
                "name": event.name,
                "id": event.id,
                "description": event.description,
                "organizer": event.organizer_id,
                "privated": event.privated,
                "participants": event.participants_id,
                "activities": event.activities_id,
                "material": event.material
            }

            for event in private_events
        ]
    }


    
#================================================== ACTIVITIES SERVICES ===========================

@app.post("/dashboard/{online_user.id}/{event_id}/create_activity")
def create_activity(name: str, description: str, event_id: str, end_day: int, end_month: int, end_year: int) -> dict:

    """
    Main function: Create a new activity in the database.

    Steps:

    - Check if the online user is the organizer of the event, if not, raise an HTTPException (400)
    - Create a new activity and add it to the database.
    - Return a message indicating success of the creation.

    Parameters:

    - name (str): Name of the activity
    - description (str): Description of the activity
    - event_id (str): id of the event
    - end_day (int): Final day for the delivery of the activity
    - end_month (int): Final month for the delivery of the activity
    - end_year (int): Final year for the delivery of the activity

    Raises:

    - HTTPException: If the user is not the organizer of the event

    Returns:

    - dict: Message of the activity creation successfully

    Example:
    ```
    create_activity("activity name", "This is an activity", "event_id", 12, 6, 2025)

    ```

    """
    try:


        # Retrieve the event from the database
        event = session.query(EventsDB).filter(EventsDB.id == event_id).first()


        # Check if the online user is the organizer of the event
        if not online_user.id == event.organizer_id:

            raise HTTPException(status_code=400, detail="Invalid, the user is not the organizer of the event")


        # Define the hour difference between the time zones
        gmt_minus_5_offset = timedelta(hours=-5)


        # Obtain the current hour in UTC and adjust it to GMT-5
        start_date_gmt_minus_5 = datetime.utcnow() + gmt_minus_5_offset


        # Define the final date of the activity
        final_date = datetime(end_year, end_month, end_day, 23, 59, 59)


        # Create the new activity
        new_id = "A" + str(len(session.query(ActivitiesDB).all()) + 1)
        activity = Activity()
        activity.id = new_id
        activity.name = name
        activity.description = description
        activity.event_id = event_id
        activity.start_date = start_date_gmt_minus_5.strftime('%Y-%m-%d %H:%M:%S')
        activity.final_date = final_date.strftime('%Y-%m-%d %H:%M:%S')


        # Update the event with the new activity
        event.activities_id = func.array_append(event.activities_id, new_id)


        # Add the activity to the database
        activity.add_to_db()
        session.commit()

        return {
            "Message": "Activity created successfully"
        }
    except Exception as e:


        # Raise exception if any error occurs
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


#----------------------------------------------------------------

@app.get("dashboard/calendar/{online_user.id}/show_activities")
def show_pending_activities_actual_user() -> dict:

    """
    Main function: Shows the pending activities of the currently online user.

    Steps:

    - Get the list of activity ids for the user online.
    - Recognize each activity from the database.
    - Return the details of each activity of the user.

    Parameters:

    - user_id (str): The user's id.

    Returns:

    - dict: A dictionary containing the activities info for the user online.

    """
    
    try:


        # Obtain the user online
        global user_online


        if not user_online:


            # Raise exception if user not found
            raise HTTPException(status_code=404, detail="User not found")

        activities_info = []


        # Iterate through the participant events of the user
        for event_id in user_online.participant_events_id:


            # Retrieve the event from the database
            event = session.query(EventsDB).filter(EventsDB.id == event_id).first()

            if event:


                # Iterate through the activities of the event
                for activity_id in event.activities_id:


                    # Retrieve the activity from the database
                    activity = session.query(ActivitiesDB).filter(ActivitiesDB.id == activity_id).first()


                    if activity:

                        activities_info.append({
                            "name": activity.name,
                            "id": activity.id,
                            "description": activity.description,
                            "deliveries": activity.deliveries,
                            "event_id": activity.event_id,
                            "start_date": activity.start_date,
                            "final_date": activity.final_date,
                            "at_time_list": activity.at_time_list
                        })


                    # Remove uploaded activities from the list
                    if activity.id in user_online.uploaded_activities:

                        activities_info.remove(len(activities_info)-1)


        return {"Activities": activities_info}
    except Exception as e:


        # Raise exception if any error occurs
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


#----------------------------------------------------------------

@app.get("/dashboard/{online_user.id}/{event_id}/show_activities")
def show_activities_event(event_id: str) -> dict:

    """
    Main function: Shows all the activities of a specific event.

    Steps:

    - Get all the activities of a specific event.
    - Return all the activities of a specific event.

    Parameters:

    - event_id (str): id of the event

    Returns:

    - list: All the dictionary of the activities info in the database.

    Example:

    ```
    show_activities_event("E30")

    ```
    """

    # Retrieve the event from the database
    event = session.query(EventsDB).filter(EventsDB.id == event_id).first()


    if not event:


        # Raise exception if event not found
        raise HTTPException(status_code=404, detail="Event not found")


    # Retrieve all activities related to the event from the database
    activities = session.query(ActivitiesDB).filter(ActivitiesDB.event_id == event_id).all()

    return {
        "Activities": [
            {
                "name": activity.name,
                "id": activity.id,
                "description": activity.description,
                "deliveries": activity.deliveries,
                "event_id": activity.event_id,
                "start_date": activity.start_date,
                "final_date": activity.final_date,
                "at_time_list": activity.at_time_list

            }
            
            for activity in activities
        ]
    }


#----------------------------------------------------------------


@app.post("/{activity_id}/upload_activity")
def upload_activity(activity_id:str, file_name:str) -> dict:

    """
    Main function: Upload a file to the activity and mark it as sent.

    Steps:

    - Get the activity from the database.
    - Upload the file to the activity.
    - Mark the file as sent.

    Parameters:

    - activity_id (str): id of the activity
    - file_name (str): Name of the file to upload

    Returns:

    - dict: Message of the activity upload successfully

    Example:

    ```
    upload_activity("A30", "file.txt")

    ```

    """


    # Retrieve the activity from the database
    activity = session.query(ActivitiesDB).filter(ActivitiesDB.id == activity_id).first()


    # Retrieve the user from the database
    user = session.query(UsersDB).filter(UsersDB.id == user_online.id).first()


    # Create a new delivery record


    new_delivery = {
        "file_name": file_name,
        "user": user_online.username,
        "id": user_online.id
    }


    # Append the new delivery to the activity's deliveries list
    activity.deliveries = func.array_append(activity.deliveries, json.dumps(new_delivery))


    # Update the user's uploaded activities list
    user.uploaded_activities_id = func.array_append(user.uploaded_activities_id, activity.id)


    # Obtain the current time
    current_time = datetime.now(timezone(timedelta(hours=-5)))


    # Obtain the final date of the activity
    final_date = datetime.strptime(activity.final_date, "%Y-%m-%d %H:%M:%S")
    final_date = final_date.replace(tzinfo=timezone(timedelta(hours=-5)))


    if current_time < final_date:


        # If the delivery is on time, append user id to at_time_list of activity
        activity.at_time_list = func.array_append(activity.at_time_list, user.id)
        session.commit()


        return {"message": "Activity uploaded successfully, it was uploaded on time"}
    else:


        # If the delivery is out of time, return message accordingly
        session.commit()
        return {"message": "Activity uploaded successfully, delivery out of time"}


#----------------------------------------------------------------

@app.get("/{activity_id}/show_deliveries")
def show_deliveries(activity_id: str) -> dict:
    """
    Main function: Shows all the deliveries of a specific activity.

    Steps:

    - Get all the deliveries of a specific activity and return them.

    Parameters:

    - activity_id (str): id of the activity

    Returns:

    - list: All the dictionary of the deliveries info in the database.

    Example:

    ```
    show_deliveries("A30")

    ```

    """

    # Retrieve the activity from the database
    activity = session.query(ActivitiesDB).filter(ActivitiesDB.id == activity_id).first()

    if not activity:

        # Raise exception if activity not found or it has no deliveries
        raise HTTPException(status_code=404, detail="Activity not found or it has no deliveries")


    # Return list of deliveries for the activity
    return {
        "Deliveries" : [
        json.loads(delivery)
        for delivery in activity.deliveries
    ]
    }
#----------------------------------------------------------------

@app.post("/dashboard/{online_user.id}/{event_id}/add_comment")
def add_comment_to_event(event_id: str, file_name: str, comment: str) -> dict:

    """

    Main function: Add a comment to an event.

    Steps:

    - Get the event from the database.
    - Take the file name, comment, and the user who wrote it, and upload to the event's comments.

    Parameters:

    - event_id (str): id of the event
    - file_name (str): Name of the file that will be uploaded
    - comment (str): The comment that will be uploaded

    Returns:

    - dict: Message of the comment upload successfully

    Example:
    ```
    add_comment_to_event("E30", "file.txt", "This is a Comment")

    ```

    """


    # Retrieve the event from the database
    event = session.query(EventsDB).filter(EventsDB.id == event_id).first()


    # Create a new comment record
    new_comment = {
        "file_name": file_name,
        "comment": comment,
        "user": user_online.username,
        "id user": user_online.id
    }


    # Append the new comment to the event's comments list
    event.comments = func.array_append(event.comments, json.dumps(new_comment))


    # Commit the changes to the database
    session.commit()

    return {"Message": "Comment uploaded correctly"}

#----------------------------------------------------------------

@app.get("/dashboard/{online_user.id}/{event_id}/show_comments")
def show_comments_event(event_id: str) -> dict:

    """
    Main function: Shows all the comments of a specific event.

    Steps:

    - Get all the comments of a specific event.
    - Return all the comments of a specific event.

    Parameters:

    - event_id (str): id of the event

    Returns:

    - dict: All the dictionary of the comments info in the database.

    Example:

    ```
    show_comments_event("E30")

    ```

    """

    # Retrieve the event from the database
    event = session.query(EventsDB).filter(EventsDB.id == event_id).first()

    if not event:

        # Raise exception if event not found
        raise HTTPException(status_code=404, detail="Event not found")

    # Return list of comments for the event

    return {"Comments": [
        json.loads(comment)
        for comment in event.comments
    ]}
#====================================== DEVELOPER TOOLS =================================

#----------------------------------------------------------------

@app.get("/dev_tool/search_user_by_id")
def search_user_by_id(user_id: str) -> dict:
    """
    Main function: Searches a user by id in the database.

    Steps:
    - Check if the user id exists in the database.
    - Return the user data if the user id exists.

    Parameters:
    - user_id (str): The id of the user.

    Raises:
    - HTTPException: If the user id doesn't exist.

    Returns:
    - str: "Invalid user id" if the user id doesn't exist.
    - dict: User info except password if the user id exists.

    Example:
    ```
    search_user_by_id("U30")
    ```

    """

    try:

        # Check if the user id exists in the database

        user_exists = session.query(UsersDB).filter(UsersDB.id == user_id).first()

        if not user_exists:

            raise HTTPException(status_code=400, detail="Invalid user id")

    except Exception as e:

        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

    # Return user info

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

@app.get("/dev_tool/show_users")
def show_users() -> dict:

    """
    Main function: Shows all the users in the database.

    Steps:
    
    - Get all the users in the database.
    - Return all the users in the database.

    Parameters:

    - None

    Returns:

    - dict: All the dictionary of the users info in the database (Except password).

    """


    # Retrieve all users from the database
    users = session.query(UsersDB).all()


    # Construct a list of user info dictionaries
    users_info = [
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


    # Return the list of user info dictionaries
    return {"users": users_info}



#--------------------------------------------------------------------

@app.get("/dev_tool/search_event_by_id")
def search_event_by_id(id:str) -> dict:
    
    """
    Main function: Search an event by id.

    Steps:

    - Check if the event id exists in the database, otherwise raise an HTTPException (400).
    - If the event id exists, return the event info, except password.

    Parameters:

    - id (str): id of the event.

    Raises:

    - HTTPException: If the event id doesn't exist.

    Returns:

    - dict: Contains the event info if the event id exists.
    - "Invalid id, it does not exist" if the event id doesn't exist.

    Example:

    ```
    search_event_by_id("E30")

    ```

    """


    # Retrieve all events from the database
    events_db = session.query(EventsDB).all()


    # Check if the event id exists
    event_exists = session.query(EventsDB).filter(EventsDB.id == id).first()

    try:
        if not event_exists:

            # Raise an HTTPException if the event id doesn't exist
            raise HTTPException(status_code=400, detail= "Invalid id, it does not exist")


    except Exception as e:

        # Raise an HTTPException if any error occurs
        raise HTTPException(status_code=400, detail= f"An error occurred: {str(e)}")


    # Return the event info if the event id exists
    return {
        "name": event_exists.name,
        "id": event_exists.id,
        "description": event_exists.description,
        "organizer": event_exists.organizer_id,
        "privated": event_exists.privated,
        "participants": event_exists.participants_id,
        "activities": event_exists.activities_id,
    }

#----------------------------------------------------------------

@app.get("/dev_tool/show_activities")
def show_activities() -> dict:

    """
    Main function: Shows all the activities in the database.

    Steps:

    - Retrieve all the activities from the database.
    - Return all the activities in the database.

    Parameters:

    - None

    Returns:

    - dict: Contains a list of dictionaries representing the activities info in the database.

    """

    # Retrieve all activities from the database
    activities = session.query(ActivitiesDB).all()


    # Create a list of dictionaries containing the activities info
    return {
        "Activities": [
            {
                "name": activity.name,
                "id": activity.id,
                "description": activity.description,
                "deliveries": activity.deliveries,
                "event_id": activity.event_id,
                "start_date": activity.start_date,
                "final_date": activity.final_date,
                "at_time_list": activity.at_time_list
            }
            for activity in activities
        ]
    }
