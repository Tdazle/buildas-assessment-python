from models import User
from repositories.user_repository import UserRepository
from werkzeug.security import generate_password_hash, check_password_hash

class UserService:
    @staticmethod
    def register_user(username, password) -> None:
        """
            Registers a new user.

            This method checks if a user with the given username already exists.
            If not, it hashes the provided password and creates a new user
            in the database.

            Args:
                username (str): The username for the new user.
                password (str): The plaintext password for the new user.

            Raises:
                ValueError: If a user with the given username already exists.
            """

        # Check if the user already exists
        if User.query.filter_by(username=username).first():
            raise ValueError("User already exists")

        # Hash the password
        hashed_password = generate_password_hash(password)

        # Create the new user and add it to the database
        UserRepository.create_user(username, hashed_password, )

    @staticmethod
    def get_user_by_username(username) -> User:
        """
            Retrieves a user from the database by their username.

            Args:
                username (str): The username of the user to retrieve.

            Returns:
                User: The User object corresponding to the given username, or None if no user is found.
        """
        return UserRepository.get_user_by_username(username)

    @staticmethod
    def get_all_users() -> list[User]:
        """
            Retrieves all users from the database.

            This method fetches all user records from the database and returns them
            as a list of User objects.

            Returns:
                list[User]: A list of all User objects in the database.
        """
        return UserRepository.get_all_users()

    @staticmethod
    def verify_password(stored_password, input_password) -> bool:
        """
            Compares a given password with a stored, hashed password.

            Args:
                stored_password (str): The hashed password stored in the database.
                input_password (str): The password input by the user.

            Returns:
                bool: A boolean indicating if the passwords match.
        """
        return check_password_hash(stored_password, input_password)
