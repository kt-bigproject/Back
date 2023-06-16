import subprocess
from predict.models import Predict_Result
from rest_framework import viewsets
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from predict.serializers import MyPredictSerializer


# 여기 있어야할거
# senteces랑 font, 사용자 이미지파일 필요함
# 첫번째로 font 선택, 문장 표시, 이미지파일 업로드
# 이미지파일을 predict/test/에 저장하고
# 파일 경로 /tab senteces이렇게 된 gt.txt파일을 input폴더 안에 생성하게 해줘야함

# mdb파일로 만들기
def to_mdb():
    command = "python C:/Users/User/Desktop/Big/Git/Back/Back_1/predict/create_lmdb_dataset.py --inputPath C:/Users/User/Desktop/Big/Git/Back/Back_1/predict/media/ --gtFile C:/Users/User/Desktop/Big/Git/Back/Back_1/predict/input/gt.txt --outputPath C:/Users/User/Desktop/Big/Git/Back/Back_1/predict/data/"
    subprocess.run(command)

# mdb 폰트 모델에 넣고 돌리기
def to_predict():
    command = "python C:/Users/User/Desktop/Big/Git/Back/Back_1/predict/test.py --eval_data C:/Users/User/Desktop/Big/Git/Back/Back_1/predict/data --workers 0 --batch_size 128 --saved_model C:/Users/User/Desktop/Big/Git/Back/Back_1/predict/models/KyoboHandwriting2019_beginner_96.pth --batch_max_length 25 --imgH 64 --imgW 200 --data_filtering_off --Transformation TPS --FeatureExtraction ResNet --SequenceModeling BiLSTM --Prediction Attn"
    subprocess.run(command)

# model 에서 출력된 txt파일의 정보 띄우기
def save_the_result():
    txt_path = "C:/Users/User/Desktop/Big/Git/Back/Back_1/predict/result/KyoboHandwriting2019_beginner_96.pth/log_evaluation.txt"
    with open(txt_path, "r") as file:
        lines = file.readlines()

    prediction = ""
    ground_truth = ""
    confidence = ""
    is_correct = ""

    for line in lines:
        line = line.strip()
        if line.startswith("Prediction:"):
            prediction = line.split(":")[1].strip()
        elif line.startswith("Ground Truth:"):
            ground_truth = line.split(":")[1].strip()
        elif line.startswith("Confidence:"):
            confidence = line.split(":")[1].strip()
        elif line.startswith("정답여부:"):
            is_correct = line.split(":")[1].strip()

    result = Predict_Result(prediction=prediction, ground_truth=ground_truth, confidence=confidence, is_correct=is_correct)
    result.save()

# 필요없을거 같음
# class predict(viewsets.ModelViewSet):
#     QuerySet = Predict_Result.objects.all()
#     serializer_class = MyPredictSerializer

class PredictAPIView(viewsets.ModelViewSet):
    queryset = Predict_Result.objects.all()
    serializer_class = MyPredictSerializer
    to_mdb()
    to_predict()

    def post(self, request, format=None):
        # to_mdb()
        # to_predict()
        save_the_result()
        result = Predict_Result.objects.last()
        serialized_result = MyPredictSerializer(result)


        response_data = {
            'message': 'Predictions executed successfully.',
            'data': {
                'prediction': serialized_result.data['prediction'],
                'confidence': serialized_result.data['confidence'],
                'is_correct': serialized_result.data['is_correct'],
            }
        }

        return Response(response_data)

    @classmethod
    def get_extra_actions(cls):
        return []

