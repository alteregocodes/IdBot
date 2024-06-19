# module/__init__.py

from .carbon import carbon
from .update import update
from .start import start
from .getid import get_id
from .help import help_command, help_update, help_start, help_carbon, help_getid

def initialize_handlers(client: Client):
    client.add_handler(update, prefix='update')
    client.add_handler(start, prefix='start')
    client.add_handler(carbon, prefix='carbon')
    client.add_handler(get_id, prefix='getid')
    client.add_handler(help_command, prefix='help')
    client.add_handler(help_update, prefix='help_update')
    client.add_handler(help_start, prefix='help_start')
    client.add_handler(help_carbon, prefix='help_carbon')
    client.add_handler(help_getid, prefix='help_getid')
