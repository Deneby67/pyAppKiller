from subprocess import Popen, PIPE

import time

from proc import Proc
import os
import signal


def memory():
    """
    Get node total memory and memory usage
    """
    with open('/proc/meminfo', 'r') as mem:
        ret = {}
        tmp = 0
        for i in mem:
            sline = i.split()
            if str(sline[0]) == 'MemTotal:':
                ret['total'] = int(sline[1])
            elif str(sline[0]) in ('MemFree:', 'Buffers:', 'Cached:'):
                tmp += int(sline[1])
            elif str(sline[0]) == 'SwapTotal:':
                ret['swapt'] = sline[1]
            elif str(sline[0]) == 'SwapFree:':
                ret['swapf'] = sline[1]
        ret['free'] = tmp
        ret['used'] = int(ret['total']) - int(ret['free'])
        ret['total_mem'] = int(ret['total']) + int(ret['swapt'])
        ret['total_used'] = int(ret['swapf']) + int(ret['used'])
        ret['proc_usage'] = ret['total_used'] * 100 / ret['total_mem']
    return ret


def get_proc_list():
    """ Return a list [] of Proc objects representing the active
    process list list """
    proc_list = []
    sub_proc = Popen(['ps', 'aux'], shell=False, stdout=PIPE)
    sub_proc.stdout.readline()
    for line in sub_proc.stdout:
        # print(line)
        # The separator for splitting is 'variable number of spaces'
        proc_info = line.decode('utf-8').split()
        proc_list.append(Proc(proc_info))
    proc_list.sort(key=lambda x: x.mem, reverse=True)
    return proc_list[0]


def kill_app():
    while True:
        mem = memory()
        proc = get_proc_list()
        if mem['proc_usage'] >= 70.0:
            print(proc.to_str())
            os.kill(proc.pid, signal.SIGTERM)
            print(memory()['used'])
        time.sleep(1)


kill_app()
