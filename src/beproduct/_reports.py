"""
File: _reports.py
Author: Yuri Golub
Email: yuri.golub@beproduct.com
Github: https://github.com/BeProduct
Description: Reports Public API
"""

from .sdk import BeProduct, BeProductAsync


class Reports:
    """Implements Reports API"""

    def __init__(self, client: BeProduct | BeProductAsync):
        """Constructor"""
        self.client = client

    def list(self, page_size: int = 30):
        """Lists available reports

        :page_size: Page size
        :returns: Enumerator of reports

        """
        return self.client.beproduct_paging_iterator(
            page_size,
            lambda psize, pnum: self.client.raw_api.get(
                f"Report/List?pageSize={psize}&pageNumber={pnum}"
            ),
        )

    def data(self, report_id: str, search, page_size: int = 100, page_number: int = 0):
        """Runs a report and returns one page of its data

        :report_id: Report ID
        :search: Report filter dictionary (may be empty)
        :page_size: Rows per page
        :page_number: Zero-based page
        :returns: Page of report rows

        """
        return self.client.raw_api.post(
            f"Report/Data/{report_id}?pageSize={page_size}&pageNumber={page_number}", body=search
        )

    def flat_bom(self, search, page_size: int = 100, page_number: int = 0):
        """Flat BOM report: one row per style x material

        :search: BOM search filter dictionary (may be empty)
        :page_size: Rows per page
        :page_number: Zero-based page
        :returns: Page of flat BOM rows

        """
        return self.client.raw_api.post(
            f"Report/FlatBom?pageSize={page_size}&pageNumber={page_number}", body=search
        )
