"""
File: _common_revisions.py
Author: Yuri Golub
Email: yuri.golub@beproduct.com
Github: https://github.com/BeProduct
Description: Revisions Mixin for every master folder
"""


class RevisionsMixin:

    """
    Revisions mixin class for every master folder
    """

    def attributes_revision_list(self, header_id: str):
        """ Returns Attributes app revisions

        :header_id: ID of style/material/image etc
        :returns: List of revisions

        """
        return self.client.raw_api.get(
            f"Revision/Heeader/{header_id}")

    def attributes_revision_add(self, header_id: str, revision: str):
        """Adds a revision to Attributes app

        :header_id: ID of style/material/image etc
        :revision: revision text
        :returns: Added revision

        """
        return self.client.raw_api.post(
            f"Revision/Header/{header_id}/Create",
            body={
                'revision': revision
            })

    def attributes_revision_edit(self, header_id: str, revision_id: str, revision: str):
        """Edits a revision in Attributes app

        :header_id: ID of style/material/image etc
        :revision_id: revision ID
        :revision: revision text
        :returns: Edited revision

        """
        return self.client.raw_api.post(
            f"Revision/Header/{header_id}/Edit?revisionId={revision_id}",
            body={
                'revision': revision
            })

    def attributes_revision_delete(self, header_id: str, revision_id: str):
        """Deletes a revision from Attributes app

        :header_id: ID of style/material/image etc
        :revision_id: revision ID
        :returns: 

        """
        return self.client.raw_api.delete(
            f"Revision/Header/{header_id}/Delete?revisionId={revision_id}")

    def app_revision_list(self, header_id: str, app_id: str):
        """ Returns application revisions

        :header_id: ID of style/material/image etc
        :app_id: App ID
        :returns: List of revisions

        """
        return self.client.raw_api.get(
            f"Revision/Page/{header_id}/{app_id}")

    def app_revision_add(self, header_id: str, app_id: str,  revision: str):
        """Adds a revision to application

        :header_id: ID of style/material/image etc
        :app_id: App ID
        :revision: revision text
        :returns: Added revision

        """
        return self.client.raw_api.post(
            f"Revision/Page/{header_id}/{app_id}/Create",
            body={
                'revision': revision
            })

    def app_revision_edit(self, header_id: str, app_id: str, revision_id: str, revision: str):
        """Edits a revision in application

        :header_id: ID of style/material/image etc
        :app_id: App ID
        :revision_id: revision ID
        :revision: revision text
        :returns: Edited revision

        """
        return self.client.raw_api.post(
            f"Revision/Page/{header_id}/{app_id}/Edit?revisionId={revision_id}",
            body={
                'revision': revision
            })

    def app_revision_delete(
            self,
            header_id: str,
            app_id: str,
            revision_id: str):
        """Deletes a revision from Attributes app

        :header_id: ID of style/material/image etc
        :app_id: App ID
        :revision_id: revision ID
        :returns:

        """
        return self.client.raw_api.delete(
            f"Revision/Page/{header_id}/{app_id}/Delete?" +
            f"revisionId={revision_id}")
