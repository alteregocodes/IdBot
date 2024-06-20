# module/__init__.py

from .carbon import *
from .start import *
from .getid import *
from .welcome import *
from .tts import *

def register_all_handlers(app):
    carbon_register_handlers(app)
    start_register_handlers(app)
    getid_register_handlers(app)
    welcome_register_handlers(app)
    tts_register_handlers(app)
