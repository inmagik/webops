from collections import OrderedDict
from django.conf import settings
import warnings
#import logging
#logger = logging.getLogger(__name__)
import sys
import imp
import importlib
import json
import os

from .composition import create_partial_serializer, create_partial_op
from rest_framework import serializers
import copy
from .ops import BaseOp
from .helpers import export_file


WEBOPS_BREAK_ON_FAIL_TEST = getattr(settings, "WEBOPS_BREAK_ON_FAIL_TEST", False)
WEBOPS_OPS = getattr(settings, "WEBOPS_OPS", None)


class Register(object):

    def __init__(self):
        self.ops = OrderedDict()

    def register_op(self, op):

        try:
            op.check_op()
            
        except NotImplementedError:
            pass
        except:
            if(WEBOPS_BREAK_ON_FAIL_TEST):
                raise
            #logger.error("Op registration failed, skipping %s" % op.op_name)
            print >>sys.stderr, "!! WEBOPS: Op registration failed, skipping %s" % op.op_id
            return                

        self.ops[op.op_id] = op
    
    def deregister_op(self, op_name):
        pass


    def compose_graph(self, data):
        """
        should return a new composed op...
        """
        partial_ops = {}
        partials  = { }
        ops_inputs = {}

        #TODO:PASS IN RANDOM NAME
        op_id = data["op_id"]
        op_name = data["op_name"] or "GraphOp"
        op_description = data["op_description"] or "GraphOp op_description"

        ops = data["ops"]
        for op in ops:
            #print op
            base_op = self.ops[op["op"]]
            op_label = str(op["label"])
            if "partials" in op:
                o2 = create_partial_op (op_label, base_op, op["partials"])
                partial_ops[op_label] = o2
                partials[op_label] = op["partials"]
                
            else:
                partial_ops[op_label] = base_op

        all_ops = partial_ops.keys()
        for op_label in all_ops:
            ser = partial_ops[op_label].parameters_serializer()
            fields = ser.get_fields()
            for field in fields:
                field_clean = field.replace(":", "-")
                fieldname = "%s:%s" % (op_label, field_clean)
                ops_inputs[fieldname] = fields[field]


        output_candidates = all_ops
        
        deps = {}
        wires = []
        if "wires" in data:
            wires = data["wires"]
        

        for wire in wires:
            target_op_id, target_input = wire["to"].split(":")
            if target_op_id not in deps:
                deps[target_op_id] = []
            #check for circular dep
            if wire["from"] in deps and target_op_id in deps[wire["from"]]:
                raise APIException(detail="Circular dependency between %s and %s" % (target_op, wire["from"]))
            
            deps[target_op_id].append({"name": wire["from"], "target" : target_input})
            del ops_inputs[wire["to"]]

            try:
                output_candidates.remove(wire["from"])
            except:
                pass

        if not len(output_candidates):
            #should be impossible to reach .. unless no ops are posted
            raise APIException(detail="No output candidates remained")

        if len(output_candidates) > 1 and "output_op" not in data:
            raise APIException(detail="Too many output candidates. Please use output_op to specify exactly one")        

        output_op = output_candidates[0]
        
        #we should have 1 output candidate, deps and inputs there.
        
        # let's build the process function
        # it should:
        # - remap serializer inputs
        # - combine process functions.
        def new_process(self, parameters):
            outputs = { }

            def remap_parameters(p2, op_id):

                params = {}
                ins = ops_inputs.keys()
                for fieldname in ins:
                    op, name = fieldname.split(":")
                    if fieldname in p2:
                        name = name.replace("-", ":")
                        params[name] = p2[fieldname]
                return params


            def process_op(op):
                p = {}
                if op in deps:
                    for dep in deps[op]:
                        if dep["name"] not in outputs:
                            out_file = process_op(dep["name"])
                            x = getattr(partial_ops[op], "output_descriptor", None)
                            if x is not None:
                                outputs[dep["name"]] = out_file    
                            else:
                                outputs[dep["name"]] = export_file(out_file['filename'])                        
                            print "ook", dep
                            
                        p[dep["target"]] = outputs[dep["name"]]
                
                op_params = remap_parameters(parameters, op)
                op_params.update(p)

                ser = partial_ops[op].parameters_serializer(data=op_params)
                ser.is_valid(raise_exception=True)
                
                print "processing", op
                out =  partial_ops[op]().process(ser.validated_data)
                print "done", op
                return out
            
            return process_op(output_op)
        
        #let's build a new serializer to validate input
        new_parameters_serializer = type("GraphOpSerializer", (serializers.Serializer,), copy.deepcopy(ops_inputs))
        new_output_descriptor = getattr(partial_ops[output_op], "output_descriptor", None)

        #finally the composed operation
        graph_op = type("GraphOp", 
            (BaseOp,),
            {"process": new_process, "parameters_serializer" : new_parameters_serializer,
            "op_id" : op_id,
            "op_name" : op_name, "op_description": op_description, "output_descriptor" : new_output_descriptor }
        )
        
        return graph_op


_register = Register()


loaded = False
if not loaded:
    
    for app in settings.INSTALLED_APPS:
        # For each app, we need to look for an webops.py inside that app's
        # package. We can't use os.path here -- recall that modules may be
        # imported different ways (think zip files) -- so we need to get
        # the app's __path__ and look for admin.py on that path.

        # Step 1: find out the app's __path__ Import errors here will (and
        # should) bubble up, but a missing __path__ (which is legal, but weird)
        # fails silently -- apps that do weird things with __path__ might
        # need to roll their own admin registration.
        try:
            app_path = importlib.import_module(app).__path__
        except AttributeError:
            continue

        # Step 2: use imp.find_module to find the app's webops.py. For some
        # reason imp.find_module raises ImportError if the app can't be found
        # but doesn't actually try to import the module. So skip this app if
        # its webops.py doesn't exist
        try:
            imp.find_module('webops', app_path)
        except ImportError:
            continue

        # Step 3: import the app's admin file. If this has errors we want them
        # to bubble up.
        importlib.import_module("%s.webops" % app)
        # autodiscover was successful, reset loading flag.
    
    loaded = True

    for item in WEBOPS_OPS:
            if 'op_class' in item:
                pieces = item['op_class'].split(".")
                cls = pieces[-1]
                module = ".".join(pieces[:-1])
                m = importlib.import_module(module)
                kls = getattr(m, cls)
                _register.register_op(kls)

            elif 'op_graph' in item:
                with open(item['op_graph']) as t:
                    data = json.load(t)
                    graph = _register.compose_graph(data)
                    _register.register_op(graph)



