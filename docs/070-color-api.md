# Color API
Listing and searching is analogous to Style with exception that each call should start with `client.color`
## List of Color folders
Refer to [Style folder listing](./040-style-api.md#list-of-style-folders).
## Listing and Searching Color palettes
### Getting all Color palettes
Refer to [Getting all styles](./040-style-api.md#getting-all-styles).
### Searching Color palettes
Refer to [Searching styles](./040-style-api.md#searching-styles).

## Getting Color Palette Attributes

Example below returns image Attributes as a dictionary

```python
color_dict = client.color.attributes_get(header_id='e81d3be5-f5c2-450f-888e-8a854dfc2824')
```

## Creating new Color Palette or Updating Color Palette Attibutes and colors
Colors can only be replaced in a Color Palette. Updating/Adding individual colors is not supported.
Example:
```python
fields_update = {
    'header_name': 'New Image Name',
    'some_other_field_id': 'value'
    }

colors = [
{
  'colorNumber': 'PB1',
  'colorName': 'Pitch Black',
  'hex': '000000'
},
{
  'Id': ''
  'colorNumber': 'G1',
  'colorName': 'Grey',
  'hex': '0F0F0F'
}
]
    
# Creates new color palette
client.color.attributes_create(
  fields=fields_update,
  colors=colors)

# Updates a color palette
client.color.attributes_update(
            header_id='e81d3be5-f5c2-450f-888e-8a854dfc2824',
            fields=fields_update,
            colors=colors)
```


## Deleting a Color Palette
```python
client.color.attributes_delete(header_id='e81d3be5-f5c2-450f-888e-8a854dfc2824')
```
