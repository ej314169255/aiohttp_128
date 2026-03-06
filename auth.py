import bcrypt
import jwt

import time
from datetime import timezone, datetime, timedelta

from jwt.exceptions import ExpiredSignatureError, DecodeError


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
    
def decorator(additional_parametr):
    def wrapper(f):
        def new_f(*args, **kwargs):
            print(f"function running at {additional_parametr}")
            print("action before")
            res = f(*args, **kwargs)
            print("action after")
            return res
        return new_f
    return wrapper

@decorator(datetime.now())
def f(param):
    public_key = param["public_key"]
    encoded = param["encoded"]
    
    try:
        print(jwt.decode(encoded, public_key, algorithms=["ES256"]))
    except jwt.InvalidIssuerError:
        print("invalid issuer")
        print("Hello World")
        print(f"I am {name}")

    payload = {"exp": datetime.now(tz=timezone.utc) + timedelta(seconds=600)}
    token = jwt.encode(payload, "secret")
    time.sleep(3)
    # JWT payload is now expired
    # But with some leeway, it will still validate

    try:
        decoded = jwt.decode(token, "secret", leeway=1, algorithms=["HS256"])
        print(f"decoded {decoded}")
        # payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except ExpiredSignatureError:
    # Handle the specific case of an expired token
        print("The token has expired. Please log in again.")
    # Return an appropriate HTTP response (e.g., 401 Unauthorized)
    except DecodeError:
    # Handle other decoding errors (e.g., invalid signature, malformed token)
        print("Invalid token.")
    # Return an appropriate HTTP response (e.g., 400 Bad Request)
    except Exception as e:
    # Handle any other potential exceptions
        print(f"An unexpected error occurred: {e}")
    return param


# name = f({"some": "payload", "iss": "urn:fo5o"})
# print(f.__name__)
# print(name)

# import aiohttp
# import asyncio

# async def main():
#     url = 'http://httpbin.org/post'
#     payload = {'example': 'text', 'value': 123}
#     async with aiohttp.ClientSession() as session:
#         async with session.post(url, json=payload) as resp:
#             print(await resp.text())

# if __name__ == '__main__':
#     asyncio.run(main())
