# Image API
Listing and searching is analogous to Style with exception that each call should start with `client.image`
## List of Image folders
Refer to [Style folder listing](./040-style-api.md#list-of-style-folders).
## Listing and Searching Images
### Getting all images
Refer to [Getting all styles](./040-style-api.md#getting-all-styles).
### Searching images
Refer to [Searching styles](./040-style-api.md#searching-styles).

## Getting image Attributes

Example below returns image Attributes as a dictionary

```python
image_dict = client.image.attributes_get(header_id='e81d3be5-f5c2-450f-888e-8a854dfc2824')
```

## Creating new Image or Updating Image Attibutes
Example:
```python
fields_update = {
    'header_name': 'New Image Name',
    'some_other_field_id': 'value'
    }
    
# Creates new image
client.image.attributes_create(folder_id='f81d3be5-f5c2-450f-888e-8a854dfc2824',fields=fields_update)

# Updates a image
client.image.attributes_update(
            header_id='e81d3be5-f5c2-450f-888e-8a854dfc2824',
            fields=fields_update)
```

## Deleting an Image
```python
client.image.attributes_delete(header_id='e81d3be5-f5c2-450f-888e-8a854dfc2824')
```

## Uploading images to the Image Attributes
It is often a case when you need to upload an image to the Image Attributes page.
Upload process consists of two stages. 

* **UPLOADING** of the file. 
* **PROCESSING** of the file in BeProduct. It is **highly recommended** that you don't do any changes to the image which is in processing stage until it's completed.

You have 2 options for uploading a file to BeProduct: either from *file system* or by providing a *file url*. In both cases *upload id* is returned.

Uploading stage looks as follows:
```python
# Uploading from file system
upload_id = client.image.attributes_upload(
    header_id='e81d3be5-f5c2-450f-888e-8a854dfc2824',   # image ID
    filepath='/home/beproduct/your_image.jpg')          # File location 

# Uploading from remote URL
upload_id = client.image.attributes_upload(
    header_id='e81d3be5-f5c2-450f-888e-8a854dfc2824',   # image ID
    fileurl="https://us.beproduct.com/your_image.jpg") # File URL
```
After that the image is being processed and we have to make sure the process has finished sucessfully before proceeding working with that image. 

To check the image processing status you may want to implement something that looks as follows:
```python
while True:
    (is_finished, is_error, error_msg) = client.image.upload_status(upload_id=upload_id)
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

