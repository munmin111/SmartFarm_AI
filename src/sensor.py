import time
import board
import adafruit_dht


# ==========================================
# DHT11 설정
# DATA 핀 → Raspberry Pi GPIO 4
# ==========================================
dht = adafruit_dht.DHT11(board.D4)


def read_sensor():
    """
    DHT11에서 온도와 습도를 읽는다.

    return:
        temperature : 온도(°C)
        humidity    : 습도(%)
    """

    try:
        temperature = dht.temperature
        humidity = dht.humidity

        return temperature, humidity

    except RuntimeError as e:
        print("DHT11 읽기 오류:", e)
        return None, None


def main():

    print("================================")
    print(" Smart Farm DHT11 Sensor")
    print("================================")
    print("센서 측정을 시작합니다.")
    print("Ctrl + C : 종료")
    print()

    try:

        while True:

            temperature, humidity = read_sensor()

            if temperature is not None and humidity is not None:

                print(
                    f"온도: {temperature:.1f} °C | "
                    f"습도: {humidity:.1f} %"
                )

            time.sleep(2)

    except KeyboardInterrupt:

        print("\n센서 테스트 종료")

    finally:

        dht.exit()


if __name__ == "__main__":
    main()
