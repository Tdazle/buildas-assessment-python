from abc import ABC, abstractmethod
from typing import List, Optional
from models.user import User

class IUserRepository(ABC):
    @abstractmethod
    def create_user(self, username: str, password: str) -> User:
        """
        Creates a new user in the database.

        Args:
            username (str): The username of the new user.
            password (str): The password of the new user.

        Returns:
            User: The newly created User object.
        """
        pass

    @abstractmethod
    def get_user_by_username(self, username: str) -> Optional[User]:
        """
        Retrieves a user from the database by their username.

        Args:
            username (str): The username of the user to retrieve.

        Returns:
            User: The User object corresponding to the given username, or None if no user is found.
        """
        pass

    @abstractmethod
    def get_all_users(self) -> List[User]:
        """
        Retrieves all users from the database.

        Returns:
            List[User]: A list of all User objects in the database.
        """
        pass
