from typing import Union

from flask import request
import jwt

from config.config import Config


# Custom function to extract claims from JWT token
def get_claims_from_request() -> Union[dict, None]:
    """
    Retrieves and decodes a JSON Web Token (JWT) from the Authorization header of
    the request. If no token is present, or if the token is invalid or expired,
    it returns None.

    Returns:
        dict | None: A dictionary containing the claims of the JWT, or None if
            there was an error or no token was present.
    """
    token = request.cookies.get('Authorization')  # Get token from headers

    if not token:
        #print("No token found in request cookies.")
        return None

    try:
        decoded_token = jwt.decode(token, Config.SECRET_KEY, algorithms='HS256')
        return decoded_token
    except jwt.ExpiredSignatureError:
        #print("Token expired.")
        return None
    except jwt.InvalidTokenError:
        #print("Invalid token.")
        return None
