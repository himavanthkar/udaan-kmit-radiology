from django.shortcuts import render

# Create your views here.
def Home(request):
    return render(request, "home.html")

def Viewer(request):
    return render(request, "DCMviewer.html")