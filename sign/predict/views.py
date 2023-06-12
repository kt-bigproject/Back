from django.shortcuts import render
from PIL import Image
import numpy as np
from tensorflow.keras.models import load_model

def index(request):
    return render(request, 'predict/index.html')

def preprocess_image(image):
    if image is None:
        return None

    # 이미지를 numpy 배열로 변환
    img_array = np.array(image)
    # 이미지 크기 조정
    resized_image = cv2.resize(img_array, (28, 28))
    # 이미지 정규화
    normalized_image = resized_image.astype(float) / 255.0
    return normalized_image

def load_model_weights():
    model = load_model('predict/models/MNIST2.h5')
    return model

def make_prediction(input_data, model):
    # 예측 로직을 구현하여 예측 수행
    # 예측 결과를 반환하거나 원하는 작업을 수행
    # 실제로 예측 로직을 구현해야 함
    prediction = model.predict(input_data)
    return prediction

def predict(request):
    if request.method == 'POST':
        # POST 요청에서 이미지 데이터 가져오기
        image = Image.open(request.FILES['image'])
        image = image.convert('L')  # 이미지를 흑백으로 변환
        image = image.resize((28, 28))  # 이미지 크기 조정
        image = np.array(image)  # 이미지를 배열로 변환
        image = image.reshape(1, 784)  # 형상 조정

        # 모델 가중치를 로드합니다.
        model = load_model_weights()

        # 예측을 수행합니다.
        prediction = make_prediction(image, model)
        predicted_label = np.argmax(prediction)

        return render(request, 'predict/result.html', {'predicted_label': predicted_label})

    return render(request, 'predict/predict.html')


