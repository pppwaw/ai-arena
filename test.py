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
        if abs(shu) >= 2:
            y = abs(shu)
            x = math.sqrt(10.2**2 - y**2)
            r_last_shu = api.a2r(r1 + api.r2a(api.relative_radian(0, 0, x, y)) + 180)
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
