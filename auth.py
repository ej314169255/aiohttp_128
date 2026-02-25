import bcrypt


def hash(password: str):

    password = password.encode()
    password = bcrypt.hashpw(password, bcrypt.gensalt())
    password = password.decode()
    return password


def check(password: str, hashed_password: str):
    password = password.encode()
    hashed_password = hashed_password.encode()
    is_correct = bcrypt.checkpw(password, hashed_password)
    return is_correct
