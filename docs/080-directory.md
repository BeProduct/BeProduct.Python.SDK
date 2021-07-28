# Directory API

## Directory records
To store contacts in BeProduct we use *Directory*. Each vendor, factory, partner or any other type of contact 
correspond to a single directory record. Each record has unique header ID.

In turn each directory records contains a list of contacts.

## Listing all directory records
```python
# Listing all directory records
for record in client.directory.directory_list():
    print(record)
```

## Getting a single directory record
```python
# Getting a single directory record by header id
record = client.directory.directory_get(header_id="4f0b0c2f-4ff6-44ca-950f-93f991bf0f93")
print(record)
```

## Getting all contacts from a directory record
```python
# Getting all contacts from directory by directory header id
for contact in client.directory.directory_contact_list(header_id="498896be-562d-4b96-8b31-7c11da34a4a7"):
    print(contact)
```

## Creating new directory record
```python
directory_record_fields = {
  'directoryId': 'ABCD',
  'name': 'Factory Name',
  'address': '1 Name St.',
  'country': 'USA',
  'zip': '9010',
  'state': 'NY',
  'city': 'New York',
  'phone': '12 123 123',
  'partnerType': 'VENDOR',
  'website': 'www.beproduct.com',
  'fax': '12 123 123',
  'active': True,
  'contacts': [
    {
      'email': 'support@beproduct.com',
      'firstName': 'BeProduct',
      'lastName': 'Vendor',
      'title': 'BP Vendor',
      'mobilePhone': '12 123 123',
      'workPhone': '12 123 123',
      'role': 'Vendor Full'
    }
  ]
}

client.directory.directory_add(fields=directory_record_fields)
```

## Adding a contact to a directory record
```python
contact_fields = {
      'email': 'support@beproduct.com',
      'firstName': 'BeProduct',
      'lastName': 'Vendor',
      'title': 'BP Vendor',
      'mobilePhone': '12 123 123',
      'workPhone': '12 123 123',
      'role': 'Vendor Full'
    }

client.directory.directory_contact_add(
  header_id="498896be-562d-4b96-8b31-7c11da34a4a7,
  fields = contact_fields)
```


## Updating and removing directory records and contacts
Adding and removing directory records is not supported in the current version of the API.
