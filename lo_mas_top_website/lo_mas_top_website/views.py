#Server
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from http import HTTPStatus

#Utilities
from datetime import datetime
import os
import socket

def status(request):
    try:
        return JsonResponse({
                'message': 'Lo Mas Top Web working properly.',
                'date': datetime.now().strftime('%b %dth, %Y - %H:%M Hrs'),
                'hostname':socket.gethostname()
            }, status=HTTPStatus.OK)
    except Exception as ex:
        print(ex)
        return JsonResponse({'message': 'An error'}, status=HTTPStatus.INTERNAL_SERVER_ERROR)
    
def page_no_found(request, exception=None):
    return render(request,'page_no_found.html')