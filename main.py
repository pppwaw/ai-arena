import math
from collections import namedtuple
from queue import Queue

import api

data = namedtuple("data", ["is_space", "data"])
step = ""
q = Queue()
spaces = 0
Atom = namedtuple("Atom", ["x", "y", "vx", "vy", "r", "mass", "type"])
SHANBI_CISHU = 3
TARGET_CISHU = 3

# def will_coll(atom1: Atom, atom2: Atom):
#     # (x1+vx1t-x2-vx2t)^2+(y1+vy1t-y2-vy2t)^2-(r1+r2)^2=0
#
#     min_t = 0
#     max_t = 100
#     while ()
kk = 0.5


def GoodAngle(me, m, s):
    mX = m.x + (m.vx - me.vx) * s
    mY = m.y + (m.vy - me.vy) * s
    Radian_me_m = api.relative_radian(me.x, me.y, m.x, m.y)
    if Radian_me_m < 0:
        Radian_me_m = math.pi * 2 + Radian_me_m

    Vx = me.vx - m.vx
    Vy = me.vy - m.vy
    AV_me_m = api.relative_angle(0, 0, Vx, Vy)

    LV = math.sqrt(Vx * Vx + Vy * Vy)
    AV = math.atan2(Vy, Vx)
    if AV < 0:
        AV = math.pi * 2 + AV

    GoodV = LV * math.cos(AV - Radian_me_m)
    BadV = abs(LV * math.sin(AV - Radian_me_m))
    x1 = me.x - m.x
    y1 = me.y - m.y
    L = math.sqrt(x1 * x1 + y1 * y1)

    angleMe2Mo = api.relative_radian(me.x, me.y, mX, mY)
    angleMe2Mo2 = angleMe2Mo + math.atan2(BadV, (L * kk))
    return angleMe2Mo2


def jiaodu(me: Atom, atom: Atom):
    return api.a2r(api.r2a(GoodAngle(me, atom, 1)) + 180)
    r_vx, r_vy = atom.vx - me.vx, atom.vy - me.vy
    return api.a2r(api.relative_angle(me.x, me.y, atom.x + r_vx, atom.y + r_vy) + 180)


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
        return -1
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
            if cal_t(e.x - me.x, e.y - me.y, e.vx - me.vx, e.vy - me.vy) > 3:
                print("More than 3s, ignore")
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
        for i in range(SHANBI_CISHU):
            q.put(data(False, ang))
    print("******shanbi******")


def have_bigger_atom(context, me: api.Atom, i: api.Atom):
    p_l = (me.x + me.radius * math.cos(me.radian + math.pi / 2), me.x + me.radius * math.sin(me.radian + math.pi / 2))
    p_r = (me.x + me.radius * math.cos(me.radian - math.pi / 2), me.x + me.radius * math.sin(me.radian - math.pi / 2))
    print("have bigger atom: p_l={}, p_r={}".format(p_l, p_r))
    enemies = [i for i in context.enemies if i.mass >= me.mass - me.mass * api.SHOOT_AREA_RATIO * TARGET_CISHU]
    if len(api.raycast(enemies, p_l, me.radian_to_atom(i), me.distance_to(i))) + len(
            api.raycast(enemies, p_r, me.radian_to_atom(i), me.distance_to(i))) > 0:
        return True
    return False


def handle_target(context: api.RawContext):
    me = context.me

    max_qw, max_atom, shoot = 0, None, False

    print("******target******")
    # 先看不动
    if me.vx != 0 or me.vy != 0:
        enemies = [i for i in context.enemies if i.mass < me.mass]
        atoms = me.get_forward_direction_atoms(enemies)
        atoms.sort(key=lambda x: me.distance_to(x))
        print(f"stright forward atoms:{[print_atom(i) for i in atoms]}")
        if atoms:
            i = atoms[0]
            for j in atoms:
                if i.mass < j.mass < me.mass:
                    i = j
            print(f"stright forward atom:{print_atom(i)}")
            t = cal_t((i.x - me.x), (i.y - me.y), me.vx, me.vy)
            qw = atoms[0].mass + 100 / (t / 10)
            max_qw = qw
            max_atom = i
            print(f"max_atom: {print_atom(max_atom)}, max_qw: {max_qw}")
    # 再找没遮挡的目标
    enemies = [i for i in context.enemies if i.mass < me.mass - me.mass * api.SHOOT_AREA_RATIO * TARGET_CISHU]

    atoms = api.find_neighbors(me, enemies)
    for i in atoms:
        if api.distance(0, 0, i.vx, i.vy) > 100:
            continue
        if have_bigger_atom(context, me, i):
            print(f"Have bigger atom in road, continue")
            continue
        x, y = me.get_shoot_change_velocity(jiaodu(me, i))
        t = cal_t((i.x - me.x), (i.y - me.y), i.vx - x, i.vy - y)
        qw = i.mass - me.mass * api.SHOOT_AREA_RATIO * TARGET_CISHU + 100 / (t / 10)
        if qw > max_qw:
            print(f"{print_atom(i)} qw:{qw} t:{t}")
            max_qw = qw
            max_atom = i
            shoot = True
            print(f"max_atom: {print_atom(max_atom)}, max_qw: {max_qw}")
    if max_atom:
        print(f"final angle:{api.r2a(jiaodu(me, max_atom))}")
        if shoot:
            if not me.colliding:
                for i in range(TARGET_CISHU):
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
    elif context.step % 10 == 0:
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
