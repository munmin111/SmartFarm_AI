import cv2
import requests
import numpy as np
import time

from collections import deque
from ai_model import predict_image_array
from PIL import Image, ImageDraw, ImageFont


URL = "http://192.168.55.108:8080/shot.jpg"

recent_results = deque(maxlen=5)

# -----------------------------
# AI 결과 → 한국어 변환
# 0 = 안좋음
# 1 = 건강함
# -----------------------------
def korean_label(label):
    label_str = str(label).strip().lower()

    if label_str in ["0", "0.0", "diseased", "disease", "bad", "unhealthy"]:
        return "안좋음"

    if label_str in ["1", "1.0", "healthy", "good", "normal"]:
        return "건강함"

    return str(label)


# -----------------------------
# 한글 폰트
# -----------------------------
FONT_PATH = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"

try:
    font = ImageFont.truetype(FONT_PATH, 32)
except Exception:
    print("한글 폰트를 찾지 못했습니다.")
    font = ImageFont.load_default()


print("Smart Farm AI 시작...")


# 오류가 연속으로 발생하는 횟수
error_count = 0
max_errors = 5


while True:
    try:
        # -----------------------------
        # 휴대폰 카메라 사진 요청
        # -----------------------------
        response = requests.get(URL, timeout=3)

        if response.status_code != 200:
            print("HTTP 오류:", response.status_code)

            error_count += 1

            if error_count >= max_errors:
                print("연속 오류가 너무 많아서 프로그램을 종료합니다.")
                break

            time.sleep(1)
            continue

        # 정상적으로 받아오면 오류 횟수 초기화
        error_count = 0

        # -----------------------------
        # JPEG → NumPy
        # -----------------------------
        image = np.frombuffer(
            response.content,
            dtype=np.uint8
        )

        # -----------------------------
        # JPEG → OpenCV
        # -----------------------------
        frame = cv2.imdecode(
            image,
            cv2.IMREAD_COLOR
        )

        if frame is None:
            print("이미지 디코딩 실패")

            error_count += 1

            if error_count >= max_errors:
                print("이미지 오류가 반복되어 종료합니다.")
                break

            time.sleep(1)
            continue

        # -----------------------------
        # OpenCV(BGR) → RGB
        # -----------------------------
        rgb_frame = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        # -----------------------------
        # AI 판단
        # -----------------------------
        label, confidence = predict_image_array(rgb_frame)

        # AI 결과 한국어 변환
        korean = korean_label(label)

        print(
            f"AI 결과: {korean} / "
            f"정확도: {confidence * 100:.1f}%"
        )

        # -----------------------------
        # 최근 5개 결과 저장
        # -----------------------------
        recent_results.append(korean)

        # -----------------------------
        # 가장 많이 나온 결과 계산
        # -----------------------------
        counts = {}

        for result in recent_results:
            counts[result] = counts.get(result, 0) + 1

        stable_label = max(
            counts,
            key=counts.get
        )

        # -----------------------------
        # 한글 출력
        # -----------------------------
        pil_frame = Image.fromarray(
            cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        )

        draw = ImageDraw.Draw(pil_frame)

        text1 = f"AI: {korean} ({confidence * 100:.1f}%)"
        text2 = f"상태: {stable_label}"

        draw.text(
            (20, 20),
            text1,
            font=font,
            fill=(0, 255, 0)
        )

        draw.text(
            (20, 60),
            text2,
            font=font,
            fill=(0, 255, 0)
        )

        # -----------------------------
        # PIL → OpenCV
        # -----------------------------
        frame = cv2.cvtColor(
            np.array(pil_frame),
            cv2.COLOR_RGB2BGR
        )

        # -----------------------------
        # 화면 출력
        # -----------------------------
        cv2.imshow(
            "Smart Farm AI",
            frame
        )

        # q 누르면 종료
        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
            print("프로그램을 종료합니다.")
            break

        time.sleep(1)

    except KeyboardInterrupt:
        print("\n사용자가 프로그램을 종료했습니다.")
        break

    except Exception as e:
        print("오류 발생:", e)

        error_count += 1

        if error_count >= max_errors:
            print("오류가 5회 연속 발생하여 프로그램을 종료합니다.")
            break

        time.sleep(1)


cv2.destroyAllWindows()
