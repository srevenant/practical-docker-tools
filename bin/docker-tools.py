# vim:set expandtab ts=4 sw=4 ai ft=python:
# vim modeline (put ":set modeline" into your ~/.vimrc)

"""common / simplification wrapper"""

import os
import sys
import socket
import time
import json
import subprocess
import traceback

log_hdr = 0
log_cmd = 1
log_msg = 2
log_dbg = 3
log_err = 4
colors = {
    "fgblue":"\033[34m",
    "fgred":"\033[31m",
    "fggrn":"\033[32m",
    "fggray":"\033[37m",
    "reset":"\033[0m",
}

################################################################################
# simple subprocess caller
def sys_out(exc, print_error=False):
    if type(exc) == list:
        shell = False
    else:
        shell = True
    sub = subprocess.Popen(exc,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE,
                           shell=shell)
    out, err = sub.communicate()
    if not isinstance(out, str):
        out = out.decode()
    if err and print_error:
        print(err)
    if sub.returncode == 0:
        return out.strip()
    raise Exception("failed to exec: {}".format(exc))

################################################################################
# call a series of functions with fallback
def get_sys_fallback(func1, func2):
    try:
        var = func1()
        if isinstance(var, str):
            return var
    except:
        #traceback.print_exc()
        try:
            var = func2()
            if isinstance(var, str):
                return var
        except:
            pass
    return 'unknown'

################################################################################
# figure out who we are
MY_HOST = get_sys_fallback(lambda: sys_out(['hostname']),
                           lambda: socket.gethostname().split(".")[0])
MY_IPADDR = get_sys_fallback(lambda: sys_out(['hostname', '-I']).split(" ")[0],
                             lambda: socket.gethostbyname(socket.gethostname()))

################################################################################
def go_fmt(*keys):
    return "{{." + "}}\t{{.".join(keys) + "}}"

################################################################################
def shortest_keysize(info, maxsz):
    def _shortest(size, keys):
        sub = set()
        for key in keys:
            sub.add(key[:size])
        if len(sub) == len(keys):
            for key in keys:
                info[key]['shid'] = key[:size]
            return True
        return False
    for size in range(2, maxsz):
        if _shortest(size, info.keys()):
            break

################################################################################
class Core(object):
    outfd = sys.stdout
    cfg = dict(REPOS=dict(),
               COLOR=True,
               ECR=dict(LASTFILE="~/.docker-tools-ecr-last",
                        LOGIN_MAX_AGE=11,
                        REGION=""))
    ecr_last = ""
    _cmd = sys.argv.pop(0)
    _syntax = None
    _debug = False

    def __init__(self, config=None, syntax=None, debug=False):
        if config:
            self.cfg.update(config)
        if config.get('ECR', {}).get('LASTFILE'):
            self.ecr_last = os.path.expanduser(self.cfg['ECR']['LASTFILE'])
        self._debug = debug

        if syntax:
            self._syntax = syntax

    ############################################################
    def die(self, msg):
        self.log(msg, level=log_err)
        self.outfd.write("\n\n")
        sys.exit(1)

    ############################################################
    def log(self, msg, level=log_hdr, linebreak=True):
        coloron = ''
        docolor = self.cfg['COLOR']
        if level == log_hdr:
            fmt = "=====[ {time} {host}({ip}) ]===== {msg}"
            if docolor:
                coloron = colors['fgblue']
        elif level == log_err:
            fmt = "!!!!![ {time} {host}({ip}) ]!!!!! {msg}"
            if docolor:
                coloron = colors['fgred']
        elif level == log_msg:
            fmt = "{msg}"
        elif level == log_cmd:
            fmt = ">>> {msg}\n"
            if docolor:
                coloron = colors['fggrn']
        elif level == log_dbg:
            fmt = "<<<<<< {time} {host}({ip}) >>>>>> DEBUG"
            if docolor:
                fmrt += colors['reset']
                coloron = colors['fggray']
            fmt += "\n\n    {msg}"
        else:
            fmt = "UNKNOWN LOG LEVEL " + str(log_msg) + ": {msg}"

        coloroff = ''
        if coloron:
            coloroff = colors['reset']
        if linebreak:
            self.outfd.write("\n")
        self.outfd.write(coloron +
                         fmt.format(msg=msg,
                                    host=MY_HOST,
                                    ip=MY_IPADDR,
                                    time=time.strftime("%FT%T")) +
                         coloroff)
        self.outfd.flush()

    ############################################################
    def sys(self, cmd, abort=False):
        self.outfd.flush()
        if type(cmd) == list:
            shell = False
        else:
            shell = True
        sub = subprocess.call(cmd, shell=shell)
        self.outfd.flush()
        if sub:
            if abort:
                sys.exit(sub)
            return False
        return True

    ############################################################
    # different from module sys_out as it manages flushing output
    def sys_out(self, cmd, abort=False):
        self.outfd.flush()
        if type(cmd) == list:
            shell = False
        else:
            shell = True
        sub = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=shell)
        output, err = sub.communicate()
        self.outfd.flush()
        if type(output) != str:
            output = output.decode() # grr bytes object
        if sub.returncode > 0:
            if abort:
                sys.exit(output)
            return (False, output)
        return (True, output)

    ############################################################
    def do(self, cmd, abort=True):
        buf = ""
        if type(cmd) == str:
            shell = True
            buf += cmd
        else:
            shell = False
            arg0 = True
            for arg in cmd:
                if arg0:
                    arg = os.path.basename(arg)
                    arg0 = False
                if " " in arg:
                    arg = json.dumps(arg) # easy way to get quoting right
                buf += " " + arg
        buf += "\n"
        self.log(buf, level=log_cmd)
        return self.sys(cmd, abort=abort)

    ############################################################################
    def syntax(self, msg):
        if self._syntax:
            self._syntax(self, msg)
        print("Error: " + str(msg))

    ############################################################################
    def call_abort(self, func, *args):
        try:
            if self._debug:
                self.log(".call_abort({}, *{})".format(func, args), level=log_dbg)
            return func(*args)
        except Exception as err:
            self.log(str(err), level=log_err)
            sys.exit(1)

    ############################################################################
    def aws_ecr_login(self):
        age = 365 * 24 # random age, 1 year old
        if os.path.exists(self.ecr_last):
            # age in hours since now
            age = (time.time() - os.path.getmtime(self.ecr_last)) / 60 / 60

        if age > self.cfg['ECR']['LOGIN_MAX_AGE']:
            self.log("Refreshing AWS ECR Login\n", level=log_hdr)
            self.log("\n>>> aws ecr get-login --region " + self.cfg['ECR']['REGION'] + "\n\n",
                     level=log_cmd)
            status, output = self.sys_out([
                "aws", "ecr", "get-login", "--region", self.cfg['ECR']['REGION']
            ])
            if status:
                # cleanup deprecated msg
                output = output.replace("-e none ", "")
                if self.sys(output):
                    with open(self.ecr_last, "w") as out:
                        out.write("\n")

    ############################################################################
    def xload_services(self):
        fmt = "{{.ID}}\t{{.Name}}\t{{.Mode}}\t{{.Replicas}}\t{{.Image}}\t{{.Ports}}"
        info = dict()
        status, output = self.sys_out(["docker", "service", "ls", "--format", fmt], abort=True)
        idsz = 0
        for line in output.split('\n'):
            split = line.split('\t')
            if not line or len(split) != 6:
                continue
            sid, name, mode, replicas, img, port = split
            if idsz < len(sid):
                idsz = len(sid)
            host, repo = (img.split("/") + [None])[:2]
            if not repo:
                repo = host
                host = "docker.io"

            info[sid] = dict(name=name,
                             mode=mode,
                             img=img,
                             replicas=replicas,
                             repo=repo,
                             port=port,
                             repohost=host,
                             shkey='')

        shortest_keysize(info, idsz)
        return info

    def load_services(self):
        return self.docker_fmt(cmd=["docker", "service", "ls", "--format", None],
                               keys=["ID", "Name", "Mode", "Replicas", "Image", "Ports"])

    def load_service(self, svc):
        return self.docker_fmt(cmd=["docker", "service", "ps", "--format", None, svc],
                               keys=["ID", "Name", "Image", "Node", "DesiredState",
                                     "CurrentState", "Error", "Ports"])

    def docker_ps(self):
        return self.docker_fmt(cmd=["docker", "ps", "--format", None],
                               keys=["ID", "Image", "Command", "Status",
                                     "Ports", "Names"])

    ############################################################################
    def docker_fmt(self, cmd=None, keys=None):
        """cmd is an array of strings, with a None value for where fmt should go"""
        if not cmd or not keys:
            raise ValueError("docker_fmt() cmd or keys missing")
        fmt = go_fmt(*keys)
        for x in range(0, len(cmd)):
            if cmd[x] == None:
                cmd[x] = fmt
        info = dict()
        status, output = self.sys_out(cmd, abort=True)
        lower = [x.lower() for x in keys]
        idsz = 0
        for line in output.split('\n'):
            split = line.split('\t')
            if not line or len(split) != len(keys):
                continue

            svc = dict(zip(lower, split))
            sid = svc['id'] # required
            svc['shid'] = '' # shortest id

            if idsz < len(sid):
                idsz = len(sid)

            if svc.get('image'):
                host, repo = (svc['image'].split('/') + [None])[:2]
                if not repo:
                    svc['repo'] = host
                    svc['repohost'] = "docker.io"
                else:
                    svc['repo'] = repo
                    svc['repohost'] = host

            info[sid] = svc

        shortest_keysize(info, idsz)
        return info

