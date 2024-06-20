# module/__init__.py

from .carbon import register_handlers as register_carbon_handlers
from .start import register_handlers as register_start_handlers
from .getid import register_handlers as register_getid_handlers
from .welcome import register_handlers as register_welcome_handlers
from .tts import register_handlers as register_tts_handlers
from .help import register_handlers as register_help_handlers
from .song import register_handlers as register_song_handlers
from .play import register_handlers as register_play_handlers  # Import play handlers

def register_all_handlers(app):
    register_carbon_handlers(app)
    register_start_handlers(app)
    register_getid_handlers(app)
    register_welcome_handlers(app)
    register_tts_handlers(app)
    register_help_handlers(app)
    register_song_handlers(app)
    register_play_handlers(app)  # Register play handlers
