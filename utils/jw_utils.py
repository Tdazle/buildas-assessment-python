import datetime

import jwt

from config.config import Config


def generate_jwt(user):

    """
    Generates a JSON Web Token (JWT) given a user instance.

    The generated JWT contains the user's ID, username, and an expiration time
    (set to 1 hour from now). The token is encoded using the HS256 algorithm
    with the secret key specified in the configuration.

    Args:
        user (User): The user instance to generate a JWT for.

    Returns:
        tuple: A tuple containing the generated JWT and an error message if any.
    """
    try:
        payload = {
            'user_id': user.id,
            'username': user.username,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # Token expiration time
        }
        token = jwt.encode(payload, Config.SECRET_KEY, algorithm='HS256')
        return token, None
    except Exception as e:
        print(f"Error generating JWT: {e}")
        return None, str(e)
