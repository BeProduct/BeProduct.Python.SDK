# Material API
Listing and searching is analogous to Style with exception that each call should start with `client.material`
## List of Material folders
Refer to [Style folder listing](./040-style-api.md#list-of-style-folders).
## Listing and Searching Styles
### Getting all styles
Refer to [Getting all styles](./040-style-api.md#getting-all-styles).
### Searching styles
Refer to [Searching styles](./040-style-api.md#searching-styles).

## Getting Material Attributes

Example below returns Material Attributes as a dictionary

```python
material_dict = client.material.attributes_get(header_id='e81d3be5-f5c2-450f-888e-8a854dfc2824')
```

## Creating new Material or Updating material Attibutes

In material Attributes you may create or update:

* Attributes fields
* Colorways fields
* Sizes
* Suppliers

You can update all of the above within the same call.

### Creating a Material or Updating Material Attributes 
Example:
```python
fields_update = {
    'header_name': 'New Material Name',
    'some_other_field_id': 'value'
    }
    
# Creates new material
client.material.attributes_create(fields=fields_update)

# Updates a material
client.material.attributes_update(
            header_id='e81d3be5-f5c2-450f-888e-8a854dfc2824',
            fields=fields_update)
```

### Updating Material colorway fields
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
            # end required 
            'some_other_colorway_field_id': 'value'
        }
    }
]
client.material.attributes_update(
                header_id='e81d3be5-f5c2-450f-888e-8a854dfc2824',
                colorways=colorway_update)
```

### Updating Material sizes
```python
size1 = {
    'name': 'XXS',
    'price': 1.1,
    'currency': 'USD',
    'unitOfMeasure': 'inch',
    'comments': 'Awesome size!',
    }
size2 = {....
        
client.material.attributes_update(
                header_id='e81d3be5-f5c2-450f-888e-8a854dfc2824',
                sizes=[size1, size2, ...])
```

### Updating Material suppliers
```python
supplier1 = {
     'Address': '1 Nice St.',
     'City': 'New York',
     'Country': 'USA',
     'Name': 'BeProduct',
     'Phone': '12 123 123',
     'State': 'NY',
     'Website': 'www.beproduct.com',
     'Fax': '12 123 123',
     'Zip': '9010',
     'SupplierType': 'VENDOR'
     }
supplier2 = {....
        
client.material.attributes_update(
                header_id='e81d3be5-f5c2-450f-888e-8a854dfc2824',
                suppliers=[supplier1, supplier2, ...])
```

### Creating a Material or Updating all of the above fields within the same call 
```python
# Creates a material
client.material.attributes_create(
                fields=fields_update,
                colorway_update=colorway_update,
                sizes=[size1, size2, ...])

# Updates a material
client.material.attributes_update(
                header_id='e81d3be5-f5c2-450f-888e-8a854dfc2824',
                fields=fields_update,
                colorway_update=colorway_update,
                sizes=[size1, size2, ...],
                suppliers=[supplier1, supplier2,...])
```

## Deleting a Material
```python
client.material.attributes_delete(header_id='e81d3be5-f5c2-450f-888e-8a854dfc2824')
```

## Uploading images to the Material Attributes
It is often a case when you need to upload an image to the Material Attributes page.
Upload process consists of two stages. 

* **UPLOADING** of the file. 
* **PROCESSING** of the file in BeProduct. It is **highly recommended** that you don't do any changes to the material which is in processing stage until it's completed.

You have 2 options for uploading a file to BeProduct: either from *file system* or by providing a *file url*. In both cases *upload id* is returned.
You also have a choice to specify material position where you want to upload your image. It can be main or detail.

Uploading stage looks as follows:
```python
# Uploading from file system
upload_id = client.material.attributes_upload(
    header_id='e81d3be5-f5c2-450f-888e-8a854dfc2824',   # material ID
    filepath='/home/beproduct/your_image.jpg')          # File location 

# Uploading from remote URL
upload_id = client.material.attributes_upload(
    header_id='e81d3be5-f5c2-450f-888e-8a854dfc2824',   # material ID
    fileurl="https://us.beproduct.com/your_image.jpg") # File URL

# Uploading only to front side or back
upload_id = client.material.attributes_upload(
    header_id='e81d3be5-f5c2-450f-888e-8a854dfc2824',   # material ID
    filepath='/home/beproduct/your_image.jpg',          # File location
    position='main')                                    # Position 'main', 'detail'
```
After that the image is being processed and we have to make sure the process has finished sucessfully before proceeding working with that material. 

To check the image processing status you may want to implement something that looks as follows:
```python
while True:
    (is_finished, is_error, error_msg) = client.material.upload_status(upload_id=upload_id)
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

