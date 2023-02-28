from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from fileparser.parser import pdfParser
@csrf_exempt
def parseFile(request):
    if request.method == 'POST':
        if 'file' in request.FILES:
            pdffile = request.FILES['file']
            data = pdfParser(pdffile)
            if len(data) == 0:
                return HttpResponse(json.dumps({'success' : False, 'message' : 'File content was unable to be parsed'}), content_type='application/json')
            return HttpResponse(json.dumps({'success' : True, 'message' : 'File parsed successfully', 'data': data}), content_type='application/json')
        else:
            return HttpResponse(json.dumps({'success' : False, 'message' : 'File is empty'}), content_type='application/json')
    return HttpResponse("Method Not Allowed")