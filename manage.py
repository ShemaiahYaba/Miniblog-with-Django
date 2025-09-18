#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
# Import necessary modules for Django management
import os
import sys


def main():
    """Run administrative tasks."""
    # Tell Django where to find our settings file
    # This points to config/settings.py in our project
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    
    try:
        # Import Django's command-line management utility
        # This handles commands like 'runserver', 'migrate', 'makemigrations'
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        # If Django isn't installed, show a helpful error message
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    
    # Execute the command passed from the command line
    # sys.argv contains the command and its arguments (e.g., ['manage.py', 'runserver'])
    execute_from_command_line(sys.argv)


# This ensures main() only runs when this file is executed directly
# (not when imported as a module)
if __name__ == '__main__':
    main()
