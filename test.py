import math


def calculate_angles(x1, y1, theta2, M):
    # convert theta2 from degrees to radians if it is in degrees
    theta2 = math.radians(theta2) if theta2 > math.pi else theta2

    # current velocity components of ball a
    vx1 = x1
    vy1 = y1

    # target velocity direction of ball a
    vx2_dir = math.cos(theta2)
    vy2_dir = math.sin(theta2)

    # Calculate the direction of velocity components
    dx_dir = vx2_dir - vx1 / (math.sqrt(vx1 ** 2 + vy1 ** 2) + 1e-8)
    dy_dir = vy2_dir - vy1 / (math.sqrt(vx1 ** 2 + vy1 ** 2) + 1e-8)

    # calculate the first ejection angle
    a1 = math.atan2(dy_dir, dx_dir)

    # calculate the mass of the ejected ball
    m = M / 50

    # update the velocity and mass of ball a after the first ejection
    vx1 += dx_dir * m / M
    vy1 += dy_dir * m / M
    M -= m

    # initialize a2 and a3 to None
    a2 = None
    a3 = None

    # check if the target direction has been reached, if not, perform the second ejection
    if not math.isclose(vx1 / (math.sqrt(vx1 ** 2 + vy1 ** 2) + 1e-8), vx2_dir, abs_tol=1e-3) or not math.isclose(
            vy1 / (math.sqrt(vx1 ** 2 + vy1 ** 2) + 1e-8), vy2_dir, abs_tol=1e-3):
        # calculate the direction of velocity components for the second ejection
        dx_dir = vx2_dir - vx1 / (math.sqrt(vx1 ** 2 + vy1 ** 2) + 1e-8)
        dy_dir = vy2_dir - vy1 / (math.sqrt(vx1 ** 2 + vy1 ** 2) + 1e-8)

        # calculate the second ejection angle
        a2 = math.atan2(dy_dir, dx_dir)

        # calculate the mass of the ejected ball
        m = M / 50

        # update the velocity and mass of ball a after the second ejection
        vx1 += dx_dir * m / M
        vy1 += dy_dir * m / M
        M -= m

        # check if the target direction has been reached, if not, perform the third ejection
        if not math.isclose(vx1 / (math.sqrt(vx1 ** 2 + vy1 ** 2) + 1e-8), vx2_dir, abs_tol=1e-3) or not math.isclose(
                vy1 / (math.sqrt(vx1 ** 2 + vy1 ** 2) + 1e-8), vy2_dir, abs_tol=1e-3):
            # calculate the direction of velocity components for the third ejection
            dx_dir = vx2_dir - vx1 / (math.sqrt(vx1 ** 2 + vy1 ** 2) + 1e-8)
            dy_dir = vy2_dir - vy1 / (math.sqrt(vx1 ** 2 + vy1 ** 2) + 1e-8)

            # calculate the third ejection angle
            a3 = math.atan2(dy_dir, dx_dir)

    return a1, a2, a3  # returning only the ejection angles


print(calculate_angles(1, 1, math.pi/4, 10000))