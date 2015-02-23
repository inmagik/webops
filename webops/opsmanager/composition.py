from rest_framework.views import APIView
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework import serializers
import copy
from .register import _register
from .ops import BaseOp
from .helpers import export_file

def create_partial_serializer(name, base_serializer_class, partials):
    ser = base_serializer_class()
    fields = ser.get_fields()
    for p in partials:
        if p in fields:
            del fields[p]

    return type(name, (serializers.Serializer,), copy.deepcopy(fields) )
    


def create_partial_op(name, op_class, partials):

    def process_with_partials(self, parameters):
        parameters.update(partials)
        return op_class.process(self, parameters)

    partial_serializer = create_partial_serializer(name + "ParametersSerializer", op_class.parameters_serializer, partials)

    newclass = type(name, (op_class,),
        {"process": process_with_partials, "parameters_serializer" : partial_serializer })
    return newclass



def compose_graph(data):
    """
    should return a new composed op...
    """
    #print _register.ops
    partial_ops = {}
    partials  = { }
    ops_inputs = {}

    #TODO:PASS IN RANDOM NAME
    op_name = data["op_name"] or "GraphOp"
    op_description = data["op_description"] or "GraphOp op_description"

    ops = data["ops"]
    for op in ops:
        #print op
        base_op = _register.ops[op["op"]]
        op_id = str(op["id"])
        if "partials" in op:
            o2 = create_partial_op (op_id, base_op, op["partials"])
            partial_ops[op_id] = o2
            partials[op_id] = op["partials"]
            
        else:
            partial_ops[op_id] = base_op

    all_ops = partial_ops.keys()
    for op_id in all_ops:
        ser = partial_ops[op_id].parameters_serializer()
        fields = ser.get_fields()
        for field in fields:
            fieldname = "%s:%s" % (op_id, field)
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
                    params[name] = p2[fieldname]
            return params


        def process_op(op):
            p = {}
            if op in deps:
                for dep in deps[op]:
                    if dep["name"] not in outputs:
                        out_file = process_op(dep["name"])
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
    
    #finally the composed operation
    graph_op = type("GraphOp", 
        (BaseOp,),
        {"process": new_process, "parameters_serializer" : new_parameters_serializer,
        "op_name" : op_name, "op_description": op_description }
    )
    
    return graph_op
    





class OpsGraphView(APIView):
    """
    
    """
    #authentication_classes = (authentication.TokenAuthentication,)
    #permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        out = {}
        op = compose_graph(request.DATA)
        return Response(out)


    

