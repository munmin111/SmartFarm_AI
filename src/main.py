from ai_model import predict_image


images = [
    "hea1.jpg",
    "hea2.jpg",
    "hea3.jpg",
    "hea4.jpg",
    "hea5.jpg",
    "hea6.jpg",
    "hea7.jpg",
    "hea8.jpg",
    "hea9.jpg",
    "sick1.jpg",
    "sick2.jpg",
    "sick3.jpg",
    "sick4.jpg",
    "sick5.jpg",
    "sick6.jpg",
    "sick7.jpg",
    "sick8.jpg",
    "sick9.jpg"
]


print("=" * 50)
print("스마트팜 AI 테스트")
print("=" * 50)


for image_path in images:

    label, confidence = predict_image(image_path)

    print(f"{image_path:10} → {label} ({confidence * 100:.2f}%)")