# Style API

## Getting Style Attributes

Example below returns Style Attributes as a dictionary

```python
style_dict = client.style.attributes_get(style_id='e81d3be5-f5c2-450f-888e-8a854dfc2824')
```

## Updating Style Attibutes

In Style Attributes you may update:

* Attributes fields
* Colorways fields
* Sizes

You can update all of the above within the same call.

### Updating Style attributes fields
Example:
```python
fields_update = {
    'header_name': 'New Style Name',
    'some_other_field_id': 'value'
    }
    
client.style.attributes.update(
                style_id='e81d3be5-f5c2-450f-888e-8a854dfc2824',
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
                style_id='e81d3be5-f5c2-450f-888e-8a854dfc2824',
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
        
client.style.attributes_update(
                style_id='e81d3be5-f5c2-450f-888e-8a854dfc2824',
                sizes=[size1, size2, ...])
```

### Updatinga all of the above within the same call 
```python
client.style.attributes_update(
                style_id='e81d3be5-f5c2-450f-888e-8a854dfc2824',
                fields=fields_update,
                colorway_update=colorway_update,
                sizes=[size1, size2, ...])
```
