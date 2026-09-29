import time
import board
import adafruit_dht

# DHT11이 연결된 GPIO 번호에 맞게 수정
# 예: GPIO 4 = board.D4
dht = adafruit_dht.DHT11(board.D4)

print("DHT11 센서 테스트 시작")
print("Ctrl + C를 누르면 종료됩니다.")

try:
    while True:
        try:
            temperature = dht.temperature
            humidity = dht.humidity

            print(
                f"온도: {temperature:.1f} °C | "
                f"습도: {humidity:.1f} %"
            )

        except RuntimeError as e:
            # DHT11은 가끔 읽기 오류가 발생할 수 있음
            print("센서 읽기 재시도:", e)

        time.sleep(2)

except KeyboardInterrupt:
    print("\n테스트 종료")

finally:
    dht.exit()
