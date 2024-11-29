from abc import ABC

from models.user import db, User
from sqlalchemy.exc import SQLAlchemyError

from repositories.user_interface import IUserRepository


class UserRepository(IUserRepository, ABC):
    def create_user(self, username: str, password: str) -> User:
        """
        Creates a new user in the database.

        Args:
            username (str): The username of the new user.
            password (str): The password of the new user.

        Returns:
            User: The newly created User object.

        Raises:
            SQLAlchemyError: If there is an error during the transaction,
            such as a database connection issue or integrity constraint violation.
        """
        try:
            new_user = User(username=username, password=password)
            db.session.add(new_user)
            db.session.commit()
            return new_user
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e

    def get_user_by_username(self, username: str) -> User:
        """
            Retrieves a user from the database by their username.

            Args:
                username (str): The username of the user to retrieve.

            Returns:
                User: The User object corresponding to the given username, or None if no user is found.
        """
        return User.query.filter_by(username=username).first()

    def get_all_users(self) -> list[User]:
        """
            Retrieves all users from the database.

            Returns:
                List[User]: A list of all User objects in the database.
        """
        return User.query.all()
