from __future__ import annotations

from functools import wraps
from typing import Callable, Any

import jwt
from flask import Blueprint, jsonify, redirect, url_for, render_template, make_response
from werkzeug import Response

from config.config import Config
from services.user_service import UserService
from utils.jw_utils import generate_jwt
from utils.requests import request, get_claims_from_request

user_blueprint = Blueprint('user_blueprint', __name__)


def redirect_if_authenticated() -> Response | None:
    """
        Checks if the user is authenticated by looking for an 'Authorization' cookie.
        If the cookie is present, redirect the user to the home page.
        Returns a Response object if redirection is needed, otherwise returns None.
    """
    # Check for the presence of the 'Authorization' cookie
    token = request.cookies.get('Authorization')
    if token:
        # If the token exists, redirect to /home
        return redirect(url_for('user_blueprint.home'))
    return None


def token_required(f) -> Callable[[tuple[Any, ...], dict[str, Any]], Response | Any]:
    """
        Decorator to check if the request contains a valid JWT token in the
        'Authorization' header. If the token is valid, it extracts the user
        information and stores it in the request context for later use. If
        invalid or missing, it redirects the user to the login page.

        Args:
            f: The function to be decorated.

        Returns:
            The decorated function.
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        """
            Decorated function that checks for a valid JWT token in the 'Authorization'
            header. If the token is valid, it extracts the user information and stores
            it in the request context for later use. If invalid or missing, it redirects
            the user to the login page.

            Args:
                *args: Variable length argument list.
                **kwargs: Arbitrary keyword arguments.

            Returns:
                The result of the decorated function or a redirect response to the
                login page if the token is invalid or missing.
        """
        token = None
        if 'Authorization' in request.cookies:
            token = request.cookies.get('Authorization')

        if not token:
            return redirect(url_for('user_blueprint.user_login_form'))

        try:
            # Decode the token to extract user information
            payload = jwt.decode(token, Config.SECRET_KEY, algorithms='HS256')
            request.claims = payload  # Store claims in request context for later use
        except jwt.ExpiredSignatureError:
            return redirect(url_for('user_blueprint.user_login_form'))
        except jwt.InvalidTokenError:
            return redirect(url_for('user_blueprint.user_login_form'))

        return f(*args, **kwargs)

    return decorated_function


@user_blueprint.route('/home', methods=['GET'])
@token_required
def home() -> str:
    """
        Renders the home page with a list of all registered users.

        This function handles GET requests to the '/home' endpoint.
        It extracts the username from the claims stored in the request context,
        fetches all users from the database, and renders the home page with
        the user list.

        Returns:
            Response: A rendered HTML template response with a list of users.

        Raises:
            Exception: If there's an error while fetching users from the database.
    """
    # Fetch the claims from the request using the helper function
    request.claims = get_claims_from_request()

    try:
        # Get the username from the claims
        username = request.claims['username']


        # Fetch all users from the database
        users = UserService.get_all_users()

        # Render the home page with the user list
        return render_template('home.html', username=username, users=users)

    except Exception as e:
        return render_template('error.html', error=str(e))


@user_blueprint.route('/add', methods=['POST'])
def add_user():
    """
    Handles user registration.

    Extracts user data from the POST request, calls the userService to
    register the new user, and redirects to the home page if successful.
    If an error occurs, render an error page.

    Returns:
        Response: Redirects to the home page if user registration is successful,
                  or renders an error page if an error occurs.
    """

    # Get post-data
    username = request.form.get('username')
    password = request.form.get('password')

    # Call the user service to register the new user
    user_service = UserService()

    try:
        # Attempt to register the user
        user_service.register_user(username, password)

        # Redirect to home page if successful
        return redirect(url_for('user_blueprint.home'))

    except Exception as e:
        # Render error page if registration fails
        return render_template("error.html", error=str(e)), 500


@user_blueprint.route('/login', methods=['GET'])
def user_login_form() -> Response | str:
    """
        Renders the login page.

        This function handles GET requests to the '/login' endpoint.
        It checks if the user is authenticated by attempting to redirect them
        to the home page. If the user is not authenticated, it renders the
        login page.

        Returns:
            Response: A redirect response to the home page if the user is authenticated.
            str: The rendered HTML of the login page if the user is not authenticated.
    """
    # Check if the user is authenticated
    redirection = redirect_if_authenticated()
    if redirection:
        return redirection

    # If not authenticated, render the login page
    return render_template('login.html')


@user_blueprint.route('/login', methods=['POST'])
def login_user() -> tuple[str, int] | Response:
    """
        Handles user login.

        This function handles POST requests to the '/login' endpoint.
        It validates user credentials by checking if the user exists
        and if the password is correct. If the credentials are valid,
        it generates a JWT token using the helper function and sets
        the token as a cookie (optional for session management).

        Returns:
            Response: A rendered HTML template response with a list of users.
            Tuple[str, int]: A tuple containing the rendered HTML template
                and a status code (401 for invalid credentials, 500 for
                errors during the login process).

        Raises:
            Exception: If there's an error during the login process.
    """

    # Extract credentials from the request
    username = request.form.get('username')
    password = request.form.get('password')

    # Validate user credentials
    user_service = UserService()

    try:
        # Retrieve user by username
        user = user_service.get_user_by_username(username)
        if not user:
            return render_template("error.html", error="Invalid credentials"), 401

        # Check password
        if not user_service.verify_password(user.password, password):
            return render_template("error.html", error="Invalid credentials"), 401

        # Generate JWT token using the helper function
        token = generate_jwt(user)
        if not token:
            return render_template("error.html", error="Could not generate token"), 500

        # Set the token as a cookie (optional for session management)
        response = make_response(render_template("home.html", username=user.username))
        response.set_cookie('Authorization', token, httponly=True, max_age=3600)

        return response

    except Exception as e:
        # If there's an error during the login process
        return render_template("error.html", error=f"Error during login: {str(e)}"), 500


@user_blueprint.route('/register', methods=['GET'])
def user_register_form() -> Response | str:
    """
        Renders the user registration form.

        This function handles GET requests to the '/register/form' endpoint.
        It checks if the user is authenticated by attempting to redirect them
        to the home page. If the user is not authenticated, it renders the
        registration page.

        Returns:
            Response: A redirect response to the home page if the user is authenticated.
            str: The rendered HTML of the registration page if the user is not authenticated.
    """
    # Check if the user is authenticated
    redirection = redirect_if_authenticated()
    if redirection:
        return redirection

    # If not authenticated, render the registration page
    return render_template('register.html')


@user_blueprint.route('/register', methods=['POST'])
def register_user() -> tuple[Response, int] | Response:
    """
        Handles user registration.

        This function handles POST requests to the '/register' endpoint.
        It extracts the username and password from the request, calls the
        userService to handle registration logic, generates a JWT token
        after successful registration, and sets the token as a cookie.

        Returns:
            tuple[Response, int]: A JSON response containing an error message
                and a 400 status code if the registration fails.
            Response: A redirect response to the home page if the registration
                is successful.

        Raises:
            Exception: If there's an error during the registration process.
    """

    # Extract credentials from the request
    username = request.form.get('username')
    password = request.form.get('password')

    # Call the userService to handle registration logic
    user_service = UserService()
    try:
        user_service.register_user(username, password)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

    # Generate JWT token after successful registration
    user = user_service.get_user_by_username(username)
    token, err = generate_jwt(user)

    if err:
        return jsonify({"error": f"JWT generation failed: {err}"}), 500

    # Set the token as a cookie
    response = make_response(redirect(url_for('user_blueprint.home')))
    response.set_cookie('Authorization', token, max_age=3600, secure=False, httponly=True)

    return response

