#!/usr/bin/env python3
"""
Example: Getting Styles List from BeProduct (Asynchronous)
This example demonstrates how to:
1. Initialize the BeProduct client
2. Retrieve a list of styles
3. Process the styles list
4. Handle potential errors
"""

from beproduct import BeProductAsync
from beproduct._exception import BeProductException
import os
import asyncio
from typing import List, Dict, Any
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
env_path = Path(__file__).parents[1] / '.env'
if env_path.exists():
    load_dotenv(env_path)

async def main():
    # Initialize the BeProduct client
    client = BeProductAsync(
        client_id=os.getenv('BEPRODUCT_CLIENT_ID'),
        client_secret=os.getenv('BEPRODUCT_CLIENT_SECRET'),
        refresh_token=os.getenv('BEPRODUCT_REFRESH_TOKEN'),
        company_domain=os.getenv('BEPRODUCT_COMPANY_DOMAIN'),
        public_api_url=os.getenv('BEPRODUCT_PUBLIC_API_URL'),
        token_endpoint=os.getenv('BEPRODUCT_TOKEN_ENDPOINT')
    )

    try:
        # Get available folders
        print("Fetching style folders...")
        folders = await client.style.folders()
        if not folders:
            print("No style folders found.")
            return

        # Use the first available folder
        folder = folders[0]
        print(f"Using folder: {folder['name']} (ID: {folder['id']})")
        
        # Get and process styles using async iteration
        print("\nStyles List:")
        count = 0
        async for style in client.style.attributes_list(folder_id=folder['id']):
            count += 1
            print(f"{style['id']}: {style.get('headerNumber', 'N/A')}")
        print(f"\nTotal styles found: {count}")
            
    except BeProductException as e:
        print(f"BeProduct API Error: {str(e)}")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
    finally:
        # Ensure we close the client's session
        await client.raw_api.close_session()

    # Alternative way to initialize the client
    credentials = {
        'client_id': os.getenv('BEPRODUCT_CLIENT_ID'),
        'client_secret': os.getenv('BEPRODUCT_CLIENT_SECRET'),
        'refresh_token': os.getenv('BEPRODUCT_REFRESH_TOKEN'),
        'company_domain': os.getenv('BEPRODUCT_COMPANY_DOMAIN'),
        'public_api_url': os.getenv('BEPRODUCT_PUBLIC_API_URL'),
        'token_endpoint': os.getenv('BEPRODUCT_TOKEN_ENDPOINT')
    }

    try:
        # Initialize the BeProduct client
        async with BeProductAsync(**credentials) as client:
            # First get available folders
            print("Fetching style folders...")
            folders = await client.style.folders()
            if not folders:
                print("No style folders found.")
                return

            # Use the first available folder
            folder = folders[0]
            print(f"Using folder: {folder['name']} (ID: {folder['id']})")
            
            # Get and process styles using async iteration
            print("\nStyles List:")
            count = 0
            async for style in client.style.attributes_list(folder_id=folder['id']):
                count += 1
                print(f"{style['id']}: {style.get('headerNumber', 'N/A')}")
            print(f"\nTotal styles found: {count}")
            
    except BeProductException as e:
        print(f"BeProduct API Error: {str(e)}")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main()) 