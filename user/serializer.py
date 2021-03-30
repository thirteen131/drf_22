from django.conf import settings
from rest_framework import serializers

# 定义一个序列化器类 与想要序列化的模型的字段进行对应
from user.models import Student


class EmployeeSerializer(serializers.Serializer):
    """
    需要为每一个model去编写一个序列化器类
    """
    # 想要序列化的模型的字段
    username = serializers.CharField()
    # password = serializers.CharField()
    # gender = serializers.IntegerField()
    phone = serializers.CharField()

    # 自定义字段 使用 SerializerMethodField来定义
    aaa = serializers.SerializerMethodField()

    # 自定义字段的属性名随意  但我们需要为该字段提供get_属性名的方法来定义返回值
    # get_字段名：是为了自定义字段提供值的方法  self是参与当前序列化器的类
    # 方法的返回值就是自定义字段返回到前端的值
    def get_aaa(self, obj):
        return "bbb"

    gender = serializers.SerializerMethodField()

    # 自定义性别的返回值  obj是当前要序列化的对象
    def get_gender(self, obj):
        # 性别是choices类型  get_字段名_display直接访问
        return obj.get_gender_display()

    # 自定义返回图片的全路径
    pic = serializers.SerializerMethodField()

    def get_pic(self, obj):
        # http://127.0.0.1:8000/media/pic/8.jpg

        return "%s%s%s" % ("http://127.0.0.1:8000/", settings.MEDIA_URL, str(obj.pic))


# 定义反序列化器
class EmployeeDeSerializer(serializers.Serializer):
    """
    反序列化：将前台提交的数据保存入库
    1. 前台需要提供哪些字段
    2. 对字段进行安全校验
    3. 哪些字段需要额外的校验
    反序列化不存在自定义字段，因为是要将数据保存至数据库
    """

    username = serializers.CharField(
        max_length=8,
        min_length=3,
        error_messages={
            "max_length": "名字长度太长了",
            "min_length": "名字长度太短了",
        }
    )
    # password = serializers.CharField()
    phone = serializers.CharField(
        max_length=11,
        min_length=11,
    )
    birthday = serializers.DateField()

    # 如果想要完成员工的新增 必须重写create()方法
    # Serializer以及父类只是声明了create方法，并没有做实现 所以在调用时会保存
    def create(self, validated_data):
        # 自己完成对象的创建 validated_data是前端传递的需要保存到数据库的数据
        emp_obj = Student.objects.create(**validated_data)
        # 把创建成功的对象返回
        return emp_obj
