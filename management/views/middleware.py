from ..models import RequestCounter

class RequestCountMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Increment request count for each incoming request
        request_counter, created = RequestCounter.objects.get_or_create(pk=1)
        request_counter.count += 1
        request_counter.save()

        response = self.get_response(request)
        return response
