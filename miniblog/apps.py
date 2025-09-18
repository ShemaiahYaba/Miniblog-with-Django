# Import Django's AppConfig for app configuration
from django.apps import AppConfig


class MiniblogConfig(AppConfig):
    """
    Configuration class for the miniblog Django app
    This class defines app-specific settings and metadata
    """
    # Default field type for auto-generated primary keys
    # BigAutoField uses 64-bit integers for primary keys
    default_auto_field = 'django.db.models.BigAutoField'
    
    # The name of the app - must match the app directory name
    name = 'miniblog'
