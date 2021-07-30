# User API

## Getting a list of your company's users
```python
for user in client.user.user_list():
    print(user)
```

## Creating a user
```python
client.user.user_create(fields={
    'username': "UserName",
    'email': 'user@email.address',
    'firstName': 'First',
    'lastName': 'Last',
    'culture': 'EN-US',
    'title': 'Lead engineer',
    'roleId': '98f99c6f-9087-4c5d-b096-e44a140c842f'
})
```

## Updating a user
```python
client.user.user_update(fields={
    'email': 'user@email.address',
    'firstName': 'First',
    'lastName': 'Last',
    'culture': 'EN-US',
    'title': 'Lead engineer',
    'roleId': '98f99c6f-9087-4c5d-b096-e44a140c842f'
    'emailNotification': True,
    'active': True
})
```

## Finding user by email
```python
client.user.user_get(email='user@email.address')
```

## Finding user's role
```python
client.user.role_get(user_id='bee652b9-0697-493d-a7d8-f1e4642dab47')
```

## List existing roles
```python
for role in client.user.role_list():
    print(role)
```
