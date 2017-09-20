import os
from aquizz.app import create_app


os.environ.setdefault('FLASK_SETTINGS', 'production')
app = create_app()
