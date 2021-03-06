import json
import os
from django.apps import AppConfig
from webops_django.register import _register
from webops_django.ops import compose_graph
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
graph_test = compose_graph(_register, data)
_register.register_op(graph_test)