import requests
import os
import argparse
import sys
import logging
import json
import base64
"""

parser.add_argument('integers', metavar='N', type=int, nargs='+',
                   help='an integer for the accumulator')
parser.add_argument('--sum', dest='accumulate', action='store_const',
                   const=sum, default=max,
                   help='sum the integers (default: find the max)')

args = parser.parse_args()
print args.accumulate(args.integers)
"""


def exit_with_error(err):
    print "\n|webops| (error) sorry .. something went wrong :(  \n"
    print "\t"+err
    print
    sys.exit(1)   

def log_message(msg):
    print "|webops| ", msg


def get_clean_host(host):
    if not host.startswith("http://") and not host.startswith("https://"):
        host = "http://" + host
        return host


def get_ops_list(host):
    h = get_clean_host(host)
    out = requests.get(h+"/ops/")
    ops = out.json()
    return ops

def print_ops_list(ops):
    for x in ops:
        print x['id']
        print x['description']
        print


def get_op_meta(host, op):
    h = get_clean_host(host)
    out = requests.get(h+"/ops/" + op + "/")
    x = out.json()
    return x

def print_op_meta(x):
    print
    print x['id']
    print x['name']
    print x['description']
    print    
    print "PARAMETERS"
    print
    for p in x['parameters']:
        print p
        print "Description:", x['parameters'][p]['description']
        print "Type:",x['parameters'][p]['type']
        print "Required:",x['parameters'][p]['required']
        print


def get_parser(op_meta):
    #print op_meta
    p = argparse.ArgumentParser(description=op_meta['description'])
    params = op_meta['parameters']
    for param in params:
        if params[param]['required']:
            nargs = '?'
            required = True
        else:
            nargs = '?'
            required = False
        p.add_argument(param, nargs=nargs)
    return p

def run_op(host, op, op_args, outfile=None):          
    h = get_clean_host(host)
    #out = requests.post(h+"/ops/" + op + "/")
    meta = get_op_meta(host, op)
    #p = get_parser(meta)
    #print args
    #op_args = p.parse_args(args)
    #print op_args

    #todo: USE A new PARSER
    xargs = zip(*2*[iter(op_args)])
    http_params  ={}
    http_files = {}

    params = meta['parameters']


    for a in xargs:
        pname = a[0].replace("-", "")
        pp = params[pname]
        if pp ['type'] != 'FileField':
            http_params[pname] = a[1]
        else:
            http_files[pname] = open(a[1], 'rb')

    #print http_params
    uri = h+"/ops/" + op + "/" 
    #headers = {'content-type': 'application/json'}
    out = requests.post(uri, data=http_params, files=http_files)
    if out.status_code == 200:
        j = out.json()
        if meta["output_descriptor"] == 'FileData':
            fname = outfile or j['filename']
            with open(fname, "wb") as outfile:
                outfile.write(base64.b64decode(j['data']))
            log_message("%s done. output written to %s" % (op,fname))
        else:
            log_message("%s done. Output:\t%s" % (op,str(j)))

    else:
        print out.json()





parser = argparse.ArgumentParser(description='Webops command line utility', add_help=True)
parser.add_argument('--host',  type=str, nargs='?',
                   help='webops host name and port or ip address and port')


parser.add_argument('--outfile',  type=str, nargs='?', default=None,
                   help='file output name')

parser.add_argument('--list', action="store_true", default=False,
                   help='print list')

parser.add_argument('--meta', action="store_true", default=False,
                   help='print op meta')

parser.add_argument('--run', action="store_true", default=False,
                   help='run op')

parser.add_argument('op', type=str, nargs='?', 
                   help='op name to operate on')


parser.add_argument('opargs', nargs=argparse.REMAINDER)



args = parser.parse_args()
host =  args.host
if 'WEBOPS_HOST' in os.environ:
    host = os.environ['WEBOPS_HOST']

if not host:
    exit_with_error('no WEBOPS_HOST')

log_message("operating on %s" % host)

if args.list:
    lst = get_ops_list(host)
    print_ops_list(lst)



if args.meta:
    if not args.op:
        exit_with_error("meta requires an op.")
    meta = get_op_meta(host, args.op)
    print_op_meta(meta)

if args.run:
    if not args.op:
        exit_with_error("meta requires an op.")
    run_op(host, args.op, args.opargs, outfile=args.outfile)







