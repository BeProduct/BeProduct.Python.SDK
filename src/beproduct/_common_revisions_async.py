"""
File: _common_revisions_async.py
Author: Yuri Golub
Email: yuri.golub@beproduct.com
Github: https://github.com/BeProduct
Description: Common Revisions Mixin - Async Version
"""

from .sdk_async import BeProductAsync
class RevisionsMixinAsync:
    """
    Common revisions methods for any master folder (Style, Material, etc.) - Async Version
    """

    def __init__(self, client: BeProductAsync):
        self.client = client

    async def revisions_list(self, header_id: str):
        """Returns list of revisions asynchronously

        :header_id: ID of the style, material, etc
        :returns: List of revisions

        """
        return await self.client.raw_api.get(
            f"{self.master_folder}/Revisions?headerId={header_id}")

    async def revisions_get(self, header_id: str, revision_id: str):
        """Returns revision by ID asynchronously

        :header_id: ID of the style, material, etc
        :revision_id: ID of the revision
        :returns: Revision dictionary

        """
        return await self.client.raw_api.get(
            f"{self.master_folder}/Revision?headerId={header_id}" +
            f"&revisionId={revision_id}")

    async def revisions_create(self, header_id: str, name: str = None):
        """Creates new revision asynchronously

        :header_id: ID of the style, material, etc
        :name: Name of the revision
        :returns: Created revision

        """
        return await self.client.raw_api.post(
            f"{self.master_folder}/Revision/Create?headerId={header_id}" +
            (f"&name={name}" if name else ""))

    async def revisions_restore(self, header_id: str, revision_id: str):
        """Restores revision asynchronously

        :header_id: ID of the style, material, etc
        :revision_id: ID of the revision
        :returns: None

        """
        return await self.client.raw_api.post(
            f"{self.master_folder}/Revision/Restore?headerId={header_id}" +
            f"&revisionId={revision_id}")

    async def revisions_delete(self, header_id: str, revision_id: str):
        """Deletes revision asynchronously

        :header_id: ID of the style, material, etc
        :revision_id: ID of the revision
        :returns: None

        """
        return await self.client.raw_api.post(
            f"{self.master_folder}/Revision/Delete?headerId={header_id}" +
            f"&revisionId={revision_id}")

    async def attributes_revision_list(self, header_id: str):
        """Returns Attributes app revisions asynchronously

        :header_id: ID of style/material/image etc
        :returns: List of revisions

        """
        return await self.client.raw_api.get(
            f"Revision/Header/{header_id}")

    async def attributes_revision_add(self, header_id: str, revision: str):
        """Adds a revision to Attributes app asynchronously

        :header_id: ID of style/material/image etc
        :revision: Revision text
        :returns: Added revision

        """
        return await self.client.raw_api.post(
            f"Revision/Header/{header_id}/Create",
            body={
                'revision': revision
            })

    async def attributes_revision_edit(self, header_id: str, revision_id: str, revision: str):
        """Edits a revision in Attributes app asynchronously

        :header_id: ID of style/material/image etc
        :revision_id: Revision ID
        :revision: Revision text
        :returns: Edited revision

        """
        return await self.client.raw_api.post(
            f"Revision/Header/{header_id}/Edit?revisionId={revision_id}",
            body={
                'revision': revision
            })

    async def attributes_revision_delete(self, header_id: str, revision_id: str):
        """Deletes a revision from Attributes app asynchronously

        :header_id: ID of style/material/image etc
        :revision_id: Revision ID
        :returns: None

        """
        return await self.client.raw_api.delete(
            f"Revision/Header/{header_id}/Delete?revisionId={revision_id}")

    async def app_revision_list(self, header_id: str, app_id: str):
        """Returns application revisions asynchronously

        :header_id: ID of style/material/image etc
        :app_id: App ID
        :returns: List of revisions

        """
        return await self.client.raw_api.get(
            f"Revision/Page/{header_id}/{app_id}")

    async def app_revision_add(self, header_id: str, app_id: str, revision: str):
        """Adds a revision to application asynchronously

        :header_id: ID of style/material/image etc
        :app_id: App ID
        :revision: Revision text
        :returns: Added revision

        """
        return await self.client.raw_api.post(
            f"Revision/Page/{header_id}/{app_id}/Create",
            body={
                'revision': revision
            })

    async def app_revision_edit(self, header_id: str, app_id: str, revision_id: str, revision: str):
        """Edits a revision in application asynchronously

        :header_id: ID of style/material/image etc
        :app_id: App ID
        :revision_id: Revision ID
        :revision: Revision text
        :returns: Edited revision

        """
        return await self.client.raw_api.post(
            f"Revision/Page/{header_id}/{app_id}/Edit?revisionId={revision_id}",
            body={
                'revision': revision
            })

    async def app_revision_delete(self, header_id: str, app_id: str, revision_id: str):
        """Deletes a revision from application asynchronously

        :header_id: ID of style/material/image etc
        :app_id: App ID
        :revision_id: Revision ID
        :returns: None

        """
        return await self.client.raw_api.delete(
            f"Revision/Page/{header_id}/{app_id}/Delete?revisionId={revision_id}") 