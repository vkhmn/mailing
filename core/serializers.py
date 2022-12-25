from rest_framework import serializers
from core.models import Client, Code, Tag, Mailing, Filter


class ClientSerializer(serializers.ModelSerializer):
    code = serializers.IntegerField(source='code.value', allow_null=True)
    tag = serializers.IntegerField(source='tag.value', allow_null=True)

    class Meta:
        model = Client
        fields = ('id', 'phone', 'code', 'tag', 'time_zone')

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


class FilterSerializer(serializers.ModelSerializer):
    code = serializers.IntegerField(source='code.value')
    tag = serializers.IntegerField(source='tag.value', allow_null=True)

    class Meta:
        model = Filter
        fields = ['code', 'tag']


class MailingSerializer(serializers.ModelSerializer):
    filter = FilterSerializer()

    class Meta:
        model = Mailing
        fields = ['id', 'time_start', 'time_end', 'filter', 'message_text']

    @classmethod
    def __get_filter_instance(cls, validated_data):
        f = validated_data.pop('filter')
        code_data = f.get('code')
        tag_data = f.get('tag')
        code_instance, _ = Code.objects.get_or_create(**code_data)
        tag_instance = None
        if tag_data.get('value'):
            tag_instance, _ = Tag.objects.get_or_create(**tag_data)
        return Filter.objects.create(
            code=code_instance,
            tag=tag_instance,
        )

    def create(self, validated_data):
        instance = Mailing.objects.create(
            filter=self.__get_filter_instance(validated_data),
            **validated_data
        )
        return instance

    def update(self, instance: Mailing, validated_data):
        f = self.__get_filter_instance(validated_data)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.filter = f
        instance.save()

        return instance
