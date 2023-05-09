import math
from math import sqrt
from collections import namedtuple
from queue import Queue

import api

data = namedtuple("data", ["is_space", "data"])
step = ""
q = Queue()
spaces = 0
Atom = namedtuple("Atom", ["x", "y", "vx", "vy", "r", "mass"])

cal = lambda x1, vx1, x2, vx2, y1, vy1, y2, vy2, r1, r2, t: \
    (x1 + vx1 * t - x2 - vx2 * t) ** 2 + (y1 + vy1 * t - y2 - vy2 * t) ** 2 - (r1 + r2) ** 2


def will_coll(atom1: Atom, atom2: Atom):
    # (x1+vx1t-x2-vx2t)^2+(y1+vy1t-y2-vy2t)^2-(r1+r2)^2=0

    min_t = 0
    max_t = 100
    while ()


def handle_shanbi(context: api.RawContext):
    pass


def handle_target(context: api.RawContext):
    pass


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
