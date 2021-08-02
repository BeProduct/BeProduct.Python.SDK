# Applications
**NOTE: Below examples are provided for the style API but it is the same for every other master folder
(material/color/image/style).**
Make sure to call correct API `client.<material/style/color/image>.<api method>`

## Getting Style/Material/Image/Color applications

Each style within the **same style folder** has an identical set of appications(pages) associated with it.

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

## Updating LIST-based applications
You can create, update and delete list items using a single call. Also there is a separate sdk/api call to upload images into list items.
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



