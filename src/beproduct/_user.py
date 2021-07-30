"""
File: _user.py
Author: Yuri Golub
Email: yuri.golub@beproduct.com
Github: https://github.com/BeProduct
Description: User Public API
"""
from .sdk import BeProduct


class User:

    """ Implements User API """

    def __init__(self, client: BeProduct):
        """ Constructor """
        self.client = client

    def user_get(self, email: str):
        """Gets user by email address

        :user_id: email of the user
        :returns: User dictionary

        """
        return self.client.raw_api.get(f"Users/GetByEmail?email={email}")

    def user_list(self):
        """ Returns list of existing users
        :returns: List of existing users

        """
        return self.client.raw_api.get('Users/List')

    def user_create(self, fields):
        """ Creates new user

        :fields: Dictionary with user fields
        :returns: Created user dictionary

        """
        return self.client.raw_api.post(
                'Users/Create',
                body=fields)

    def user_update(self, user_id: str, fields):
        """ Updates existing user

        :user_id: User ID
        :fields: Dictionary with user fields
        :returns: Created user dictionary

        """
        return self.client.raw_api.post(
                f"Users/{user_id}/Update",
                body=fields)

    def role_list(self):
        """ List of exising user roles

        :returns: List of exising user roles

        """
        return self.client.raw_api.get('Users/Roles')

    def role_get(self, user_id: str):
        """ Returns user's role

        :user_id: User ID
        :returns: Role of the user

        """
        return self.client.raw_api.get(f"Users/{user_id}/Role")
