from django.apps import AppConfig
from opsmanager.register import _register
from .ops.convert import ConvertOp
from .ops.pdftotext import PDFToTextOp
 
_register.register_op(ConvertOp)
_register.register_op(PDFToTextOp)
 
class ImageOpsAppConfig(AppConfig):

    name = 'imageops'
    verbose_name = 'ImageOps'
        
        