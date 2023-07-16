import math
from collections import namedtuple
from math import sin, cos
from queue import Queue

import api
from api import Atom

data = namedtuple("data", ["is_space", "data"])
step = ""
q = Queue()
spaces = 0
AtomTuple = namedtuple(
    "Atom", ["x", "y", "vx", "vy", "r", "theta", "mass", "type", "id"]
)
SHANBI_CISHU = 3
TARGET_CISHU = 3
MAX_SPEED = 50
SHANBI_TIME = 2


def qw_c(mass, t):
    return mass + 100 / (t / 100)


def Angle(me: api.Atom, atom: api.Atom) -> list[float]:
    rtn = []
    r1 = api.relative_radian(me.x, me.y, atom.x, atom.y) % (2 * math.pi)
    r2 = me.radian_to_atom(atom) % (2 * math.pi)
    me_v = api.distance(0, 0, me.vx, me.vy)
    shu = me_v * sin(r2)
    heng = me_v * cos(r2)
    r_shu = api.a2r(270) + r1
    r_heng = api.a2r(api.r2a(r1) + 180)
    cishu = TARGET_CISHU
    print(f"r1={api.r2a(r1)}, r2={api.r2a(r2)}, shu={shu}, heng={heng}")
    if abs(shu) >= 0.1:
        # 先将竖直分量修正为0
        shu_time = int(shu // 10.2)
        print(f"Angle shu_time={shu_time}")
        if abs(shu) >= 10.2:  # 至少有一次
            if shu_time >= cishu:  # 忽略超过 TARGET_CISHU 的部分
                rtn = [r_shu] * cishu
            elif shu_time < 0:
                r_shu = api.a2r(90) + r1
                abs_shu_time = abs(shu_time)
                if abs_shu_time >= cishu:
                    rtn = [r_shu] * cishu
                else:
                    rtn = [r_shu] * abs_shu_time
            else:
                rtn += [r_shu] * shu_time
            shu -= shu_time * 10.2
        if abs(shu) >= 0.1:
            y = shu
            x = math.sqrt(10.2**2 - y**2)
            r_last_shu = api.a2r(r1 - api.r2a(api.relative_radian(0, 0, x, y)) + 180)
            rtn.append(r_last_shu)
            print(f"Angle shu={shu}, last_shu={api.r2a(r_last_shu)}")
        # 如果次数足够，则修复横向
        if len(rtn) >= cishu:
            return rtn
    rtn += [r_heng] * (cishu - len(rtn))
    print(f"Angle rtn={[api.r2a(i) for i in rtn]}")
    return rtn


def shanbiAngle(me: api.Atom, atom: api.Atom) -> list[float]:
    rtn = []
    r1 = api.relative_radian(me.x, me.y, atom.x, atom.y)
    r2 = me.radian_to_atom(atom)
    me_v = api.distance(0, 0, me.vx, me.vy)
    shu = me_v * sin(r2)
    heng = me_v * cos(r2)
    r_shu = api.a2r(90) + r1
    r_heng = api.r2a(r1)
    cishu = SHANBI_CISHU
    print(f"shanbiAngle r1={api.r2a(r1)}, r2={api.r2a(r2)}, shu={shu}, heng={heng}")
    # 确保heng = 0，由于此时必定在向小球靠近，所以heng必然为正，heng也是
    heng_time = int(heng // 10.2)
    if heng >= 10.2:
        if heng_time >= cishu:
            rtn = [r_heng] * cishu
        else:
            rtn = [r_heng] * heng_time
        heng -= heng_time * 10.2
        if heng > 0:
            rtn += [r_heng]
    # 如果次数足够，则一半修复竖直，一半原理
    if len(rtn) >= cishu:
        return rtn
    rtn += [r_shu] * (cishu - len(rtn)) / 2 + [r_heng] * (cishu - len(rtn)) / 2
    print(f"shanbiAngle rtn={[api.r2a(i) for i in rtn]}")
    return rtn


def jiaodu(me: Atom, atom: Atom, shanbi=False):
    if shanbi:
        return shanbiAngle(me, atom)
    else:
        return Angle(me, atom)


def get_shoot_change_velocity(radian) -> tuple[float, float]:  # x,y
    return -cos(radian) * 10.2, -sin(radian) * 10.2


def print_atom(atom: api.Atom):
    if atom:
        return AtomTuple(
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
            if t > SHANBI_TIME:
                print(f"More than {SHANBI_TIME}s, ignore")
                continue
            elif t == -1:
                print("No collide")
                continue
            cr = (e.vx - me.vx) * (e.y - me.y) - (e.vy - me.vy) * (e.x - me.x)
            # print(
            #     f"shanbi cr={cr}, jd={api.r2a(jd)} angle={api.relative_angle(0, 0, e.vx - me.vx, e.vy - me.vy)}"
            # )
            if cr >= 0:
                ang = api.a2r(api.relative_angle(0, 0, e.vx - me.vx, e.vy - me.vy) + 90)
            else:
                ang = api.a2r(api.relative_angle(0, 0, e.vx - me.vx, e.vy - me.vy) - 90)
            # angs.extend(jiaodu(me, e, True))
            angs.append(ang)
    print(f"angs: {angs}")
    ang = hebing(angs)
    if angs:
        print(f"final angle: {api.r2a(ang)}")
        while not q.empty():
            q.get()
        for i in range(SHANBI_CISHU):
            q.put(data(False, ang))
    print("******shanbi******")


def have_bigger_atom(context, me: api.Atom, i: api.Atom):
    radian = me.radian_to_atom(i)
    p_l = (
        me.x - me.radius * cos(math.pi / 2 - radian),
        me.x - me.radius * sin(math.pi / 2 - radian),
    )
    p_r = (
        me.x + me.radius * cos(math.pi / 2 - radian),
        me.x + me.radius * sin(math.pi / 2 - radian),
    )
    print(f"have_bigger_atom radian={radian}, p_l={p_l}, p_r={p_r}")
    enemies = [
        i
        for i in context.enemies
        if i.mass >= me.mass * (1 - api.SHOOT_AREA_RATIO) ** TARGET_CISHU
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
    # 先看不改变方向。如果速度超过 MAX_SPEED 则不动
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
            if api.distance(0, 0, me.vx, me.vy) >= MAX_SPEED:
                t = cal_t(me, i, 0, 0)
                qw = qw_c(i.mass, t)
            else:
                x, y = 0, 0
                for j in jiaodu(me, i):
                    xx, yy = get_shoot_change_velocity(j)
                    x += xx
                    y += yy
                print(f"shoot change velocity: x={x + me.vx}, y={y + me.vy}")
                t = cal_t(me, i, x, y)
                qw = qw_c(
                    i.mass
                    - me.mass * (1 - api.SHOOT_AREA_RATIO) ** TARGET_CISHU
                    + me.mass,
                    t,
                )
                if i.type == "npc" or i.type == "player":
                    qw += 200
                shoot = True
            max_qw = qw + 100
            max_atom = i
            print(f"max_atom: {print_atom(max_atom)}, max_qw: {max_qw}")
    # 再找没遮挡的目标
    enemies = [
        i
        for i in context.enemies
        if i.mass < me.mass * (1 - api.SHOOT_AREA_RATIO) ** TARGET_CISHU
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
        x, y = 0, 0
        for j in jiaodu(me, i):
            xx, yy = get_shoot_change_velocity(j)
            x += xx
            y += yy
        print(f"shoot change velocity: {x + me.vx}, {y + me.vy}")
        t = cal_t(me, i, x, y)
        qw = qw_c(
            i.mass - me.mass * (1 - api.SHOOT_AREA_RATIO) ** TARGET_CISHU + me.mass, t
        )
        if i.type == "npc" or i.type == "player":
            qw += 200
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
                jd = jiaodu(me, max_atom)
                print(f"final angle:{[api.r2a(i) for i in jd]}")
                for i in jd:
                    q.put(data(False, i))
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
