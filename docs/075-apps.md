# Applications
**NOTE: Below examples are provided for the style API, but it is the same for every other master folder
(material/color/image/style).**
Make sure to call correct API `client.<material/style/color/image>.<api method>`

## Getting Style/Material/Image/Color applications

Each style within the **same style folder** has an identical set of applications(pages) associated with it.

**Important note**: Application IDs are not unique for a particular *style* but are unique for a *style folder*. Put it simply: 
Every *style folder* has the same application ID's for every style.

Example:
```python
apps = client.style.app_list(header_id='bab33ce0-867f-4141-b849-1b0c41f68c8b') # header_id = ID of the style
print(apps)
```
Example output:
```text
[
   {
      'id':'00000000-0000-0000-0000-000000000000',
      'title':'Artboard',
      'type':'Artboard'
   },
   {
      'id':'f9528ea5-703d-4c91-83a4-fb62325cb2bf',
      'title':'3D Style',
      'type':'3DStyle'
   },
   {
      'id':'fbd93c34-68de-4591-9224-984f23962fd2',
      'title':'DESIGN SPEC',
      'type':'Artboard'
   },
   {
      'id':'fa2ca4bf-b122-49bb-a30f-f2806c380698',
      'title':'Proto Sample',
      'type':'SampleRequestApp'
   },
   {
      'id':'d02754d0-3d94-42fd-9138-f86ff5186700',
      'title':'Tech Pack',
      'type':'TechPack'
   },
   {
      'id':'1af353a4-7ce2-46d1-a4ce-b7bb09ea70f9',
      'title':'Form Application',
      'type':'Form'
   }
]
```
You may want to *cache* the output above for every style folder to prevent calling the same method again and again for every style. 

After you know your **application id** from the previous function you can retrieve a particular style app as follows:
```python
my_app_content = client.style.app_get(
    header_id='bab33ce0-867f-4141-b849-1b0c41f68c8b',
    app_id='1af353a4-7ce2-46d1-a4ce-b7bb09ea70f9')
```

## Updating FORM-based applications
Style may contain simple customer defined *Form* applications.
Form application is just a dictionary of the attributes.
You may update a **form** app as follows:
```python

client.style.app_form_update(
    header_id='bab33ce0-867f-4141-b849-1b0c41f68c8b',
    app_id='1af353a4-7ce2-46d1-a4ce-b7bb09ea70f9',
    fields={
        'field_id_to_update': 'updated_value'
    })
```
## Updating GRID-based applications
Style may contain simple customer defined *Grid* applications.
This app is a table of rows where each row is a dictionary of the attributes/fields. 

Each row has an ID. To update a grid application we have to construct a list of rows to update. 

Below example performs 3 changes:

* Removes a row
* Creates a new row
* Updates a row

```python
# deletes row with id
delete_row = {
    'rowId': '1af353a4-7ce2-46d1-a4ce-b7bb09ea70f8',
    'deleteRow': True
}

# creates new row
new_row = {
    'rowFields': [ # NOTE that all required fields must be present
        {'id':'some_field_id','value':'some value'},
        {'id':'another_field_id','value':'some value'},
    ]
}

# updates row with id
update_row = {
    'rowId': '2af353a4-7ce2-46d1-a4ce-b7bb09ea70f8',
    'rowFields': [
        {'id':'some_field_id','value':'some value'},
        {'id':'another_field_id','value':'some value'},
    ]
}

client.style.app_grid_update(
    header_id='bab33ce0-867f-4141-b849-1b0c41f68c8b', # Style ID
    app_id='1af353a4-7ce2-46d1-a4ce-b7bb09ea70f9',    # Grid app id
    rows=[delete_row, new_row, update_row])
```

## Uploading images to Artboard app

Artboard app exist only in Styles and Materials. SDK allows adding new versions to the Artboard app

```python
# Uploading local file
upload_id = client.style.app_artboard_version_upload(
    header_id='e81d3be5-f5c2-450f-888e-8a854dfc2824',   # Style ID
    filepath='/home/beproduct/your_image.jpg')          # File location 

# Uploading from remote URL
upload_id = client.style.app_artboard_version_upload(
    header_id='e81d3be5-f5c2-450f-888e-8a854dfc2824',   # Style ID
    fileurl="https://us.beproduct.com/your_image.jpg")  # File URL
```
To check the image upload processing status use the same technique as in [Attributes](./040-style-api.md#uploading-images-to-the-style-attributes)


## Updating LIST-based applications
You can create, update and delete list items using a single call. Also, there is a separate sdk/api call to upload images into list items.
### Updating LIST items
Below example performs 3 changes:

* Removes a list item
* Creates a new list item
* Updates a list item


```python
# deletes list item with id
delete_list_item = {
    'itemId': '1af353a4-7ce2-46d1-a4ce-b7bb09ea70f8',
    'deleteItem': True
}

# creates a new list item
new_list_item = {
    'itemFields': [ # NOTE that all required fields must be present
        {'id':'some_field_id','value':'some value'},
        {'id':'another_field_id','value':'some value'},
    ]
}

# updates a list item
update_list_item = {
    'itemId': '2af353a4-7ce2-46d1-a4ce-b7bb09ea70f8',
    'itemFields': [
        {'id':'some_field_id','value':'some value'},
        {'id':'another_field_id','value':'some value'},
    ]
}

client.style.app_list_update(
    header_id='bab33ce0-867f-4141-b849-1b0c41f68c8b', # Style ID
    app_id='1af353a4-7ce2-46d1-a4ce-b7bb09ea70f9',    # Grid app id
    list_items=[delete_list_item, new_list_item, update_list_item])
```

### Uploading images into LIST items
```python
# Uploading local file
upload_id = client.style.app_list_upload(
    header_id='e81d3be5-f5c2-450f-888e-8a854dfc2824',   # Style or Material ID
    app_id="1c1abc4a-8541-49d0-8eb4-01010c1e8d38",      # App ID
    list_item_id="430a9ddc-0889-4995-92c0-94db1ca37cbb",# List item ID
    filepath='/home/beproduct/your_image.jpg')          # File location 

# Uploading from remote URL
upload_id = client.style.app_list_upload(
    header_id='e81d3be5-f5c2-450f-888e-8a854dfc2824',   # Style or Material ID
    app_id="1c1abc4a-8541-49d0-8eb4-01010c1e8d38",      # App ID
    list_item_id="430a9ddc-0889-4995-92c0-94db1ca37cbb",# List item ID
    fileurl="https://us.beproduct.com/your_image.jpg")  # File URL
```

To check the image upload processing status use the same technique as in [Attributes](./040-style-api.md#uploading-images-to-the-style-attributes)


## Working with SKU app

Only Styles in BeProduct can have SKU apps.

### Generating SKUs
To generate all SKUs for your dimensions from Attributes page we could use code below:

```python
client.style.app_sku_generate(
    header_id='e81d3be5-f5c2-450f-888e-8a854dfc2824',   # Style ID
    app_id="1c1abc4a-8541-49d0-8eb4-01010c1e8d38",      # App ID
    )
```

### Updating SKU's fields
```python
client.style.app_sku_generate(
    header_id='e81d3be5-f5c2-450f-888e-8a854dfc2824',   # Style ID
    app_id="1c1abc4a-8541-49d0-8eb4-01010c1e8d38",      # App ID
    fields = [
      {
          "id": "GUID of the SKU row",
          "fields": [
                      {
                        "id": "field_id",
                        "value": "my value"
                      }
                    ]
      }, .... # more items follow if needed
    ]
  ) 
```
## Updating BOM app
```python

# delete material by row ID
delete_bom_material = {
  'materialUpdate': {
      'rowId': '2af353a4-7ce2-46d1-a4ce-b7bb09ea70f8',
      'deleteRow': True
  }
}

# Insert material by material ID
insert_existing_material = {
  'materialIdToInsert': '1af353a4-7ce2-46d1-a4ce-b7bb09ea70f9'
}

# update or ad-hoc new material
update_bom_material = {
  'materialUpdate': {
      'rowId': '2af353a4-7ce2-46d1-a4ce-b7bb09ea70f8', # Create new ad-hoc if row id is None, otherwise update
      'rowFields': [
        {
          'id': 'field_id',
          'value': 'value'
        },
        .... # other fields
      ],
  },
  'colorUpdate': [
    {
      'colorId': '<ANY GUID>',
      'colorNumber': 'color number',
      'colorName': 'color name',
      'hex': '000000',
      'colorwayId': 'string'
    }
  ]
}


client.style.app_bom_update(
    header_id='bab33ce0-867f-4141-b849-1b0c41f68c8b', # Style ID
    app_id='1af353a4-7ce2-46d1-a4ce-b7bb09ea70f9',    # Bom app id
    rows=[delete_bom_material, insert_existing_material, update_bom_material])
```


## Attachments app

### Uploading a file into Attachments app
```python
# Uploading local file
client.style.app_attachments_upload(
    header_id='e81d3be5-f5c2-450f-888e-8a854dfc2824',   # Style or Material ID
    app_id="1c1abc4a-8541-49d0-8eb4-01010c1e8d38",      # App ID
    filepath='/home/beproduct/your_image.jpg')          # File location 

# Uploading from remote URL
client.style.app_attachments_upload(
    header_id='e81d3be5-f5c2-450f-888e-8a854dfc2824',   # Style or Material ID
    app_id="1c1abc4a-8541-49d0-8eb4-01010c1e8d38",      # App ID
    fileurl="https://us.beproduct.com/your_image.jpg")  # File URL
```
Attachments app doesn't have a preview on files hence checking upload status is not required.
Upload is effective after the method call is finished.

### Deleting a file from Attachments app
```python
client.style.app_attachments_delete(
    header_id='e81d3be5-f5c2-450f-888e-8a854dfc2824',        # Style or Material ID
    app_id="1c1abc4a-8541-49d0-8eb4-01010c1e8d38",           # App ID
    filenames_to_remove = ['file1.name', 'file2.name',...]): # Filenames to remove
```

## ImageGrid and ImageForm Apps
To update grid and form components use `app_form_update` and `app_grid_update` correspondingly.
To upload images 
```python

# Uploading local file
# Uncomment needed below
#upload_id = client.style.app_imageform_upload(
#upload_id = client.style.app_imagegrid_upload(
    header_id='e81d3be5-f5c2-450f-888e-8a854dfc2824',   # Style or Material ID
    app_id="1c1abc4a-8541-49d0-8eb4-01010c1e8d38",      # App ID
    filepath='/home/beproduct/your_image.jpg')          # File location 

# Uploading from remote URL
# Uncomment needed below
# upload_id = client.style.app_imageform_upload(
# upload_id = client.style.app_imagegrid_upload(
    header_id='e81d3be5-f5c2-450f-888e-8a854dfc2824',   # Style or Material ID
    app_id="1c1abc4a-8541-49d0-8eb4-01010c1e8d38",      # App ID
    fileurl="https://us.beproduct.com/your_image.jpg")  # File URL
```

## 3D Style App
### Create 3D Style version

To create new 3D Style version:
```python
header_id = '46812b88-22ac-456a-b6df-ef4560ab3b13'
app_id = '3ad18337-b612-4eb1-af54-e639e81b0c97'

res = client.style.app_3D_style_version_create(
    header_id, app_id, 'Version Name')

print(res['id'])
```

### Update 3D Style version
To update existing 3D Style version:
```python
header_id = '46812b88-22ac-456a-b6df-ef4560ab3b13'
app_id = '3ad18337-b612-4eb1-af54-e639e81b0c97'
version_id = '6bee4817-8894-4c83-a20d-cc116db53322'

version_update = {
    'versionName': {
        'value': 'Updated version name'
    },
    'versionStatus': {
        'value': 'OnHold'  # Updating version status
    },
    'colorways': [
        # TO DELETE COLORWAY
        {
            'id': '74cf935e-a846-47c7-8a8e-dbaa02067aed',
            'deleteColorway': True,
        },
        # TO CREATE COLORWAY
        {
            'colorName': 'New color name'
        },
        # TO UPDATE COLORWAY
        {
            'id': 'b256fcd6-69d1-48ca-b0bc-65201d99e49c',
            # To map to the attributes colorway uncomment below
            # 'colorwayId': {
            #    'value': 'Attributes colorway ID'
            # },

            # 'mainImage': True, # make colorway a style main image
            # 'colorwayImage': True, # push to attributes colorway image if color is mapped

            'colorName': 'Updated name',
            'status': 'ForReview'
        }
    ]
}

client.style.app_3D_style_version_update(
    header_id, app_id, version_id, version_update)
```

### Copy 3D Style version
To copy/clone existing 3D Style version:
```python
header_id = '46812b88-22ac-456a-b6df-ef4560ab3b13'
app_id = '3ad18337-b612-4eb1-af54-e639e81b0c97'
copy_from_version_id = "e2ac0240-c086-414f-a03a-ec77e352a307"

res = client.style.app_3D_style_version_copy(
    header_id, app_id, copy_from_version_id, 'New Version Name')

print(res['id'])
```

### Delete 3D Style version
To delete existing 3D Style version:
```python
header_id = '46812b88-22ac-456a-b6df-ef4560ab3b13'
app_id = '3ad18337-b612-4eb1-af54-e639e81b0c97'
version_id = '0338df8d-1561-490a-89e3-6e7e4448774d'
client.style.app_3D_style_version_delete(header_id, app_id, version_id)
```

### Upload turntable into 3D Style app
You can upload new 3D turntable version into **3D style** app using below example:
```python
header_id = '46812b88-22ac-456a-b6df-ef4560ab3b13'
tt_zip_path = '/home/demo/demo_tt/turntable.zip' # must be None if you upload from url
tt_zip_url = None # because we are uploading local file this is None 
version_id = None  # if this is None new version will be created
# if version id is not None then you may choose to replace turntable images
replace_images = False

upload_id = client.style.app_3D_style_turntable_upload(
    header_id,
    version_id=version_id,
    replace_images=replace_images,
    filepath=tt_zip_path, # Uploading from file system
    fileurl=tt_zip_url    # Uploading from remote URL
    )
```
To check the image upload processing status use the same technique as in [Attributes](./040-style-api.md#uploading-images-to-the-style-attributes)

### Upload 3D Style working files
To upload a working file into existing 3D Style version:

```python
header_id = '46812b88-22ac-456a-b6df-ef4560ab3b13'
app_id = "3ad18337-b612-4eb1-af54-e639e81b0c97"
version_id = '6bee4817-8894-4c83-a20d-cc116db53322'
working_file_path = '/home/demo/file.bw'

upload_id = client.style.app_3D_style_working_file_upload(
    header_id, app_id, version_id,
    filepath=working_file_path
    # ,fileurl='https://file.url'  # or use url instead of local file path
    )
```
To check the upload processing status use the same technique as in [Attributes](./040-style-api.md#uploading-images-to-the-style-attributes)

### Upload 3D Style preview files
This method is used to upload a single preview file into existing 3D Style colorway within specific version. 

**NOTE:** If you need to batch upload previews/turntable use [Turntable Upload](./075-apps.md#upload-turntable-into-3d-style-app) instead.

```python
header_id = '46812b88-22ac-456a-b6df-ef4560ab3b13'
app_id = "3ad18337-b612-4eb1-af54-e639e81b0c97"
version_id = '6bee4817-8894-4c83-a20d-cc116db53322'
colorway_id = 'b256fcd6-69d1-48ca-b0bc-65201d99e49c'
preview_file = '/home/demo/image.png'

upload_id = client.style.app_3D_style_preview_upload(
    header_id, app_id, version_id, colorway_id
    filepath=preview_file
    # ,fileurl='https://file.url'  # or use url instead of local file path
    )
```
To check the upload processing status use the same technique as in [Attributes](./040-style-api.md#uploading-images-to-the-style-attributes)

## 3D Material App
### Uploading asset file into 3D material app
```python
# Uploading local file
upload_id = client.material.app_3d_material_asset_upload(
    header_id='c629fb8b-7a24-4773-b335-d0b6f38196f5',   # Style or Material ID
    app_id='1ad3f9a0-4e71-4325-a55f-d6c004fef38d',      # App ID
    colorway_id='70bb8273-7818-40f2-81e6-07931d8164f1', # Attributes colorway ID
    filepath='/home/beproduct/your_image.jpg')          # File location 

# Uploading from remote URL
upload_id = client.material.app_3d_material_asset_upload(
    header_id='c629fb8b-7a24-4773-b335-d0b6f38196f5',   # Style or Material ID
    app_id='1ad3f9a0-4e71-4325-a55f-d6c004fef38d',      # App ID
    colorway_id='70bb8273-7818-40f2-81e6-07931d8164f1', # Attributes colorway ID
    fileurl='https://us.beproduct.com/your_image.jpg')  # File URL
```
To check the image upload processing status use the same technique as in [Attributes](./040-style-api.md#uploading-images-to-the-style-attributes)

### Uploading a preview file into 3D material app
```python
# Uploading local file
upload_id = client.material.app_3d_material_preview_upload(
    header_id='c629fb8b-7a24-4773-b335-d0b6f38196f5',   # Style or Material ID
    app_id='1ad3f9a0-4e71-4325-a55f-d6c004fef38d',      # App ID
    colorway_id='70bb8273-7818-40f2-81e6-07931d8164f1', # Attributes colorway ID
    filepath='/home/beproduct/your_image.jpg')          # File location 

# Uploading from remote URL
upload_id = client.material.app_3d_material_preview_upload(
    header_id='c629fb8b-7a24-4773-b335-d0b6f38196f5',   # Style or Material ID
    app_id='1ad3f9a0-4e71-4325-a55f-d6c004fef38d',      # App ID
    colorway_id='70bb8273-7818-40f2-81e6-07931d8164f1', # Attributes colorway ID
    fileurl='https://us.beproduct.com/your_image.jpg')  # File URL
```
To check the image upload processing status use the same technique as in [Attributes](./040-style-api.md#uploading-images-to-the-style-attributes)

### Uploading front/back texture file into 3D material app
```python
# Uploading local file
upload_id = client.material.app_3d_material_texture_upload(
    header_id='c629fb8b-7a24-4773-b335-d0b6f38196f5',   # Style or Material ID
    app_id='1ad3f9a0-4e71-4325-a55f-d6c004fef38d',      # App ID
    colorway_id='70bb8273-7818-40f2-81e6-07931d8164f1', # Attributes colorway ID
    side='front', # or back
    filepath='/home/beproduct/your_image.jpg')          # File location 

# Uploading from remote URL
upload_id = client.material.app_3d_material_texture_upload(
    header_id='c629fb8b-7a24-4773-b335-d0b6f38196f5',   # Style or Material ID
    app_id='1ad3f9a0-4e71-4325-a55f-d6c004fef38d',      # App ID
    colorway_id='70bb8273-7818-40f2-81e6-07931d8164f1', # Attributes colorway ID
    side='front', # or back
    fileurl='https://us.beproduct.com/your_image.jpg')  # File URL
```
To check the image upload processing status use the same technique as in [Attributes](./040-style-api.md#uploading-images-to-the-style-attributes)
