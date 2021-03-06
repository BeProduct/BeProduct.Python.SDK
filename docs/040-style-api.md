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
You can iterate over *all* styles using `attributes_list()` method which returns an iterator.
Styles are retrieved by batches/pages as you iterate over them and loaded as you progress.

Example:
```python
for style in client.style.attributes_list():
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
for style in client.style.attributes_list(folder_id='592413ca-9ecd-4899-be24-b70cb42944bf'):
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
for style in client.style.attributes_list(filters=[filter_1, filter_2]):
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
style_dict = client.style.attributes_get(header_id='e81d3be5-f5c2-450f-888e-8a854dfc2824')
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
client.style.attributes_create(folder_id='f81d3be5-f5c2-450f-888e-8a854dfc2824',fields=fields_update)

# Updates a style
client.style.attributes_update(
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
client.style.attributes_update(
                header_id='e81d3be5-f5c2-450f-888e-8a854dfc2824',
                colorways=colorway_update)
```
### Deleting colorway
You can delete colorway by ID
```python
client.style.attributes_colorway_delete(
                header_id='e81d3be5-f5c2-450f-888e-8a854dfc2824',
                colorway_id = 'f71d3be5-f5c2-450f-888e-8a854dfc2835')
```


### Replacing Style sizes
Sizes are replaced. You cant update individual sizes. You should provide a whole size range.
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
        
client.style.attributes_update(
                header_id='e81d3be5-f5c2-450f-888e-8a854dfc2824',
                sizes=[size1, size2, ...])
```

### Creating a Style or Updating all of the above fields within the same call 
```python
# Creates a style
client.style.attributes_create(
                fields=fields_update,
                colorway_update=colorway_update,
                sizes=[size1, size2, ...])

# Updates a style
client.style.attributes_update(
                header_id='e81d3be5-f5c2-450f-888e-8a854dfc2824',
                fields=fields_update,
                colorway_update=colorway_update,
                sizes=[size1, size2, ...])
```

## Deleting a Style
```python
client.style.attributes_delete(header_id='e81d3be5-f5c2-450f-888e-8a854dfc2824')
```

## Uploading images to the Style Attributes
It is often a case when you need to upload an image to the Style Attributes page.
Upload process consists of two stages. 

* **UPLOADING** of the file. 
* **PROCESSING** of the file in BeProduct. It is **highly recommended** that you don't do any changes to the style which is in processing stage until it's completed.

You have 2 options for uploading a file to BeProduct: either from *file system* or by providing a *file url*. In both cases *upload id* is returned.
You also have a choice to specify style position where you want to upload your image. It can be front,side or back.

Uploading stage looks as follows:
```python
# Uploading from file system
upload_id = client.style.attributes_upload(
    header_id='e81d3be5-f5c2-450f-888e-8a854dfc2824',   # Style ID
    filepath='/home/beproduct/your_image.jpg')          # File location 

# Uploading from remote URL
upload_id = client.style.attributes_upload(
    header_id='e81d3be5-f5c2-450f-888e-8a854dfc2824',   # Style ID
    fileurl="https://us.beproduct.com/your_image.jpg") # File URL

# Uploading only to front side or back
upload_id = client.style.attributes_upload(
    header_id='e81d3be5-f5c2-450f-888e-8a854dfc2824',   # Style ID
    filepath='/home/beproduct/your_image.jpg',          # File location
    position='front')                                   # Position 'front', 'side' or 'back'
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
    if is_finished and is_error:
        # OMG_ERROR logic
        print('Error occured:', error_msg)
        break
    sleep(3) # Let's wait 3 sec and try again
```

## Uploading Colorway images

```python
# Uploading from file system
upload_id = client.style.attributes_colorway_upload(
    header_id='e81d3be5-f5c2-450f-888e-8a854dfc2824',     # Style ID
    colorway_id = 'b71d3be5-f5c2-450f-888e-8a854dfc2824', # Colorway ID
    filepath='/home/beproduct/your_image.jpg')            # File location 

# Uploading from remote URL
upload_id = client.style.attributes_colorway_upload(
    header_id='e81d3be5-f5c2-450f-888e-8a854dfc2824',   # Style ID
    colorway_id = 'b71d3be5-f5c2-450f-888e-8a854dfc2824', # Colorway ID
    fileurl="https://us.beproduct.com/your_image.jpg") # File URL
```

Use example from the previous section to check the upload status.
