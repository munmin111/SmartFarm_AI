import time
import board
import adafruit_dht

dht = adafruit_dht.DHT11(
    board.D4,
    use_pulseio=False
)

print("DHT11 테스트 시작")
print("Ctrl + C 로 종료")

while True:
    try:
        temperature = dht.temperature
        humidity = dht.humidity

        print(f"온도: {temperature} °C")
        print(f"습도: {humidity} %")
        print("----------------")

    except RuntimeError as e:
        print("읽기 실패:", e)

    time.sleep(2)
