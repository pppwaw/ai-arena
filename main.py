import math
from collections import namedtuple
from math import sin, cos, sqrt
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
SHANBI_CISHU = 5
TARGET_CISHU = 5
MAX_SPEED = 30
SHANBI_TIME = 2

def v(me:api.Atom):
    # 动量守恒 m1v1+api.
     return api.SHOOT_AREA_RATIO * api.DELTA_VELOCITY - sqrt(me.vx**2 + me.vy**2)
def qw_c(mass, t):
    return mass / (t*100)

def Angle(me: api.Atom, atom: api.Atom, cishu) -> list[float]:
    rtn = []
    d = api.distance(me.x, me.y, atom.x, atom.y)
    u_xiangdui = ((atom.x - me.x) / d, (atom.y - me.y) / d) # 连线方向上的单位向量
    v_xiangdui = (me.vx - atom.vx, me.vy - atom.vy) # 相对速度
    # 沿连线方向上的速度
    v_lianxian = v_xiangdui[0] * u_xiangdui[0] + v_xiangdui[1] * u_xiangdui[1]
    # 垂直连线方向上的速度
    u_chuizhi = (-u_xiangdui[1], u_xiangdui[0])
    v_chuizhi =  v_xiangdui[0] * u_chuizhi[0] + v_xiangdui[1] * u_chuizhi[1]
    # 垂直连线方向的速度
    print(f"angle_xiangdui = {round(api.relative_angle(0, 0, *u_xiangdui),3)}, angle_v_xiangdui = {round(api.relative_angle(0, 0,* v_xiangdui),3)}")
    print(f"v_lianxian = {v_lianxian}, v_chuizhi = {v_chuizhi}")
    ang_pen_chui =  api.angle_to_radian(api.relative_angle(0, 0, *u_chuizhi) +180)
    ang_pen_lian = api.angle_to_radian(api.relative_angle(0, 0, *u_xiangdui) + 180)
    if abs(v_chuizhi > 0.1):
        
        if abs(v_chuizhi) < v(me):
            v_shuiping = sqrt(v(me)**2 - v_chuizhi**2)
            pen_x, pen_y = v_chuizhi * cos(ang_pen_chui) + v_shuiping * cos(ang_pen_lian), v_chuizhi * sin(ang_pen_chui) + v_shuiping * sin(ang_pen_lian)
            rtn.append(api.relative_radian(0, 0, pen_x, pen_y))
        else:
            cishu_chuizhi = int(abs(v_chuizhi) // v(me))
            if cishu_chuizhi >= cishu:
                rtn = [ang_pen_chui] * cishu
            else:
                rtn = [ang_pen_chui] * cishu_chuizhi
            v_chuizhi -= cishu_chuizhi * v(me)
            if abs(v_chuizhi) > 0.1:
                v_shuiping = sqrt(v(me)**2 - v_chuizhi**2)
                pen_x, pen_y = v_chuizhi * cos(ang_pen_chui) + v_shuiping * cos(ang_pen_lian), v_chuizhi * sin(ang_pen_chui) + v_shuiping * sin(ang_pen_lian)
                rtn.append(api.relative_radian(0, 0, pen_x, pen_y))
    if len(rtn) >= cishu:
        print(f"angle rtn={[round(api.r2a(i),3) for i in rtn]}")
        return rtn
    rtn += [ang_pen_lian] * (cishu - len(rtn))
    print(f"angle rtn={[round(api.r2a(i),3) for i in rtn]}")
    return rtn


def shanbiAngle(me: api.Atom, atom: api.Atom) -> list[float]:
    rtn = []
    d = api.distance(me.x, me.y, atom.x, atom.y)
    u_xiangdui = ((atom.x - me.x) / d, (atom.y - me.y) / d) # 连线方向上的单位向量
    v_xiangdui = (me.vx - atom.vx, me.vy - atom.vy) # 相对速度
    # 沿连线方向上的速度
    v_lianxian = v_xiangdui[0] * u_xiangdui[0] + v_xiangdui[1] * u_xiangdui[1]
    # 垂直连线方向上的速度
    u_chuizhi = (-u_xiangdui[1], u_xiangdui[0])
    v_chuizhi =  v_xiangdui[0] * u_chuizhi[0] + v_xiangdui[1] * u_chuizhi[1]
    # 垂直连线方向的速度
    print(f"angle_xiangdui = {api.relative_angle(0, 0, *u_xiangdui)}, angle_v_xiangdui = {api.relative_angle(0, 0,* v_xiangdui)}")
    print(f"v_lianxian={v_lianxian}, v_chuizhi={v_chuizhi}")
    ang_pen_chui =  api.angle_to_radian(api.relative_angle(0, 0, *u_chuizhi) +180)
    ang_pen_lian = api.angle_to_radian(api.relative_angle(0, 0, *u_xiangdui) + 180)
    if abs(v_lianxian > 0.1):
        if abs(v_lianxian) < v(me):
            v_shuiping = sqrt(v(me)**2 - v_lianxian**2)
            pen_x, pen_y = v_lianxian * cos(ang_pen_lian) + v_shuiping * cos(ang_pen_chui), v_lianxian * sin(ang_pen_lian) + v_shuiping * sin(ang_pen_chui)
            rtn.append(api.relative_radian(0, 0, pen_x, pen_y))
        else:
            cishu_lianxian = int(abs(v_lianxian) // v(me))
            rtn = [ang_pen_lian] * cishu_lianxian
            v_lianxian -= cishu_lianxian * v(me)
            if abs(v_lianxian) > 0.1:
                v_shuiping = sqrt(v(me)**2 - v_lianxian**2)
                pen_x, pen_y = v_lianxian * cos(ang_pen_lian) + v_shuiping * cos(ang_pen_chui), v_lianxian * sin(ang_pen_lian) + v_shuiping * sin(ang_pen_chui)
                rtn.append(api.relative_radian(0, 0, pen_x, pen_y))
    if len(rtn) >= SHANBI_CISHU:
        print(f"angle rtn={[round(api.r2a(i),3) for i in rtn]}")
        return rtn
    rtn += [ang_pen_chui] * (SHANBI_CISHU - len(rtn))
    print(f"angle rtn={[round(api.r2a(i),3) for i in rtn]}")
    return rtn


def get_shoot_change_velocity(me, radian) -> tuple[float, float]:  # x,y
    return -cos(radian) * v(me), -sin(radian) * v(me)


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
    l = me.get_atom_surface_dist(atom)
    r = api.relative_radian(me.x, me.y, atom.x, atom.y)
    x, y = l * cos(r), l * sin(r)
    vx = me.vx + vx - atom.vx
    vy = me.vy + vy - atom.vy
    print(f"cal_t x={x}, y={y}, vx={vx}, vy={vy}, t={(x / vx + y / vy) / 2}")
    if x / vx >= -0.2 and y / vy >= -0.2:
        return (x / vx + y / vy) / 2
    else:
        return -1


def handle_shanbi(context: api.RawContext):
    me = context.me
    enemies = [i for i in context.enemies.copy() if i.mass > me.mass]
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
            elif t <= -1:
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
        print(f"final angle: {round(api.r2a(ang),3)}")
        while not q.empty():
            q.get()
        for i in range(SHANBI_CISHU):
            q.put(data(False, ang))
    print("******shanbi******")


def have_bigger_atom(context, me: api.Atom, i: api.Atom, cishu):
    radian = api.relative_radian(me.x, me.y, i.x, i.y)
    p_l = (
        me.x - me.radius * cos(math.pi / 2 - radian),
        me.y - me.radius * sin(math.pi / 2 - radian),
    )
    p_r = (
        me.x + me.radius * cos(math.pi / 2 - radian),
        me.y + me.radius * sin(math.pi / 2 - radian),
    )
    # print(f"have_bigger_atom radian={radian}, p_l={p_l}, p_r={p_r}")
    enemies = [
        i
        for i in context.enemies
        if i.mass >= (me.mass * (1 - api.SHOOT_AREA_RATIO) ** cishu)
    ]
    if (
        len(api.raycast(enemies, p_l, radian, me.distance_to(i)))
        + len(api.raycast(enemies, p_r, radian, me.distance_to(i)))
        > 0
    ):
        # print(f"have_bigger_atom {print_atom(i)}, continue")
        return True
    return False


def handle_target(context: api.RawContext):
    me = context.me

    max_qw, max_atom, shoot = 0, None, False

    print("******target******")
    print(f"me: {print_atom(context.me)}")
    # 先看不改变方向。如果速度超过 MAX_SPEED 则不动
    if me.vx != 0 or me.vy != 0:
        enemies = [i for i in context.enemies if i.mass < me.mass and (i.vx**2 + i.vy**2) < 10000]
        atoms = me.get_forward_direction_atoms(enemies)
        atoms.sort(key=lambda x: me.distance_to(x))
        print(f"stright forward atoms:{[print_atom(i) for i in atoms]}")
        if atoms:
            i = atoms[0]
            for j in atoms:
                if i.mass < j.mass < me.mass:
                    i = j
            print(f"stright forward atom:{print_atom(i)}")
            speed = api.distance(0, 0, me.vx, me.vy)
            if speed >= MAX_SPEED:
                t = cal_t(me, i, 0, 0)
                qw = qw_c(i.mass, t)
            else:
                cishu = int(
                    min(
                        (MAX_SPEED - speed) // v(me),
                        math.log(i.mass / me.mass, 1 - api.SHOOT_AREA_RATIO),
                    )
                )
                if cishu > TARGET_CISHU:
                    cishu = TARGET_CISHU
                x, y = 0, 0
                for j in Angle(me, i, cishu):
                    xx, yy = get_shoot_change_velocity(me, j)
                    x += xx
                    y += yy
                print(
                    f"shoot change to velocity: x={x + me.vx}, y={y + me.vy} cishu: {cishu}"
                )
                t = cal_t(me, i, x, y)
                qw = qw_c(
                    i.mass - me.mass * (1 - api.SHOOT_AREA_RATIO) ** cishu + me.mass,
                    t,
                )
                if i.type == "npc" or i.type == "player":
                    qw -= 500
                max_cishu = cishu
                shoot = True
            max_qw = qw + 100
            max_atom = i
            print(f"max_atom: {print_atom(max_atom)}, max_qw: {max_qw}")
    # 再找没遮挡的目标
    enemies = [
        i for i in context.enemies if i.mass < me.mass * (1 - api.SHOOT_AREA_RATIO) and i.mass >= me.mass * api.SHOOT_AREA_RATIO and (i.vx**2 + i.vy**2) < 90000
    ]
    for i in enemies:
        if api.distance(0, 0, i.vx, i.vy) > 1000:
            continue
        cishu = int(math.log(i.mass / me.mass, 1 - api.SHOOT_AREA_RATIO))
        if cishu > TARGET_CISHU:
            cishu = TARGET_CISHU
        if have_bigger_atom(context, me, i, cishu):
            continue
        print()
        print(f"atom: {print_atom(i)}")
        x, y = 0, 0
        for j in Angle(me, i, cishu):
            xx, yy = get_shoot_change_velocity(me, j)
            x += xx
            y += yy
        print(f"shoot change to velocity: x={x + me.vx}, y={y + me.vy} cishu: {cishu}")
        t = cal_t(me, i, x, y)
        qw = qw_c(i.mass - me.mass * (1 - api.SHOOT_AREA_RATIO) ** cishu + me.mass, t)
        if i.type == "npc" or i.type == "player":
            qw -= 500
        print(f"qw:{qw} t:{t} cishu:{cishu}")
        if qw > max_qw *1.05 and t >= -0.5:
            # print(f"{print_atom(i)} qw:{qw} t:{t}")
            max_qw = qw
            max_atom = i
            max_cishu = cishu
            shoot = True
            print(
                f"max_atom: {print_atom(max_atom)}, max_qw: {max_qw}, max_cishu: {max_cishu}"
            )
    if max_atom:
        if shoot:
            if not me.colliding:
                print(f"final atom: {print_atom(max_atom)}")
                jd = Angle(me, max_atom, max_cishu)
                print(f"final angle:{[round(api.r2a(i),3) for i in jd]}")
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
    # if context.step == 1:
    #     return api.a2r(75)
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
