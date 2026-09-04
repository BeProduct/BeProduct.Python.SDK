"""
File: _style.py
Author: Yuri Golub
Email: yuri.golub@beproduct.com
Github: https://github.com/BeProduct
Description: BeProduct Public API Style methods
"""

from .sdk import BeProduct
from ._common_upload import UploadMixin
from ._common_attributes import AttributesMixin
from ._common_apps import AppsMixin
from ._common_comments import CommentsMixin
from ._common_revisions import RevisionsMixin
from ._common_share import ShareMixin
from ._common_tags import TagsMixin

from ._exception import BeProductException


class Style(
    UploadMixin,
    AttributesMixin,
    AppsMixin,
    CommentsMixin,
    RevisionsMixin,
    ShareMixin,
    TagsMixin,
):
    """
    Implements Style API
    """

    def __init__(self, client: BeProduct):
        self.client = client
        self.master_folder = "Style"

    def folder_colorway_schema(self, folder_id: str):
        """Gets colorway schema (list of fields ) for a folder

        :folder_id: ID of the folder
        :returns: Colorway schema

        """
        return self.client.raw_api.get(f"Style/ColorwaySchema?folderId={folder_id}")

    # ATTRIBUTES

    def attributes_update(
        self, header_id: str, fields=None, colorways=None, sizes=None
    ):
        """Updates style attributes

        :header_id: ID of the style
        :fields: Dictionary of fields {'field_id':'field_value'}
        :colorways Dictionary in Colorway update format
        :sizes Dictionary in Size format
        :returns: dictionary of the requested style attributes

        """

        # transform attributes dictionary
        unwound_attributes_fields = []
        if fields:
            for field_id in fields:
                unwound_attributes_fields.append(
                    {"id": field_id, "value": fields[field_id]}
                )

        # transform colorway dictionary
        colorway_fields = []
        if colorways:
            for color in colorways:
                unwound_colorway_fields = []

                for field_id in color["fields"]:
                    unwound_colorway_fields.append(
                        {"id": field_id, "value": color["fields"][field_id]}
                    )

                api_colorway = {
                    'id': color['id'],
                    'fields': unwound_colorway_fields
                }

                if 'imageHeaderId' in color:
                    api_colorway['imageHeaderId'] = color['imageHeaderId']
                if 'unlinkImage' in color:
                    api_colorway['unlinkImage'] = color['unlinkImage']
                if 'colorSourceId' in color:
                    api_colorway['colorSourceId'] = color['colorSourceId']

                colorway_fields.append(api_colorway)

        return self.client.raw_api.post(
            f"Style/Header/{header_id}/Update",
            {
                "fields": unwound_attributes_fields,
                "colorways": colorway_fields,
                "sizes": sizes,
            },
        )

    def attributes_create(self, folder_id: str, fields, colorways=None, sizes=None, force_version_update: bool = False):
        """Creates new style

        :folder_id: ID of the folder to create style in
        :fields: Dictionary of fields {'field_id':'field_value'}
        :colorways Dictionary of colorway fields
        :sizes Dictionary in Size format
        :force_version_update: If true, the header version from fields will be applied on creation
        :returns: dictionary of the created style attributes
        """

        # transform attributes dictionary
        unwound_attributes_fields = []
        for field_id in fields:
            unwound_attributes_fields.append(
                {"id": field_id, "value": fields[field_id]}
            )

        # transform colorway dictionary
        colorway_fields = []
        if colorways:
            for color in colorways:
                unwound_colorway_fields = []

                for field_id in color["fields"]:
                    unwound_colorway_fields.append(
                        {"id": field_id, "value": color["fields"][field_id]}
                    )

                api_colorway = {
                    'id': color['id'],
                    'fields': unwound_colorway_fields
                }

                if 'imageHeaderId' in color:
                    api_colorway['imageHeaderId'] = color['imageHeaderId']
                if 'unlinkImage' in color:
                    api_colorway['unlinkImage'] = color['unlinkImage']
                if 'colorSourceId' in color:
                    api_colorway['colorSourceId'] = color['colorSourceId']

                colorway_fields.append(api_colorway)

        return self.client.raw_api.post(
            f"Style/Header/Create?folderId={folder_id}&preserveVersion={str(force_version_update).lower()}",
            {
                "fields": unwound_attributes_fields,
                "colorways": colorway_fields,
                "sizes": sizes,
            },
        )

    def attributes_colorway_delete(self, header_id: str, colorway_id: str):
        """Deletes single colorway from Attributes app

        :header_id: Style ID
        :colorway_id: ID of the colorway to be deleted

        """
        return self.client.raw_api.get(
            f"Style/Header/{header_id}/Colorway/Delete/{colorway_id}"
        )

    def attributes_colorway_upload(
        self,
        header_id: str,
        colorway_id: str = None,
        filepath: str = None,
        fileurl: str = None,
        color_number: str = None,
    ):
        """Uploads colorway image

        :header_id: Style ID
        :colorway_id: Colorway ID
        :color_number: Color number
        :filepath: Local file path
        :fileurl: Remote file URL
        :returns: Upload ID

        """
        if filepath:
            return self.client.raw_api.upload_local_file(
                filepath,
                f"Style/Header/{header_id}/ColorwayImage/Upload?"
                + f"colorNumber={color_number}&colorId={colorway_id}",
            )
        if fileurl:
            return self.client.raw_api.upload_from_url(
                fileurl,
                f"Style/Header/{header_id}/ColorwayImage/Upload?"
                + f"colorNumber={color_number}&colorId={colorway_id}",
            )

        return BeProductException("No file provided")

    # APPS

    def app_sku_generate(self, header_id: str, app_id: str):
        """Populates SKU with actual data from Attributes app

        :header_id: ID of the Style
        :app_id: App ID
        :returns: SKU app dictionary

        """
        return self.client.raw_api.post(f"Style/Sku/{header_id}/{app_id}/Generate", {})

    def app_sku_update(self, header_id, app_id, fields):
        """Updates fields in individual SKU rows

        :header_id: ID of the Style
        :app_id: App ID
        :fields: Fields dictionary
        :returns: SKU app dictionary

        """
        return self.client.raw_api.post(
            f"Style/PageSku?headerId={header_id}&pageId={app_id}", body=fields
        )

    def app_artboard_version_upload(
        self, header_id: str, filepath: str = None, fileurl: str = None
    ):
        """Uploads an image as a new version into Artboard application

        :header_id: Style ID
        :filepath: Local file path
        :fileurl: Remote file URL
        :returns: Upload ID

        """
        if filepath:
            return self.client.raw_api.upload_local_file(
                filepath, f"Style/Header/{header_id}/Image/Upload"
            )
        if fileurl:
            return self.client.raw_api.upload_from_url(
                fileurl, f"Style/Header/{header_id}/Image/Upload"
            )

        return BeProductException("No file provided")

    def app_bom_update(self, header_id: str, app_id: str, rows):
        """Updates BOM application

        :header_id: ID of the style, material, etc
        :app_id: ID of the application / page
        :row: List of row/material dictionaries

        """

        return self.client.raw_api.post(
            f"Style/PageCBOM?headerId={header_id}&pageId={app_id}", body=rows
        )

    # ── BOM Variations app ──────────────────────────────────────────────
    # A BOMVariations app holds several parallel BOMs on one style, each with
    # its own rows, colour pitches and variation-level metadata. Style only.

    def app_bom_variation_schema(self, app_id: str):
        """Schema of a BOM Variations application

        :app_id: ID of the BOM Variations application / page
        :returns: dict with `enableBomVariations`, `metadata` (variation-level
                  fields) and `grid` (row-level fields)

        """
        return self.client.raw_api.get(f"Style/PageSchema?pageId={app_id}")

    def app_bom_variation_list(self, header_id: str, app_id: str):
        """Lists the variations of a BOM Variations application (metadata only)

        The API returns a list when variations are enabled on the app and a
        single object carrying rows (the implicit default variation) when they
        are not; this method always returns a list. Rows are not included —
        use app_bom_variation_get.

        Caution: on an app with `enableBomVariations` false this read CREATES
        the default variation server-side. Check app_bom_variation_schema first
        if your code must not write.

        :header_id: Style ID
        :app_id: ID of the BOM Variations application / page
        :returns: List of variation metadata dictionaries

        """
        page = self.client.raw_api.get(
            f"Style/Page?headerId={header_id}&pageId={app_id}"
        )
        data = page.get("data") if isinstance(page, dict) else None
        if data is None:
            return []
        if isinstance(data, list):
            return data
        return [data.get("metadata") or data]

    def app_bom_variation_get(self, header_id: str, app_id: str, variation_id: str):
        """Gets one BOM variation with its rows and colour pitches

        :header_id: Style ID
        :app_id: ID of the BOM Variations application / page
        :variation_id: Variation ID (from app_bom_variation_list)
        :returns: Variation dictionary: `id`, `metadata`, `rows`, audit fields

        """
        return self.client.raw_api.get(
            f"Style/{header_id}/PageBomVariation/{app_id}/Variation/{variation_id}"
        )

    def app_bom_variation_create(self, header_id: str, app_id: str, variation):
        """Creates a BOM variation

        Requires variations to be enabled on the app; fails once its
        `MaxBomVariations` limit is reached.

        :header_id: Style ID
        :app_id: ID of the BOM Variations application / page
        :variation: dict with any of `variationName`, `isDefault`,
                    `syncColorways`, `selectedVariationColorways`,
                    `metadataFields` ([{id, value}]) and `rows`
                    ([{materialId, rowFields: [{id, value}], colorUpdate: [...]}])
        :returns: The created variation

        """
        return self.client.raw_api.post(
            f"Style/{header_id}/PageBomVariation/{app_id}/CreateVariation",
            body=variation,
        )

    def app_bom_variation_update(
        self, header_id: str, app_id: str, variation_id: str, update
    ):
        """Incrementally updates one BOM variation — rows, colour pitches, metadata

        Only what is present in `update` changes. Server rules: deleting a
        `rowId` the server does not know is a 400; `UserLabel` and
        `FormulaField` grid fields are read-only; the default variation cannot
        be un-defaulted (make another one the default instead).

        :header_id: Style ID
        :app_id: ID of the BOM Variations application / page
        :variation_id: Variation ID
        :update: dict — same keys as app_bom_variation_create; a row without
                 `rowId` is added, `deleteRow: True` removes one;
                 `selectedVariationColorwaysUpdate: {add: [...], remove: [...]}`
                 patches the colourway list
        :returns: The updated variation

        """
        return self.client.raw_api.post(
            f"Style/{header_id}/PageBomVariation/{app_id}/Variation/{variation_id}/Update",
            body=update,
        )

    def app_bom_variation_reset(self, header_id: str, app_id: str, variation_id: str):
        """Clears every row of a BOM variation; its metadata is kept

        :header_id: Style ID
        :app_id: ID of the BOM Variations application / page
        :variation_id: Variation ID
        :returns: The reset variation

        """
        return self.client.raw_api.post(
            f"Style/{header_id}/PageBomVariation/{app_id}/Variation/{variation_id}/Reset",
            body={},
        )

    def app_bom_variation_delete(self, header_id: str, app_id: str, variation_id: str):
        """Permanently deletes a BOM variation. The default variation cannot be deleted.

        :header_id: Style ID
        :app_id: ID of the BOM Variations application / page
        :variation_id: Variation ID

        """
        return self.client.raw_api.delete(
            f"Style/{header_id}/PageBomVariation/{app_id}/Variation/{variation_id}"
        )

    # ── parity with the TypeScript SDK ──────────────────────────────────

    def folder_size_range_schema(self, folder_id: str):
        """Gets the size-range schema (list of fields) for a style folder

        :folder_id: ID of the folder
        :returns: Size range schema

        """
        return self.client.raw_api.get(f"Style/SizeRangeSchema?folderId={folder_id}")

    def app_request_schema(self, app_id: str):
        """Schema of a request application (sample requests)

        :app_id: ID of the request application / page
        :returns: Request page schema

        """
        return self.client.raw_api.get(f"Request/PageSchema?pageId={app_id}")

    def attributes_where_used_in_sets(self, header_id: str):
        """Lists the Sets apps (on other styles) that reference this style

        :header_id: Style ID
        :returns: List of where-used entries

        """
        return self.client.raw_api.get(f"Style/WhereUsedInSets/{header_id}")

    def flat_bom(self, search, page_size: int = 100, page_number: int = 0):
        """Flat BOM report: one row per style x material across the company

        :search: BOM search filter dictionary (may be empty)
        :page_size: Rows per page
        :page_number: Zero-based page
        :returns: Page of flat BOM rows

        """
        return self.client.raw_api.post(
            f"Style/FlatBom?pageSize={page_size}&pageNumber={page_number}", body=search
        )

    def app_textlist_update(self, header_id: str, app_id: str, list_items):
        """Updates the items of a TextList application

        :header_id: Style ID
        :app_id: ID of the TextList application / page
        :list_items: [{"itemId": ..., "itemFields": [{"id": ..., "value": ...}]}]
                     Omit itemId to add an item; set "deleteItem": True to remove one.

        """
        return self.client.raw_api.post(
            f"Style/PageTextList/List?headerId={header_id}&pageId={app_id}", body=list_items
        )

    def app_textlist_editor_update(self, header_id: str, app_id: str, editor_data: str):
        """Replaces the rich-text editor content of a TextList application

        :header_id: Style ID
        :app_id: ID of the TextList application / page
        :editor_data: HTML string

        """
        return self.client.raw_api.post(
            f"Style/PageTextList/TextEditor?headerId={header_id}&pageId={app_id}",
            body={"editorData": editor_data},
        )

    def app_bom_details_update(self, header_id: str, app_id: str, materials):
        """Updates a BOM Details application

        :header_id: Style ID
        :app_id: ID of the BOM Details application / page
        :materials: List of material detail dictionaries

        """
        return self.client.raw_api.post(
            f"Style/{header_id}/PageBOMDetails/{app_id}", body={"materials": materials}
        )

    def app_bom_item_delete(self, header_id: str, app_id: str, row_id: str):
        """Deletes one row from a BOM application

        :header_id: Style ID
        :app_id: ID of the BOM application / page
        :row_id: BOM row ID

        """
        return self.client.raw_api.delete(
            f"Style/PageCBOMItemDelete?headerId={header_id}&pageId={app_id}&rowId={row_id}"
        )

    def app_bom_reset(self, header_id: str, app_id: str):
        """Removes every row from a BOM application

        :header_id: Style ID
        :app_id: ID of the BOM application / page

        """
        return self.client.raw_api.post(f"Style/{header_id}/CBOM/{app_id}/Reset", body={})

    def app_sets_update(self, header_id: str, app_id: str, items):
        """Updates a Sets application

        :header_id: Style ID
        :app_id: ID of the Sets application / page
        :items: [{"styleIdToInsert": ..., "styleUpdate": {"rowId": ..., "rowFields": [...]}}]

        """
        return self.client.raw_api.post(
            f"Style/PageSets?headerId={header_id}&pageId={app_id}", body=items
        )

    def app_multimeasurements_update(self, header_id: str, app_id: str, data):
        """Updates a MultiMeasurements (points of measure) application

        :header_id: Style ID
        :app_id: ID of the MultiMeasurements application / page
        :data: {"sizeClass": ..., "poms": [{"id": ..., "code": ..., "pointOfMeasure": ...}]}

        """
        return self.client.raw_api.post(
            f"Style/{header_id}/PageMultiMeasurements/{app_id}", body=data
        )

    def app_multimeasurements_reset(self, header_id: str, app_id: str):
        """Resets a MultiMeasurements application

        :header_id: Style ID
        :app_id: ID of the MultiMeasurements application / page

        """
        return self.client.raw_api.post(
            f"Style/{header_id}/PageMultiMeasurements/{app_id}/Reset", body={}
        )

    def app_sample_request_multi_add_submit(
        self, header_id: str, app_id: str, data, timeline_id: str = None
    ):
        """Adds a submit to a multi-size Sample Request application

        :header_id: Style ID
        :app_id: ID of the SampleRequestMulti application / page
        :data: Submit dictionary
        :timeline_id: Tracking timeline ID for request apps (optional)

        """
        url = f"Style/{header_id}/PageSampleRequestMulti/{app_id}/AddSubmit"
        if timeline_id:
            url += f"?timelineId={timeline_id}"
        return self.client.raw_api.post(url, body=data)

    def app_link_pages_update(self, header_id: str, app_id: str, items):
        """Updates a Link Pages application

        :header_id: Style ID
        :app_id: ID of the LinkPages application / page
        :items: List of link item dictionaries

        """
        return self.client.raw_api.post(
            f"Style/PageLinkPages?headerId={header_id}&pageId={app_id}", body=items
        )

    def app_artboard_image_assign(self, body):
        """Assigns an existing image to a style artboard

        :body: Assignment dictionary as accepted by Style/ArtboardImageAssign

        """
        return self.client.raw_api.post("Style/ArtboardImageAssign", body=body)

    def attributes_update_sample_size(self, header_id: str, size_class_id: str, new_sample_size: str):
        """Changes the sample size of a size class

        :header_id: Style ID
        :size_class_id: Size class ID (see attributes_get()["sizeClasses"])
        :new_sample_size: Size name, e.g. "M"

        """
        return self.client.raw_api.post(
            f"Style/{header_id}/SizeClass/{size_class_id}/UpdateSampleSize",
            body={"newSampleSize": new_sample_size},
        )

    def attributes_block_link(self, header_id: str, block_header_id: str, size_classes=None):
        """Links a block to the style

        :header_id: Style ID
        :block_header_id: Block ID
        :size_classes: Optional list of size-class mappings

        """
        return self.client.raw_api.post(
            f"Style/Header/{header_id}/Block/Link",
            body={"blockHeaderId": block_header_id, "sizeClasses": size_classes},
        )

    def attributes_block_unlink(self, header_id: str):
        """Unlinks the block from the style

        :header_id: Style ID

        """
        return self.client.raw_api.get(f"Style/Header/{header_id}/Block/Unlink")

    def attributes_carry_over(self, header_id: str, skip_colorways: bool = False):
        """Carries the style over into a new style (copy)

        :header_id: Style ID
        :skip_colorways: Do not copy colorways
        :returns: The new style

        """
        return self.client.raw_api.post(
            f"Style/Header/{header_id}/CarryOver", body={"skipColorways": skip_colorways}
        )

    def attributes_move(self, header_id: str, target_folder_id: str, generate_new_header_number: bool = False):
        """Moves the style to another folder

        :header_id: Style ID
        :target_folder_id: Destination folder ID
        :generate_new_header_number: Assign a new style number in the destination folder

        """
        return self.client.raw_api.post(
            f"Style/Header/{header_id}/Move",
            body={"targetFolderId": target_folder_id,
                  "generateNewHeaderNumber": generate_new_header_number},
        )

    def attributes_colorways_delete(self, header_id: str, colorway_ids):
        """Deletes several colorways at once

        :header_id: Style ID
        :colorway_ids: List of colorway IDs

        """
        return self.client.raw_api.post(
            f"Style/Header/{header_id}/Colorways/Delete", body={"colorwayIds": colorway_ids}
        )

    def app_request_list(self, header_id: str):
        """List of request apps

        :header_id: Style ID
        :returns: List of Style Request Applications

        """
        return self.client.raw_api.get(f"Style/RequestPages?headerId={header_id}")

    def app_request_get(self, header_id: str, app_id: str, timeline_id: str = None):
        """Gets request level app

        :header_id: Style ID
        :app_id: App ID
        :timeline_id: (Optional) Plan Timeline ID if you need a specific app record
        :returns: List of Request Apps for all plan timelines where app exists

        """

        return self.client.raw_api.get(
            f"Style/RequestPage?headerId={header_id}&pageId={app_id}"
            + (f"&timelineId={timeline_id}" if timeline_id else "")
        )

    def app_request_form_update(
        self, header_id: str, app_id: str, timeline_id: str, fields
    ):
        """Updates form application

        :header_id: ID of the style, material, etc
        :app_id: ID of the application / page
        :timeline_id: Plan Timeline Id
        :fields: Dictionary of fields to update {'field_id':'value'}

        """
        return self.client.raw_api.post(
            f"Style/RequestPageForm?headerId={header_id}"
            + f"&pageId={app_id}&timelineId={timeline_id}",
            body=[{"id": field_id, "value": fields[field_id]} for field_id in fields],
        )

    def app_3D_style_turntable_upload(
        self,
        header_id: str,
        version_id: str = None,
        replace_images: bool = False,
        filepath: str = None,
        fileurl: str = None,
    ):
        """Uploads a zipped turntable images into 3D style app version

        :header_id: Style ID
        :version_id: Version ID or if None new version is created,
        :replace_images: Replace 3D style previews instead of adding
        :filepath: Local file path
        :fileurl: Remote file URL
        :returns: Upload ID

        """

        query = ""
        if version_id:
            query += f"versionId={version_id}&"
        if replace_images:
            query += "replaceImages=true&"

        if filepath:
            return self.client.raw_api.upload_local_file(
                filepath,
                f"Style/Header/{header_id}/Image/Upload/Turntable?"
                + (query if query else ""),
            )
        if fileurl:
            return self.client.raw_api.upload_from_url(
                fileurl,
                f"Style/Header/{header_id}/Image/Upload/Turntable?"
                + (query if query else ""),
            )

        return BeProductException("No file provided")

    def app_3D_style_version_create(
        self, header_id: str, app_id: str, version_name: str
    ):
        """Creates new 3D Style version

        :header_id: str,
        :app_id: str,
        :version_name: Version name
        :returns: Created version

        """
        return self.client.raw_api.post(
            f"Style/{header_id}/" + f"Page3DStyle/{app_id}/CreateVersion",
            body={"versionName": version_name},
        )

    def app_3D_style_version_copy(
        self, header_id: str, app_id: str, copy_from_version_id: str, version_name: str
    ):
        """Copy 3D Style version

        :header_id: Header ID,
        :app_id: 3D Style App Id,
        :copy_from_version_id: Version id to copy from
        :version_name: New version name
        :returns: Created version

        """
        return self.client.raw_api.post(
            f"Style/{header_id}/" + f"Page3DStyle/{app_id}/CreateVersion",
            body={"copyVersionId": copy_from_version_id, "versionName": version_name},
        )

    def app_3D_style_version_delete(self, header_id: str, app_id: str, version_id: str):
        """Delete 3D style version

        :header_id: Header ID,
        :app_id: 3D Style App id,
        :version_id: Version ID
        :copy_from_version_id: Version id to delete
        :returns: Throws BeProductException in case of error

        """
        return self.client.raw_api.delete(
            f"Style/{header_id}/" + f"Page3DStyle/{app_id}/Version/{version_id}"
        )

    def app_3D_style_version_update(
        self, header_id: str, app_id: str, version_id: str, version_update
    ):
        """Update 3D Style version

        :header_id: Header ID,
        :app_id: 3D Style App id,
        :version_id: Version ID
        :updated_version: Dict with version data to update
        :returns: Updated version

        """
        return self.client.raw_api.post(
            f"Style/{header_id}/" + f"Page3DStyle/{app_id}/Version/{version_id}/Update",
            body=version_update,
        )

    def app_3D_style_working_file_upload(
        self,
        header_id: str,
        app_id: str,
        version_id: str,
        filepath: str = None,
        fileurl: str = None,
    ):
        """Upload a file into 3D Style version

        :header_id: Header ID,
        :app_id: 3D Style App id,
        :version_id: Version ID
        :filepath: Local file path
        :fileurl: Remote file URL
        :returns: Upload ID

        """
        if filepath:
            return self.client.raw_api.upload_local_file(
                filepath,
                f"Style/{header_id}/Page3DStyle/{app_id}/Version/"
                + f"{version_id}/WorkingFile/Upload",
            )
        if fileurl:
            return self.client.raw_api.upload_from_url(
                fileurl,
                f"Style/{header_id}/Page3DStyle/{app_id}/Version/"
                + f"{version_id}/WorkingFile/Upload",
            )

        return BeProductException("No file provided")

    def app_3D_style_preview_upload(
        self,
        header_id: str,
        app_id: str,
        version_id: str,
        colorway_id: str,
        filepath: str = None,
        fileurl: str = None,
    ):
        """Upload a file into 3D Style version

        :header_id: Header ID,
        :app_id: 3D Style App id,
        :version_id: Version ID
        :colorway_id: Colorway ID,
        :filepath: Local file path
        :fileurl: Remote file URL
        :returns: Upload ID

        """

        if filepath:
            return self.client.raw_api.upload_local_file(
                filepath,
                f"Style/{header_id}/Page3DStyle/{app_id}/Version/"
                + f"{version_id}/Colorway/{colorway_id}/Preview/Upload",
            )
        if fileurl:
            return self.client.raw_api.upload_from_url(
                fileurl,
                f"Style/{header_id}/Page3DStyle/{app_id}/Version/"
                + f"{version_id}/Colorway/{colorway_id}/Preview/Upload",
            )

        return BeProductException("No file provided")
