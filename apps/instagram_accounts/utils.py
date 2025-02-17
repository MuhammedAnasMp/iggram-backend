import requests
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def proxy_image(request):
    url = request.GET.get("url")
    if not url:
        return HttpResponse("No URL provided", status=400)

    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return HttpResponse(response.content, content_type="image/jpeg")
    return HttpResponse("Failed to fetch image", status=500)
