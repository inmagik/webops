import subprocess
import StringIO


def get_imagemagik_formats():

    ps = subprocess.Popen(('identify', '-list', 'format'), stdout=subprocess.PIPE)
    output = subprocess.check_output(('grep', 'rw+'), stdin=ps.stdout)
    ps.wait()
    out = []
    f = StringIO.StringIO(output)
    for l in f.readlines():
        l = l.replace("\n", "")
        pieces = l.split()
        out.append((pieces[0].replace("*", ""), pieces[1] + " " +  " ".join(pieces[3:-1])))

    return out






