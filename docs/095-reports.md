# Reports API

```python
for report in client.reports.list():
    ...
# One page of a report's data
page = client.reports.data(report_id, {}, page_size=100, page_number=0)
# Flat BOM: one row per style x material across the company
page = client.reports.flat_bom({}, page_size=100, page_number=0)
```
