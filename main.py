import math
from math import sqrt

import api

t = -114514


def cal_will_collide(x1, y1, vx1, vy1, x2, y2, vx2, vy2, r1, r2) -> (bool, float):
    # point1_t = (x1+vx1*t, y1+vy1*t)
    # point2_t = (x2+vx2*t, y2+vy2*t)
    # point1_t and point2_t's distance is radius1+radius2
    # (x1+vx1*t-x2-vx2*t)^2+(y1+vy1*t-y2-vy2*t)^2 = (radius1+radius2)^2
    print(x1, y1, vx1, vy1, x2, y2, vx2, vy2, r1, r2, sep=',')
    try:
        up1 = -vx1 * x1 + vx1 * x2 + vx2 * x1 - vx2 * x2 - vy1 * y1 + vy1 * y2 + vy2 * y1 - vy2 * y2
        up2 = sqrt(
            r1 ** 2 * vx1 ** 2 - 2 * r1 ** 2 * vx1 * vx2 + r1 ** 2 * vx2 ** 2 + r1 ** 2 * vy1 ** 2 - 2 * r1 ** 2 * vy1 * vy2 + r1 ** 2 * vy2 ** 2 + 2 * r1 * r2 * vx1 ** 2 - 4 * r1 * r2 * vx1 * vx2 + 2 * r1 * r2 * vx2 ** 2 + 2 * r1 * r2 * vy1 ** 2 - 4 * r1 * r2 * vy1 * vy2 + 2 * r1 * r2 * vy2 ** 2 + r2 ** 2 * vx1 ** 2 - 2 * r2 ** 2 * vx1 * vx2 + r2 ** 2 * vx2 ** 2 + r2 ** 2 * vy1 ** 2 - 2 * r2 ** 2 * vy1 * vy2 + r2 ** 2 * vy2 ** 2 - vx1 ** 2 * y1 ** 2 + 2 * vx1 ** 2 * y1 * y2 - vx1 ** 2 * y2 ** 2 + 2 * vx1 * vx2 * y1 ** 2 - 4 * vx1 * vx2 * y1 * y2 + 2 * vx1 * vx2 * y2 ** 2 + 2 * vx1 * vy1 * x1 * y1 - 2 * vx1 * vy1 * x1 * y2 - 2 * vx1 * vy1 * x2 * y1 + 2 * vx1 * vy1 * x2 * y2 - 2 * vx1 * vy2 * x1 * y1 + 2 * vx1 * vy2 * x1 * y2 + 2 * vx1 * vy2 * x2 * y1 - 2 * vx1 * vy2 * x2 * y2 - vx2 ** 2 * y1 ** 2 + 2 * vx2 ** 2 * y1 * y2 - vx2 ** 2 * y2 ** 2 - 2 * vx2 * vy1 * x1 * y1 + 2 * vx2 * vy1 * x1 * y2 + 2 * vx2 * vy1 * x2 * y1 - 2 * vx2 * vy1 * x2 * y2 + 2 * vx2 * vy2 * x1 * y1 - 2 * vx2 * vy2 * x1 * y2 - 2 * vx2 * vy2 * x2 * y1 + 2 * vx2 * vy2 * x2 * y2 - vy1 ** 2 * x1 ** 2 + 2 * vy1 ** 2 * x1 * x2 - vy1 ** 2 * x2 ** 2 + 2 * vy1 * vy2 * x1 ** 2 - 4 * vy1 * vy2 * x1 * x2 + 2 * vy1 * vy2 * x2 ** 2 - vy2 ** 2 * x1 ** 2 + 2 * vy2 ** 2 * x1 * x2 - vy2 ** 2 * x2 ** 2)
        down = (vx1 ** 2 - 2 * vx1 * vx2 + vx2 ** 2 + vy1 ** 2 - 2 * vy1 * vy2 + vy2 ** 2)
        t1 = (up1 - up2) / down

        t2 = (up1 + up2) / down

    except:
        return False, 0
    print("cal", t1, t2)
    if math.isnan(t1) or math.isnan(t2):
        return False, 0
    if t1 < -2 and t2 < -2:
        return False, 0
    if t1 < 0:
        tt = t2
    else:
        tt = min(t1, t2)
    return True, tt


def cal_shouyi(mass, coll_list) -> float:
    shouyi = 0
    for i in coll_list:
        if mass <= i.mass:
            return -mass
        shouyi += i.mass
    return shouyi


def get_coll_list(context, x, y):
    coll_list = []
    sum_col = 0
    for j in context.monsters + context.other_players + context.npc:
        if (x + j.vx) ** 2 + (y + j.vy) ** 2 < 0.1:
            continue
        cal = cal_will_collide(context.me.x, context.me.y, x, y, j.x, j.y, j.vx, j.vy, context.me.radius, j.radius)
        print(cal)
        if cal[0]:
            coll_list.append(j)
            sum_col += cal[1]
    coll_list.sort(key=lambda atom: math.sqrt((context.me.x + x - atom.x - atom.vx) ** 2 + (
            context.me.y + y - atom.y - atom.vy) ** 2))
    if sum_col == 0:
        sum_col = 0.01

    return coll_list, sum_col


def update(context: api.RawContext):
    if context.step % 10 != 0:
        return None
    x, y = context.me.vx, context.me.vy
    print(" ".join([i.type for i in context.monsters + context.other_players + context.npc]))
    coll_list, sum_col = get_coll_list(context, x, y)
    if len(coll_list) != 0:
        best_shouyi = cal_shouyi(context.me.mass, coll_list) + 10 / sum_col
    else:
        best_shouyi = 0
    best_rad = -114
    print("no coll_list", coll_list)
    print("no", best_shouyi)
    angles = []
    for i in context.monsters + context.other_players + context.npc:
        angle = api.relative_angle(context.me.x, context.me.y, i.x, i.y, 0)
        angles += [angle, angle + 180, angle + 90, angle - 90]
    for i in angles:
        radian = api.angle_to_radian(i)
        size = context.me.mass * api.SHOOT_AREA_RATIO
        x, y = context.me.get_shoot_change_velocity(radian)
        coll_list, sum_col = get_coll_list(context, x, y)
        if len(coll_list) != 0:
            shouyi = cal_shouyi(context.me.mass, coll_list) + 10 / sum_col
        else:
            shouyi = 0
        print(i, "coll_list", coll_list)
        print(i, "shouyi", shouyi)
        if shouyi > best_shouyi:
            best_shouyi = cal_shouyi(context.me.mass - size, coll_list)
            best_rad = radian
    best_rad = best_rad.normalize()
    print("best", best_rad, best_shouyi)
    if best_rad != -114:
        return best_rad
