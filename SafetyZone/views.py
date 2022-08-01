from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http.response import StreamingHttpResponse
from django.http.response import JsonResponse
import base64

from SafetyZone.RealTimeDetection.Camera import VideoCamera

SafetyZone = VideoCamera()

@csrf_exempt
def video_feed(request):
    return HttpResponse(SafetyZone.jpeg, content_type="image/jpeg")
@csrf_exempt
def org_image(request):
    #print(SafetyZone.image)
    image = "\"data:image/jpeg;base64," + str(base64.b64encode(SafetyZone.image))[2:] + "\""
    return HttpResponse(image, content_type="application/json; charset=utf-8")

@csrf_exempt
def predicted_image(request):
    image = "\"data:image/jpeg;base64," + str(base64.b64encode(SafetyZone.jpeg))[2:] + "\""
    data = {"PredictionTime": str(SafetyZone.predictiontime), "Base64String": str(image)[1:-2]}
    return JsonResponse(data, safe=False)

@csrf_exempt
def logs(request):
    logs = [{"Date": "", "Title": "", "Message" : ""}]
    return JsonResponse(logs, safe=False)

@csrf_exempt
def status(request):
    return JsonResponse(True, safe=False)

@csrf_exempt
def reload_parameters(request):
    return JsonResponse(True, safe=False)

@csrf_exempt
def set_bypass(request):
    return JsonResponse("böyle birşey yok:)", safe=False)

@csrf_exempt
def get_bypass(request):
    return JsonResponse(False, safe=False)

@csrf_exempt
def app_restart(request):
    return JsonResponse("böyle birşey yok:)", safe=False)
    