# module/__init__.py

from .carbon import *
from .start import *
from .getid import *
from .welcome import *

def register_handlers(app):
    carbon.register_handlers(app)
    start.register_handlers(app)
    getid.register_handlers(app)
    welcome.register_handlers(app)
