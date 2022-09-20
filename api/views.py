from rest_framework.response import Response
from rest_framework.decorators import api_view
from quizes.models import Subjects1
from .serializers import Subjects1Serializer

@api_view(['GET'])
def subjects_api_overview(request):
  api_urls = {
    'list_all_subjects': '/api/subjects/all/',
    'one_subject': '/api/subjects/<int:id>/',
    'create_subject': '/api/subjects/create/',
    'update_subject': '/api/subjects/update/<int:id>/',
    'delete_subject': '/api/subjects/delete/<int:id>/',
  }
  return Response(api_urls)

@api_view(['GET'])
def list_all_subjects(request):
  subjects = Subjects1.objects.all()
  serializer = Subjects1Serializer(subjects, many=True)
  return Response(serializer.data)

@api_view(['GET'])
def one_subject(request, id):
  subject = Subjects1.objects.get(id=id)
  serializer = Subjects1Serializer(subject)
  return Response(serializer.data)

@api_view(['POST'])
def create_subject(request):
  serializer = Subjects1Serializer(data=request.data)
  if serializer.is_valid():
    serializer.save()
  return Response(serializer.data)

@api_view(['POST'])
def update_subject(request, id):
  subject = Subjects1.objects.get(id=id)
  serializer = Subjects1Serializer(instance=subject, data=request.data)
  if serializer.is_valid():
    serializer.save()
  return Response(serializer.data)

@api_view(['DELETE'])
def delete_subject(request, id):
  subject = Subjects1.objects.get(id=id)
  subject.delete()
  return Response('Deleted Successfully')

@api_view(['GET'])
def subjects_of_std(request, std):
  subjects = Subjects1.objects.filter(std=std)
  serializer = Subjects1Serializer(subjects, many=True)
  return Response(serializer.data)