from passlib.context import CryptContext

#------------------------------------------------------------
def hash_password(password:str) -> str:
    
    """ 
    Main function:
    
    - Is used to hash the password of the user
    Parameters:
    - password (str) the password to be hashed
    Returns:
    - str: the hashed password of the user
    """
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context.hash(password)
# ---------------------------------------------------------------
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """ This method is used to verify the password of the user """
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context.verify(plain_password, hashed_password)