from django.shortcuts import render

# Create your views here.
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from user.models import Student
from user.serializer import EmployeeSerializer, EmployeeDeSerializer


class UserAPIView(APIView):
    # 局部使用渲染器 为单个视图指定渲染器
    renderer_classes = (JSONRenderer,)
    parser_classes = [JSONParser]

    def get(self, request, *args, **kwargs):  # drf的request对象  其中包含原生的request

        # 获取django原生的request对象  可以通过_request来访问django原生的request对象  不推荐
        user_id_2 = request._request.GET.get("id")
        print(user_id_2)
        # 通过DRF的request对象  获取参数
        user_id_1 = request.GET.get("id")
        print(user_id_1)
        # 通过query_params来获取参数  DRF扩展的获取参数的方式
        print(request.query_params.get("id"))
        # 获取路径中参数
        user_id_3 = kwargs.get("id")
        print(user_id_3)

        return Response("GET  请求")

    def post(self, request, *args, **kwargs):
        # post 请求参数的形式有多种 form-data  www-urlencoded json
        # 获取参数的方式
        # print(request._request.POST)  # django远程的request对象  不推荐
        print(request.POST)  # DRF封装后的request   可以用
        # DRF扩展的获取参数的方式  可以获取任意类型的参数
        print(request.data)

        return Response("POST  请求")

    def put(self, request, *args, **kwargs):
        print(request.data)
        return Response("PUT")


class EmployeeAPIView(APIView):

    def get(self, request, *args, **kwargs):
        """
        提供查询员工的功能
        """
        emp_id = kwargs.get("id")

        if emp_id:
            # 查询单个
            emp_obj = Student.objects.get(pk=emp_id)

            # 查询出的单个用户无法直接序列化，需要使用序列化器去完成序列化
            # .data 将序列化后的数据打包成字典
            serializer = EmployeeSerializer(emp_obj).data

            return Response({
                "status": 200,
                "message": "查询单个用户成功",
                "results": serializer
            })
        else:
            # 查询所有
            employee_objects_all = Student.objects.all()

            # TODO 使用序列化器完成多个对象序列化时 需要指定参数 many=True
            data = EmployeeSerializer(employee_objects_all, many=True).data

            return Response({
                "status": 200,
                "message": "查询单个用户成功",
                "results": data,
            })

    def post(self, request, *args, **kwargs):

        # 获取前端传递的参数
        user_data = request.data

        # TODO 前端发送的数据需要保存到数据库时  必须对前台的数据进行校验
        if not isinstance(user_data, dict) or user_data == {}:
            return Response({
                "status": 400,
                "message": "请求参数有误"
            })

        # 使用序列化器对前台提交的数据进行反序列化
        # 在反序列化时需要指定关键字参数 data
        serializer = EmployeeDeSerializer(data=user_data)

        # 校验失败的错误信息
        # 对反序列化数据的进行校验  通过is_valid进行校验  如果校验通过，该方法返回True
        if serializer.is_valid():
            # 校验通过，则调用save()方法去保存对象 创建成功会返回对象
            # 底层调用的是create(）方法完成的对象的创建
            emp_obj = serializer.save()

            if emp_obj:
                # 有员工对象代表创建成功 返回到前端
                return Response({
                    "status": 201,
                    "message": "创建单个对象成功",
                    # 将创建成功后的对象返回到前端时需要序列化
                    "results": EmployeeSerializer(emp_obj).data
                })

        return Response({
            "status": 400,
            "message": "创建失败",
            "errors": serializer.errors
        })
