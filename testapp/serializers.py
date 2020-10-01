from rest_framework import serializers
from .models import StudentModel


class StudentSerializer(serializers.Serializer):
    sno = serializers.IntegerField()
    sname = serializers.CharField(max_length=50)
    smarks = serializers.IntegerField()
    saddress = serializers.CharField(max_length=100)

    def create(self, validated_data):
        return StudentModel.objects.create(**validated_data)
