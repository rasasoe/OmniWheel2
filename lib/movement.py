from motor_control import motor0, motor1, motor2

import math

def holonomic(f_agl, f_speed):
    radianA = math.radians(180 - (180 - f_agl if f_agl <= 180 else 540 - f_agl))
    radianB = math.radians(90 - (180 - (180 - f_agl if f_agl <= 180 else 540 - f_agl)))

    Fx = 0
    Fy = 0
    Fw = 0

    if 0 <= f_agl < 360:
        Fx = f_speed * math.cos(radianA)
        Fy = f_speed * math.cos(radianB)
    elif f_agl < 0:
        Fw = -f_speed
    elif f_agl >= 360:
        Fw = f_speed

    V = [
        0.057 * Fx + 0.033 * Fy + 0.14 * Fw,
        -0.065 * Fy + 0.14 * Fw,
        -0.057 * Fx + 0.033 * Fy + 0.14 * Fw
    ]

    # 속도 제한
    for i in range(3):
        if V[i] > 40:
            V[i] = 40
        elif V[i] < -40:
            V[i] = -40

    # PWM 16bit로 변환 (임의 스케일)
    motor0.set_speed(int(V[0] * 65535 / 40))
    motor1.set_speed(int(V[1] * 65535 / 40))
    motor2.set_speed(int(V[2] * 65535 / 40))

def non_holonomic(Fx, Fy, Fw):
    V = [
        0.056 * Fx + 0.033 * Fy + 0.14 * Fw,
        -0.065 * Fy + 0.14 * Fw,
        -0.056 * Fx + 0.033 * Fy + 0.14 * Fw,
    ]

    for i in range(3):
        if V[i] > 40:
            V[i] = 40
        elif V[i] < -40:
            V[i] = -40

    motor0.set_speed(int(V[0] * 65535 / 40))
    motor1.set_speed(int(V[1] * 65535 / 40))
    motor2.set_speed(int(V[2] * 65535 / 40))

def stop_all():
    motor0.stop()
    motor1.stop()
    motor2.stop()
