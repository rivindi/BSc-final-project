"""findteacher URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import include
from django.contrib import admin
from django.urls import path

from findteacher.views import homepage, register_as_a_teacher, who_are_we_view
from teacher.views import (
    ContactUsView,
    list_schedules_view,
    shedule_details_view,
)

urlpatterns = [
    path("", view=homepage, name="homepage"),
    path("schedules", view=list_schedules_view, name="schedules"),
    path("schedule/<int:id>", view=shedule_details_view, name="schedule-details"),
    path("teacher/", include("teacher.urls")),
    path("contact", ContactUsView.as_view(), name="contact-us"),
    path("who-are-we", view=who_are_we_view, name="who-are-we"),
    path(
        "register-as-a-teacher",
        view=register_as_a_teacher,
        name="register-as-a-teacher",
    ),
]
