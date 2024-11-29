import unittest
from unittest.mock import patch

from flask import Flask
from flask_testing import TestCase

from api.v1.user_routes import user_blueprint
from config.config import Config


class UserBlueprintTestCase(TestCase):
    def create_app(self):
        # Set up your app with the blueprint for testing
        app = Flask(__name__)
        app.config.from_object(Config)  # Use your actual config
        app.register_blueprint(user_blueprint)
        return app

    @patch('utils.jw_utils.generate_jwt', return_value=("token", None))
    def test_register_user_error(self, mock_generate_jwt):
        with self.client:
            # Simulate an error during registration
            mock_generate_jwt.return_value = (None, "JWT generation error")
            response = self.client.post('/register', data={
                'username': 'newuser',
                'password': 'password123'
            })
            self.assertEqual(response.status_code, 400)  # Bad request due to JWT generation failure
            self.assertIn('error', response.json)


    def test_redirect_if_authenticated(self):
        with self.client:
            # Simulate a logged-in user by setting a cookie
            self.client.set_cookie('localhost', 'Authorization', 'valid_jwt_token')
            response = self.client.get('/login')
            self.assertEqual(response.status_code, 302)  # Should redirect to home
            self.assertIn('/home', response.location)


if __name__ == '__main__':
    unittest.main()
