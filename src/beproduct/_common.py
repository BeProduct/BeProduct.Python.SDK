"""
File: _common.py
Author: Yuri Golub
Email: yuri.golub@beproduct.com
Github: https://github.com/BeProduct
Description: Common Mixin for every master folder
"""

from ._helpers import beproduct_paging_iterator


class CommonMixin:
    """
    Common mixin class for every master folder
    """

    def __init__(self, master_folder):
        self.master_folder = master_folder

    def folders(self):
        """
        :returns: List of folders
        """
        return self.client.raw_api.get(f"{self.master_folder}/Folders")

    def folder_schema(self, folder_id: str):
        """Gets attributes schema (list of fields ) for a folder

        :folder_id: ID of the folder
        :returns: Attributes schema

        """
        return self.client.raw_api.get(
            f"{self.master_folder}/FolderSchema?folderId={folder_id}")

    # ATTRIBUTES

    def attributes_list(
            self,
            folder_id: str = "",
            filters=None,
            colorway_filters=None,
            page_size=30):
        """
        :folder_id: Folder ID
        :filters: List of filter dictionaries
        :colorway_filters: List of colorway filter dictionaries
        :returns: Enumerator of Attributes
        """

        return beproduct_paging_iterator(
            page_size,
            lambda psize, pnum: self.client.raw_api.post(
                f"{self.master_folder}/Headers?folderId={folder_id}" +
                f"&pageSize={psize}&pageNumber={pnum}",
                body={
                    'filters':  filters,
                    'colorwayFilters': colorway_filters
                }))

    def attributes_get(self, header_id: str):
        """Returns style attibutes

        :header_id: ID of the style, material, image etc.
        :returns: dictionary of the requested style attributes

        """
        return self.client.raw_api.get(f"{self.master_folder}/Header/{header_id}")

    def attributes_delete(self, header_id: str):
        """Deletes Style/Material/Image by ID

        :header_id: ID of the Style/Material/Image
        :returns:
        """
        return self.client.raw_api.get(
            f"{self.master_folder}/Header/Delete/{header_id}")

    # APPLICATIONS
    def app_schema(self, app_id: str):
        """ Returns an app schema
        :app_id: ID of the application / page
        :returns: Dictionary with app schema data
        """
        return self.client.raw_api.get(
            f"{self.master_folder}/PageSchema?pageId={app_id}")

    def app_list(self, header_id: str):
        """ Returns list of apps/pages
        for a specific style, material, etc

        :header_id: ID of the style, material, etc
        :returns: List of apps
        """
        return self.client.raw_api.get(
            f"{self.master_folder}/Pages?headerId={header_id}")

    def app_get(self, header_id: str, app_id: str):
        """ Returns a particular app

        :header_id: ID of the style, material, etc
        :app_id: ID of the application / page
        :returns: Dictionary with app data
        """
        return self.client.raw_api.get(
            f"{self.master_folder}/Page?headerId={header_id}&pageId={app_id}")

    def app_form_update(self, header_id: str, app_id: str, fields):
        """ Updates form application
        :header_id: ID of the style, material, etc
        :app_id: ID of the application / page
        :fields: Dictionary of fields to update {'field_id':'value'}
        """
        return self.client.raw_api.post(
            f"{self.master_folder}/PageForm?headerId={header_id}&pageId={app_id}",
            body=[{'id': field_id, 'value': fields[field_id]} for field_id in fields])

    def app_grid_update(self, header_id: str, app_id: str, rows):
        """ Updates form application
        :header_id: ID of the style, material, etc
        :app_id: ID of the application / page
        :rows: List of row dictionaries
        """
        return self.client.raw_api.post(
            f"{self.master_folder}/PageGrid?headerId={header_id}&pageId={app_id}",
            body=rows)

    def app_list_update(self, header_id: str, app_id: str, list_items):
        """ Updates List application
        :header_id: ID of the style, material, etc
        :app_id: ID of the application / page
        :list_items: Items of the list app
        """
        return self.client.raw_api.post(
            f"{self.master_folder}/PageList?headerId={header_id}&pageId={app_id}",
            body=list_items)

    def app_attachments_delete(
            self,
            header_id: str,
            app_id: str,
            filenames_to_remove):
        """ Deletes files from Attachments app
        :header_id: ID of the style, material, etc
        :app_id: ID of the application / page
        :filenames_to_remove: List of filenames to be removed
        """
        return self.client.raw_api.post(
            f"{self.master_folder}/AttachmentRemove?headerId={header_id}&pageId={app_id}",
            body=filenames_to_remove)

    # SHARE

    def attributes_share(self, header_id: str, partner_list):
        """Shares attributes page

        :header_id: ID of style/material/image etc
        :partner_list: list of partner IDs

        """
        return self.client.raw_api.post(
            f"Share/Header/{header_id}/Share",
            body=partner_list
        )

    def app_share(self, header_id: str, app_id: str, partner_list):
        """Shares application

        :header_id: ID of style/material/image etc
        :app_id: ID of the application
        :partner_list: list of partner IDs

        """
        return self.client.raw_api.post(
            f"Share/Page/{header_id}/{app_id}/Share",
            body=partner_list
        )

    def attributes_unshare(self, header_id: str, partner_list):
        """Unshares attributes page

        :header_id: ID of style/material/image etc
        :partner_list: list of partner IDs

        """
        return self.client.raw_api.post(
            f"Share/Header/{header_id}/Unshare",
            body=partner_list
        )

    def app_unshare(self, header_id: str, app_id: str, partner_list):
        """Shares application

        :header_id: ID of style/material/image etc
        :app_id: ID of the application
        :partner_list: list of partner IDs

        """
        return self.client.raw_api.post(
            f"Share/Page/{header_id}/{app_id}/Unshare",
            body=partner_list
        )

    def attributes_shared_with(self, header_id: str):
        """ Gets list of all partners with whom
            attributes page is shared

        :header_id: ID of style/material/image etc
        :returns: List of partners

        """
        return self.client.raw_api.get(f"Share/Header/{header_id}/Get")

    def app_shared_with(self, header_id: str, app_id: str):
        """ Gets list of all partners with whom
            app is shared

        :header_id: ID of style/material/image etc
        :app_id: ID of the application
        :returns: List of partners

        """
        return self.client.raw_api.get(f"Share/Page/{header_id}/{app_id}/Get")

    # COMMENTS

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

    # REVISIONS

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

    # TAGS

    def tag_list(self):
        """List of Style/Material/Image/Color tags

        :master_folder: Must be equal Style or Material or Image or Color
        :returns: List of tags

        """
        return self.client.raw_api.get(
            f"Tag/{self.master_folder}/List")

    def tag_create(self, name: str, integration: str = None, share_with=None):
        """Creates new tag

        :name: Tag name
        :integration: 'Browzwear' if needs to be integrated with Browzwear otherwise none
        :share_with: List of user IDs
        :returns: Created tag

        """
        return self.client.raw_api.post(
            f"Tag/{self.master_folder}/Create",
            body={
                'name': name,
                'integration': integration,
                'shareWith': share_with if share_with else []
            }
        )

    def tag_update(self, tag_id: str, name: str, integration: str = None):
        """Updates a tag

        :tag_id: Tag ID
        :name: Tag name
        :integration: 'Browzwear' if needs to be integrated with Browzwear otherwise none
        :returns: Updated tag

        """
        return self.client.raw_api.post(
            f"Tag/{tag_id}/Update",
            body={
                'name': name,
                'integration': integration,
            }
        )

    def tag_share(self, tag_id: str, share_with):
        """Shares a tag

        :tag_id: Tag ID
        :share_with: List of User IDs to share with
        :returns:

        """
        return self.client.raw_api.post(
            f"Tag/{tag_id}/Share",
            body=share_with
        )

    def tag_unshare(self, tag_id: str, unshare_with):
        """Unshares a tag

        :tag_id: Tag ID
        :share_with: List of User IDs to unshare with
        :returns:

        """
        return self.client.raw_api.post(
            f"Tag/{tag_id}/Unshare",
            body=unshare_with
        )

    def tag_delete(self, tag_id: str):
        """Deletes a tag

        :tag_id: Tag ID
        :returns:

        """
        return self.client.raw_api.delete(f"Tag/{tag_id}/Delete")

    def attributes_tag_list(self, header_id: str):
        """List of Style/Material/Image/Color tags

        :header_id: ID of the style, material, image etc.
        :returns: List of tags

        """
        return self.client.raw_api.get(f"Tag/Header/{header_id}")

    def attributes_tag_add(self, header_id: str, tag_names):
        """Adds tags to the Attributes app

        :header_id: ID of the style, material, image etc.
        :tag_names: List of strings (tag names)
        :returns:

        """
        return self.client.raw_api.post(
            f"Tag/Header/{header_id}/Add",
            body=tag_names
        )

    def attributes_tag_remove(self, header_id: str, tag_names):
        """Remove tags from the Attributes app

        :header_id: ID of the style, material, image etc.
        :tag_names: List of strings (tag names)
        :returns:

        """
        return self.client.raw_api.post(
            f"Tag/Header/{header_id}/Remove",
            body=tag_names
        )
