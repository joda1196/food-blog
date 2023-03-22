from django.shortcuts import render

# Create your views here.
def test(request):
    context = {"test": "testing_django"}
    return render(request, "test.html", context)


def homepage(request):
    return render(request, "homepage.html")
