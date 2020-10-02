from rest_framework import serializers
from .models import StudentModel


# Normal Serializers
class StudentSerializer(serializers.Serializer):
    sno = serializers.IntegerField()
    sname = serializers.CharField(max_length=50)
    # smarks = serializers.IntegerField(validators="marks_validator") Calling field level validators
    smarks = serializers.IntegerField()
    saddress = serializers.CharField(max_length=100)

    # Validators
    def validate_smarks(self, marks):
        if marks > 100:
            raise serializers.ValidationError("Marks must be less than 100")
        return marks

    # Object Level Validators
    def validate(self, attrs):
        name = attrs.get('sname')
        address = attrs.get('saddress')
        if name.lower() == "sai":
            if address.upper() != "KNR":
                raise serializers.ValidationError("If name is Sai then , address must be knr")
        return attrs

    def marks_validator(self, marks):
        if marks < 35:
            raise serializers.ValidationError("marks is less than 35 , student got failed")
        return marks

    def create(self, validated_data):
        return StudentModel.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.sno = validated_data.get('sno', instance.sno)
        instance.sname = validated_data.get('sname', instance.sname)
        instance.smarks = validated_data.get('smarks', instance.smarks)
        instance.saddress = validated_data.get('saddress', instance.saddress)
        instance.save()
        return instance

# Model Level Serializers
# class StudentSerializer(serializers.ModelSerializer):
#
#     def validate(self, attrs):
#         marks = attrs.get('smarks')
#         if marks > 100:
#             raise serializers.ValidationError("Marks must be less than 100")
#
#     class Meta:
#         model = StudentModel
#         fields = "__all__"
