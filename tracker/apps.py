from django.apps import AppConfig
from rootdir import ROOT_DIR
from builder.manager import WallManager
from builder.configurator import WallConfigurator

import os

LOG_FILE_PATH = os.path.join(ROOT_DIR, 'data', 'wall.log')
INI_FILE_PATH = os.path.join(ROOT_DIR, 'data', 'wall.ini')


class WallTrackerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tracker'

    # Initialize the wall configurator
    config = WallConfigurator.from_ini(INI_FILE_PATH)

    # Initialize the wall manager
    manager = WallManager(log_filepath=LOG_FILE_PATH)
    manager.set_config(config)
