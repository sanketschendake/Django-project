from django.http import HttpResponse, JsonResponse


def home_page(request):
    name = ['sanket', 'chendake']

    # return HttpResponse('<h1>This is home page<h1>')
    return JsonResponse(name, safe=False)
