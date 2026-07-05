"""
Project FALCON - Kite Login
"""

import os
import sys

# Add the project root (FALCON/) to Python's import path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from kiteconnect import KiteConnect
from config.settings import API_KEY

kite = KiteConnect(api_key=API_KEY)

print("=" * 60)
print("PROJECT FALCON - KITE LOGIN")
print("=" * 60)

print("\nLogin URL:\n")
print(kite.login_url())