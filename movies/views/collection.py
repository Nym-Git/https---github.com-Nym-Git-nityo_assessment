from rest_framework.decorators import api_view, permission_classes
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
import requests


@csrf_exempt
@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticated,))
def collection(request):
    # if request.method == 'POST':


    page = request.GET.get('page', 1)
    url = f"http://demo.credy.in/api/v1/maya/movies?page={page}"

    username = "iNd3jDMYRKsN1pjQPMRz2nrq7N99q4Tsp9EY9cM0"
    password = "Ne5DoTQt7p8qrgkPdtenTK8zd6MorcCR5vXZIJNfJwvfafZfcOs4reyasVYddTyXCz9hcL5FGGIVxw3q02ibnBLhblivqQTp4BIC93LZHj4OppuHQUzwugcYu7TIC5H1"

    headers = {
        'Authorization': f'Basic {username}:{password}'
    }

    response = requests.request("GET", url, headers=headers, verify=False)

    if response.status_code == 200:
        data = response.json()
        return Response(data, status=status.HTTP_200_OK)
    else:
        return Response({"error":response,
            "message":"Error from the vendor(MAYA) API"}, status=response.status_code)


