import operator
from .ops import BinaryNumberInputSerializer
from rest_framework import serializers
from webops_django.wrappers import wrap_function
from webops_django.register import _register

wrapped = [operator.add, operator.sub, operator.mul, operator.div, operator.pow]
for w in wrapped:
    x = wrap_function("com.inmagik."+w.__name__, w, BinaryNumberInputSerializer, serializers.FloatField())
    _register.register_op(x)
