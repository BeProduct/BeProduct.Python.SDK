# BeProduct Python SDK

Official Python SDK for BeProduct API with both synchronous and asynchronous support.

## Documentation
Full documentation available at **[https://sdk.beproduct.com](https://sdk.beproduct.com)**

## Installation

```bash
pip install --upgrade beproduct
```

## Quick Start

### Synchronous Usage

```python
from beproduct import BeProduct

# Initialize the client
client = BeProduct(
    client_id='YOUR_CLIENT_ID',
    client_secret='YOUR_CLIENT_SECRET',
    refresh_token='YOUR_REFRESH_TOKEN',
    company_domain='YOUR_COMPANY_DOMAIN'
)

# Get style details
style = client.style.attributes_get(header_id='e81d3be5-f5c2-450f-888e-8a854dfc2824')
print(style)

# List styles in a folder
folder = client.style.folders()[0]  # Get first available folder
styles = client.style.attributes_list(folder_id=folder['id'])
for style in styles:
    print(f"{style['id']}: {style.get('headerNumber', 'N/A')}")
```

### Asynchronous Usage

```python
import asyncio
from beproduct import BeProductAsync

async def main():
    # Initialize the async client
    async with BeProductAsync(
        client_id='YOUR_CLIENT_ID',
        client_secret='YOUR_CLIENT_SECRET',
        refresh_token='YOUR_REFRESH_TOKEN',
        company_domain='YOUR_COMPANY_DOMAIN'
    ) as client:
        # Get style details
        style = await client.style.attributes_get(
            header_id='e81d3be5-f5c2-450f-888e-8a854dfc2824'
        )
        print(style)

        # List styles in a folder
        folders = await client.style.folders()
        if folders:
            async for style in client.style.attributes_list(folder_id=folders[0]['id']):
                print(f"{style['id']}: {style.get('headerNumber', 'N/A')}")

if __name__ == "__main__":
    asyncio.run(main())
```

## Features

- Full BeProduct API support
- Both synchronous and asynchronous interfaces
- Automatic token refresh
- File upload support (local files and URLs)
- Comprehensive error handling
- Type hints for better IDE support

## Main Components

- `Style` / `StyleAsync`: Style management
- `Material` / `MaterialAsync`: Material management
- `Color` / `ColorAsync`: Color management
- `Image` / `ImageAsync`: Image handling
- `Directory` / `DirectoryAsync`: Directory operations
- And more...

## Examples

Check the `examples/` directory for more detailed examples:

- Style management
- Material handling
- Image uploads
- Folder operations
- And more...

## Error Handling

The SDK uses custom exceptions for better error handling:

```python
from beproduct import BeProductException

try:
    style = client.style.attributes_get(header_id='invalid-id')
except BeProductException as e:
    print(f"BeProduct API Error: {e}")
```

## Environment Variables

You can use environment variables for configuration:

```python
# .env file
BEPRODUCT_CLIENT_ID=your_client_id
BEPRODUCT_CLIENT_SECRET=your_client_secret
BEPRODUCT_REFRESH_TOKEN=your_refresh_token
BEPRODUCT_COMPANY_DOMAIN=your_company_domain
```

```python
from dotenv import load_dotenv
load_dotenv()

client = BeProduct()  # Will automatically use environment variables
```

## Contributing

We welcome contributions! Please check our contribution guidelines for more information.

## License

This project is licensed under the terms of the MIT license.




