# Block API
Listing and searching is analogous to Style with exception that each call should start with `client.block`
## List of Block folders
Refer to [Style folder listing](./040-style-api.md#list-of-style-folders).
## Listing and Searching Blocks
### Getting all blocks
Refer to [Getting all styles](./040-style-api.md#getting-all-styles).
### Searching blocks
Refer to [Searching styles](./040-style-api.md#searching-styles).

## Getting Block Attributes

Example below returns block Attributes as a dictionary

```python
block = client.block.attributes_get(header_id='e81d3be5-f5c2-450f-888e-8a854dfc2824')
```

## Creating new Block
Example:
```python
fields_dict = {
    'header_name': 'New Block Name',
    'some_other_field_id': 'value'
    }

size_classes = [
    {
      'name': 'size class 1',
      'notes': 'my notes',
      'active': True,
      'sizes': [
        {
          'name': 'size1',
          'isSampleSize': True,
          'hideSize': False,
          'comments': 'nice size'
        }
      ]
    }
]
    
# Creates new block
client.block.attributes_create(folder_id='f81d3be5-f5c2-450f-888e-8a854dfc2824',fields=fields_dict, size_classes=size_classes)
```

##  Updating a Block
Example:
```
fields_dict = {
    'header_name': 'New Block Name',
    'some_other_field_id': 'value'
    }
size_classes = [
    # deletes size class
    {
      'key': 'id or name',
      'deleteSizeClass': True,
    },
    # updates size class
    {
      'key': 'id or name',
      # optional
      'name': { 
        'value': 'new name '
      },
      # optional
      'notes': {
        'value': 'some notes'
      },
      # optional
      'active': {
        'value': True
      },
      # optional but if provided must be a full size range
      'sizes': [
        {
          'name': 'size 1',
          'isSampleSize': True,
          'hideSize': False,
          'comments': 'Nice size too'
        }
      ]
    }
  ]

client.block.attributes_update(header_id='f81d3be5-f5c2-450f-888e-8a854dfc2824', fields=fields_dict, size_classes=size_classes)
```

## Deleting a Block
```python
client.block.attributes_delete(header_id='e81d3be5-f5c2-450f-888e-8a854dfc2824')
```


## Uploading 3D asset file into Block Size Class
```python
# Uploading local file
upload_id = client.block.app_block_size_class_3d_asset_upload(
    header_id='c629fb8b-7a24-4773-b335-d0b6f38196f5',   # Block ID
    size_class_id_or_name='1ad3f9a0-4e71-4325-a55f-d6c004fef38d',      # Size Class ID or Name
    filepath='/home/beproduct/your_image.jpg')          # File location 

# Uploading from remote URL
upload_id = client.material.app_3d_material_asset_upload(
    header_id='c629fb8b-7a24-4773-b335-d0b6f38196f5',   # Block ID
    size_class_id_or_name='size name 1',      # Size Class ID or Name
    fileurl='https://us.beproduct.com/your_image.jpg')  # File URL
```
To check the image upload processing status use the same technique as in [Attributes](./040-style-api.md#uploading-images-to-the-style-attributes)
