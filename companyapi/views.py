from django.http import HttpResponse
import json
def home_page(request):
    return HttpResponse(json.dumps({'title': 'Home'}), content_type = "application/json")