import os

def get_secret(secret_id, backup=None):
    # GET variabel env atau kembalikan nilai cadangannya.
    return os.getenv(secret_id, backup)

# Import environment-specific settings
if get_secret('PIPELINE') == 'production':
    from .production import *
else:
    from .local import *
