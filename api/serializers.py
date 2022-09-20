from dataclasses import field
from rest_framework import serializers
from quizes.models import Subjects1

class Subjects1Serializer(serializers.ModelSerializer):
  class Meta:
    model = Subjects1
    fields = '__all__'