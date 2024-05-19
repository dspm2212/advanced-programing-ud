from fastapi import  FastAPI
from Users.Users import Participant, UsersDB
from db_conection import PostgresConnection


app = FastAPI()

 
@app.get("/")
def test():
    
   # connection = PostgresConnection("Daniel", "perez123", "localhost", 5432, "Virtual_Xperience")
   # session = connection.session()
   # users_db  = session.query(UsersDB).all()
   # users_list = []

   # for user in users_db: 
   #     users_list.append(user)

    #if len(users_list)== 0:

        
        return "No hay usuarios"