from django.apps import AppConfig
from .register import _register

 
class OpsAppConfig(AppConfig):

    name = 'opsmanager'
    verbose_name = 'OpsManager'
 
    def ready(self):
        pass
 
        