# module/__init__.py

from .start import *
from .update import *
from .carbon_module import *
from .getid import *
from .help import *

def init(app):
    start.init(app)
    update.init(app)
    carbon_func.init(app)
    get_user_id.init(app)
    help.init(app)
