from django.conf.urls import patterns, include, url
from rest_framework import routers
from .views import OpsView
from .register import _register


urlpatterns = [
    url(r'^$', OpsView.as_view(), name = "ops")
]

for o in _register.ops:
    op = _register.ops[o]
    urlpatterns.append(url(r'^%s/$' % op.op_name, op.as_view(), name = '%s' % op.op_name))
    #TODO (maybe): register with router instead?
    #something like: router.register(, op, base_name = op.op_name)


