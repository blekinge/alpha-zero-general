import builtins
import traceback
from os.path import relpath


def dprint(*args, **kwargs):
    """Pre-pends the filename and linenumber to the print statement"""

    stack = traceback.extract_stack()[:-1]
    i = -1
    last = stack[i]

    if last.name in ('clearln', 'finish'):
        return builtins.__dict__['oldprint'](*args, **kwargs)

    # Handle print wrappers in pytorch_classification/utils/progress/progress/helpers.py
    while last.name in ('writeln','write','update','write'):
        i = i - 1
        last = stack[i]



    # Handle different versions of the traceback module
    if hasattr(last, 'filename'):
        out_str = "{}:{} ".format(relpath(last.filename), last.lineno)
    else:
        out_str = "{}:{} ".format(relpath(last[0]), last[1])

    # Prepend the filename and linenumber
    return builtins.__dict__['oldprint'](out_str, *args, **kwargs)


def enable():
    if 'oldprint' not in builtins.__dict__:
        builtins.__dict__['oldprint'] = builtins.__dict__['print']
    builtins.__dict__['print'] = dprint


def disable():
    if 'oldprint' in builtins.__dict__:
        builtins.__dict__['print'] = builtins.__dict__['oldprint']