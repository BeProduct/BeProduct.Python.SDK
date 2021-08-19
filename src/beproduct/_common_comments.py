"""
File: _common_comments.py
Author: Yuri Golub
Email: yuri.golub@beproduct.com
Github: https://github.com/BeProduct
Description: Comments Mixin for every master folder
"""


class CommentsMixin:

    """
    Comments mixin class for every master folder
    """

    def attributes_comment_list(self, header_id: str):
        """ Returns Attributes app comments

        :header_id: ID of style/material/image etc
        :returns: List of comments

        """
        return self.client.raw_api.get(
            f"Comment/Heeader/{header_id}")

    def attributes_comment_add(self, header_id: str, comment: str):
        """Adds a comment to Attributes app

        :header_id: ID of style/material/image etc
        :comment: Comment text
        :returns: Added comment

        """
        return self.client.raw_api.post(
            f"Comment/Header/{header_id}/Create",
            body={
                'comment': comment
            })

    def attributes_comment_edit(self, header_id: str, comment_id: str, comment: str):
        """Edits a comment in Attributes app

        :header_id: ID of style/material/image etc
        :comment_id: Comment ID
        :comment: Comment text
        :returns: Edited comment

        """
        return self.client.raw_api.post(
            f"Comment/Header/{header_id}/Edit?commentId={comment_id}",
            body={
                'comment': comment
            })

    def attributes_comment_delete(self, header_id: str, comment_id: str):
        """Deletes a comment from Attributes app

        :header_id: ID of style/material/image etc
        :comment_id: Comment ID
        :returns: 

        """
        return self.client.raw_api.delete(
            f"Comment/Header/{header_id}/Delete?commentId={comment_id}")

    def app_comment_list(self, header_id: str, app_id: str):
        """ Returns application comments

        :header_id: ID of style/material/image etc
        :app_id: App ID
        :returns: List of comments

        """
        return self.client.raw_api.get(
            f"Comment/Page/{header_id}/{app_id}")

    def app_comment_add(self, header_id: str, app_id: str,  comment: str):
        """Adds a comment to application

        :header_id: ID of style/material/image etc
        :app_id: App ID
        :comment: Comment text
        :returns: Added comment

        """
        return self.client.raw_api.post(
            f"Comment/Page/{header_id}/{app_id}/Create",
            body={
                'comment': comment
            })

    def app_comment_edit(self, header_id: str, app_id: str, comment_id: str, comment: str):
        """Edits a comment in application

        :header_id: ID of style/material/image etc
        :app_id: App ID
        :comment_id: Comment ID
        :comment: Comment text
        :returns: Edited comment

        """
        return self.client.raw_api.post(
            f"Comment/Page/{header_id}/{app_id}/Edit?commentId={comment_id}",
            body={
                'comment': comment
            })

    def app_comment_delete(self, header_id: str, app_id: str, comment_id: str):
        """Deletes a comment from Attributes app

        :header_id: ID of style/material/image etc
        :app_id: App ID
        :comment_id: Comment ID
        :returns:

        """
        return self.client.raw_api.delete(
            f"Comment/Page/{header_id}/{app_id}/Delete?commentId={comment_id}")
