#!/usr/bin/env python3
"""
Example: Creating a Style in BeProduct (Synchronous)
This example demonstrates how to:
1. Initialize the BeProduct client
2. Create a new style with attributes
3. Add colorways to the style
4. Handle potential errors
"""

from beproduct import BeProduct
from beproduct._exception import BeProductException
import os
from typing import Dict, Any
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
env_path = Path(__file__).parents[1] / '.env'
if env_path.exists():
    load_dotenv(env_path)

def create_style(client: BeProduct, folder_id: str) -> Dict[str, Any]:
    """
    Create a new style with sample data.
    
    Args:
        client: BeProduct client instance
        folder_id: ID of the folder to create the style in
    
    Returns:
        Dict containing the created style data
    """
    # Sample style attributes
    style_fields = {
        "name": "Sample Style",
        "description": "A sample style created via Python SDK",
        "season": "Spring 2024",
        "category": "Tops",
        "designer": "John Doe"
    }
    
    # Sample colorways
    colorways = [
        {
            "id": "color1",
            "fields": {
                "name": "Navy Blue",
                "color_code": "#000080",
                "pantone": "19-4021"
            }
        },
        {
            "id": "color2",
            "fields": {
                "name": "Forest Green",
                "color_code": "#228B22",
                "pantone": "18-6030"
            }
        }
    ]
    
    # Sample sizes
    sizes = {
        "size_range": ["XS", "S", "M", "L", "XL"],
        "standard": "US"
    }
    
    try:
        # Create the style with all attributes
        new_style = client.style.attributes_create(
            folder_id=folder_id,
            fields=style_fields,
            colorways=colorways,
            sizes=sizes
        )
        print(f"Successfully created style with ID: {new_style['id']}")
        return new_style
        
    except BeProductException as e:
        print(f"Failed to create style: {str(e)}")
        raise

def main():
    # Get credentials from environment variables
    credentials = {
        'client_id': os.getenv('BEPRODUCT_CLIENT_ID'),
        'client_secret': os.getenv('BEPRODUCT_CLIENT_SECRET'),
        'refresh_token': os.getenv('BEPRODUCT_REFRESH_TOKEN'),
        'company_domain': os.getenv('BEPRODUCT_COMPANY_DOMAIN')
    }
        
    try:
        # Initialize the BeProduct client
        client = BeProduct(**credentials)
        
        # Get the first available style folder
        folders = client.style.folders()
        if not folders:
            print("No style folders found")
            return
            
        folder_id = folders[0]['id']
        print(f"Using folder: {folders[0]['name']} (ID: {folder_id})")
        
        # Create the style
        new_style = create_style(client, folder_id)
        
        # Print style details
        print("\nStyle Details:")
        print(f"ID: {new_style['id']}")
        print(f"Name: {new_style['fields'].get('name', 'N/A')}")
        print(f"Description: {new_style['fields'].get('description', 'N/A')}")
        print(f"Number of colorways: {len(new_style.get('colorways', []))}")
        
    except BeProductException as e:
        print(f"BeProduct API Error: {str(e)}")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")

if __name__ == "__main__":
    main() 