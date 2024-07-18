from .carbon import register_handlers as register_carbon_handlers
from .start import register_handlers as register_start_handlers
from .getid import register_handlers as register_getid_handlers
from .welcome import register_handlers as register_welcome_handlers
from .tts import register_handlers as register_tts_handlers
from .help import register_handlers as register_help_handlers
from .song import register_handlers as register_song_handlers
from .audteks import register_handlers as register_audteks_handlers
from .namebl import register_handlers as register_namebl_handlers
from .string import register_handlers as register_string_handlers
from .update import register_update_handler  # Mengimpor register_update_handler dari module/update.py
from .dev import register_handlers as register_dev_handlers  # Mengimpor register_handlers dari module/dev.py

def register_all_handlers(app):
    register_carbon_handlers(app)
    register_start_handlers(app)
    register_getid_handlers(app)
    register_welcome_handlers(app)
    register_tts_handlers(app)
    register_help_handlers(app)
    register_song_handlers(app)
    register_audteks_handlers(app)
    register_namebl_handlers(app)
    register_string_handlers(app)
    register_update_handler(app)
    register_dev_handlers(app)  # Mendaftarkan handler dari dev.py
