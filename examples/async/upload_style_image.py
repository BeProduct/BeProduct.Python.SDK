#!/usr/bin/env python3
"""
Example: Uploading an Image to a Style from URL (Asynchronous)
This example demonstrates how to:
1. Initialize the BeProduct client using either OAuth2 or token authentication
2. Upload an image from a URL to a specific style
3. Check upload processing status
4. Handle potential errors
"""

from beproduct import BeProductAsync
from beproduct._exception import BeProductException
import os
import asyncio
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
env_path = Path(__file__).parents[1] / '.env'
if env_path.exists():
    load_dotenv(env_path)

async def check_upload_status(client, upload_id: str) -> bool:
    """Check upload status with exponential backoff."""
    wait_time = 1  # Start with 1 second wait
    max_wait = 10  # Maximum wait time between checks
    max_attempts = 30  # Maximum number of attempts (5 minutes with exponential backoff)
    
    for attempt in range(max_attempts):
        is_finished, is_error, error_msg = await client.style.upload_status(upload_id=upload_id)
        
        if is_finished:
            if is_error:
                print(f'Error occurred during processing: {error_msg}')
                return False
            else:
                print('Upload processing completed successfully.')
                return True
                
        print(f'Processing in progress... (attempt {attempt + 1}/{max_attempts})')
        await asyncio.sleep(min(wait_time, max_wait))
        wait_time *= 1.5  # Exponential backoff
    
    print('Upload processing timed out.')
    return False

async def upload_with_oauth2(style_id: str, image_url: str):
    """Upload an image using OAuth2 authentication."""
    print("\nUsing OAuth2 authentication...")
    
    # Initialize with OAuth2
    credentials = {
        'client_id': os.getenv('BEPRODUCT_CLIENT_ID'),
        'client_secret': os.getenv('BEPRODUCT_CLIENT_SECRET'),
        'refresh_token': os.getenv('BEPRODUCT_REFRESH_TOKEN'),
        'company_domain': os.getenv('BEPRODUCT_COMPANY_DOMAIN')
    }

    # Add optional API endpoints if provided
    if os.getenv('BEPRODUCT_PUBLIC_API_URL'):
        credentials['public_api_url'] = os.getenv('BEPRODUCT_PUBLIC_API_URL')
    if os.getenv('BEPRODUCT_TOKEN_ENDPOINT'):
        credentials['token_endpoint'] = os.getenv('BEPRODUCT_TOKEN_ENDPOINT')

    async with BeProductAsync(**credentials) as client:
        # First verify the style exists
        print(f"Verifying style {style_id}...")
        style = await client.style.attributes_get(style_id)
        print(f"Found style: {style.get('headerNumber', 'N/A')}")

        # Upload the image from URL
        print(f"\nUploading image from {image_url}...")
        upload_id = await client.style.attributes_upload(
            header_id=style_id,
            fileurl=image_url
        )
        print(f"Upload initiated! Upload ID: {upload_id}")
        
        # Check upload status until completion
        print("\nChecking upload processing status...")
        success = await check_upload_status(client, upload_id)
        if success:
            print(f"\nImage successfully uploaded and processed for style {style.get('headerNumber', 'N/A')}")
        else:
            print(f"\nFailed to process image for style {style.get('headerNumber', 'N/A')}")

async def upload_with_token(style_id: str, image_url: str):
    """Upload an image using token-based authentication."""
    print("\nUsing token-based authentication...")
    
    # Initialize with token and company
    credentials = {
        'access_token': os.getenv('BEPRODUCT_ACCESS_TOKEN'),
        'company_domain': os.getenv('BEPRODUCT_COMPANY_DOMAIN'),
        'public_api_url': 'https://dev-public-api-beproduct-eastus.azurewebsites.net'
    }

    # Add optional API endpoint if provided
    if os.getenv('BEPRODUCT_PUBLIC_API_URL'):
        credentials['public_api_url'] = os.getenv('BEPRODUCT_PUBLIC_API_URL')

    async with BeProductAsync(**credentials) as client:
        # First verify the style exists
        print(f"Verifying style {style_id}...")
        style = await client.style.attributes_get(style_id)
        print(f"Found style: {style.get('headerNumber', 'N/A')}")

        # Upload the image from URL
        print(f"\nUploading image from {image_url}...")
        upload_id = await client.style.attributes_upload(
            header_id=style_id,
            fileurl=image_url
        )
        print(f"Upload initiated! Upload ID: {upload_id}")
        
        # Check upload status until completion
        print("\nChecking upload processing status...")
        success = await check_upload_status(client, upload_id)
        if success:
            print(f"\nImage successfully uploaded and processed for style {style.get('headerNumber', 'N/A')}")
        else:
            print(f"\nFailed to process image for style {style.get('headerNumber', 'N/A')}")

async def main():
    try:
        style_id = "9663f006-ed56-49ef-bc5a-6cda0d665445"
        image_url = "https://encrypted-tbn1.gstatic.com/shopping?q=tbn:ANd9GcR3KCPFCMHtrQR10FomY5zaaMCEDWSufI5kQ-xHoV0ETz8jLWxZ9-gtTSjlsM-kh5iiVd7VkrHCEpfKKH2DpbTfnayoRtd96MGWPUIabA8wmFL5CXXPB6Y2"
        await upload_with_token(style_id, image_url)
    except BeProductException as e:
        print(f"BeProduct API Error: {str(e)}")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main()) 