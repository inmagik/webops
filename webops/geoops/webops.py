import json
import os
from django.apps import AppConfig
from opsmanager.register import _register
from .ops.ogr2ogr import OgrOp
from .ops.buffer import BufferOp
from .ops.intersection import IntersectionOp
from .ops.gdaltranslate import GDALTranslateOp
from .ops.geocode import GeocodeOp

_register.register_op(OgrOp)
_register.register_op(GDALTranslateOp)
_register.register_op(BufferOp)
_register.register_op(IntersectionOp)
_register.register_op(GeocodeOp)



fpath = os.path.join(os.path.dirname(__file__), "ops/composition_test.json")
with open(fpath) as t:
    data = json.load(t)
graph_test = _register.compose_graph(data)
_register.register_op(graph_test)