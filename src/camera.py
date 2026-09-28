import cv2
import requests
import numpy as np
import time
from collections import deque

from ai_model import predict_image_array


URL = "http://192.168.55.108:8080/shot.jpg"

recent_results = deque(maxlen=5)

print("휴대폰 카메라 연결 중...")

while True:
    try:
        # 휴대폰 카메라에서 이미지 가져오기
        response = requests.get(URL, timeout=3)

        if response.status_code != 200:
            print("HTTP 오류:", response.status_code)
            continue

        # JPEG 데이터를 NumPy 배열로 변환
        image = np.frombuffer(
            response.content,
            dtype=np.uint8
        )

        # JPEG → OpenCV 이미지
        frame = cv2.imdecode(
            image,
            cv2.IMREAD_COLOR
        )

        if frame is None:
            continue

        # OpenCV(BGR) → RGB
        rgb_frame = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        # AI 판단
        label, confidence = predict_image_array(rgb_frame)

        # 최근 5개의 AI 결과 저장
        recent_results.append(label)

        # 가장 많이 나온 결과 계산
        counts = {}

        for result in recent_results:
            counts[result] = counts.get(result, 0) + 1

        stable_label = max(
            counts,
            key=counts.get
        )

        # 현재 결과와 안정화 결과 표시
        text1 = f"현재: {label} ({confidence * 100:.1f}%)"
        text2 = f"최종 판단: {stable_label}"

        cv2.putText(
            frame,
            text1,
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )

        cv2.putText(
            frame,
            text2,
            (20, 80),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )

        # 화면 출력
        cv2.imshow(
            "Smart Farm AI",
            frame
        )

        # 1초 대기
        time.sleep(1)

        # Q를 누르면 종료
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    except Exception as e:
        print("오류:", e)
        time.sleep(1)


cv2.destroyAllWindows()