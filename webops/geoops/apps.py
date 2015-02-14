from django.apps import AppConfig
from opsmanager.register import _register
from .ops.ogr2ogr import OgrOp
from .ops.buffer import BufferOp

 
class GeoOpsAppConfig(AppConfig):

    name = 'geoops'
    verbose_name = 'GeoOps'
 
    def ready(self):
        _register.register_op(OgrOp)
        _register.register_op(BufferOp)
        
        #_register.register_op(ConvertOp)
        

        