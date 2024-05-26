from fastapi import  FastAPI
from Users.Users import Participant, UsersDB
from db_conection import PostgresConnection


app = FastAPI()

 
@app.get("/")
def test():
    
    connection = PostgresConnection("Daniel", "perez123", "Virtual_Xperience", 5432, "Virtual_Xperience")
    session = connection.session()
    UsersDB.metadata.create_all(bind=connection.engine)
    users_db  = session.query(UsersDB).all()
    users_list = []

    for user in users_db: 
        users_list.append(user)

    if len(users_list)== 0:

        
        return "No hay usuarios"
        

    else: 

        return "Hay usuarios"