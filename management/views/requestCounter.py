from django.http import JsonResponse
from ..models import RequestCounter
from rest_framework.decorators import api_view, permission_classes
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import AllowAny

def get_request_count(request):
    if request.method == 'GET':
        request_counter = RequestCounter.objects.first()
        count = request_counter.count if request_counter else 0
        return JsonResponse({"requests": count}, status=200)


@csrf_exempt
@api_view(['POST'])
@permission_classes((AllowAny,))
def reset_request_count(request):
    if request.method == 'POST':
        try:
            request_counter = RequestCounter.objects.first()
            if request_counter:
                request_counter.count = 0
                request_counter.save()
            else:
                RequestCounter.objects.create(count=0)
            return JsonResponse({"message": "Request count reset successfully"}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
