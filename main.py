import math
from collections import namedtuple
from math import sin, cos, sqrt
from queue import Queue
import time
import api
from api import Atom

data = namedtuple("data", ["is_space", "data"])
step = ""
start_time = 0
q = Queue()
spaces = 0
AtomTuple = namedtuple(
    "Atom", ["x", "y", "vx", "vy", "radius", "radian", "mass", "type", "id"]
)
SHANBI_CISHU = 5
TARGET_CISHU = 5
MAX_SPEED = 30
SHANBI_TIME = 2

def mirror_atoms(atoms: list[api.Atom]):
    rtn = atoms.copy()
    height = api.get_context().get_env_height() #地图高度
    width = api.get_context().get_env_width() #地图宽度
    for i in atoms:# 四个墙壁都mirror
        rtn.append(AtomTuple(-i.x, i.y, -i.vx, i.vy, i.radius, api.relative_radian(0, 0, -i.vx, i.vy), i.mass, i.type, i.id))
        rtn.append(AtomTuple(i.x, -i.y, i.vx, -i.vy, i.radius, api.relative_radian(0, 0, i.vx, -i.vy), i.mass, i.type, i.id))
        rtn.append(AtomTuple(width - i.x, i.y, -i.vx, i.vy, i.radius, api.relative_radian(0, 0, -i.vx, i.vy), i.mass, i.type, i.id))
        rtn.append(AtomTuple(i.x, height - i.y, i.vx, -i.vy, i.radius, api.relative_radian(0, 0, i.vx, -i.vy), i.mass, i.type, i.id))
    return rtn

def distance_to(me, i):
    return sqrt((me.x - i.x) ** 2 + (me.y - i.y) ** 2)

def qw_c(mass, t):
    return mass * 10 / t

def speeds(me: api.Atom, atom: api.Atom) -> tuple[float, float, float, float]: # lianxian speed, chuizhi speed, lianxian radian, chuizhi radian
    d = api.distance(me.x, me.y, atom.x, atom.y)
    u_xiangdui = ((atom.x - me.x) / d, (atom.y - me.y) / d) # 连线方向上的单位向量
    v_xiangdui = (me.vx - atom.vx, me.vy - atom.vy) # 相对速度
    # 沿连线方向上的速度
    v_lianxian = v_xiangdui[0] * u_xiangdui[0] + v_xiangdui[1] * u_xiangdui[1]
    # 垂直连线方向上的速度
    u_chuizhi = (-u_xiangdui[1], u_xiangdui[0])
    v_chuizhi =  v_xiangdui[0] * u_chuizhi[0] + v_xiangdui[1] * u_chuizhi[1]
    return v_lianxian, v_chuizhi, api.relative_angle(0, 0, *u_xiangdui), api.relative_angle(0, 0, *u_chuizhi)

def Angle(me: api.Atom, atom: api.Atom, cishu) -> list[float]:
    rtn = []
    d = api.distance(me.x, me.y, atom.x, atom.y)
    u_xiangdui = ((atom.x - me.x) / d, (atom.y - me.y) / d) # 连线方向上的单位向量
    v_xiangdui = (me.vx - atom.vx, me.vy - atom.vy) # 相对速度
    # 沿连线方向上的速度
    v_lianxian, v_chuizhi , ang_lianxian, ang_chuizhi = speeds(me, atom)
    # print(f"angle_xiangdui = {round(api.relative_angle(0, 0, *u_xiangdui),3)}, angle_v_xiangdui = {round(api.relative_angle(0, 0,* v_xiangdui),3)}")
    print(f"v_lianxian = {v_lianxian}, v_chuizhi = {v_chuizhi}")
    ang_pen_lian = api.angle_to_radian(ang_lianxian + 180)
    ang_pen_chui = api.angle_to_radian(ang_chuizhi)
    if abs(v_chuizhi) > 0.1 and cishu > 0:
        if abs(v_chuizhi) < 10.2:
            v_shuiping = sqrt(10.2**2 - v_chuizhi**2)
            pen_x, pen_y = v_chuizhi * cos(ang_pen_chui) + v_shuiping * cos(ang_pen_lian), v_chuizhi * sin(ang_pen_chui) + v_shuiping * sin(ang_pen_lian)
            rtn.append(api.relative_radian(0, 0, pen_x, pen_y))
        else:
            if v_chuizhi < 0:
                v_chuizhi = -v_chuizhi
                ang_pen_chui = api.angle_to_radian(ang_chuizhi + 180)
            cishu_chuizhi = int(v_chuizhi // 10.2)
            if cishu_chuizhi >= cishu:
                rtn = [ang_pen_chui] * cishu
            else:
                rtn = [ang_pen_chui] * cishu_chuizhi
            v_chuizhi -= cishu_chuizhi * 10.2
            if abs(v_chuizhi) > 0.1 and cishu_chuizhi < cishu:
                v_shuiping = sqrt(10.2**2 - v_chuizhi**2)
                pen_x, pen_y = v_chuizhi * cos(ang_pen_chui) + v_shuiping * cos(ang_pen_lian), v_chuizhi * sin(ang_pen_chui) + v_shuiping * sin(ang_pen_lian)
                rtn.append(api.relative_radian(0, 0, pen_x, pen_y))
    if len(rtn) < cishu:
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
    ang_pen_chui =  api.angle_to_radian(api.relative_angle(0, 0, *u_chuizhi) + 180)
    ang_pen_lian = api.angle_to_radian(api.relative_angle(0, 0, *u_xiangdui))
    # if v_lianxian > 0.1:
    #     me_v = api.distance(0,0,me.vx,me.vy)
    #     if abs(v_lianxian) < 10.2:
    #         v_shuiping = sqrt(10.2**2 - v_lianxian**2)
    #         pen_x, pen_y = v_lianxian * cos(ang_pen_lian) + v_shuiping * cos(ang_pen_chui), v_lianxian * sin(ang_pen_lian) + v_shuiping * sin(ang_pen_chui)
    #         rtn.append(api.relative_radian(0, 0, pen_x, pen_y))
    #     else:
    #         cishu_lianxian = cal_cishu(v_lianxian, me_v, SHANBI_CISHU-1)
    #         rtn = [ang_pen_lian] * cishu_lianxian
    #         v_lianxian -= cishu_lianxian * 10.2
    #         if v_lianxian> 0.1 and v_lianxian < 10.2:
    #             v_shuiping = sqrt(10.2**2 - v_lianxian**2)
    #             pen_x, pen_y = v_lianxian * cos(ang_pen_lian) + v_shuiping * cos(ang_pen_chui), v_lianxian * sin(ang_pen_lian) + v_shuiping * sin(ang_pen_chui)
    #             rtn.append(api.relative_radian(0, 0, pen_x, pen_y))
    if len(rtn) < SHANBI_CISHU:
        rtn += [ang_pen_chui] * (SHANBI_CISHU - len(rtn))
    print(f"angle rtn={[round(api.r2a(i),3) for i in rtn]}")
    return rtn


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
    ang = []
    for i in range(len(angs[0])):
        x, y = 0, 0
        for j in angs:
            xx = cos(j[i])
            yy = sin(j[i])
            x += xx
            y += yy
        ang.append(api.relative_radian(0, 0, x, y))
    return ang


def cal_t(me: api.Atom, atom: api.Atom, vx, vy):
    vx = atom.vx - me.vx - vx
    vy = atom.vy - me.vy - vy
    dx = atom.x - me.x
    dy = atom.y - me.y
    r_sum = me.radius + atom.radius

    a = vx**2 + vy**2
    b = 2 * (dx * vx + dy * vy)
    c = dx**2 + dy**2 - r_sum**2

    discriminant = b**2 - 4 * a * c

    if discriminant < 0:
        return 999  # 无碰撞

    sqrt_discriminant = math.sqrt(discriminant)
    t1 = (-b - sqrt_discriminant) / (2 * a)
    t2 = (-b + sqrt_discriminant) / (2 * a)

    t = min(t1, t2)
    if t < 0:
        t = max(t1, t2)
    if t < 0:
        return 999  # 所有解为负，无碰撞
    
    return t


def handle_shanbi(context: api.RawContext):
    start_time = time.time()
    me = context.me
    enemies = [i for i in context.enemies.copy() if i.mass > me.mass]
    enemies.sort(key=lambda x: distance_to(me, x))
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
            angs.append(shanbiAngle(me, e))
    print(f"angs: {angs}")
    
    if angs:
        ang = hebing(angs)
        print(f"final angle: {[round(api.r2a(i),3) for i in ang]}")
        while not q.empty():
            q.get()
        for i in ang:
            q.put(data(False, i))
    print(f"handle_shanbi time: {time.time() - start_time}")
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
        len(api.raycast(enemies, p_l, radian, distance_to(me, i)))
        + len(api.raycast(enemies, p_r, radian, distance_to(me, i)))
        > 0
    ):
        # print(f"have_bigger_atom {print_atom(i)}, continue")
        return True
    return False


def handle_target(context: api.RawContext):
    start_time = time.time()
    me = context.me

    max_qw, max_atom, shoot = 0, None, False

    print("******target******")
    print(f"me: {print_atom(context.me)}")
    # 先看不改变方向。如果速度超过 MAX_SPEED 则不动
    if me.vx != 0 or me.vy != 0:
        enemies = [i for i in context.enemies if api.distance(0, 0, i.vx, i.vy) < 100]
        enemies = mirror_atoms(enemies)
        atoms = me.get_forward_direction_atoms(context.enemies)
        atoms.sort(key=lambda x: distance_to(me, x))
        print(f"stright forward atoms:{[print_atom(i) for i in atoms]}")
        biggest_atom = None
        for i in atoms:
            if i.mass >= me.mass:
                break
            if not biggest_atom or i.mass > biggest_atom.mass:
                biggest_atom = i
        if atoms and biggest_atom:
            print(f"stright forward biggest atom:{print_atom(biggest_atom)}")
            speed = api.distance(0, 0, me.vx, me.vy)
            if speed >= MAX_SPEED:
                t = cal_t(me, i, 0, 0)
                qw = qw_c(me.mass + i.mass, t)
            else:
                cishu = int(math.log(biggest_atom.mass / me.mass) / math.log(1 - api.SHOOT_AREA_RATIO))
                if cishu > TARGET_CISHU:
                    cishu = TARGET_CISHU
                angles = Angle(me, i, cishu)
                x, y = 0, 0
                for j in range(len(angles)):
                    xx, yy = get_shoot_change_velocity(angles[j])
                    x += xx
                    y += yy
                    print(f"shoot {j+1} time change to velocity: x={x + me.vx}, y={y + me.vy} cishu: {cishu}")
                    t = cal_t(me, i, x, y)
                    qw = qw_c(me.mass + i.mass - me.mass * (api.SHOOT_AREA_RATIO ** cishu) , t)
                    if i.type == "npc" or i.type == "player":
                        qw *= 0.8
                    print(f"qw:{qw} t:{t} cishu:{cishu}")
                    if qw > max_qw *1.02 and t >= -0.5:
                        # print(f"{print_atom(i)} qw:{qw} t:{t}")
                        max_qw = qw
                        max_atom = i
                        max_cishu = j+1
                        shoot = True
                        print(
                            f"max_atom: {print_atom(max_atom)}, max_qw: {max_qw}, max_cishu: {max_cishu}"
                        )
                    # if lianxian speed > MAX_SPEED then break
                    v_lianxian, v_chuizhi, ang_lianxian, ang_chuizhi = speeds(me, i)
                    v_lianxian += x * cos(ang_lianxian) + y * sin(ang_lianxian)
                    if api.distance(x + me.vx, y + me.vy, 0, 0) >= MAX_SPEED:
                        break
            max_qw = max_qw *1.1
            max_atom = i
            print(f"max_atom: {print_atom(max_atom)}, max_qw: {max_qw}")
    # 再找没遮挡的目标
    enemies = [
        i for i in context.enemies if i.mass < me.mass * (1 - api.SHOOT_AREA_RATIO) and i.mass >= me.mass * api.SHOOT_AREA_RATIO and api.distance(0, 0, i.vx, i.vy) < 100
    ]
    enemies = mirror_atoms(enemies)
    for i in enemies:
        cishu = int(math.log(i.mass / me.mass) / math.log(1 - api.SHOOT_AREA_RATIO))
        if cishu > TARGET_CISHU:
            cishu = TARGET_CISHU
        if have_bigger_atom(context, me, i, cishu):
            continue
        print(f"atom: {print_atom(i)}, cishu: {cishu}")
        angles = Angle(me, i, cishu)
        x, y = 0, 0
        for j in range(len(angles)):
            xx, yy = get_shoot_change_velocity(angles[j])
            x += xx
            y += yy
            print(f"shoot {j+1} time change to velocity: x={x + me.vx}, y={y + me.vy} cishu: {cishu}")
            t = cal_t(me, i, x, y)
            qw = qw_c(me.mass + i.mass - me.mass * (api.SHOOT_AREA_RATIO ** cishu) , t)
            if i.type == "npc" or i.type == "player":
                qw *= 0.8
            print(f"qw:{qw} t:{t} cishu:{cishu}")
            if qw > max_qw *1.02 and t >= -0.5:
                # print(f"{print_atom(i)} qw:{qw} t:{t}")
                max_qw = qw
                max_atom = i
            max_cishu = len(angles)
            shoot = True
            print(
                f"max_atom: {print_atom(max_atom)}, max_qw: {max_qw}, max_cishu: {max_cishu}"
            )
        # if lianxian speed > MAX_SPEED then break
        # v_lianxian, v_chuizhi, ang_lianxian, ang_chuizhi = speeds(me, i)
        # v_lianxian += x * cos(ang_lianxian) + y * sin(ang_lianxian)
        # if api.distance(x + me.vx, y + me.vy, 0, 0) >= MAX_SPEED:
        #     break
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
    print(f"handle_target time: {time.time() - start_time}")
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
