from rest_framework import serializers

from predict.models import Predict_Result


class MyPredictSerializer(serializers.ModelSerializer):
    class Meta:
        model = Predict_Result
        fields ='__all__'