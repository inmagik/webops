from django.apps import AppConfig
from .register import _register
from django.conf import settings
 
class OpsAppConfig(AppConfig):

    name = 'opsmanager'
    verbose_name = 'OpsManager'
    loaded = False
 
    def ready(self):
        #TODO (maybe): this could go elsewhere, for example in apps.py?
        pass
        
                