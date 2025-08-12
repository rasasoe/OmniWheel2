import time
from movement import holonomic, non_holonomic, stop_all

def main():
    try:
        while True:
            print("전진 (0도, 속도 30)")
            holonomic(0, 30)
            time.sleep(3)

            print("정지")
            stop_all()
            time.sleep(1)

            print("좌회전 (270도, 속도 20)")
            holonomic(270, 20)
            time.sleep(3)

            print("정지")
            stop_all()
            time.sleep(1)

            print("논홀로노믹 예시: 회전 + 전진")
            non_holonomic(0, 0, 20)  # 제자리 회전
            time.sleep(2)
            non_holonomic(10, 0, 0)  # 앞쪽으로 힘 가하기
            time.sleep(3)

            stop_all()
            break

    except KeyboardInterrupt:
        stop_all()

if __name__ == "__main__":
    main()
