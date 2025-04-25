"""
File: _user_async.py
Author: Yuri Golub
Email: yuri.golub@beproduct.com
Github: https://github.com/BeProduct
Description: User Public API - Async Version
"""
from .sdk_async import BeProductAsync


class UserAsync:

    """ Implements User API - Async Version """

    def __init__(self, client: BeProductAsync):
        """ Constructor """
        self.client = client

    async def user_get(self, email: str):
        """Gets user by email address asynchronously

        :user_id: email of the user
        :returns: User dictionary

        """
        return await self.client.raw_api.get(f"Users/GetByEmail?email={email}")

    async def user_list(self):
        """ Returns list of existing users asynchronously
        :returns: List of existing users

        """
        return await self.client.raw_api.get('Users/List')

    async def user_create(self, fields):
        """ Creates new user asynchronously

        :fields: Dictionary with user fields
        :returns: Created user dictionary

        """
        return await self.client.raw_api.post(
                'Users/Create',
                body=fields)

    async def user_update(self, user_id: str, fields):
        """ Updates existing user asynchronously

        :user_id: User ID
        :fields: Dictionary with user fields
        :returns: Created user dictionary

        """
        return await self.client.raw_api.post(
                f"Users/{user_id}/Update",
                body=fields)

    async def role_list(self):
        """ List of exising user roles asynchronously

        :returns: List of exising user roles

        """
        return await self.client.raw_api.get('Users/Roles')

    async def role_get(self, user_id: str):
        """ Returns user's role asynchronously

        :user_id: User ID
        :returns: Role of the user

        """
        return await self.client.raw_api.get(f"Users/{user_id}/Role") 