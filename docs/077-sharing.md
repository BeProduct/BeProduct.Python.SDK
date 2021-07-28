# Sharing attributes and apps
**NOTE: Below examples are provided for the style API but it is the same for every other master folder
(material/color/image/style).**
Make sure to call correct API `client.<material/style/color/image>.<api method>`

## Sharing
Every partner in BeProduct has own ID. That ID is used to share and unshare attributes and apps

```python
# list of partners with home attributes and app is shared

client.style.attributes_shared_with(
    header_id='bab33ce0-867f-4141-b849-1b0c41f68c8b' # Style ID
    )

client.style.app_shared_with(
    header_id='bab33ce0-867f-4141-b849-1b0c41f68c8b', # Style ID
    app_id='1af353a4-7ce2-46d1-a4ce-b7bb09ea70f9'    # App id
    )


# to share with a partner or several

client.style.attributes_share(
    header_id='bab33ce0-867f-4141-b849-1b0c41f68c8b', # Style ID
    partner_list=['34f353a4-7ce2-46d1-a4ce-b7bb09ea70f8','Some different partner id']
    )

client.style.app_share(
    header_id='bab33ce0-867f-4141-b849-1b0c41f68c8b', # Style ID
    app_id='1af353a4-7ce2-46d1-a4ce-b7bb09ea70f9'    # App id
    partner_list=['34f353a4-7ce2-46d1-a4ce-b7bb09ea70f8','Some different partner id']
    )

# to unshare

client.style.attributes_unshare(
    header_id='bab33ce0-867f-4141-b849-1b0c41f68c8b', # Style ID
    partner_list=['34f353a4-7ce2-46d1-a4ce-b7bb09ea70f8','Some different partner id']
    )

client.style.app_unshare(
    header_id='bab33ce0-867f-4141-b849-1b0c41f68c8b', # Style ID
    app_id='1af353a4-7ce2-46d1-a4ce-b7bb09ea70f9'    # App id
    partner_list=['34f353a4-7ce2-46d1-a4ce-b7bb09ea70f8','Some different partner id']
    )
```
