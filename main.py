import math
from collections import namedtuple
from math import sin, cos
from queue import Queue

import api

data = namedtuple("data", ["is_space", "data"])
step = ""
q = Queue()
spaces = 0
Atom = namedtuple("Atom", ["x", "y", "vx", "vy", "r", "theta", "mass", "type", "id"])
SHANBI_CISHU = 3
TARGET_CISHU = 1


kk = 0.5


def qw_c(mass, t):
    return mass + 100 / (t / 100)


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
    return GoodAngle(me, atom, 1) + 3.14
    # return api.a2r(api.r2a(GoodAngle(me, atom, 1)) + 180)
    r_vx, r_vy = atom.vx - me.vx, atom.vy - me.vy
    return api.a2r(api.relative_angle(me.x, me.y, atom.x + r_vx, atom.y + r_vy) + 180)


def get_shoot_change_velocity(radian) -> tuple[float, float]:  # x,y
    return -cos(radian) * 10.2, -sin(radian) * 10.2


def print_atom(atom: api.Atom):
    if atom:
        return Atom(
            round(atom.x, 3),
            round(atom.y, 3),
            round(atom.vx, 3),
            round(atom.vy, 3),
            round(atom.radius, 3),
            round(atom.radian, 3),
            round(atom.mass, 3),
            atom.type,
            atom.id,
        )
    else:
        return None


def hebing(angs):
    x, y = 0, 0
    for i in angs:
        xx = cos(i)
        yy = sin(i)
        x += xx
        y += yy
    return api.relative_radian(0, 0, x, y)


def cal_t(me: api.Atom, atom: api.Atom, vx, vy):
    x, y = (
        atom.x - me.x - atom.radius + me.radius,
        atom.y - me.y - atom.radius + me.radius,
    )
    vx = me.vx + vx - atom.vx
    vy = me.vy + vy - atom.vy
    print(f"cal_t x={x}, y={y}, vx={vx}, vy={vy}")
    if x / vx < -0.3 or y / vy < -0.3:
        return -1
    else:
        return (x / vx + y / vy) / 2


def handle_shanbi(context: api.RawContext):
    me = context.me
    enemies = [i for i in context.enemies.copy() if i.mass >= me.mass]
    enemies.sort(key=lambda x: me.distance_to(x))
    # print(f"shanbi me={print_atom(me)}")
    # print(f"shanbi enemies={[print_atom(i) for i in enemies]}")
    print("******shanbi******")
    print(f"me: {print_atom(context.me)}")
    angs = []
    for e in enemies:
        if e.whether_collide(me):
            print(f"shanbi {print_atom(e)} will collide")
            t = cal_t(me, e, 0, 0)
            if t > 3:
                print("More than 3s, ignore")
                continue
            elif t == -1:
                print("No collide")
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
        while not q.empty():
            q.get()
        for i in range(SHANBI_CISHU):
            q.put(data(False, ang))
    print("******shanbi******")


def have_bigger_atom(context, me: api.Atom, i: api.Atom):
    radian = me.radian_to_atom(i)
    p_l = (
        me.x + me.radius * cos(radian + math.pi / 2),
        me.x + me.radius * sin(radian + math.pi / 2),
    )
    p_r = (
        me.x + me.radius * cos(radian - math.pi / 2),
        me.x + me.radius * sin(radian - math.pi / 2),
    )
    print("have bigger atom: p_l={}, p_r={}".format(p_l, p_r))
    enemies = [
        i
        for i in context.enemies
        if i.mass >= me.mass - me.mass * api.SHOOT_AREA_RATIO * TARGET_CISHU
    ]
    if (
        len(api.raycast(enemies, p_l, me.radian_to_atom(i), me.distance_to(i)))
        + len(api.raycast(enemies, p_r, me.radian_to_atom(i), me.distance_to(i)))
        > 0
    ):
        return True
    return False


def handle_target(context: api.RawContext):
    me = context.me

    max_qw, max_atom, shoot = 0, None, False

    print("******target******")
    print(f"me: {print_atom(context.me)}")
    # 先看不改变方向。如果速度超过40m/s则不动
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
            if api.distance(0, 0, me.vx, me.vy) >= 40:
                t = cal_t(me, i, 0, 0)
                qw = qw_c(i.mass, t)
            else:
                x, y = get_shoot_change_velocity(jiaodu(me, i))
                x, y = x * TARGET_CISHU, y * TARGET_CISHU
                print(f"shoot change velocity: x={x}, y={y}")
                t = cal_t(me, i, x, y)
                qw = qw_c(i.mass - me.mass * api.SHOOT_AREA_RATIO * TARGET_CISHU, t)
                shoot = True
            max_qw = qw + 100
            max_atom = i
            print(f"max_atom: {print_atom(max_atom)}, max_qw: {max_qw}")
    # 再找没遮挡的目标
    enemies = [
        i
        for i in context.enemies
        if i.mass < me.mass - me.mass * api.SHOOT_AREA_RATIO * TARGET_CISHU
    ]
    atoms = api.find_neighbors(me, enemies)
    for i in atoms:
        if api.distance(0, 0, i.vx, i.vy) > 100:
            continue
        print()
        print(f"atom: {print_atom(i)}")
        if have_bigger_atom(context, me, i):
            print(f"Have bigger atom in road, continue")
            continue
        x, y = get_shoot_change_velocity(jiaodu(me, i))
        x, y = x * TARGET_CISHU, y * TARGET_CISHU
        print(f"shoot change velocity: {x + me.vx}, {y + me.vy}")
        t = cal_t(me, i, x, y)
        qw = qw_c(i.mass - me.mass * api.SHOOT_AREA_RATIO * TARGET_CISHU, t)
        print(f"qw:{qw} t:{t}")
        if qw > max_qw + 10:
            # print(f"{print_atom(i)} qw:{qw} t:{t}")
            max_qw = qw
            max_atom = i
            shoot = True
            print(f"max_atom: {print_atom(max_atom)}, max_qw: {max_qw}")
    if max_atom:
        if shoot:
            if not me.colliding:
                print(f"final angle:{api.r2a(jiaodu(me, max_atom))}")
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
    # print(f"me: {print_atom(context.me)}")
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
