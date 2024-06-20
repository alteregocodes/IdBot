# module/__init__.py

from .carbon import register_handlers as carbon_register_handlers
from .start import register_handlers as start_register_handlers
from .getid import register_handlers as getid_register_handlers
from .welcome import register_handlers as welcome_register_handlers

def register_all_handlers(app):
    carbon_register_handlers(app)
    start_register_handlers(app)
    getid_register_handlers(app)
    welcome_register_handlers(app)
