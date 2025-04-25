#!/usr/bin/env python3
"""
Example: Creating a Style in BeProduct (Asynchronous)
This example demonstrates how to:
1. Initialize the BeProduct client
2. Create a new style with attributes
3. Add colorways to the style
4. Handle potential errors
"""

from beproduct import AsyncBeProduct
from beproduct._exception import BeProductException
import os
import asyncio
from typing import Dict, Any
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
env_path = Path(__file__).parents[1] / '.env'
if env_path.exists():
    load_dotenv(env_path)

# ... existing code ... 