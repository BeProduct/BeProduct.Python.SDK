# Master Data API

Field definitions: company-wide, and as configured per folder.

```python
field = client.master_data.get(field_id)
client.master_data.create(fields)
client.master_data.update(field_id, fields)

# The same field as configured for one folder (choices, defaults, ...)
field = client.master_data.folder_field_get(folder_id, field_id)
client.master_data.folder_field_update(folder_id, field_id, fields)
```
