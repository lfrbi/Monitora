import os

def get_secret(secret_id, backup=None):
    """Retrieve the environment variable or return the backup value."""
    return os.getenv(secret_id, backup)

# Import environment-specific settings
if get_secret('PIPELINE') == 'production':
    from .production import *
else:
    from .local import *
