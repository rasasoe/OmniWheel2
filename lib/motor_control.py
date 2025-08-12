from machine import Pin, PWM
import time

class Motor:
    def __init__(self, en_pin, in1_pin, in2_pin, pwm_freq=1000):
        self.en = PWM(Pin(en_pin))
        self.en.freq(pwm_freq)
        self.in1 = Pin(in1_pin, Pin.OUT)
        self.in2 = Pin(in2_pin, Pin.OUT)
        self.stop()

    def forward(self, speed=5000):
        self.in1.value(0)
        self.in2.value(1)
        self.set_speed(speed)

    def backward(self, speed=5000):
        self.in1.value(1)
        self.in2.value(0)
        self.set_speed(speed)

    def stop(self):
        self.set_speed(0)
        self.in1.value(0)
        self.in2.value(0)

    def set_speed(self, speed):
        if speed < 0:
            speed = 0
        elif speed > 65535:
            speed = 65535
        self.en.duty_u16(speed)

class Encoder:
    def __init__(self, pin_a):
        self.pin_a = Pin(pin_a, Pin.IN, Pin.PULL_UP)
        self.count = 0
        self.pin_a.irq(trigger=Pin.IRQ_RISING, handler=self._pulse)

    def _pulse(self, pin):
        self.count += 1

    def get_count(self):
        return self.count

    def reset(self):
        self.count = 0

# 인스턴스 생성 (핀 번호 하드웨어에 맞게 수정)
motor0 = Motor(2, 0, 1)
motor1 = Motor(8, 6, 7)
motor2 = Motor(12, 10, 11)

encoder0 = Encoder(3)
encoder1 = Encoder(9)
encoder2 = Encoder(13)

def p_control_multi(target_pulse, kp=50, control_interval=0.1):
    pwm0 = 5000
    pwm1 = 5000
    pwm2 = 5000

    motor0.forward(pwm0)
    motor1.forward(pwm1)
    motor2.forward(pwm2)

    WHEEL_DIAMETER_CM = 6.0
    GEAR_RATIO = 30
    PPR = 11
    PULSE_PER_WHEEL_REV = PPR * GEAR_RATIO

    def pwm_to_255(pwm_val):
        return int(pwm_val / 65535 * 255)

    try:
        while True:
            encoder0.reset()
            encoder1.reset()
            encoder2.reset()

            time.sleep(control_interval)

            pulse0 = encoder0.get_count()
            pulse1 = encoder1.get_count()
            pulse2 = encoder2.get_count()

            rpm0 = (pulse0 / PULSE_PER_WHEEL_REV) / control_interval * 60
            speed0 = rpm0 * (3.1416 * WHEEL_DIAMETER_CM) / 60

            rpm1 = (pulse1 / PULSE_PER_WHEEL_REV) / control_interval * 60
            speed1 = rpm1 * (3.1416 * WHEEL_DIAMETER_CM) / 60

            rpm2 = (pulse2 / PULSE_PER_WHEEL_REV) / control_interval * 60
            speed2 = rpm2 * (3.1416 * WHEEL_DIAMETER_CM) / 60

            error0 = target_pulse - pulse0
            error1 = target_pulse - pulse1
            error2 = target_pulse - pulse2

            pwm0 += int(kp * error0)
            pwm1 += int(kp * error1)
            pwm2 += int(kp * error2)

            pwm0 = max(0, min(65535, pwm0))
            pwm1 = max(0, min(65535, pwm1))
            pwm2 = max(0, min(65535, pwm2))

            motor0.forward(pwm0)
            motor1.forward(pwm1)
            motor2.forward(pwm2)

            target_rpm = (target_pulse / PULSE_PER_WHEEL_REV) / control_interval * 60

            print("모터0 | 목표 RPM: {:.2f} | 측정 RPM: {:.2f} | 속도: {:.2f} cm/s | PWM: {}".format(
                target_rpm, rpm0, speed0, pwm_to_255(pwm0)))
            print("모터1 | 목표 RPM: {:.2f} | 측정 RPM: {:.2f} | 속도: {:.2f} cm/s | PWM: {}".format(
                target_rpm, rpm1, speed1, pwm_to_255(pwm1)))
            print("모터2 | 목표 RPM: {:.2f} | 측정 RPM: {:.2f} | 속도: {:.2f} cm/s | PWM: {}".format(
                target_rpm, rpm2, speed2, pwm_to_255(pwm2)))
            print("-" * 60)

    except KeyboardInterrupt:
        motor0.stop()
        motor1.stop()
        motor2.stop()
        print("제어 종료")
