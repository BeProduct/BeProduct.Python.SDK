# Making HTTP calls manually

## Making HTTP calls to BeProduct Public API

If some BeProduct Public API methods are missing in the sdk package you can still call all the methods manually 
without having to worry about token refresh and API throttling.

Example:
```python

   # get request
   result = client.raw_api.get(f"{self.master_folder}/Header/{header_id}")

   # post request
   result = self.client.raw_api.post(
        f"Share/Page/{header_id}/{app_id}/Share",
        body=<dict or list>
    )
```


## Making HTTP calls to other systems

This sdk uses **requests** package to do HTTP calls. We recommend using the same package because it is 
always present if you save/host your integration script in/with BeProduct.

Example:
```python
import requests

r = requests.get('https://api.github.com/events')
r = requests.post('https://httpbin.org/post', data = {'key':'value'})
r = requests.put('https://httpbin.org/put', data = {'key':'value'})
r = requests.delete('https://httpbin.org/delete')
r = requests.head('https://httpbin.org/get')
r = requests.options('https://httpbin.org/get')
```

Refer to full [ Requests documentation ]( https://docs.python-requests.org/en/master/ )
