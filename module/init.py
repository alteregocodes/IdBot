# module/__init__.py

from . import start, update, carbon_module, getid, help

def init(app):
    start.init(app)
    update.init(app)
    carbon_module.init(app)
    getid.init(app)
    help.init(app)
