"""
conftest.py - pytest configuration file.
Sets the PYTHONPATH so tests can import from the backend app.
"""
import sys
import os

# Add the backend directory to sys.path so 'from app.x import y' works
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
