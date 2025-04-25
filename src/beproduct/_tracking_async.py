"""
File: _tracking_async.py
Author: Yuri Golub
Email: yuri.golub@beproduct.com
Github: https://github.com/BeProduct
Description: BeProduct Public API Tracking methods - Async Version
"""

from .sdk_async import BeProductAsync


class TrackingAsync():
    """
    Implements Image API - Async Version
    """

    def __init__(self, client: BeProductAsync):
        self.client = client

    async def folders(self):
        """List of available tracking folders asynchronously
        :returns: List of tracking folder objects

        """
        return await self.client.raw_api.get('Tracking/Folders')

    async def plan_list(self, filters=None, folder_id: str = None):
        """ Returns plan list and performs filtering
            if necessary asynchronously

        :filters: List of plan filters to apply search
        :folder_id: Folder ID if search needs to be within a folder
        :returns: Async iterator of plans

        """
        async def get_page(psize, pnum):
            return await self.client.raw_api.post(
                f"Tracking/Plans?folderId={folder_id}" +
                f"&pageSize={psize}&pageNumber={pnum}",
                body={
                    'filters':  filters,
                    'colorwayFilters': []
                })

        # Create an async generator
        async def async_iterator():
            page_size = 30
            page_number = 1
            while True:
                page = await get_page(page_size, page_number)
                if not page or not page.get('items'):
                    break
                for item in page['items']:
                    yield item
                if page.get('isLastPage'):
                    break
                page_number += 1

        return async_iterator()

    async def plan_get(self, plan_id: str):
        """Returns a plan by ID asynchronously

        :plan_id: Plan ID
        :returns: Requested plan

        """
        return await self.client.raw_api.post(f"Tracking/Plan/{plan_id}", body={})

    async def plan_style_timeline_list(self, plan_id: str, filters=None):
        """Returns a list of style timeline records from specific plan
           Filtering is applied if specified asynchronously

        :plan_id: Plan ID
        :filters: Filters
        :returns: Async iterator of Style Timeline records

        """
        async def get_page(psize, pnum):
            return await self.client.raw_api.post(
                f"Tracking/Plan/{plan_id}/Style/Timeline" +
                f"?pageSize={psize}&pageNumber={pnum}",
                body={
                    'filters':  filters,
                })

        # Create an async generator
        async def async_iterator():
            page_size = 20
            page_number = 1
            while True:
                page = await get_page(page_size, page_number)
                if not page or not page.get('items'):
                    break
                for item in page['items']:
                    yield item
                if page.get('isLastPage'):
                    break
                page_number += 1

        return async_iterator()

    async def plan_style_tracking_view(self, plan_id: str, view_id: str, filters=None):
        """Returns a list of style timeline records from specific plan
           Filtering is applied if specified asynchronously

        :plan_id: Plan ID
        :view_id: Tracking view ID
        :filters: Filters
        :returns: Async iterator of Style Timeline records

        """
        async def get_page(psize, pnum):
            return await self.client.raw_api.post(
                f"Tracking/Plan/{plan_id}/Style/View/{view_id}" +
                f"?pageSize={psize}&pageNumber={pnum}",
                body={
                    'filters':  filters,
                })

        # Create an async generator
        async def async_iterator():
            page_size = 20
            page_number = 1
            while True:
                page = await get_page(page_size, page_number)
                if not page or not page.get('items'):
                    break
                for item in page['items']:
                    yield item
                if page.get('isLastPage'):
                    break
                page_number += 1

        return async_iterator()

    async def plan_style_timeline_update(self,  plan_id: str, timelines):
        """ Updates timelines in a plan asynchronously

        :plan_id: Id of Style plan
        :timelines: List of timeline dictionaries to update
        :returns:

        """
        return await self.client.raw_api.post(
            f"Tracking/Plan/{plan_id}/Style/Timelines/Edit",
            body=timelines)

    async def plan_material_timeline_list(self, plan_id: str, filters=None):
        """Returns a list of material plan timeline records from specific plan
           Filtering is applied if specified asynchronously

        :plan_id: Plan ID
        :filters: Filters
        :returns: Async iterator of Material Timeline records

        """
        async def get_page(psize, pnum):
            return await self.client.raw_api.post(
                f"Tracking/Plan/{plan_id}/Material/Timeline" +
                f"?pageSize={psize}&pageNumber={pnum}",
                body={
                    'filters':  filters,
                })

        # Create an async generator
        async def async_iterator():
            page_size = 20
            page_number = 1
            while True:
                page = await get_page(page_size, page_number)
                if not page or not page.get('items'):
                    break
                for item in page['items']:
                    yield item
                if page.get('isLastPage'):
                    break
                page_number += 1

        return async_iterator()

    async def plan_material_tracking_view(self, plan_id: str, view_id: str, filters=None):
        """Returns a list of material timeline records from specific plan
           Filtering is applied if specified asynchronously

        :plan_id: Plan ID
        :view_id: Tracking view ID
        :filters: Filters
        :returns: Async iterator of Style Timeline records

        """
        async def get_page(psize, pnum):
            return await self.client.raw_api.post(
                f"Tracking/Plan/{plan_id}/Material/View/{view_id}" +
                f"?pageSize={psize}&pageNumber={pnum}",
                body={
                    'filters':  filters,
                })

        # Create an async generator
        async def async_iterator():
            page_size = 20
            page_number = 1
            while True:
                page = await get_page(page_size, page_number)
                if not page or not page.get('items'):
                    break
                for item in page['items']:
                    yield item
                if page.get('isLastPage'):
                    break
                page_number += 1

        return async_iterator()

    async def plan_material_timeline_update(self,  plan_id: str, timelines):
        """ Updates timelines in a plan asynchronously

        :plan_id: Id of Style plan
        :timelines: List of timeline dictionaries to update
        :returns:

        """
        return await self.client.raw_api.post(
            f"Tracking/Plan/{plan_id}/Material/Timelines/Edit",
            body=timelines) 