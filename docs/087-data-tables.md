# Data Tables API

Company reference tables (e.g. size charts, care codes).

```python
for table in client.data_tables.list():          # enumerator, optional filters
    ...
schema = client.data_tables.schema(table_id)     # columns
for row in client.data_tables.data(table_id):    # enumerator, optional filters
    ...

# Insert / update / delete rows — omit the row id to add, set "deleteRow": True to remove
client.data_tables.update(table_id, rows)
# Remove every row
client.data_tables.reset(table_id)
```
