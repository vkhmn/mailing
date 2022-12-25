from datetime import datetime

from django.db.models import Count
from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Client, Mailing, Message, Status
from .serializers import ClientSerializer, MailingSerializer
from .services import ActiveMailing
from .tasks import send_message_task


@api_view(['GET', 'DELETE', 'PUT'])
def get_delete_update_client(request, pk):
    try:
        client = Client.objects.get(pk=pk)
    except Client.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ClientSerializer(client)
        return Response(serializer.data)
    elif request.method == 'DELETE':
        client.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    elif request.method == 'PUT':
        serializer = ClientSerializer(client, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def get_post_clients(request):
    if request.method == 'GET':
        clients = Client.objects.all()
        serializer = ClientSerializer(clients, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        try:
            code = int(request.data.get('code')) if request.data.get('code') else None
            data = {
                'phone': int(request.data.get('phone')),
                'code': code,
                'tag': request.data.get('tag'),
                'time_zone': int(request.data.get('time_zone'))
            }
        except ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer = ClientSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'DELETE', 'PUT'])
def get_delete_update_mailing(request, pk):
    try:
        instance = Mailing.objects.get(pk=pk)
    except Mailing.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = MailingSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'DELETE':
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    elif request.method == 'PUT':

        pattern = '%d-%m-%Y %H:%M'
        data = {
            'time_start': datetime.strptime(
                request.data.get('time_start'), pattern),
            'time_end': datetime.strptime(
                request.data.get('time_end'), pattern),
            'filter': request.data.get('filter'),
            'message_text': request.data.get('message_text'),
        }
        serializer = MailingSerializer(instance, data=data)
        #print(serializer)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def get_post_mailing(request):
    if request.method == 'GET':
        mailing = Mailing.objects.all()
        serializer = MailingSerializer(mailing, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        pattern = '%d-%m-%Y %H:%M'
        data = {
            'time_start': datetime.strptime(
                request.data.get('time_start'), pattern),
            'time_end': datetime.strptime(
                request.data.get('time_end'), pattern),
            'filter': request.data.get('filter'),
            'message_text': request.data.get('message_text'),
        }
        serializer = MailingSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_common_mailing_stat(request):
    # получения общей статистики по созданным рассылкам
    # и количеству отправленных сообщений по ним с группировкой по статусам

    status_count = Message.objects.values(
        'status').annotate(count=Count('status'))

    sc = {Status(d.get('status')).name: d.get('count') for d in status_count}

    return Response(
        dict(
            Count=Mailing.objects.count(),
            Messages=sc,
        )
    )


@api_view(['GET'])
def get_mailing_stat(request, pk):
    # получения детальной статистики отправленных
    # сообщений по конкретной рассылке
    try:
        mailing = Mailing.objects.get(pk=pk)
    except Mailing.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    status_count = Message.objects.filter(mailing=mailing).values(
        'status').annotate(count=Count('status'))

    sc = {Status(d.get('status')).name: d.get('count') for d in status_count}

    return Response(
        dict(
            Messages=sc,
        )
    )


@api_view(['GET'])
def start_mailing(request):
    active_mailings = ActiveMailing.execute()
    for pk in active_mailings:
        send_message_task.delay(pk)
    return Response(
        dict(active_mailings=active_mailings),
        status.HTTP_200_OK
    )
