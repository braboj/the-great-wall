from django.apps import AppConfig


class WallTrackerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tracker'

    num_teams = 20

    config_list = [
        [21, 25, 28],
        [17],
        [17, 22, 17, 19, 17, ]
    ]

