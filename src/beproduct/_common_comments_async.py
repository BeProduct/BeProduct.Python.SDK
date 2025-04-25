"""
File: _common_comments_async.py
Author: Yuri Golub
Email: yuri.golub@beproduct.com
Github: https://github.com/BeProduct
Description: Common Comments Mixin - Async Version
"""

from .sdk_async import BeProductAsync

class CommentsMixinAsync:
    """
    Common comments methods for any master folder (Style, Material, etc.) - Async Version
    """

    def __init__(self, client: BeProductAsync):
        self.client = client

    async def comments_list(self, header_id: str):
        """Returns list of comments asynchronously

        :header_id: ID of the style, material, etc
        :returns: List of comments

        """
        return await self.client.raw_api.get(
            f"{self.master_folder}/Comments?headerId={header_id}")

    async def comments_add(self, header_id: str, text: str):
        """Adds new comment asynchronously

        :header_id: ID of the style, material, etc
        :text: Comment text
        :returns: Created comment

        """
        return await self.client.raw_api.post(
            f"{self.master_folder}/Comments/Add?headerId={header_id}",
            body=text)

    async def comments_delete(self, header_id: str, comment_id: str):
        """Deletes comment asynchronously

        :header_id: ID of the style, material, etc
        :comment_id: ID of the comment
        :returns: None

        """
        return await self.client.raw_api.post(
            f"{self.master_folder}/Comments/Delete?headerId={header_id}" +
            f"&commentId={comment_id}")

    async def comments_update(self, header_id: str, comment_id: str, text: str):
        """Updates comment asynchronously

        :header_id: ID of the style, material, etc
        :comment_id: ID of the comment
        :text: New comment text
        :returns: Updated comment

        """
        return await self.client.raw_api.post(
            f"{self.master_folder}/Comments/Update?headerId={header_id}" +
            f"&commentId={comment_id}",
            body=text)

    async def attributes_comment_list(self, header_id: str):
        """Returns Attributes app comments asynchronously

        :header_id: ID of style/material/image etc
        :returns: List of comments

        """
        return await self.client.raw_api.get(
            f"Comment/Header/{header_id}")

    async def attributes_comment_add(self, header_id: str, comment: str):
        """Adds a comment to Attributes app asynchronously

        :header_id: ID of style/material/image etc
        :comment: Comment text
        :returns: Added comment

        """
        return await self.client.raw_api.post(
            f"Comment/Header/{header_id}/Create",
            body={
                'comment': comment
            })

    async def attributes_comment_edit(self, header_id: str, comment_id: str, comment: str):
        """Edits a comment in Attributes app asynchronously

        :header_id: ID of style/material/image etc
        :comment_id: Comment ID
        :comment: Comment text
        :returns: Edited comment

        """
        return await self.client.raw_api.post(
            f"Comment/Header/{header_id}/Edit?commentId={comment_id}",
            body={
                'comment': comment
            })

    async def attributes_comment_delete(self, header_id: str, comment_id: str):
        """Deletes a comment from Attributes app asynchronously

        :header_id: ID of style/material/image etc
        :comment_id: Comment ID
        :returns: None

        """
        return await self.client.raw_api.delete(
            f"Comment/Header/{header_id}/Delete?commentId={comment_id}")

    async def app_comment_list(self, header_id: str, app_id: str):
        """Returns application comments asynchronously

        :header_id: ID of style/material/image etc
        :app_id: App ID
        :returns: List of comments

        """
        return await self.client.raw_api.get(
            f"Comment/Page/{header_id}/{app_id}")

    async def app_comment_add(self, header_id: str, app_id: str, comment: str):
        """Adds a comment to application asynchronously

        :header_id: ID of style/material/image etc
        :app_id: App ID
        :comment: Comment text
        :returns: Added comment

        """
        return await self.client.raw_api.post(
            f"Comment/Page/{header_id}/{app_id}/Create",
            body={
                'comment': comment
            })

    async def app_comment_edit(self, header_id: str, app_id: str, comment_id: str, comment: str):
        """Edits a comment in application asynchronously

        :header_id: ID of style/material/image etc
        :app_id: App ID
        :comment_id: Comment ID
        :comment: Comment text
        :returns: Edited comment

        """
        return await self.client.raw_api.post(
            f"Comment/Page/{header_id}/{app_id}/Edit?commentId={comment_id}",
            body={
                'comment': comment
            })

    async def app_comment_delete(self, header_id: str, app_id: str, comment_id: str):
        """Deletes a comment from application asynchronously

        :header_id: ID of style/material/image etc
        :app_id: App ID
        :comment_id: Comment ID
        :returns: None

        """
        return await self.client.raw_api.delete(
            f"Comment/Page/{header_id}/{app_id}/Delete?commentId={comment_id}") 