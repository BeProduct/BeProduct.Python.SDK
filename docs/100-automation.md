
# Automation Portal Helper Methods

BeProduct SDK also contains some helper methods that make it easier to implement BeProduct Automation logic.


Learn more at the [ **Automation Portal** ](https://automation.beproduct.com)

## Autogenerate Number (Autonumber)
You can easily create a unique number for your entities using the ID of the autonumber logic template:
```python
# generates autonumber based on the template e.g.: tmp00002
new_autonumber = client.automation.autonumber_generate("e6711819-cb43-44bb-acfa-768318a52c13")
print(new_autonumber)

```

Below example shows how you can combine autonumber with BeProduct dropdown field **codes** (*not values*)

```python
def get_code_by_value(field_id, value):
    folder_schema = client.style.folder_schema(style['folder']['id'])
    field_schema = next((f['properties']['Choices'] for f in folder_schema if f['fieldId'] == field_id), None)
    if field_schema:
        return next((f['code'] for f in field_schema if f['value'] == value), None)
    return None 

style = client.style.attributes_get('7fbbb0ec-9395-4532-b2e1-39153ef1b57c')
season_year_value = next((f['value'] for f in style['headerData']['fields'] if f['id'] == 'season_year'), None)

season_code = get_code_by_value('season_year', season_year_value)
next_autonumber = client.automation.autonumber_generate('EA79BF5E-BEDC-4233-8CFD-199C203C1BA3')

# prints something like FA17XXXX00001
print(f'{season_code}{next_autonumber}')

```

