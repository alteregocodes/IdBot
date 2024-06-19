# module/__init__.py

from . import start, update, carbon, getid, help

def init(app):
    start.init(app)
    update.init(app)
    carbon.init(app)
    getid.init(app)
    help.init(app)
