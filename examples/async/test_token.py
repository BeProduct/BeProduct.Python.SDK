#!/usr/bin/env python3
"""
Example: Testing Token Authentication (Asynchronous)
This example demonstrates how to:
1. Initialize the BeProduct client using token authentication
2. List styles to verify the token works
3. Handle potential errors
"""

from beproduct import BeProductAsync
from beproduct._exception import BeProductException
import os
import asyncio
import json
import base64
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
env_path = Path(__file__).parents[1] / '.env'
if env_path.exists():
    load_dotenv(env_path)

def decode_jwt(token):
    """Decode a JWT token without verification."""
    parts = token.split('.')
    if len(parts) != 3:
        return None
    
    # Decode the payload (second part)
    try:
        # Add padding if needed
        payload = parts[1]
        padding = len(payload) % 4
        if padding:
            payload += '=' * (4 - padding)
        
        decoded = base64.b64decode(payload)
        return json.loads(decoded)
    except Exception as e:
        print(f"Error decoding token: {str(e)}")
        return None

async def test_token_auth():
    """Test token-based authentication by listing styles."""
    print("\nTesting token-based authentication...")
    
    # Initialize with token and company
    credentials = {
        'access_token': 'eyJhbGciOiJSUzI1NiIsImtpZCI6IkhCVlNCT0VTRjBaVzhyOTQ2UkxJaXFXUV9WcyIsIng1dCI6IkhCVlNCT0VTRjBaVzhyOTQ2UkxJaXFXUV9WcyIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJodHRwczovL2Rldi1pZHMuYmVwcm9kdWN0LmNvbS9pZHMiLCJleHAiOjE3NDU1OTk1MjAsImlhdCI6MTc0NTU3MDcyMCwianRpIjoiZWMyNzNhY2QtYjZlYi00ZWYyLWI3NWEtZTM5MTdjMjc1OWM3Iiwic3ViIjoiY2RlNjUyYjktMDY5Ny00OTNkLWE3ZDgtZjFlNDY0MmRhYjQ3IiwiZW1haWwiOiJzdXBwb3J0QGJlcHJvZHVjdC5jb20iLCJuYW1lIjoiYmVzdXBwb3J0IiwicHJlZmVycmVkX3VzZXJuYW1lIjoiYmVzdXBwb3J0Iiwib2lfYXVfaWQiOiJkZmJjNTBjZS1hYzk5LTQ2NjUtOWJiMC1kN2UzZjkyYzRlYTAiLCJvaV9wcnN0IjoiZG9jdW1lbnRhdGlvbiIsImNsaWVudF9pZCI6ImRvY3VtZW50YXRpb24iLCJzY29wZSI6WyJvcGVuaWQiLCJwcm9maWxlIiwiZW1haWwiLCJyb2xlcyIsIkJlUHJvZHVjdFB1YmxpY0FwaSJdLCJvaV90a25faWQiOiJmNmEwZGRjOS02YThiLTQ5ZWQtYWU4MS00Zjg5YTU4YWM1MDYifQ.h6v4aIcY4ZmzpYUVcs3Sxd553f8dzTExAl81UO728kVs7WowheWWYy1VdrjRiH17d9nE442p859_Qczn2LWUEeXwcn-2OlumUhqV8QB2rQGKTWDotd6gcQoiaXzO8tkhUDL4AGmoJObNPnOzIn6GhUhqz1zEdlJ-4EbFLir6U9WYK3YB0s3GpLHMcyUwNG2LeFob82s64RMuDpC5TGMLD4qLHlaGnYNHmdXbpV86QFMGoQvdUAXJ1fSN05fHBxwCX84v7a3Twm9EG4BdO2SOuEawvtSRk5pQWdonhyhdlvBo1M5j6HbO1sH0YCWBArdMef07BbXtVTfRDn0nmRoc3Q',
        'company_domain': 'bp',
        'public_api_url': 'https://dev-public-api-beproduct-eastus.azurewebsites.net'  # Base URL without /api/bp
    }

    # Decode and check token
    token_data = decode_jwt(credentials['access_token'])
    if token_data:
        print("\nToken information:")
        print(f"Issuer: {token_data.get('iss')}")
        print(f"Expiration: {datetime.fromtimestamp(token_data.get('exp')).isoformat()}")
        print(f"Issued at: {datetime.fromtimestamp(token_data.get('iat')).isoformat()}")
        print(f"Subject: {token_data.get('sub')}")
        print(f"Client ID: {token_data.get('client_id')}")
        print(f"Scopes: {', '.join(token_data.get('scope', []))}")
        
        # Check if token is expired
        exp_time = token_data.get('exp')
        if exp_time:
            now = datetime.now().timestamp()
            if now > exp_time:
                print("\nWARNING: Token is expired!")
            else:
                print("\nToken is valid until:", datetime.fromtimestamp(exp_time).isoformat())

    print("\nCredentials being used:")
    print(f"Company Domain: {credentials.get('company_domain')}")
    print(f"Public API URL: {credentials.get('public_api_url', 'default')}")
    print(f"Access Token: {credentials.get('access_token', 'not set')[:30]}...")

    async with BeProductAsync(**credentials) as client:
        # Try to list style folders
        print("\nAttempting to list style folders...")
        try:
            folders = await client.style.folders()
            if folders:
                print("\nSuccess! Found style folders:")
                for folder in folders:
                    print(f"- {folder.get('name', 'N/A')} (ID: {folder.get('id', 'N/A')})")
            else:
                print("\nNo style folders found.")
                
            # Try to list styles from the first folder if any exist
            if folders:
                first_folder = folders[0]
                print(f"\nAttempting to list styles from folder: {first_folder.get('name', 'N/A')}")
                async for style in client.style.attributes_list(folder_id=first_folder['id']):
                    print(f"- Style: {style.get('headerNumber', 'N/A')}")
                    # Only show first style to avoid too much output
                    break
                
        except BeProductException as e:
            print(f"\nAPI Error: {str(e)}")
            if "403" in str(e):
                print("\nPossible issues:")
                print("1. Token might be invalid or expired")
                print("2. Token might not have the required permissions")
                print("3. Company domain might be incorrect")
                print("4. API URL might be incorrect")

async def main():
    try:
        await test_token_auth()
    except BeProductException as e:
        print(f"\nBeProduct API Error: {str(e)}")
    except Exception as e:
        print(f"\nUnexpected error: {str(e)}")
        raise

if __name__ == "__main__":
    asyncio.run(main()) 