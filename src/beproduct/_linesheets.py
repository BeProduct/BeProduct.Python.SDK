"""
File: _linesheets.py
Author: Yuri Golub
Email: yuri.golub@beproduct.com
Github: https://github.com/BeProduct
Description: Line Sheets Public API
"""

from .sdk import BeProduct, BeProductAsync


class LineSheets:
    """Implements Line Sheets API"""

    def __init__(self, client: BeProduct | BeProductAsync):
        """Constructor"""
        self.client = client

    def folders(self, master_folder: str = None):
        """Lists line sheet folders

        :master_folder: Restrict to 'Style' or 'Material' (optional)
        :returns: List of folders

        """
        q = f"?masterFolder={master_folder}" if master_folder else ""
        return self.client.raw_api.get(f"LineSheet/ListLineSheetFolders{q}")

    def list(self, folder_id: str = None, name: str = None, description: str = None):
        """Lists line sheets, optionally filtered

        :folder_id: Line sheet folder ID
        :name: Name filter
        :description: Description filter
        :returns: List of line sheets

        """
        params = {"folderId": folder_id, "lineSheetName": name, "lineSheetDescription": description}
        q = "&".join(f"{k}={v}" for k, v in params.items() if v)
        return self.client.raw_api.get("LineSheet/ListLineSheets" + (f"?{q}" if q else ""))

    def get(self, linesheet_id: str):
        """Gets one line sheet

        :linesheet_id: Line sheet ID
        :returns: Line sheet dictionary

        """
        return self.client.raw_api.get(f"LineSheet/get/{linesheet_id}")
