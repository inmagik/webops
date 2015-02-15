from django.conf import settings
import os
import json
from git import Repo
from opsmanager.helpers import serializer_from_dict
from opsmanager.ops import BaseOp
from rest_framework import serializers



class SimpleInFilesSerializer(serializers.Serializer):
    in_file = serializers.FileField(help_text='Input file')


GITOPS_REMOTE_OPS = getattr(settings, "GITOPS_REMOTE_OPS", [])
GITOPS_BASE_CACHE = getattr(settings, "GITOPS_BASE_CACHE", "")


def get_repo_path(op):
    pieces = op.split("/")
    return os.path.join(GITOPS_BASE_CACHE, "_".join(pieces[2:]));


def create_op_klass(opname, **options):
    return type(opname+"Op", (BaseOp,), dict(**options))


def op_from_config(data):
    #
    #serializer_from_dict
    options = json.loads(data["meta.json"])
    print options

    options["files_serializer"] = SimpleInFilesSerializer

    if "parameters.json" in data:
        params = json.loads(data["parameters.json"])
        params_serializer_klass = serializer_from_dict("parameters", params)
        print params_serializer_klass
        options["parameters_serializer"] = params_serializer_klass

    return create_op_klass(str(options["op_name"]), **options)
    





def load_remote_op(op):
    path = get_repo_path(op)

    interesting_files = ["meta.json", "process.py", "parameters.json"]
    data = {}

    if not os.path.isdir(path):
        print "CLONING REMOTE WEBOP: ", op
        #empty_repo = Repo.init(path)
        Repo.clone_from(op, path)
        #origin = empty_repo.create_remote('origin', op)
        #assert origin.exists()
        #origin.fetch()
        #empty_repo.create_head('master', origin.refs.master).set_tracking_branch(origin.refs.master)
        #empty_repo.head.reset(index=True, working_tree=True)
        #origin.pull()
    
    print "PULLING REPO DATA:", op
    repo = Repo(path)
    repo.remotes[0].pull()
    #repo.head.reset(index=True, working_tree=True)

    index = repo.index
    for (fpath, stage), entry in index.entries.items():
        if fpath in interesting_files:
            with open(os.path.join(path, fpath)) as f:
                data[fpath] = f.read()

    op = op_from_config(data)
    return op





def load_remote_ops():
    out = []
    for op in GITOPS_REMOTE_OPS:
        out.append(load_remote_op(op))
    return out
        



def bootstrap():
    if not os.path.isdir(GITOPS_BASE_CACHE):
        os.mkdir(GITOPS_BASE_CACHE)

    load_remote_ops()