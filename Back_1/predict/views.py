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

    command = "python create_lmdb_dataset.py --inputPath input/test/ --gtFile input/gt.txt --outputPath data/"

    subprocess.run(command, cwd=current_path)

font_select = {
    # 페이지에서 입력 받는 값으로 변경
    # 예시) '폰트이름' : '폰트의 모델 가중치 이름'
    'lv01' : 'KyoboHandwriting2019_beginner_96',
    'lv02' : 'nanum_slow_standard_93',
    'lv03' : 'ChosunCentennial_intermediate_96',
    'lv04' : 'KyoboHandwriting2020pdy_expert_98',
    'lv05' : 'KCC-Ahnjunggeun_art_98',
}
# mdb 폰트 모델에 넣고 돌리기
def to_predict():
    current_path = os.path.dirname(os.path.abspath(__file__))

    # font_select[페이지에서 입력 받는 값으로]
    command = "python test.py --eval_data data/ --workers 0 --batch_size 128 --saved_model models/"+font_select['lv01']+".pth --batch_max_length 25 --imgH 64 --imgW 200 --data_filtering_off --Transformation TPS --FeatureExtraction ResNet --SequenceModeling BiLSTM --Prediction Attn"

    subprocess.run(command, cwd=current_path)

# model 에서 출력된 txt파일의 정보 띄우기
def save_the_result():
    current_path = os.path.dirname(os.path.abspath(__file__))
    txt_path = current_path+"/result/"+font_select['lv01']+".pth/log_evaluation.txt"
    with open(txt_path, "r") as file:
        lines = file.readlines()
        
    for line in lines:
        line = line.strip()
        if line.startswith("Prediction:"):
            prediction = line.split(",")[0].split(":")[1].strip()
            ground_truth = line.split(",")[1].split(":")[1].strip()
            confidence = line.split(",")[2].split(":")[1]
            is_correct = line.split(",")[3].split(":")[1].strip()
    
   
    result = Predict_Result(prediction=prediction, ground_truth=ground_truth, confidence=confidence, is_correct=is_correct)
    result.save()


class PredictAPIView(viewsets.ModelViewSet):
    queryset = Predict_Result.objects.all()
    serializer_class = MyPredictSerializer
    to_mdb()
    to_predict()
    save_the_result()

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

