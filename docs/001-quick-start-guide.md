# Quick start guide

## Install package using pip

`pip install --upgrade beproduct`

## Get refresh token
You can skip this step if you already have a refresh token.

If you don't have a refresh token you can read how to obtain it [here](./003-getting-refresh-token.md)

## Identify Your company domain

Go to [BeProduct](https://www.beproduct.com) website. You can identify your company domain by inspecting webbrowser's url.

*Example*:
https://us.beproduct.com/**SampleCompany**/Home

Here the company domain is: *SampleCompany*


## Create BeProduct API client
```python
from beproduct.sdk import BeProduct

client = BeProduct(client_id='YOUR_CLIENT_ID',
                   client_secret='YOUR_CLIENT_SECRET',
                   refresh_token='REFRESH_TOKEN',
                   company_domain="YOUR_COMPANY_DOMAIN'
```
## Use it

```python
style = client.style.attributes_get(style_id='e81d3be5-f5c2-450f-888e-8a854dfc2824')
print(style)
```
Result example is a Python dictionary:
```python
{
   'id':'e81d3be5-f5c2-450f-888e-8a854dfc2824',
   'headerNumber':'Test-3D-1',
   'headerName':'updated headerasdasd dc',
   'folder':{
      'id':'7a59e00e-5970-4640-8820-b4c5a4be5638',
      'name':'TEST'
   },
   'headerData':{
      'fields':[
         {
            'id':'header_number',
            'name':'Style Number',
            'value':'Test-3D-1',
            'type':'Text',
            'required':True
         },
         {
            'id':'header_name',
            'name':'Style Name',
            'value':'updated headerasdasd dc',
            'type':'Text',
            'required':True
         },
         {
            'id':'created_by',
            'name':'Created',
            'value':'joy.foo-bp @ 4/5/2021 3:51:58 PM',
            'type':'UserLabel',
            'required':False
         },
         {
            'id':'modified_by',
            'name':'Modified',
            'value':'pakman @ 7/8/2021 8:52:24 AM',
            'type':'UserLabel',
            'required':False
         },
         {
            'id':'active',
            'name':'Active',
            'value':'Yes',
            'type':'TrueFalse',
            'required':False
         },
         {
            'id':'version',
            'name':'Version',
            'value':'40',
            'type':'Text',
            'required':True
         },
         {
            'id':'inactive_users',
            'name':'Inactive users',
            'value':None,
            'type':'Users',
            'required':False
         }
      ],
      'frontImage':{
         'preview':'https://winks-share-svc-prod-eastus.azurewebsites.net/media/preview/469071e0-8e0f-47aa-b518-80ad83af9e5f/673e1744-d790-48e1-bf1a-cf143d86c318/1/0/673e1744-d790-48e1-bf1a-cf143d86c318.jpg?width=1000',
         'origin':'https://beproduct-cdn.azureedge.net/storage/469071e0-8e0f-47aa-b518-80ad83af9e5f/673e1744-d790-48e1-bf1a-cf143d86c318/1/test-3d-1-test-3d-1.bw'
      },
      'sideImage':{
         'preview':None,
         'origin':None
      },
      'backImage':{
         'preview':None,
         'origin':None
      },
      'availableArtboards':[
         {
            'artboarIndex':0,
            'imageUrl':'https://winks-share-svc-prod-eastus.azurewebsites.net/media/preview/469071e0-8e0f-47aa-b518-80ad83af9e5f/673e1744-d790-48e1-bf1a-cf143d86c318/1/0/673e1744-d790-48e1-bf1a-cf143d86c318.jpg?width=1000'
         }
      ]
   },
   'createdBy':{
      'id':'b7aff40a-59ab-4c0b-9ff1-730a86468480',
      'name':'joy.foo-bp'
   },
   'createdAt':'2021-04-05T15:51:58.072Z',
   'modifiedBy':{
      'id':'cde652b9-0697-493d-a7d8-f1e4642dab47',
      'name':'pakman'
   },
   'modifiedAt':'2021-07-08T08:52:24.139Z',
   'colorways':[
      {
         'id':'b49d7301-aa68-4385-9dbd-8cdd457a5cba',
         'colorNumber':'1',
         'colorName':'CW1',
         'primaryColor':'',
         'secondaryColor':'',
         'comments':'',
         'hideColorway':False,
         'fields':{
            'core_colorway_main_material':''
         },
         'image':None
      }
   ],
   'sizeRange':[
      {
         'name':'One Size',
         'price':None,
         'currency':None,
         'unitOfMeasure':None,
         'comments':None,
         'isSampleSize':True,
         'fields':{
            
         }
      }
   ],
   'planIds':None,
   'isDeleted':False
}
```

