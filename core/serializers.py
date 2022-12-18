from rest_framework import serializers
from core.models import Client, Code, Tag


class ClientSerializer(serializers.ModelSerializer):
    code = serializers.IntegerField(source='code.value', allow_null=True)
    tag = serializers.IntegerField(source='tag.value', allow_null=True)

    class Meta:
        model = Client
        fields = ('phone', 'code', 'tag', 'time_zone')

    @classmethod
    def __get_code_tag_instance(cls, validated_data):
        code_data = validated_data.pop('code')
        tag_data = validated_data.pop('tag')
        code_instance, _ = Code.objects.get_or_create(**code_data)
        tag_instance = None
        if tag_data.get('value'):
            tag_instance, _ = Tag.objects.get_or_create(**tag_data)
        return code_instance, tag_instance

    def create(self, validated_data):
        code, tag = self.__get_code_tag_instance(validated_data)
        return Client.objects.create(code=code, tag=tag, **validated_data)

    def update(self, instance: Client, validated_data):
        code, tag = self.__get_code_tag_instance(validated_data)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.code = code
        instance.tag = tag
        instance.save()

        return instance
