"""
File: _common_tags.py
Author: Yuri Golub
Email: yuri.golub@beproduct.com
Github: https://github.com/BeProduct
Description: Tags Mixin for every master folder
"""


class TagsMixin:
    """
    Tags mixin class for every master folder
    """

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
