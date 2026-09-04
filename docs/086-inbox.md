# Inbox API

Tasks (to-dos attached to styles, materials, images or colors) and their
message threads.

```python
# Tasks for a master folder — enumerator; filters like the header list filters
for task in client.inbox.task_list("Style", filters=None, folder_id=None, page_size=30):
    ...
task = client.inbox.task_get(task_id)
task = client.inbox.task_create({
    "taskName": "Check lab dips", "startDate": "2026-09-01T00:00:00Z", "dueDate": "2026-09-15T00:00:00Z",
    "priority": "High", "status": "Open",
    "assignees": [{"value": user_id}], "participants": [],
    "references": {"page": "Style", "headers": [style_id]},
})
client.inbox.task_update(task_id, fields)
client.inbox.task_delete(task_id)

# Messages on a task
for message in client.inbox.message_list(task_id):
    ...
message = client.inbox.message_create(task_id, {"message": "Dips approved", "type": "Comment"})
client.inbox.message_update(message_id, fields)
client.inbox.message_delete(message_id)
upload_id = client.inbox.message_attachments_upload(message_id, filepath="/path/to/file.pdf")
upload_id = client.inbox.message_attachments_upload(message_id, fileurl="https://example.com/file.pdf")
```
