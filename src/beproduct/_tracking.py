"""
File: _tracking.py
Author: Yuri Golub
Email: yuri.golub@beproduct.com
Github: https://github.com/BeProduct
Description: BeProduct Public API Traking methods
"""

from .sdk import BeProduct
from ._helpers import beproduct_paging_iterator


class Tracking():
    """
    Implements Image API
    """

    def __init__(self, client: BeProduct):
        self.client = client

    def folders(self):
        """List of available tracking folders
        :returns: List of tracking folder objects

        """
        return self.client.raw_api.get('Tracking/Folders')

    def plan_list(self, filters=None, folder_id: str = None):
        """ Returns plan list and performs filtering
            if necessary

        :filters: List of plan filters to apply search
        :folder_id: Folder ID if search needs to be within a forler
        :returns: List of plans

        """
        return beproduct_paging_iterator(
            30,
            lambda psize, pnum: self.client.raw_api.post(
                f"Tracking/Plans?folderId={folder_id}" +
                f"&pageSize={psize}&pageNumber={pnum}",
                body={
                    'filters':  filters,
                    'colorwayFilters': []
                }))

    def plan_get(self, plan_id: str):
        """Returns a plan by ID

        :plan_id: Plan ID
        :returns: Requested plan

        """
        return self.client.raw_api.post(f"Tracking/Plan/{plan_id}", body={})

    def plan_style_timeline_list(self, plan_id: str, filters=None):
        """Returns a list of style timeline records from specific plan
           Filtering is applied if specified

        :plan_id: Plan ID
        :filters: Filters
        :returns: List of Style Timeline records

        """
        return beproduct_paging_iterator(
            20,
            lambda psize, pnum: self.client.raw_api.post(
                f"Tracking/Plan/{plan_id}/Style/Timeline" +
                f"?pageSize={psize}&pageNumber={pnum}",
                body={
                    'filters':  filters,
                }))

    def plan_style_tracking_view(self, plan_id: str, view_id: str, filters=None):
        """Returns a list of style timeline records from specific plan
           Filtering is applied if specified

        :plan_id: Plan ID
        :view_id: Tracking view ID
        :filters: Filters
        :returns: List of Style Timeline records

        """
        return beproduct_paging_iterator(
            20,
            lambda psize, pnum: self.client.raw_api.post(
                f"Tracking/Plan/{plan_id}/Style/View/{view_id}" +
                f"?pageSize={psize}&pageNumber={pnum}",
                body={
                    'filters':  filters,
                }))

    def plan_style_timeline_update(self,  plan_id: str, timelines):
        """ Updates timelines in a plan

        :plan_id: Id of Style plan
        :timelines: List of timeline dictionaries to update
        :returns:

        """
        return self.client.raw_api.post(
            f"Tracking/Plan/{plan_id}/Style/Timelines/Edit",
            body=timelines)

    def plan_material_timeline_list(self, plan_id: str, filters=None):
        """Returns a list of material plan timeline records from specific plan
           Filtering is applied if specified

        :plan_id: Plan ID
        :filters: Filters
        :returns: List of Material Timeline records

        """
        return beproduct_paging_iterator(
            20,
            lambda psize, pnum: self.client.raw_api.post(
                f"Tracking/Plan/{plan_id}/Material/Timeline" +
                f"?pageSize={psize}&pageNumber={pnum}",
                body={
                    'filters':  filters,
                }))

    def plan_material_tracking_view(self, plan_id: str, view_id: str, filters=None):
        """Returns a list of material timeline records from specific plan
           Filtering is applied if specified

        :plan_id: Plan ID
        :view_id: Tracking view ID
        :filters: Filters
        :returns: List of Style Timeline records

        """
        return beproduct_paging_iterator(
            20,
            lambda psize, pnum: self.client.raw_api.post(
                f"Tracking/Plan/{plan_id}/Material/View/{view_id}" +
                f"?pageSize={psize}&pageNumber={pnum}",
                body={
                    'filters':  filters,
                }))

    def plan_material_timeline_update(self,  plan_id: str, timelines):
        """ Updates timelines in a plan

        :plan_id: Id of Style plan
        :timelines: List of timeline dictionaries to update
        :returns:

        """
        return self.client.raw_api.post(
            f"Tracking/Plan/{plan_id}/Material/Timelines/Edit",
            body=timelines)
