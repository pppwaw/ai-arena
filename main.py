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


# def will_coll(atom1: Atom, atom2: Atom):
#     # (x1+vx1t-x2-vx2t)^2+(y1+vy1t-y2-vy2t)^2-(r1+r2)^2=0
#
#     min_t = 0
#     max_t = 100
#     while ()


def jiaodu(me: Atom, atom: Atom):
    return api.a2r(api.relative_angle(me.x, me.y, atom.x + atom.vx - me.vx, atom.y + atom.vy - me.vy) + 180)


def print_atom(atom: api.Atom):
    return Atom(round(atom.x, 3), round(atom.y, 3), round(atom.vx, 3), round(atom.vy, 3), round(atom.radian, 3),
                round(atom.mass, 3))


def handle_shanbi(context: api.RawContext):
    me = context.me
    enemies = [i for i in context.enemies.copy() if i.type != "bullet"]
    enemies.sort(key=lambda x: me.distance_to(x))
    # print(f"shanbi me={print_atom(me)}")
    # print(f"shanbi enemies={[print_atom(i) for i in enemies]}")
    for e in enemies:
        if e.mass > me.mass and e.whether_collide(me):
            print(f"shanbi {print_atom(e)} will collide")
            # jd = jiaodu(me, e)
            cr = (e.vx - me.vx) * (e.y - me.y) - (e.vy - me.vy) * (e.x - me.x)
            # print(f"shanbi cr={cr}, jd={api.r2a(jd)} angle={api.relative_angle(0, 0, e.vx - me.vx, e.vy - me.vy)}")
            if cr >= 0:
                ang = api.a2r(api.relative_angle(0, 0, e.vx - me.vx, e.vy - me.vy) + 90)
            else:
                ang = api.a2r(api.relative_angle(0, 0, e.vx - me.vx, e.vy - me.vy) - 90)
            while not q.empty(): q.get()
            for i in range(3):
                q.put(data(False, ang))
            break


def handle_target(context: api.RawContext):
    pass


def handler(context: api.RawContext):
    if context.step % 3 == 0:
        handle_shanbi(context)
    elif context.step % 5 == 0:
        handle_target(context)


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
