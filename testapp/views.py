from django.shortcuts import render
from .models import StudentModel
from .serializers import StudentSerializer
from django.views.generic import View
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse
import io

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


# Create your views here.
@method_decorator(csrf_exempt, name="dispatch")
class StudentView(View):
    def is_user_exists(self, id):
        try:
            student = StudentModel.objects.get(id=id)
            data = student
        except StudentModel.DoesNotExist:
            data = None
        return data

    def get(self, request, *args, **kwargs):
        data = request.body
        stream = io.BytesIO(data)
        p_data = JSONParser().parse(stream)
        student_id = p_data.get('id', None)
        if student_id is not None:
            student_data = self.is_user_exists(id=student_id)
            if student_data is not None:
                serializer = StudentSerializer(student_data)
                student_json_data = JSONRenderer().render(serializer.data)
                return HttpResponse(student_json_data, content_type="application/json")
            json_data = {'msg': "Student with provided id does not exists"}
            return HttpResponse(JSONRenderer().render(json_data), content_type="application/json", status=300)
        qa = StudentModel.objects.all()
        serializer = StudentSerializer(qa, many=True)
        json_data = JSONRenderer().render(serializer.data)
        return HttpResponse(json_data, content_type="application/json")

    def post(self, request, *args, **kwargs):
        data = request.body
        byte_data = io.BytesIO(data)
        p_data = JSONParser().parse(byte_data)
        serializer = StudentSerializer(data=p_data)  # gives data in dictionary format
        if serializer.is_valid():
            serializer.save()  # create method is called in serializer
            msg = {"msg": "Resource Successfully Created"}
            return HttpResponse(JSONRenderer().render(msg), content_type="application/json")
        json_data = JSONRenderer().render(serializer.errors)
        return HttpResponse(json_data, content_type="application/json", status=400)
