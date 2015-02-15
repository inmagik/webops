from collections import OrderedDict

class Register(object):

    def __init__(self):
        self.ops = OrderedDict()

    def register_op(self, op):
        self.ops[op.op_name] = op
    
    def deregister_op(self, op_name):
        pass


_register = Register()

