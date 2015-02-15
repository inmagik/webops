from django.apps import AppConfig
from opsmanager.register import _register
from gitops import helpers

ops = helpers.load_remote_ops()
for op in ops:
    _register.register_op(op)
 
class GitOpsAppConfig(AppConfig):

    name = 'gitops'
    verbose_name = 'GitOps'
        

        