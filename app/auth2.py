from jose import JWSError, jwt
from datetime import datetime, timedelta
secret_key = "eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6Ik"
algorithm = "HS256"
token_expire_minutes = 30

def create_access_token (data: dict):

    expire_time = datetime.now() + timedelta(minutes=token_expire_minutes)
    data.update({"exp": expire_time}) #payload

    encoded_jwt = jwt.encode(data, secret_key, algorithm=algorithm) #payload, secretkey, header
    return encoded_jwt
