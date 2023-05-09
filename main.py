import math
from math import sqrt
from collections import namedtuple
from queue import Queue

import api

data = namedtuple("data", ["is_space", "data"])
step = ""
q = Queue()
spaces = 0


def handle_shanbi(context: api.RawContext):
    pass


def handle_target(context: api.RawContext):


def handler(context: api.RawContext):
    if context.step % 3 == 0:
        return handle_shanbi(context)
    elif context.step % 5 == 0:
        return handle_target(context)


def update(context: api.RawContext):
    handler(context)
    global spaces
    if spaces:
        spaces -= 1
        return None
    elif not q.empty():
        r: data = q.get()
        if r.is_space:
            spaces += r.data - 1
            return None
        else:
            return r.data
    else:
        return None
