import math

import api


def cal_will_collide(x1, y1, vx1, vy1, x2, y2, vx2, vy2, r1, r2) -> bool:
    # point1_t = (x1+vx1*t, y1+vy1*t)
    # point2_t = (x2+vx2*t, y2+vy2*t)
    # point1_t and point2_t's distance is radius1+radius2
    # (x1+vx1*t-x2-vx2*t)^2+(y1+vy1*t-y2-vy2*t)^2 = (radius1+radius2)^2
    print(x1, y1, vx1, vy1, x2, y2, vx2, vy2, r1, r2)
    try:
        t1 = -(vx1 * x1 - vx1 * x2 - vx2 * x1 + vx2 * x2 + vy1 * y1 - vy1 * y2 - vy2 * y1 + vy2 * y2) / (
                vx1 ** 2 - 2 * vx1 * vx2 + vx2 ** 2 + vy1 ** 2 - 2 * vy1 * vy2 + vy2 ** 2) - math.sqrt(
            r1 ** 2 * vx1 ** 2 - 2 * r1 ** 2 * vx1 * vx2 + r1 ** 2 * vx2 ** 2 + r1 ** 2 * vy1 ** 2 - 2 * r1 ** 2 * vy1 * vy2 + r1 ** 2 * vy2 ** 2 + 2 * r1 * r2 * vx1 ** 2 - 4 * r1 * r2 * vx1 * vx2 + 2 * r1 * r2 * vx2 ** 2 + 2 * r1 * r2 * vy1 ** 2 - 4 * r1 * r2 * vy1 * vy2 + 2 * r1 * r2 * vy2 ** 2 + r2 ** 2 * vx1 ** 2 - 2 * r2 ** 2 * vx1 * vx2 + r2 ** 2 * vx2 ** 2 + r2 ** 2 * vy1 ** 2 - 2 * r2 ** 2 * vy1 * vy2 + r2 ** 2 * vy2 ** 2 - vx1 ** 2 * y1 ** 2 + 2 * vx1 ** 2 * y1 * y2 - vx1 ** 2 * y2 ** 2 + 2 * vx1 * vx2 * y1 ** 2 - 4 * vx1 * vx2 * y1 * y2 + 2 * vx1 * vx2 * y2 ** 2 + 2 * vx1 * vy1 * x1 * y1 - 2 * vx1 * vy1 * x1 * y2 - 2 * vx1 * vy1 * x2 * y1 + 2 * vx1 * vy1 * x2 * y2 - 2 * vx1 * vy2 * x1 * y1 + 2 * vx1 * vy2 * x1 * y2 + 2 * vx1 * vy2 * x2 * y1 - 2 * vx1 * vy2 * x2 * y2 - vx2 ** 2 * y1 ** 2 + 2 * vx2 ** 2 * y1 * y2 - vx2 ** 2 * y2 ** 2 - 2 * vx2 * vy1 * x1 * y1 + 2 * vx2 * vy1 * x1 * y2 + 2 * vx2 * vy1 * x2 * y1 - 2 * vx2 * vy1 * x2 * y2 + 2 * vx2 * vy2 * x1 * y1 - 2 * vx2 * vy2 * x1 * y2 - 2 * vx2 * vy2 * x2 * y1 + 2 * vx2 * vy2 * x2 * y2 - vy1 ** 2 * x1 ** 2 + 2 * vy1 ** 2 * x1 * x2 - vy1 ** 2 * x2 ** 2 + 2 * vy1 * vy2 * x1 ** 2 - 4 * vy1 * vy2 * x1 * x2 + 2 * vy1 * vy2 * x2 ** 2 - vy2 ** 2 * x1 ** 2 + 2 * vy2 ** 2 * x1 * x2 - vy2 ** 2 * x2 ** 2) / (
                     vx1 ** 2 - 2 * vx1 * vx2 + vx2 ** 2 + vy1 ** 2 - 2 * vy1 * vy2 + vy2 ** 2)
        t2 = -(vx1 * x1 - vx1 * x2 - vx2 * x1 + vx2 * x2 + vy1 * y1 - vy1 * y2 - vy2 * y1 + vy2 * y2) / (
                vx1 ** 2 - 2 * vx1 * vx2 + vx2 ** 2 + vy1 ** 2 - 2 * vy1 * vy2 + vy2 ** 2) + math.sqrt(
            r1 ** 2 * vx1 ** 2 - 2 * r1 ** 2 * vx1 * vx2 + r1 ** 2 * vx2 ** 2 + r1 ** 2 * vy1 ** 2 - 2 * r1 ** 2 * vy1 * vy2 + r1 ** 2 * vy2 ** 2 + 2 * r1 * r2 * vx1 ** 2 - 4 * r1 * r2 * vx1 * vx2 + 2 * r1 * r2 * vx2 ** 2 + 2 * r1 * r2 * vy1 ** 2 - 4 * r1 * r2 * vy1 * vy2 + 2 * r1 * r2 * vy2 ** 2 + r2 ** 2 * vx1 ** 2 - 2 * r2 ** 2 * vx1 * vx2 + r2 ** 2 * vx2 ** 2 + r2 ** 2 * vy1 ** 2 - 2 * r2 ** 2 * vy1 * vy2 + r2 ** 2 * vy2 ** 2 - vx1 ** 2 * y1 ** 2 + 2 * vx1 ** 2 * y1 * y2 - vx1 ** 2 * y2 ** 2 + 2 * vx1 * vx2 * y1 ** 2 - 4 * vx1 * vx2 * y1 * y2 + 2 * vx1 * vx2 * y2 ** 2 + 2 * vx1 * vy1 * x1 * y1 - 2 * vx1 * vy1 * x1 * y2 - 2 * vx1 * vy1 * x2 * y1 + 2 * vx1 * vy1 * x2 * y2 - 2 * vx1 * vy2 * x1 * y1 + 2 * vx1 * vy2 * x1 * y2 + 2 * vx1 * vy2 * x2 * y1 - 2 * vx1 * vy2 * x2 * y2 - vx2 ** 2 * y1 ** 2 + 2 * vx2 ** 2 * y1 * y2 - vx2 ** 2 * y2 ** 2 - 2 * vx2 * vy1 * x1 * y1 + 2 * vx2 * vy1 * x1 * y2 + 2 * vx2 * vy1 * x2 * y1 - 2 * vx2 * vy1 * x2 * y2 + 2 * vx2 * vy2 * x1 * y1 - 2 * vx2 * vy2 * x1 * y2 - 2 * vx2 * vy2 * x2 * y1 + 2 * vx2 * vy2 * x2 * y2 - vy1 ** 2 * x1 ** 2 + 2 * vy1 ** 2 * x1 * x2 - vy1 ** 2 * x2 ** 2 + 2 * vy1 * vy2 * x1 ** 2 - 4 * vy1 * vy2 * x1 * x2 + 2 * vy1 * vy2 * x2 ** 2 - vy2 ** 2 * x1 ** 2 + 2 * vy2 ** 2 * x1 * x2 - vy2 ** 2 * x2 ** 2) / (
                     vx1 ** 2 - 2 * vx1 * vx2 + vx2 ** 2 + vy1 ** 2 - 2 * vy1 * vy2 + vy2 ** 2)
    except:
        return False
    print("cal", t1, t2)
    if math.isnan(t1) or math.isnan(t2):
        return False
    if t1 < -2 and t2 < -2:
        return False
    return True


def cal_shouyi(mass, coll_list) -> float:
    shouyi = 0
    for i in coll_list:
        if mass <= i.mass:
            return -mass
        shouyi += i.mass
    return shouyi


def update(context: api.RawContext):
    x, y = context.me.vx, context.me.vy
    coll_list = []
    for j in context.enemies:
        cal = cal_will_collide(context.me.x, context.me.y, x, y, j.x, j.y, j.vx, j.vy, context.me.radius, j.radius)
        print(cal)
        if cal:
            coll_list.append(j)
    coll_list.sort(key=lambda atom: math.sqrt((context.me.x + x - atom.x - atom.vx) ** 2 + (
            context.me.y + y - atom.y - atom.vy) ** 2))
    best_shouyi = cal_shouyi(context.me.mass, coll_list)
    best_rad = -1
    print("no coll_list", coll_list)
    print("no", best_shouyi)
    angles = []
    for i in context.enemies:
        angle = api.relative_angle(context.me.x, context.me.y, i.x, i.y, 0)
        angles += [angle, angle + 180, angle + 90, angle - 90]
    for i in angles:
        radian = api.angle_to_radian(i)
        size = context.me.mass * api.SHOOT_AREA_RATIO
        x, y = context.me.get_shoot_change_velocity(radian)
        coll_list = []
        for j in context.enemies:
            cal = cal_will_collide(context.me.x, context.me.y, x, y, j.x, j.y, j.vx, j.vy, context.me.radius, j.radius)
            print(cal)
            if cal:
                coll_list.append(j)
        coll_list.sort(key=lambda atom: math.sqrt((context.me.x + x - atom.x - atom.vx) ** 2 + (
                context.me.y + y - atom.y - atom.vy) ** 2))
        print(i, "coll_list", coll_list)
        shouyi = cal_shouyi(context.me.mass - size, coll_list)
        print(i, shouyi)
        if shouyi > best_shouyi:
            best_shouyi = cal_shouyi(context.me.mass - size, coll_list)
            best_rad = radian
    if best_rad != -1:
        return best_rad
