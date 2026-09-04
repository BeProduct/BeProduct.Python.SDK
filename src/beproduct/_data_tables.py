"""
File: _data_tables.py
Author: Yuri Golub
Email: yuri.golub@beproduct.com
Github: https://github.com/BeProduct
Description: Data Tables Public API
"""

from .sdk import BeProduct, BeProductAsync


class DataTables:
    """Implements Data Tables API — reference tables and their rows"""

    def __init__(self, client: BeProduct | BeProductAsync):
        """Constructor"""
        self.client = client

    def list(self, filters=None, page_size: int = 30):
        """Lists data tables

        :filters: List of filter dictionaries
        :page_size: Page size
        :returns: Enumerator of data tables

        """
        return self.client.beproduct_paging_iterator(
            page_size,
            lambda psize, pnum: self.client.raw_api.post(
                f"DataTable/List?pageSize={psize}&pageNumber={pnum}", body={"filters": filters or []}
            ),
        )

    def schema(self, data_table_id: str):
        """Gets the column schema of a data table

        :data_table_id: Data table ID
        :returns: Schema

        """
        return self.client.raw_api.get(f"DataTable/{data_table_id}/Schema")

    def data(self, data_table_id: str, filters=None, page_size: int = 30):
        """Lists the rows of a data table

        :data_table_id: Data table ID
        :filters: List of filter dictionaries
        :page_size: Page size
        :returns: Enumerator of rows

        """
        return self.client.beproduct_paging_iterator(
            page_size,
            lambda psize, pnum: self.client.raw_api.post(
                f"DataTable/{data_table_id}/Data?pageSize={psize}&pageNumber={pnum}",
                body={"filters": filters or []},
            ),
        )

    def update(self, data_table_id: str, rows):
        """Inserts / updates / deletes rows of a data table

        :data_table_id: Data table ID
        :rows: List of row dictionaries

        """
        return self.client.raw_api.post(f"DataTable/{data_table_id}/Update", body=rows)

    def reset(self, data_table_id: str):
        """Removes every row of a data table

        :data_table_id: Data table ID

        """
        return self.client.raw_api.post(f"DataTable/{data_table_id}/Reset", body={})
