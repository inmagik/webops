from django.apps import AppConfig
from opsmanager.register import _register
from .ops.convert import ConvertOp
 

 
class ImageOpsAppConfig(AppConfig):

    name = 'imageops'
    verbose_name = 'ImageOps'
 
    def ready(self):
        _register.register_op(ConvertOp)
        