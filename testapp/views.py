import io

from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer

from .models import StudentModel
from .serializers import StudentSerializer


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
        print(f"Serializer  :{serializer}")
        if serializer.is_valid():
            serializer.save()  # create method is called in serializer
            msg = {"msg": "Resource Successfully Created"}
            return HttpResponse(JSONRenderer().render(msg), content_type="application/json")
        json_data = JSONRenderer().render(serializer.errors)
        return HttpResponse(json_data, content_type="application/json", status=400)

    def put(self, request, *args, **kwargs):
        data = request.body
        bytes = io.BytesIO(data)
        pdata = JSONParser().parse(bytes)
        student_id = pdata.get('id')
        student = StudentModel.objects.get(id=student_id)
        serializer = StudentSerializer(student, data=pdata, partial=True)
        if serializer.is_valid():
            serializer.save()
            msg = {"msg": "Data successfully Updated"}
            return HttpResponse(JSONRenderer().render(msg), content_type="application/json", status=200)
        json_data = JSONRenderer().render(serializer.errors)
        return HttpResponse(json_data, content_type="application/json", status=300)

    def delete(self, request, *args, **kwargs):
        data = request.body
        stream_data = io.BytesIO(data)
        pdata = JSONParser().parse(stream_data)
        student_id = pdata.get('id')
        stu = self.is_user_exists(id=student_id)
        if stu is not None:
            status, data = stu.delete()
            if status == 1:
                return HttpResponse(JSONRenderer().render({'msg': 'Resource Deleted'}), content_type="application/json")
            return HttpResponse(JSONRenderer().render({'msg': 'Error occurred while removing resource'}),
                                content_type="application/json")
        return HttpResponse(JSONRenderer().render({'msg': 'Resource Not Found'}),
                            content_type="application/json")
