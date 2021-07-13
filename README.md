# BeProduct Python SDK Package
## Read full documentation at **[https://python.beproduct.com](https://python.beproduct.com)**
## Example
Install:
`pip install --upgrade beproduct`

Use:
```python
from beproduct.sdk import BeProduct

client = BeProduct(client_id='YOUR_CLIENT_ID',
                   client_secret='YOUR_CLIENT_SECRET',
                   refresh_token='YOUR_REFRESH_TOKEN',
                   company_domain='YOUR_COMPANY_DOMAIN')
                   
style = client.style_attributes_get(style_id='e81d3be5-f5c2-450f-888e-8a854dfc2824')
print(style)
```




