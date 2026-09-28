import tensorflow as tf
import numpy as np
from PIL import Image


MODEL_PATH = "models/model_unquant.tflite"
LABELS_PATH = "models/labels.txt"


# -------------------------
# TFLite 모델 불러오기
# -------------------------
interpreter = tf.lite.Interpreter(model_path=MODEL_PATH)
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()


# -------------------------
# 라벨 불러오기
# -------------------------
with open(LABELS_PATH, "r", encoding="utf-8") as f:
    class_names = [line.strip() for line in f.readlines()]


def predict_image(image_path):

    # 이미지 불러오기
    image = Image.open(image_path).convert("RGB")

    # 모델의 입력 크기 확인
    input_shape = input_details[0]["shape"]

    height = input_shape[1]
    width = input_shape[2]

    # 이미지 크기 변경
    image = image.resize((width, height))

    # numpy 배열로 변환
    image_array = np.asarray(image)

    # 입력 타입 확인
    input_dtype = input_details[0]["dtype"]

    if input_dtype == np.float32:
        # Teachable Machine의 일반적인 -1 ~ 1 정규화
        image_array = image_array.astype(np.float32)
        image_array = (image_array / 127.5) - 1.0

    else:
        image_array = image_array.astype(input_dtype)

    # 배치 차원 추가
    input_data = np.expand_dims(image_array, axis=0)

    # 모델에 이미지 전달
    interpreter.set_tensor(
        input_details[0]["index"],
        input_data
    )

    # 추론 실행
    interpreter.invoke()

    # 결과 가져오기
    prediction = interpreter.get_tensor(
        output_details[0]["index"]
    )[0]

    # 가장 높은 확률의 클래스
    index = np.argmax(prediction)

    label = class_names[index]
    confidence = prediction[index]

    return label, confidence

def predict_image_array(image_array):
    input_shape = input_details[0]["shape"]

    height = input_shape[1]
    width = input_shape[2]

    image = Image.fromarray(image_array)
    image = image.resize((width, height))

    image_array = np.asarray(image)

    input_dtype = input_details[0]["dtype"]

    if input_dtype == np.float32:
        image_array = image_array.astype(np.float32)
        image_array = (image_array / 127.5) - 1.0
    else:
        image_array = image_array.astype(input_dtype)

    input_data = np.expand_dims(image_array, axis=0)

    interpreter.set_tensor(
        input_details[0]["index"],
        input_data
    )

    interpreter.invoke()

    prediction = interpreter.get_tensor(
        output_details[0]["index"]
    )[0]

    index = np.argmax(prediction)

    label = class_names[index]
    confidence = prediction[index]

    return label, confidence