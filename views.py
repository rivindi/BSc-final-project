from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def homepage(request):
    return render(request, "index.html")


def who_are_we_view(request):
    return render(request, "who-are-we.html")


def register_as_a_teacher(request):
    return render(request, "register-as-a-teacher.html")
