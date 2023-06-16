import subprocess
from predict.models import Predict_Result
from rest_framework import viewsets
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from predict.serializers import MyPredictSerializer
import os


# 여기 있어야할거
# senteces랑 font, 사용자 이미지파일 필요함
# 첫번째로 font 선택, 문장 표시, 이미지파일 업로드
# 이미지파일을 predict/test/에 저장하고
# 파일 경로 /tab senteces이렇게 된 gt.txt파일을 input폴더 안에 생성하게 해줘야함

# mdb파일로 만들기
def to_mdb():
    current_path = os.path.dirname(os.path.abspath(__file__))
    command = "python create_lmdb_dataset.py --inputPath input/ --gtFile input/gt.txt --outputPath data/"
    subprocess.run(command, cwd=current_path)

# mdb 폰트 모델에 넣고 돌리기
def to_predict():
    current_path = os.path.dirname(os.path.abspath(__file__))
    command = "python test.py --eval_data data/ --workers 0 --batch_size 128 --saved_model /models/KyoboHandwriting2019_beginner_96.pth --batch_max_length 25 --imgH 64 --imgW 200 --data_filtering_off --Transformation TPS --FeatureExtraction ResNet --SequenceModeling BiLSTM --Prediction Attn"
    subprocess.run(command, cwd=current_path)

# model 에서 출력된 txt파일의 정보 띄우기
def save_the_result():
    current_path = os.path.dirname(os.path.abspath(__file__))
    txt_path = current_path+"/result/KyoboHandwriting2019_beginner_96.pth/log_evaluation.txt"
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
    # save_the_result()

    def post(self, request, format=None):
        # to_mdb()
        # to_predict()
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

