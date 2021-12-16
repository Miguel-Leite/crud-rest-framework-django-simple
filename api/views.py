from django.shortcuts import render
from django.http import JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import TaskSerializer

from .models import Task

# Create your views here.

@api_view(['GET'])
def apiOverview(request):

	api_urls = {
		'List': '/task-list',
		'Details View': '/task-details/<str:pk>/',
		'Create': '/task-create/',
		'Update': '/task-detail/<str:pk>',
		'Update': '/task-update/<str:pk>',
		'Delete': '/task-delete/<str:pk>',
	}

	return Response(api_urls)

@api_view(['GET'])
def taskList(request):
	tasks = Task.objects.all()
	serializer = TaskSerializer(tasks, many=True)
	return Response(serializer.data)

@api_view(['GET'])
def taskDetail(request, pk):
	try:
		tasks = Task.objects.filter(id=pk).values()
		serializer = TaskSerializer(tasks, many=True)
		return Response(serializer.data)
	except Task.DoesNotExist:
		raise "Registro não encontrado!"

@api_view(['POST'])
def taskCreate(request):
	try:
		serializer = TaskSerializer(data=request.data)
		
		if serializer.is_valid():
			serializer.save()

		return Response(serializer.data)

	except Exception as e:
		return "Falha ao criar nova tarefa!"


@api_view(['POST'])
def taskUpdate(request, pk):
	try:
		task = Task.objects.get(id=pk)
		serializer = TaskSerializer(instance=task,data=request.data)
		
		if serializer.is_valid():
			serializer.save()

		return Response(serializer.data)

	except Exception as e:
		return "Falha ao actualizar os dados!"


@api_view(['DELETE'])
def taskDelete(request, pk):
	try:
		task = Task.objects.get(id=pk)
		task.delete()
		if task:
			return Response({'deleted': True})
		return Response({'deleted': False})

	except Exception as e:
		return "Falha ao actualizar os dados!"