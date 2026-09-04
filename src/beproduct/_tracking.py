"""
File: _tracking.py
Author: Yuri Golub
Email: yuri.golub@beproduct.com
Github: https://github.com/BeProduct
Description: BeProduct Public API Traking methods
"""

from .sdk import BeProduct


class Tracking:
    """
    Implements Image API
    """

    def __init__(self, client: BeProduct):
        self.client = client

    def folders(self):
        """List of available tracking folders
        :returns: List of tracking folder objects

        """
        return self.client.raw_api.get("Tracking/Folders")

    def plan_list(self, filters=None, folder_id: str = None):
        """Returns plan list and performs filtering
            if necessary

        :filters: List of plan filters to apply search
        :folder_id: Folder ID if search needs to be within a forler
        :returns: List of plans

        """
        return self.client.beproduct_paging_iterator(
            30,
            lambda psize, pnum: self.client.raw_api.post(
                f"Tracking/Plans?folderId={folder_id}"
                + f"&pageSize={psize}&pageNumber={pnum}",
                body={"filters": filters, "colorwayFilters": []},
            ),
        )

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
        return self.client.beproduct_paging_iterator(
            20,
            lambda psize, pnum: self.client.raw_api.post(
                f"Tracking/Plan/{plan_id}/Style/Timeline"
                + f"?pageSize={psize}&pageNumber={pnum}",
                body={
                    "filters": filters,
                },
            ),
        )

    def plan_style_tracking_view(self, plan_id: str, view_id: str, filters=None):
        """Returns a list of style timeline records from specific plan
           Filtering is applied if specified

        :plan_id: Plan ID
        :view_id: Tracking view ID
        :filters: Filters
        :returns: List of Style Timeline records

        """
        return self.client.beproduct_paging_iterator(
            20,
            lambda psize, pnum: self.client.raw_api.post(
                f"Tracking/Plan/{plan_id}/Style/View/{view_id}"
                + f"?pageSize={psize}&pageNumber={pnum}",
                body={
                    "filters": filters,
                },
            ),
        )

    def plan_style_timeline_update(self, plan_id: str, timelines):
        """Updates timelines in a plan

        :plan_id: Id of Style plan
        :timelines: List of timeline dictionaries to update
        :returns:

        """
        return self.client.raw_api.post(
            f"Tracking/Plan/{plan_id}/Style/Timelines/Edit", body=timelines
        )

    def plan_material_timeline_list(self, plan_id: str, filters=None):
        """Returns a list of material plan timeline records from specific plan
           Filtering is applied if specified

        :plan_id: Plan ID
        :filters: Filters
        :returns: List of Material Timeline records

        """
        return self.client.beproduct_paging_iterator(
            20,
            lambda psize, pnum: self.client.raw_api.post(
                f"Tracking/Plan/{plan_id}/Material/Timeline"
                + f"?pageSize={psize}&pageNumber={pnum}",
                body={
                    "filters": filters,
                },
            ),
        )

    def plan_material_tracking_view(self, plan_id: str, view_id: str, filters=None):
        """Returns a list of material timeline records from specific plan
           Filtering is applied if specified

        :plan_id: Plan ID
        :view_id: Tracking view ID
        :filters: Filters
        :returns: List of Style Timeline records

        """
        return self.client.beproduct_paging_iterator(
            20,
            lambda psize, pnum: self.client.raw_api.post(
                f"Tracking/Plan/{plan_id}/Material/View/{view_id}"
                + f"?pageSize={psize}&pageNumber={pnum}",
                body={
                    "filters": filters,
                },
            ),
        )

    def plan_material_timeline_update(self, plan_id: str, timelines):
        """Updates timelines in a plan

        :plan_id: Id of Style plan
        :timelines: List of timeline dictionaries to update
        :returns:

        """
        return self.client.raw_api.post(
            f"Tracking/Plan/{plan_id}/Material/Timelines/Edit", body=timelines
        )

    def plan_style_progress(self, plan_id: str):
        """Style progress summary of a plan

        :plan_id: Plan ID
        :returns: Progress dictionary

        """
        return self.client.raw_api.get(f"Tracking/Plan/{plan_id}/Style/Progress")

    def plan_material_progress(self, plan_id: str):
        """Material progress summary of a plan

        :plan_id: Plan ID
        :returns: Progress dictionary

        """
        return self.client.raw_api.get(f"Tracking/Plan/{plan_id}/Material/Progress")

    def plan_style_revisions(self, plan_id: str, filters=None):
        """Style timeline revision history of a plan

        :plan_id: Plan ID
        :filters: Filters
        :returns: Enumerator of revisions

        """
        return self.client.beproduct_paging_iterator(
            20,
            lambda psize, pnum: self.client.raw_api.post(
                f"Tracking/Plan/{plan_id}/Style/Revisions?pageSize={psize}&pageNumber={pnum}",
                body={"filters": filters or []},
            ),
        )

    def plan_material_revisions(self, plan_id: str, filters=None):
        """Material timeline revision history of a plan

        :plan_id: Plan ID
        :filters: Filters
        :returns: Enumerator of revisions

        """
        return self.client.beproduct_paging_iterator(
            20,
            lambda psize, pnum: self.client.raw_api.post(
                f"Tracking/Plan/{plan_id}/Material/Revisions?pageSize={psize}&pageNumber={pnum}",
                body={"filters": filters or []},
            ),
        )

    def plan_style_add(self, plan_id: str, style_ids):
        """Adds styles to a plan (one timeline per style)

        :plan_id: Plan ID
        :style_ids: List of style IDs

        """
        return self.client.raw_api.post(f"Tracking/Plan/{plan_id}/Style/Add", body=style_ids)

    def plan_style_by_colorway_add(self, plan_id: str, style_ids):
        """Adds styles to a plan with one timeline per colorway of each style

        :plan_id: Plan ID
        :style_ids: List of style IDs

        """
        return self.client.raw_api.post(f"Tracking/Plan/{plan_id}/StyleByColorway/Add", body=style_ids)

    def plan_style_by_sku_add(self, plan_id: str, items):
        """Adds styles to a plan with one timeline per SKU

        :plan_id: Plan ID
        :items: [{"headerId": style_id, "sku": [{"colorwayId": ..., "sizes": ["S", "M"]}]}]
        :returns: Created timelines [{id, headerId, headerFolderId}]

        """
        return self.client.raw_api.post(f"Tracking/Plan/{plan_id}/StyleBySKU/Add", body=items)

    def plan_material_add(self, plan_id: str, material_ids):
        """Adds materials to a plan (one timeline per material)

        :plan_id: Plan ID
        :material_ids: List of material IDs

        """
        return self.client.raw_api.post(f"Tracking/Plan/{plan_id}/Material/Add", body=material_ids)

    def plan_material_by_colorway_add(self, plan_id: str, material_ids):
        """Adds materials to a plan with one timeline per colorway of each material

        :plan_id: Plan ID
        :material_ids: List of material IDs

        """
        return self.client.raw_api.post(f"Tracking/Plan/{plan_id}/MaterialByColorway/Add", body=material_ids)

    def plan_style_timelines_delete(self, plan_id: str, timeline_ids):
        """Deletes style timelines from a plan

        :plan_id: Plan ID
        :timeline_ids: List of timeline IDs

        """
        return self.client.raw_api.post(
            f"Tracking/Plan/{plan_id}/Style/Timelines/Delete", body={"timelineIds": timeline_ids}
        )

    def plan_style_timelines_archive(self, plan_id: str, timeline_ids):
        """Archives style timelines of a plan

        :plan_id: Plan ID
        :timeline_ids: List of timeline IDs

        """
        return self.client.raw_api.post(f"Tracking/Plan/{plan_id}/Style/Timelines/Archive", body=timeline_ids)

    def plan_material_timelines_delete(self, plan_id: str, timeline_ids):
        """Deletes material timelines from a plan

        :plan_id: Plan ID
        :timeline_ids: List of timeline IDs

        """
        return self.client.raw_api.post(
            f"Tracking/Plan/{plan_id}/Material/Timelines/Delete", body={"timelineIds": timeline_ids}
        )

