from rest_framework import serializers
from .models import *


class CollectionTitle_Serializers(serializers.ModelSerializer):
    class Meta:
        model  = CollectionTitle
        fields = '__all__'


class MovieCollection_Serializers(serializers.ModelSerializer):
    class Meta:
        model  = MovieCollection
        fields = '__all__'