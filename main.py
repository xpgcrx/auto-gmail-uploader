"""
Bridge file for Cloud Functions.
Google Cloud Functions (2nd gen) expects the entry point to be at the root of the source package.
This file imports and exposes the main execution logic from the src directory.
"""

from src.main import main
