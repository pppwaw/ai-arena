import math
from math import sqrt
from collections import namedtuple
from queue import Queue

import api

data = namedtuple("data", ["is_space", "data"])
step = ""
q = Queue()
spaces = 0
Atom = namedtuple("Atom", ["x", "y", "vx", "vy", "r", "mass", "type"])

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
    if atom:
        return Atom(round(atom.x, 3), round(atom.y, 3), round(atom.vx, 3), round(atom.vy, 3), round(atom.radian, 3),
                    round(atom.mass, 3), atom.type)
    else:
        return None


def hebing(angs):
    x, y = 0, 0
    for i in angs:
        xx = math.cos(i)
        yy = math.sin(i)
        x += xx
        y += yy
    return api.relative_radian(0, 0, x, y)


def cal_t(x, y, vx, vy):
    if x / vx < 0 or y / vy < 0:
        return -1000
    else:
        return (x / vx + y / vy) / 2


def handle_shanbi(context: api.RawContext):
    me = context.me
    enemies = [i for i in context.enemies.copy() if i.type != "bullet" and i.mass > me.mass]
    enemies.sort(key=lambda x: me.distance_to(x))
    # print(f"shanbi me={print_atom(me)}")
    # print(f"shanbi enemies={[print_atom(i) for i in enemies]}")
    print("******shanbi******")
    angs = []
    for e in enemies:
        if e.whether_collide(me):
            print(f"shanbi {print_atom(e)} will collide")
            if e.distance_to(me) / api.distance(0, 0, e.vx, e.vy) > 10:
                print("More than 10s, ignore")
                continue
            # jd = jiaodu(me, e)
            cr = (e.vx - me.vx) * (e.y - me.y) - (e.vy - me.vy) * (e.x - me.x)
            # print(f"shanbi cr={cr}, jd={api.r2a(jd)} angle={api.relative_angle(0, 0, e.vx - me.vx, e.vy - me.vy)}")
            if cr >= 0:
                ang = api.a2r(api.relative_angle(0, 0, e.vx - me.vx, e.vy - me.vy) + 90)
            else:
                ang = api.a2r(api.relative_angle(0, 0, e.vx - me.vx, e.vy - me.vy) - 90)
            angs.append(ang)
    print(f"angs: {angs}")
    ang = hebing(angs)
    if angs:
        print(f"final ang: {ang}")
        while not q.empty(): q.get()
        for i in range(3):
            q.put(data(False, ang))
    print("******shanbi******")


def handle_target(context: api.RawContext):
    me = context.me

    max_qw, max_atom, shoot = 0, None, False

    print("******target******")
    # 先看不动
    enemies = [i for i in context.enemies if i.mass < me.mass]
    atoms = me.get_forward_direction_atoms(enemies)
    atoms.sort(key=lambda x: me.distance_to(x))
    print(f"stright forward atoms:{[print_atom(i) for i in atoms]}")
    if atoms:
        i = atoms[0]
        print(f"stright forward atom:{i}")
        t = cal_t((i.x - me.x), (i.y - me.y), me.vx, me.vy)
        qw = atoms[0].mass + t / 1000
        max_qw = qw
        max_atom = i
    # 再找没遮挡的目标
    enemies = [i for i in context.enemies if i.mass < me.mass - me.mass * api.SHOOT_AREA_RATIO * 2]

    atoms = api.find_neighbors(me, enemies)
    for i in atoms:
        if api.distance(0, 0, i.vx, i.vy) > 100:
            continue
        print(f"max_atom: {print_atom(max_atom)}, max_qw: {max_qw}")
        x, y = me.get_shoot_change_velocity(jiaodu(me, i))
        t = cal_t((i.x - me.x), (i.y - me.y), x, y)
        qw = i.mass - me.mass * api.SHOOT_AREA_RATIO * 2 + t / 1000
        if qw > max_qw:
            print(f"{print_atom(i)} qw:{qw} t:{t}")
            max_qw = qw
            max_atom = i
            shoot = True
    if max_atom:
        print(f"final angle:{api.r2a(jiaodu(me, max_atom))}")
        if shoot:
            if not me.colliding:
                for i in range(2):
                    q.put(data(False, jiaodu(me, max_atom)))
            else:
                print("colliding, don't shoot")
        else:
            print("Don't need to shoot")
    else:
        print("No atom, don't shoot")
    # q.put(data(True, 2))
    print("******target******")


def handler(context: api.RawContext):
    print(f"me: {print_atom(context.me)}")
    if context.step % 3 == 0:
        handle_shanbi(context)
    elif context.step % 5 == 0:
        handle_target(context)


def update(context: api.RawContext):
    if context.step % 30 == 0:
        print(f"{context.step // 30} second")
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
