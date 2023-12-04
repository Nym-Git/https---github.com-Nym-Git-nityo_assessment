from rest_framework.decorators import api_view, permission_classes
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated
from ..serializers import *
from rest_framework.response import Response
from rest_framework import status
from collections import Counter
from itertools import chain
from django.db.models import Count, CharField, Value
from django.db.models.functions import Concat
from django.shortcuts import get_object_or_404

@csrf_exempt
@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticated,))
def collection(request):

    if request.method == 'POST':
        data = request.data
        movies_list = list(request.data['movies'])
        data['user_id'] = request.user
        del data['movies']
        # Not using serializer here because we need to add user_id instence in movies_to_create
        try:
            collection_id = CollectionTitle.objects.create(**data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        movies_to_create = list(
        map(
            lambda movie_item: MovieCollection(
                title=movie_item['title'],
                description=movie_item['description'],
                genres=movie_item['genres'],
                uuid=movie_item['uuid'],
                collection_id=collection_id
            ),
            movies_list
        ))

        try:
            MovieCollection.objects.bulk_create(
                movies_to_create,
                ignore_conflicts=True
            )
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({"collection_uuid":collection_id.id},status=status.HTTP_201_CREATED)
    
    elif request.method == 'GET':
        collections = CollectionTitle.objects.filter(user_id=request.user.id).values_list('id', flat=True)

        movies = MovieCollection.objects.filter(collection_id__in=collections).annotate(genres_concat=Concat('genres', Value(','), output_field=CharField())).values_list('genres_concat', flat=True)

        all_genres = list(chain.from_iterable([movie.split(',') for movie in movies]))
        genre_counter = Counter(all_genres)
        favorite_genres = [genre[0] for genre in genre_counter.most_common(3)]
        serialized_data = CollectionTitle_Serializers(CollectionTitle.objects.filter(user_id=request.user.id), many=True).data

        response_data = {
            "is_success": True,
            "data": {
                "collections": serialized_data,
                "favourite_genres": favorite_genres
            }
        }

        return Response(response_data, status=status.HTTP_200_OK)
    
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    

@csrf_exempt
@api_view(['GET','PUT'])
@permission_classes((IsAuthenticated,))
def collection_detail(request, collection_uuid):
    if request.method == 'GET':
        try:
            collection = get_object_or_404(CollectionTitle.objects.prefetch_related('moviecollection_set'), id=str(collection_uuid))
        except ValueError:
            return Response({"error": "Invalid UUID format"}, status=status.HTTP_400_BAD_REQUEST)
        except CollectionTitle.DoesNotExist:
            return Response({"error": "Collection UUID doesn't exist"}, status=status.HTTP_404_NOT_FOUND)

        serialized_data = CollectionTitle_Serializers(collection).data
        movies = collection.moviecollection_set.all()
        serialized_data['movies'] = MovieCollection_Serializers(movies, many=True).data

        return Response({"collection": serialized_data}, status=status.HTTP_200_OK)
    

    elif request.method == 'PUT':
        try:
            collection_id = CollectionTitle.objects.get(id=str(collection_uuid), user_id=request.user.id)
            collection_id.title = request.data.get('title', collection_id.title)
            collection_id.description = request.data.get('description', collection_id.description)
            collection_id.save()
        except CollectionTitle.DoesNotExist:
            return Response({'error': "uuid does't exist OR unauthorized user"}, status=status.HTTP_400_BAD_REQUEST)
        
        movies_to_create = list(
        map(
            lambda movie_item: MovieCollection(
                title=movie_item['title'],
                description=movie_item['description'],
                genres=movie_item['genres'],
                uuid=movie_item['uuid'],
                collection_id=collection_id
            ),
            request.data['movies']
        ))

        try:
            MovieCollection.objects.bulk_create(
                movies_to_create,
                ignore_conflicts=True
            )
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({"collection_uuid":collection_id.id},status=status.HTTP_201_CREATED)
        

    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
