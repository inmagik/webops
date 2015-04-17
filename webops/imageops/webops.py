from webops_django.register import _register
from .ops.convert import ConvertOp
from .ops.pdftotext import PDFToTextOp
 

_register.register_op(ConvertOp)
_register.register_op(PDFToTextOp)
 