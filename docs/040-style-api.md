# Style API

## List of Style folders
Styles in BeProduct are organized into folders. Each folder has its own name and ID.
You can use folder ID as filters to get the list of styles within a particular style 
folder.

Gettign the list of the style folders:
```python
folders = client.style.folders()
```
Function result example:
```python
[
   {
      "id":"f52840ad-9313-4330-bc88-7e6248690395",
      "name":"Comforter Set",
      "description":"Comforter Set Folder",
      "active":True
   },
   {
      "id":"592413ca-9ecd-4899-be24-b70cb42944bf",
      "name":"Dresses",
      "description":"Dresses",
      "active":False
   }
]
```

## Listing and Searching Styles
### Getting all styles
You can iterate over *all* styles using `list()` method which returns an iterator.
Styles are retrieved by batches/pages as you iterate over them and loaded as you progress.

Example:
```python
for style in client.style.list():
    print(style['id'], style['headerNumber'], sep=': ')
```

```text
fb321339-7597-44be-85ef-fdcaccb3b647: BA0121
44ccf3d3-3aea-41ce-98d7-9b34244cdb18: test 1
57816852-3eb5-4233-bf09-d23aa8359af3: BA0101
3aaa24c7-3bd0-45c0-9eaf-857468209618: BA0109
```

You can also specify a folder to fetch only styles from a particular style folder:
```python
for style in client.style.list(folder_id='592413ca-9ecd-4899-be24-b70cb42944bf'):
    print(style['id'], style['headerNumber'], sep=': ')
```


### Searching styles
Each *style* within the same *style folder* share the **same** set of attribute fields. We should keep that in mind when searching across folders as some fileds may exist in one folder and be missing in another.

Searching criterias are called **filters**. Each filter is a Dictionary which looks like this:

```python
filter_1 = {
   'field': 'header_number', # Field ID to filter by
   'operator':'Eq',          # one of the supported filter operators:
                             # Eq, Neq, Gt, Gte, Lt, Lte 
   'value': 'A00001'         # value to compare with
}
```

If you have multiple filters you should expect logical **AND** when applying them. 
Logical **OR** filter lists are *not supported*.

Example of usage:
```python
for style in client.style.list(filters=[filter_1, filter_2]):
    print(style['id'], style['headerNumber'], sep=': ')
```

Some *useful* standard filters for system fields are provided below:
```python
# Finds styles modified AFTER some date
# It compares against style attributes modified date
filter_by_last_modified_date = {
    'field': 'ModifiedAt',
    'operator': 'Gt',
    'value': '2021-07-01 12:00:00Z'
}

# Finds styles modified AFTER some date
# It compares against modification date of
# the attributes and style apps.

filter_by_any_modified_app_date = {
    'field': 'FolderModifiedAt',
    'operator': 'Gt',
    'value': '2021-07-01 12:00:00Z'
}

```


## Getting Style Attributes

Example below returns Style Attributes as a dictionary

```python
style_dict = client.style.get(header_id='e81d3be5-f5c2-450f-888e-8a854dfc2824')
```

## Creating new Style or Updating Style Attibutes

In Style Attributes you may create or update:

* Attributes fields
* Colorways fields
* Sizes

You can update all of the above within the same call.

### Creating a Style or Updating Style Attributes 
Example:
```python
fields_update = {
    'header_name': 'New Style Name',
    'some_other_field_id': 'value'
    }
    
# Creates new style
client.style.create(fields=fields_update)

# Updates a style
client.style.update(
            header_id='e81d3be5-f5c2-450f-888e-8a854dfc2824',
            fields=fields_update)
```

### Updating Style colorway fields
```python
colorway_update = [
    {
        'id': None, # if None - creates a new colorway
                    # otherwise should be a colorway id
        'fields': {
            # required when creating a new colorway
            'color_number': '#1',
            'color_name': 'My color',
            'primary':"000000",       # pitch black 
            'secondary': "",          # will not be pitched
            # end required 
            'some_other_colorway_field_id': 'value'
        }
    }
]
client.style.update(
                header_id='e81d3be5-f5c2-450f-888e-8a854dfc2824',
                colorways=colorway_update)
```

### Updating Style sizes
```python
size1 = {
    'name': 'XXS',
    'price': 1.1,
    'currency': 'USD',
    'unitOfMeasure': 'inch',
    'comments': 'Awesome size!',
    'isSampleSize': True
    }
size2 = {....
        
client.style.udpate(
                header_id='e81d3be5-f5c2-450f-888e-8a854dfc2824',
                sizes=[size1, size2, ...])
```

### Creating a Style or Updating all of the above fields within the same call 
```python
# Creates a style
client.style.create(
                fields=fields_update,
                colorway_update=colorway_update,
                sizes=[size1, size2, ...])

# Updates a style
client.style.update(
                header_id='e81d3be5-f5c2-450f-888e-8a854dfc2824',
                fields=fields_update,
                colorway_update=colorway_update,
                sizes=[size1, size2, ...])
```

## Deleting a Style
```python
client.style.delete(header_id='e81d3be5-f5c2-450f-888e-8a854dfc2824')
```

## Uploading images to the Style Attributes
It is often a case when you need to upload an image to the Style Attributes page.
Upload process consists of two stages. 

* **UPLOADING** of the file. 
* **PROCESSING** of the file in BeProduct. It is **highly recommended** that you don't do any changes to the style which is in processing stage until it's completed.

You have 2 options for uploading a file to BeProduct: either from *file system* or by providing a *file url*. In both cases *upload id* is returned.

Uploading stage looks as follows:
```python
# Uploading from file system
upload_id = client.style.attributes_upload(
    header_id='e81d3be5-f5c2-450f-888e-8a854dfc2824',   # Style ID
    filepath='/home/beproduct/your_image.jpg')          # File location 

# Uploading from remote URL
upload_id = client.style.attributes_upload(
    header_id='e81d3be5-f5c2-450f-888e-8a854dfc2824',   # Style ID
    file_url="https://us.beproduct.com/your_image.jpg") # File URL

```
After that the image is being processed and we have to make sure the process has finished sucessfully before proceeding working with that style. 

To check the image processing status you may want to implement something that looks as follows:
```python
while True:
    (is_finished, is_error, error_msg) = client.style.upload_status(upload_id=upload_id)
    if is_finished and not is_error:
        # WE_ARE_OK logic
        print('Success.')
        break
    if is_finised and is_error:
        # OMG_ERROR logic
        print('Error occured:', error_msg)
        break
    sleep(3) # Let's wait 3 sec and try again
```

## Getting Style applications

Each style within the **same style folder** has an identical set of appications(pages) associated with it.

**Important note**: Application IDs are not unique for a particular *style* but are unique for a *style folder*. Put it simply: 
Every *style folder* has the same application ID's for every style.

Example:
```python
apps = client.style.apps(header_id='bab33ce0-867f-4141-b849-1b0c41f68c8b') # header_id = ID of the style
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

client.style.form_app_update(
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

client.style.grid_app_update(
    header_id='bab33ce0-867f-4141-b849-1b0c41f68c8b', # Style ID
    app_id='1af353a4-7ce2-46d1-a4ce-b7bb09ea70f9',    # Grid app id
    rows=[delete_row, new_row, update_row])
```


## Sharing
Every partner in BeProduct has own ID. That ID is used to share and unshare attributes and apps

```python
# list of partners with home attributes and app is shared

client.style.attributes_shared_with(
    header_id='bab33ce0-867f-4141-b849-1b0c41f68c8b' # Style ID
    )

client.style.app_shared_with(
    header_id='bab33ce0-867f-4141-b849-1b0c41f68c8b', # Style ID
    app_id='1af353a4-7ce2-46d1-a4ce-b7bb09ea70f9'    # App id
    )


# to share with a partner or several

client.style.attributes_share(
    header_id='bab33ce0-867f-4141-b849-1b0c41f68c8b', # Style ID
    partner_list=['34f353a4-7ce2-46d1-a4ce-b7bb09ea70f8','Some different partner id']
    )

client.style.app_share(
    header_id='bab33ce0-867f-4141-b849-1b0c41f68c8b', # Style ID
    app_id='1af353a4-7ce2-46d1-a4ce-b7bb09ea70f9'    # App id
    partner_list=['34f353a4-7ce2-46d1-a4ce-b7bb09ea70f8','Some different partner id']
    )

# to unshare

client.style.attributes_unshare(
    header_id='bab33ce0-867f-4141-b849-1b0c41f68c8b', # Style ID
    partner_list=['34f353a4-7ce2-46d1-a4ce-b7bb09ea70f8','Some different partner id']
    )

client.style.app_unshare(
    header_id='bab33ce0-867f-4141-b849-1b0c41f68c8b', # Style ID
    app_id='1af353a4-7ce2-46d1-a4ce-b7bb09ea70f9'    # App id
    partner_list=['34f353a4-7ce2-46d1-a4ce-b7bb09ea70f8','Some different partner id']
    )
```
