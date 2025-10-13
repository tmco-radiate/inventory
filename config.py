import os
from flask import Flask

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
TEMPLATES = os.path.join(PROJECT_ROOT, 'templates')
DEBUG = True
LOG_FILE = 'qrcode.log'

app = Flask(__name__,
            template_folder=TEMPLATES)
if DEBUG:
    app.debug = DEBUG


