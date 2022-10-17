from django.apps import AppConfig


class MineConfig(AppConfig):
    name = 'mine'

    def ready(self):
        from . import updater
        updater.subs_start()
