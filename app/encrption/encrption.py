import bcrypt

def hash_password(password: str):
    salt= bcrypt.gensalt()
    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    return hashed_pw

def verify_password(password: str, hashed_pw: str):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_pw.encode('utf-8'))