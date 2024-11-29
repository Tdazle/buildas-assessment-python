# Buildas Technical Assessment—Python Project

## Overview

This project provides a basic user management system with features such as:

    User registration
    User login
    User listing
    Password verification
    Mock service testing for user registration

It uses the Flask framework for handling HTTP requests, PBKDF2 for hashing passwords, and PostgresSQL as the database. The application includes service, repository, and handler layers to handle the business logic, data access, and HTTP routing respectively.

## Features

- **User Registration**: Users can register by providing a username and password.
- **User Authentication**: Login functionality with password validation.
- **Get All Users**: Fetch all registered users from the database.
- **Mocking Services**: Use of mocks for testing services without depending on a real database.

## Project Structure

```
my-gin-app/
├── api/                              # Entry point for the application
│   └── v1/                           # Main application files
│       └── user_routed.py            # Main entry point
├── config/                           # Application configuration
│   └── config.py                     # Configuration file    
├── migrations/                       # Database migrations
├── models/                           
│   └── __init__.py                   # Package initialization
│   └── user.py                       # User model                           
├── repository/                              
│   └── user_interface.py             # User interface
│   └── user_repository.py            # User repository                       
├── services/                         # Application services
│   └── user_service.py               # User service interface
├── static/                           # Static files/
├── templates/                        # HTML templates/
│   └── error.html                    # Error page
│   └── home.html                     # Home page
│   └── login.html                    # Login page
│   └── register.html                 # Registration page
├── tests/                            # Unit tests
│   └── test_user.py                  # Test cases for user
├── utils/                            # Utility functions
│   └── jw_utils.py                   # JWT utility functions
│   └── requests.py                   # Request utility functions
├── .env                              # Environment variables
├── app.py                            # Application entry point
├── docker-compose.yml                # Docker compose file
├── Dockerfile                        # Dockerfile
├── README.md                         # Project README
└── requirements.txt                  # Project dependencies

```

## Requirements

- Flask 2.3.2.
- PostgresSQL for the database.
- Docker for containerization.

## Setup

### 1. Clone the repository

```bash
 git clone https://github.com/tdazle007/buildas-assessment.git
cd buildas-assessment-python

```

### 2. Install dependencies

```bash
  pip install -r requirements.txt
```

### 3. Setup database

Ensure you have PostgresSQL set up and running. Update the database connection details in .env.

Example .env file:

```
POSTGRES_USER=postgres
POSTGRES_PASSWORD=secret
POSTGRES_DB=python_crud_app
POSTGRES_HOST=database
POSTGRES_PORT=5432
```

### 4. Build the Docker image

```bash
  buildas-assessment-python> docker compose up --build
  buildas-assessment-python> docker-compose exec app flask db init  # Initialize migrations directory (only needed once)
  buildas-assessment-python> docker-compose exec app flask db migrate -m "Initial migration"  # Create migration scripts
  buildas-assessment-python> docker-compose exec app flask db upgrade  # Apply migrations to the database 
```

### 5. Test the application

```bash 
  buildas-assessment-python> docker-compose exec app flask test
```

### 6. Access the application

You can access the application at http://localhost:5000

### 7. Endpoints

The application provides the following endpoints:

- **/api/v1/user/register**: Register a new user.
- **/api/v1/user/login**: Authenticate a user.
- **/api/v1/user/home**: Get all registered/add more users.

### 8. Services

The application follows a layered architecture with services encapsulating the business logic.
- **UserService**: Handles user-related operations such as registration, fetching users, and password checks.
- **UserRepository**: Interfaces with the database to persist and retrieve user data.
- **IUserRepository**: Defines the methods required for user management, which are then implemented by ```UserService``` and mocked in tests.

### 9. Handlers

The handler package contains the HTTP handler functions that interact with the service layer:

- **/register**: Handles user registration by receiving data via a POST request, invoking ```register_user```, and redirecting the user to a success page on success.
- **/login**: Handles user login by receiving data via a POST request, invoking ```login_user```, and redirecting the user to a success page on success.
- **/home**: Handles the home page request, invoking ```get_all_users```, and rendering the home template with the list of users.

### 10. Testing

Testing is implemented using the ```pytest``` package for mocking and assertions.

This ```README.md``` provides a comprehensive overview of the project, installation steps, and explanations of the components and testing. It will guide other developers through setting up, running, and understanding the codebase effectively. 😊
